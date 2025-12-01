import os
import logging
from typing import Optional, Dict, List, Any
from datetime import datetime
from supabase import create_client, Client
import config

# Configurar logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SupabaseAuthManager:
    """Gerenciador de autenticação usando Supabase Auth"""
    
    def __init__(self):
        """Inicializar cliente Supabase"""
        if not config.SUPABASE_URL or not config.SUPABASE_KEY:
            logger.error("SUPABASE_URL e SUPABASE_KEY devem estar configurados no .env")
            raise ValueError("SUPABASE_URL e SUPABASE_KEY devem estar configurados no .env")
            
        try:
            self.supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
            logger.info("Supabase Auth inicializado")
        except Exception as e:
            logger.error(f"Erro ao inicializar Supabase: {e}")
            raise

    def sign_in(self, email: str, password: str, ip_address: str = "unknown") -> Optional[Dict[str, Any]]:
        """
        Fazer login com email e senha
        Retorna dicionário com dados do usuário e token se sucesso, None se falha
        """
        try:
            response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user:
                user_data = {
                    "user": response.user,
                    "session": response.session
                }
                
                # Buscar perfil do usuário
                profile = self.get_user_profile(response.user.id)
                if profile:
                    user_data["profile"] = profile
                    # Adicionar campos compatíveis com a interface existente
                    user_data["username"] = profile.get("email", email).split("@")[0]
                    user_data["full_name"] = profile.get("full_name", email)
                    user_data["role"] = profile.get("role", "user")
                    user_data["id"] = response.user.id
                else:
                    # Fallback se não tiver perfil
                    user_data["username"] = email.split("@")[0]
                    user_data["full_name"] = email
                    user_data["role"] = "user"
                    user_data["id"] = response.user.id
                
                # Registrar tentativa de login (sucesso)
                self._log_login_attempt(response.user.id, email, True, ip_address)
                
                return user_data
            return None
            
        except Exception as e:
            logger.error(f"Erro no login {email}: {e}")
            # Registrar tentativa de login (falha)
            self._log_login_attempt(None, email, False, ip_address, str(e))
            return None

    def authenticate(self, username, password):
        """Alias para sign_in para compatibilidade com auth_ui"""
        # Converter username para email usando a mesma lógica do create_user
        email = username if "@" in username else f"{username}@badilab.local"
        return self.sign_in(email, password)


    def sign_out(self):
        """Fazer logout"""
        try:
            self.supabase.auth.sign_out()
            return True
        except Exception as e:
            logger.error(f"Erro no logout: {e}")
            return False

    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Buscar perfil complementar do usuário"""
        try:
            response = self.supabase.table("user_profiles").select("*").eq("user_id", user_id).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar perfil {user_id}: {e}")
            return None

    def _log_login_attempt(self, user_id: Optional[str], email: str, success: bool, ip_address: str, error_message: str = None):
        """Registrar tentativa de login para auditoria"""
        try:
            data = {
                "email": email,
                "success": success,
                "ip_address": ip_address,
                "timestamp": datetime.now().isoformat()
            }
            
            if user_id:
                data["user_id"] = user_id
            
            if error_message:
                data["error_message"] = error_message
                
            self.supabase.table("login_attempts").insert(data).execute()
        except Exception as e:
            logger.error(f"Erro ao registrar tentativa de login: {e}")

    def get_all_users(self) -> List[Dict[str, Any]]:
        """
        Listar todos os usuários (apenas para admin)
        Requer service_role key configurada em config.SUPABASE_SERVICE_KEY
        """
        try:
            # Precisamos usar o cliente admin para listar usuários
            if not config.SUPABASE_SERVICE_KEY:
                logger.warning("SUPABASE_SERVICE_KEY não configurada. Não é possível listar usuários.")
                return []
                
            admin_client = create_client(config.SUPABASE_URL, config.SUPABASE_SERVICE_KEY)
            
            # Buscar perfis
            response = admin_client.table("user_profiles").select("*").execute()
            
            users = []
            for profile in response.data:
                # Buscar dados de auth se possível (opcional)
                try:
                    auth_user = admin_client.auth.admin.get_user_by_id(profile['user_id'])
                    email = auth_user.user.email
                    last_sign_in = auth_user.user.last_sign_in_at
                except:
                    email = "N/A"
                    last_sign_in = None
                
                users.append({
                    "id": profile["user_id"],
                    "username": email.split("@")[0] if email else "unknown",
                    "full_name": profile["full_name"],
                    "email": email,
                    "role": profile["role"],
                    "is_active": profile["is_active"],
                    "created_at": profile["created_at"],
                    "last_login": last_sign_in
                })
                
            return users
        except Exception as e:
            logger.error(f"Erro ao listar usuários: {e}")
            return []

    def create_user(self, username, password, full_name, email=None, role="user", created_by=None):
        """Criar novo usuário (apenas admin)"""
        try:
            if not config.SUPABASE_SERVICE_KEY:
                logger.error("SUPABASE_SERVICE_KEY necessária para criar usuários")
                return False
                
            admin_client = create_client(config.SUPABASE_URL, config.SUPABASE_SERVICE_KEY)
            
            # Se email não fornecido, usar username como email (ou criar email fictício)
            user_email = email if email else (username if "@" in username else f"{username}@badilab.local")
            
            # Criar usuário no Auth
            response = admin_client.auth.admin.create_user({
                "email": user_email,
                "password": password,
                "email_confirm": True,
                "user_metadata": {
                    "full_name": full_name,
                    "role": role
                }
            })
            
            if response.user:
                # O trigger no banco deve criar o user_profile automaticamente
                # Mas podemos forçar atualização se necessário
                return True
            return False
        except Exception as e:
            logger.error(f"Erro ao criar usuário {username}: {e}")
            return False

    def update_user(self, user_id, **kwargs):
        """Atualizar usuário"""
        try:
            if not config.SUPABASE_SERVICE_KEY:
                return False
                
            admin_client = create_client(config.SUPABASE_URL, config.SUPABASE_SERVICE_KEY)
            
            # Atualizar perfil
            data = {}
            if 'role' in kwargs:
                data['role'] = kwargs['role']
            if 'is_active' in kwargs:
                data['is_active'] = kwargs['is_active']
            if 'full_name' in kwargs:
                data['full_name'] = kwargs['full_name']
                
            if data:
                admin_client.table("user_profiles").update(data).eq("user_id", user_id).execute()
                return True
            return False
        except Exception as e:
            logger.error(f"Erro ao atualizar usuário {user_id}: {e}")
            return False

    def change_password(self, email, old_password, new_password):
        """Alterar senha do usuário atual"""
        try:
            # Primeiro verificar senha antiga fazendo login
            login = self.sign_in(email, old_password)
            if not login:
                return False
                
            # Atualizar senha
            self.supabase.auth.update_user({"password": new_password})
            return True
        except Exception as e:
            logger.error(f"Erro ao alterar senha: {e}")
            return False

    def get_login_history(self, limit=100):
        """Buscar histórico de tentativas de login"""
        try:
            response = self.supabase.table("login_attempts").select("*").order("timestamp", desc=True).limit(limit).execute()
            
            # Converter para formato compatível com auth_ui
            history = []
            for attempt in response.data:
                history.append({
                    "timestamp": attempt["timestamp"],
                    "username": attempt["email"],
                    "success": attempt["success"],
                    "ip_address": attempt.get("ip_address", "unknown")
                })
            return history
        except Exception as e:
            logger.error(f"Erro ao buscar histórico de login: {e}")
            return []

    def user_exists(self, username):
        """Verificar se usuário existe (por email)"""
        try:
            if not config.SUPABASE_SERVICE_KEY:
                return False
                
            admin_client = create_client(config.SUPABASE_URL, config.SUPABASE_SERVICE_KEY)
            
            # Buscar por email (username é tratado como email no Supabase)
            email = username if "@" in username else f"{username}@example.com"
            
            # Verificar na tabela de perfis
            response = admin_client.table("user_profiles").select("user_id").execute()
            
            # Buscar todos os usuários e verificar emails
            for profile in response.data:
                try:
                    user = admin_client.auth.admin.get_user_by_id(profile["user_id"])
                    if user.user.email == email or user.user.email.split("@")[0] == username:
                        return True
                except:
                    continue
                    
            return False
        except Exception as e:
            logger.error(f"Erro ao verificar existência de usuário: {e}")
            return False
