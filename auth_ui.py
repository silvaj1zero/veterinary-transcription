"""
Componentes de UI para autenticação
"""

import streamlit as st
import pandas as pd
from auth import AuthManager
import logging

logger = logging.getLogger(__name__)

def show_login_page(auth_manager: AuthManager):
    """Exibir página de login"""
    
    # CSS customizado para página de login
    st.markdown("""
    <style>
        .login-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        .login-header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        .login-header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        .login-header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="login-header">
            <h1>🐾 BadiLab</h1>
            <p>Sistema de Documentação Veterinária</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("👤 Usuário", placeholder="Digite seu usuário")
            password = st.text_input("🔒 Senha", type="password", placeholder="Digite sua senha")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                submit = st.form_submit_button("🚀 Entrar", use_container_width=True, type="primary")
            with col_btn2:
                if st.form_submit_button("❓ Ajuda", use_container_width=True):
                    st.info("""
                    **Credenciais padrão:**
                    - Usuário: `admin`
                    - Senha: `admin123`
                    
                    ⚠️ **Altere a senha após o primeiro login!**
                    """)
            
            if submit:
                if not username or not password:
                    st.error("❌ Por favor, preencha usuário e senha")
                else:
                    user = auth_manager.authenticate(username, password)
                    
                    if user:
                        st.session_state['authenticated'] = True
                        st.session_state['user'] = user
                        st.success(f"✅ Bem-vindo, {user['full_name']}!")
                        logger.info(f"Login bem-sucedido: {username}")
                        st.rerun()
                    else:
                        st.error("❌ Usuário ou senha incorretos")
                        logger.warning(f"Tentativa de login falhou: {username}")

def show_user_menu(user: dict):
    """Exibir menu do usuário na sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**👤 {user['full_name']}**")
    st.sidebar.caption(f"@{user['username']} | {user['role'].upper()}")
    
    if st.sidebar.button("🚪 Sair", use_container_width=True):
        st.session_state['authenticated'] = False
        st.session_state['user'] = None
        logger.info(f"Logout: {user['username']}")
        st.rerun()

def show_user_management(auth_manager: AuthManager, current_user: dict):
    """Página de gerenciamento de usuários (apenas admin)"""
    
    if current_user['role'] != 'admin':
        st.error("❌ Acesso negado. Apenas administradores podem acessar esta página.")
        return
    
    st.markdown('<p class="main-header">👥 Gerenciamento de Usuários</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📋 Usuários", "➕ Novo Usuário", "📊 Histórico de Logins"])
    
    with tab1:
        st.subheader("Lista de Usuários")
        users = auth_manager.get_all_users()
        
        if users:
            for user in users:
                with st.expander(f"{'🟢' if user['is_active'] else '🔴'} {user['full_name']} (@{user['username']})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**ID:** {user['id']}")
                        st.write(f"**Email:** {user['email'] or 'Não informado'}")
                        st.write(f"**Função:** {user['role'].upper()}")
                        st.write(f"**Status:** {'Ativo' if user['is_active'] else 'Inativo'}")
                    
                    with col2:
                        st.write(f"**Criado em:** {str(user['created_at'])[:10]}")
                        st.write(f"**Último login:** {str(user['last_login'])[:10] if user['last_login'] else 'Nunca'}")
                    
                    st.markdown("---")
                    
                    col_btn1, col_btn2, col_btn3 = st.columns(3)
                    
                    with col_btn1:
                        if user['username'] != 'admin':  # Não permitir desativar admin
                            if user['is_active']:
                                if st.button(f"🔴 Desativar", key=f"deactivate_{user['id']}"):
                                    if auth_manager.update_user(user['id'], is_active=0):
                                        st.success("Usuário desativado!")
                                        st.rerun()
                            else:
                                if st.button(f"🟢 Ativar", key=f"activate_{user['id']}"):
                                    if auth_manager.update_user(user['id'], is_active=1):
                                        st.success("Usuário ativado!")
                                        st.rerun()
                    
                    with col_btn2:
                        new_role = st.selectbox(
                            "Alterar função",
                            ["user", "admin"],
                            index=0 if user['role'] == 'user' else 1,
                            key=f"role_{user['id']}"
                        )
                        if st.button("💾 Salvar", key=f"save_role_{user['id']}"):
                            if auth_manager.update_user(user['id'], role=new_role):
                                st.success("Função atualizada!")
                                st.rerun()
        else:
            st.info("Nenhum usuário cadastrado")
    
    with tab2:
        st.subheader("Criar Novo Usuário")
        
        with st.form("new_user_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_username = st.text_input("Usuário *", placeholder="Ex: joao.silva")
                new_full_name = st.text_input("Nome Completo *", placeholder="Ex: João Silva")
                new_email = st.text_input("Email", placeholder="Ex: joao@clinica.com")
            
            with col2:
                new_password = st.text_input("Senha *", type="password", placeholder="Mínimo 6 caracteres")
                new_password_confirm = st.text_input("Confirmar Senha *", type="password")
                new_role = st.selectbox("Função", ["user", "admin"])
            
            submitted = st.form_submit_button("➕ Criar Usuário", type="primary", use_container_width=True)
            
            if submitted:
                # Validações
                if not new_username or not new_password or not new_full_name:
                    st.error("❌ Preencha todos os campos obrigatórios")
                elif len(new_password) < 6:
                    st.error("❌ A senha deve ter no mínimo 6 caracteres")
                elif new_password != new_password_confirm:
                    st.error("❌ As senhas não coincidem")
                elif auth_manager.user_exists(new_username):
                    st.error(f"❌ Usuário '{new_username}' já existe")
                else:
                    if auth_manager.create_user(
                        username=new_username,
                        password=new_password,
                        full_name=new_full_name,
                        email=new_email,
                        role=new_role,
                        created_by=current_user['username']
                    ):
                        st.success(f"✅ Usuário '{new_username}' criado com sucesso!")
                        logger.info(f"Novo usuário criado: {new_username} por {current_user['username']}")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao criar usuário")
    
    with tab3:
        st.subheader("Histórico de Logins")
        
        history = auth_manager.get_login_history(limit=100)
        
        if history:
            df = pd.DataFrame(history)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['status'] = df['success'].apply(lambda x: '✅ Sucesso' if x else '❌ Falha')
            
            st.dataframe(
                df[['timestamp', 'username', 'status', 'ip_address']].rename(columns={
                    'timestamp': 'Data/Hora',
                    'username': 'Usuário',
                    'status': 'Status',
                    'ip_address': 'IP'
                }),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Nenhum histórico de login disponível")

def show_change_password(auth_manager: AuthManager, current_user: dict):
    """Formulário para alterar senha"""
    st.subheader("🔒 Alterar Senha")
    
    with st.form("change_password_form"):
        old_password = st.text_input("Senha Atual", type="password")
        new_password = st.text_input("Nova Senha", type="password")
        new_password_confirm = st.text_input("Confirmar Nova Senha", type="password")
        
        submitted = st.form_submit_button("💾 Alterar Senha", type="primary")
        
        if submitted:
            if not old_password or not new_password:
                st.error("❌ Preencha todos os campos")
            elif len(new_password) < 6:
                st.error("❌ A nova senha deve ter no mínimo 6 caracteres")
            elif new_password != new_password_confirm:
                st.error("❌ As senhas não coincidem")
            else:
                if auth_manager.change_password(
                    current_user['username'],
                    old_password,
                    new_password
                ):
                    st.success("✅ Senha alterada com sucesso!")
                    logger.info(f"Senha alterada: {current_user['username']}")
                else:
                    st.error("❌ Senha atual incorreta")
