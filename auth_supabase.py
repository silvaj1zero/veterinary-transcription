"""
Sistema de Autenticação com Supabase
Usa Supabase Auth nativo para gerenciar usuários e sessões
"""

import logging
from typing import Optional, Dict, List
from datetime import datetime
from supabase import create_client, Client
import config

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SupabaseAuthManager:
    """Gerenciador de autenticação usando Supabase Auth"""

    def __init__(self):
        """Inicializar cliente Supabase"""
        if not config.SUPABASE_URL or not config.SUPABASE_KEY:
            raise ValueError("SUPABASE_URL e SUPABASE_KEY devem estar configurados no .env")

        self.supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
        logger.info("Supabase Auth inicializado")

    def signup(self, email: str, password: str, full_name: str, role: str = "user") -> Optional[Dict]:
        """
        Criar novo usuário no Supabase Auth

        Args:
            email: Email do usuário
            password: Senha (será hasheada pelo Supabase)
            full_name: Nome completo
            role: Função do usuário (admin/user/viewer)

        Returns:
            Dados do usuário criado ou None se falhar
        """
        try:
            # Criar usuário no Supabase Auth
            response = self.supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "full_name": full_name,
                        "role": role
                    }
                }
            })

            if response.user:
                logger.info(f"Usuário criado: {email} (role: {role})")

                # O perfil será criado automaticamente pelo trigger handle_new_user()
                # definido no schema SQL

                return {
                    'id': response.user.id,
                    'email': response.user.email,
                    'full_name': full_name,
                    'role': role
                }
            else:
                logger.error("Falha ao criar usuário: resposta vazia")
                return None

        except Exception as e:
            logger.error(f"Erro ao criar usuário {email}: {e}")
            return None

    def sign_in(self, email: str, password: str, ip_address: str = "unknown") -> Optional[Dict]:
        """
        Autenticar usuário com email/senha

        Args:
            email: Email do usuário
            password: Senha
            ip_address: IP para auditoria

        Returns:
            Dados do usuário autenticado ou None se falhar
        """
        try:
            # Autenticar com Supabase Auth
            response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if response.user:
                # Buscar perfil do usuário
                profile = self.supabase.table('user_profiles')\
                    .select('*')\
                    .eq('user_id', response.user.id)\
                    .single()\
                    .execute()

                if profile.data:
                    # Verificar se usuário está ativo
                    if not profile.data.get('is_active', True):
                        logger.warning(f"Tentativa de login com usuário inativo: {email}")
                        self._log_login_attempt(response.user.id, email, False, ip_address, "User inactive")
                        return None

                    # Registrar tentativa bem-sucedida
                    self._log_login_attempt(response.user.id, email, True, ip_address)

                    logger.info(f"Login bem-sucedido: {email}")

                    return {
                        'id': response.user.id,
                        'email': response.user.email,
                        'full_name': profile.data.get('full_name', email),
                        'role': profile.data.get('role', 'user'),
                        'is_active': profile.data.get('is_active', True),
                        'session': response.session
                    }
                else:
                    logger.error(f"Perfil não encontrado para usuário: {email}")
                    return None
            else:
                logger.warning(f"Falha no login: {email}")
                self._log_login_attempt(None, email, False, ip_address, "Invalid credentials")
                return None

        except Exception as e:
            logger.error(f"Erro no login {email}: {e}")
            self._log_login_attempt(None, email, False, ip_address, str(e))
            return None

    def sign_out(self) -> bool:
        """
        Fazer logout do usuário atual

        Returns:
            True se sucesso, False se falhar
        """
        try:
            self.supabase.auth.sign_out()
            logger.info("Logout realizado")
            return True
        except Exception as e:
            logger.error(f"Erro no logout: {e}")
            return False

    def get_session(self) -> Optional[Dict]:
        """
        Obter sessão atual do usuário

        Returns:
            Dados da sessão ou None se não estiver logado
        """
        try:
            session = self.supabase.auth.get_session()
            return session
        except Exception as e:
            logger.error(f"Erro ao obter sessão: {e}")
            return None

    def get_user(self) -> Optional[Dict]:
        """
        Obter usuário atual da sessão

        Returns:
            Dados do usuário ou None se não estiver logado
        """
        try:
            user = self.supabase.auth.get_user()
            if user:
                # Buscar perfil completo
                profile = self.supabase.table('user_profiles')\
                    .select('*')\
                    .eq('user_id', user.user.id)\
                    .single()\
                    .execute()

                if profile.data:
                    return {
                        'id': user.user.id,
                        'email': user.user.email,
                        'full_name': profile.data.get('full_name'),
                        'role': profile.data.get('role'),
                        'is_active': profile.data.get('is_active', True)
                    }
            return None
        except Exception as e:
            logger.error(f"Erro ao obter usuário: {e}")
            return None

    def change_password(self, new_password: str) -> bool:
        """
        Alterar senha do usuário atual

        Args:
            new_password: Nova senha

        Returns:
            True se sucesso, False se falhar
        """
        try:
            response = self.supabase.auth.update_user({
                "password": new_password
            })

            if response.user:
                logger.info(f"Senha alterada para usuário: {response.user.email}")
                return True
            return False

        except Exception as e:
            logger.error(f"Erro ao alterar senha: {e}")
            return False

    def update_user_profile(self, user_id: str, **kwargs) -> bool:
        """
        Atualizar perfil do usuário

        Args:
            user_id: ID do usuário
            **kwargs: Campos a atualizar (full_name, role, is_active)

        Returns:
            True se sucesso, False se falhar
        """
        try:
            allowed_fields = ['full_name', 'role', 'is_active', 'metadata']
            updates = {k: v for k, v in kwargs.items() if k in allowed_fields}

            if not updates:
                logger.warning("Nenhum campo válido para atualizar")
                return False

            updates['updated_at'] = datetime.now().isoformat()

            response = self.supabase.table('user_profiles')\
                .update(updates)\
                .eq('user_id', user_id)\
                .execute()

            if response.data:
                logger.info(f"Perfil atualizado: {user_id}")
                return True
            return False

        except Exception as e:
            logger.error(f"Erro ao atualizar perfil {user_id}: {e}")
            return False

    def get_all_users(self) -> List[Dict]:
        """
        Listar todos os usuários (apenas para admins)

        Returns:
            Lista de usuários
        """
        try:
            response = self.supabase.table('user_profiles')\
                .select('*')\
                .order('created_at', desc=True)\
                .execute()

            return response.data if response.data else []

        except Exception as e:
            logger.error(f"Erro ao listar usuários: {e}")
            return []

    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """
        Buscar usuário por ID

        Args:
            user_id: ID do usuário

        Returns:
            Dados do usuário ou None
        """
        try:
            response = self.supabase.table('user_profiles')\
                .select('*')\
                .eq('user_id', user_id)\
                .single()\
                .execute()

            return response.data if response.data else None

        except Exception as e:
            logger.error(f"Erro ao buscar usuário {user_id}: {e}")
            return None

    def get_login_history(self, email: str = None, limit: int = 50) -> List[Dict]:
        """
        Obter histórico de tentativas de login

        Args:
            email: Filtrar por email (opcional)
            limit: Número máximo de registros

        Returns:
            Lista de tentativas de login
        """
        try:
            query = self.supabase.table('login_attempts')\
                .select('*')\
                .order('timestamp', desc=True)\
                .limit(limit)

            if email:
                query = query.eq('email', email)

            response = query.execute()
            return response.data if response.data else []

        except Exception as e:
            logger.error(f"Erro ao obter histórico de login: {e}")
            return []

    def _log_login_attempt(self, user_id: Optional[str], email: str,
                          success: bool, ip_address: str, error_message: str = None):
        """
        Registrar tentativa de login

        Args:
            user_id: ID do usuário (se autenticado)
            email: Email usado
            success: Se login foi bem-sucedido
            ip_address: IP do cliente
            error_message: Mensagem de erro (se houver)
        """
        try:
            self.supabase.table('login_attempts').insert({
                'user_id': user_id,
                'email': email,
                'success': success,
                'ip_address': ip_address,
                'error_message': error_message,
                'timestamp': datetime.now().isoformat()
            }).execute()
        except Exception as e:
            logger.error(f"Erro ao registrar tentativa de login: {e}")

    def reset_password_email(self, email: str) -> bool:
        """
        Enviar email de recuperação de senha

        Args:
            email: Email do usuário

        Returns:
            True se email foi enviado
        """
        try:
            self.supabase.auth.reset_password_for_email(email)
            logger.info(f"Email de recuperação enviado para: {email}")
            return True
        except Exception as e:
            logger.error(f"Erro ao enviar email de recuperação: {e}")
            return False

    def delete_user(self, user_id: str) -> bool:
        """
        Desativar usuário (soft delete)

        Args:
            user_id: ID do usuário

        Returns:
            True se sucesso
        """
        try:
            # Soft delete - apenas desativa
            return self.update_user_profile(user_id, is_active=False)
        except Exception as e:
            logger.error(f"Erro ao desativar usuário {user_id}: {e}")
            return False

    def reactivate_user(self, user_id: str) -> bool:
        """
        Reativar usuário

        Args:
            user_id: ID do usuário

        Returns:
            True se sucesso
        """
        try:
            return self.update_user_profile(user_id, is_active=True)
        except Exception as e:
            logger.error(f"Erro ao reativar usuário {user_id}: {e}")
            return False
