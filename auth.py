"""
Sistema de Autenticação para Veterinary Transcription System
Gerenciamento de usuários com níveis de acesso e senhas criptografadas
"""

import sqlite3
import hashlib
import secrets
from pathlib import Path
from datetime import datetime
import logging
from typing import Optional, Dict, List

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthManager:
    """Gerenciador de autenticação e usuários"""
    
    def __init__(self, db_path: str = "data/users.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
        self._create_default_admin()
    
    def _init_database(self):
        """Inicializar banco de dados de usuários"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                full_name TEXT NOT NULL,
                email TEXT,
                role TEXT NOT NULL DEFAULT 'user',
                is_active INTEGER DEFAULT 1,
                created_at TEXT NOT NULL,
                last_login TEXT,
                created_by TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS login_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                success INTEGER NOT NULL,
                ip_address TEXT,
                timestamp TEXT NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
        logger.info("Banco de dados de usuários inicializado")
    
    def _create_default_admin(self):
        """Criar usuário admin padrão se não existir"""
        if not self.user_exists("admin"):
            self.create_user(
                username="admin",
                password="admin123",
                full_name="Administrador",
                email="admin@badilab.com",
                role="admin",
                created_by="system"
            )
            logger.warning("⚠️ Usuário admin padrão criado. ALTERE A SENHA IMEDIATAMENTE!")
            logger.warning("   Username: admin | Password: admin123")
    
    def _hash_password(self, password: str, salt: str = None) -> tuple:
        """Hash de senha com salt"""
        if salt is None:
            salt = secrets.token_hex(32)
        
        pwd_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return pwd_hash.hex(), salt
    
    def create_user(self, username: str, password: str, full_name: str, 
                   email: str = "", role: str = "user", created_by: str = "admin") -> bool:
        """Criar novo usuário"""
        try:
            if self.user_exists(username):
                logger.warning(f"Tentativa de criar usuário duplicado: {username}")
                return False
            
            pwd_hash, salt = self._hash_password(password)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO users (username, password_hash, salt, full_name, email, role, created_at, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (username, pwd_hash, salt, full_name, email, role, datetime.now().isoformat(), created_by))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Usuário criado: {username} (role: {role})")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao criar usuário {username}: {e}")
            return False
    
    def authenticate(self, username: str, password: str, ip_address: str = "unknown") -> Optional[Dict]:
        """Autenticar usuário"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, username, password_hash, salt, full_name, email, role, is_active
                FROM users WHERE username = ?
            """, (username,))
            
            user = cursor.fetchone()
            
            if not user:
                self._log_login_attempt(username, False, ip_address)
                logger.warning(f"Tentativa de login com usuário inexistente: {username}")
                return None
            
            user_id, username, stored_hash, salt, full_name, email, role, is_active = user
            
            if not is_active:
                logger.warning(f"Tentativa de login com usuário inativo: {username}")
                return None
            
            # Verificar senha
            pwd_hash, _ = self._hash_password(password, salt)
            
            if pwd_hash == stored_hash:
                # Login bem-sucedido
                cursor.execute("""
                    UPDATE users SET last_login = ? WHERE id = ?
                """, (datetime.now().isoformat(), user_id))
                
                conn.commit()
                self._log_login_attempt(username, True, ip_address)
                
                logger.info(f"Login bem-sucedido: {username}")
                
                user_data = {
                    'id': user_id,
                    'username': username,
                    'full_name': full_name,
                    'email': email,
                    'role': role
                }
                
                conn.close()
                return user_data
            else:
                self._log_login_attempt(username, False, ip_address)
                logger.warning(f"Senha incorreta para usuário: {username}")
                conn.close()
                return None
                
        except Exception as e:
            logger.error(f"Erro ao autenticar usuário {username}: {e}")
            return None
    
    def _log_login_attempt(self, username: str, success: bool, ip_address: str):
        """Registrar tentativa de login"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO login_attempts (username, success, ip_address, timestamp)
                VALUES (?, ?, ?, ?)
            """, (username, 1 if success else 0, ip_address, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Erro ao registrar tentativa de login: {e}")
    
    def user_exists(self, username: str) -> bool:
        """Verificar se usuário existe"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
        exists = cursor.fetchone()[0] > 0
        
        conn.close()
        return exists
    
    def get_all_users(self) -> List[Dict]:
        """Obter lista de todos os usuários"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, full_name, email, role, is_active, created_at, last_login
            FROM users
            ORDER BY created_at DESC
        """)
        
        users = []
        for row in cursor.fetchall():
            users.append({
                'id': row[0],
                'username': row[1],
                'full_name': row[2],
                'email': row[3],
                'role': row[4],
                'is_active': bool(row[5]),
                'created_at': row[6],
                'last_login': row[7]
            })
        
        conn.close()
        return users
    
    def update_user(self, user_identifier, **kwargs) -> bool:
        """Atualizar dados do usuário (aceita user_id ou username)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Determinar se é username ou user_id
            if isinstance(user_identifier, str):
                # É username - buscar ID
                cursor.execute("SELECT id FROM users WHERE username = ?", (user_identifier,))
                result = cursor.fetchone()
                if not result:
                    logger.warning(f"Usuário não encontrado: {user_identifier}")
                    conn.close()
                    return False
                user_id = result[0]
            else:
                # É user_id direto
                user_id = user_identifier

            allowed_fields = ['full_name', 'email', 'role', 'is_active']
            updates = []
            values = []

            for field, value in kwargs.items():
                if field in allowed_fields:
                    updates.append(f"{field} = ?")
                    values.append(value)

            if not updates:
                conn.close()
                return False

            values.append(user_id)
            query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"

            cursor.execute(query, values)
            conn.commit()
            conn.close()

            logger.info(f"Usuário {user_identifier} atualizado")
            return True

        except Exception as e:
            logger.error(f"Erro ao atualizar usuário {user_identifier}: {e}")
            return False
    
    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """Alterar senha do usuário"""
        try:
            # Verificar senha antiga
            user = self.authenticate(username, old_password)
            if not user:
                return False
            
            # Gerar novo hash
            pwd_hash, salt = self._hash_password(new_password)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE users SET password_hash = ?, salt = ? WHERE username = ?
            """, (pwd_hash, salt, username))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Senha alterada para usuário: {username}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao alterar senha: {e}")
            return False
    
    def delete_user(self, user_id: int) -> bool:
        """Deletar usuário (soft delete - desativa)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("UPDATE users SET is_active = 0 WHERE id = ?", (user_id,))
            conn.commit()
            conn.close()
            
            logger.info(f"Usuário {user_id} desativado")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao deletar usuário {user_id}: {e}")
            return False
    
    def get_login_history(self, username: str = None, limit: int = 50) -> List[Dict]:
        """Obter histórico de logins"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if username:
            cursor.execute("""
                SELECT username, success, ip_address, timestamp
                FROM login_attempts
                WHERE username = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (username, limit))
        else:
            cursor.execute("""
                SELECT username, success, ip_address, timestamp
                FROM login_attempts
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))
        
        history = []
        for row in cursor.fetchall():
            history.append({
                'username': row[0],
                'success': bool(row[1]),
                'ip_address': row[2],
                'timestamp': row[3]
            })
        
        conn.close()
        return history
