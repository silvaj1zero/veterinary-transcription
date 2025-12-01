# Sistema de Autenticação - Veterinary Transcription

## 📋 Resumo

Foi implementado um sistema completo de autenticação de usuários com os seguintes recursos:

### ✅ Funcionalidades Implementadas

1. **Sistema de Login/Logout**
   - Página de login estilizada
   - Autenticação segura com senhas criptografadas (PBKDF2 + SHA256)
   - Sessão persistente durante uso da aplicação

2. **Gerenciamento de Usuários** (apenas Admin)
   - Criar novos usuários
   - Editar informações de usuários
   - Ativar/Desativar usuários
   - Alterar funções (user/admin)
   - Histórico de logins

3. **Níveis de Acesso**
   - **Admin**: Acesso total + gerenciamento de usuários
   - **User**: Acesso às funcionalidades principais

4. **Segurança**
   - Senhas criptografadas com salt único por usuário
   - Histórico de tentativas de login
   - Soft delete (desativação em vez de exclusão)

### 📁 Arquivos Criados

1. **`auth.py`** - Sistema de autenticação backend
   - Classe `AuthManager` com todos os métodos de gerenciamento
   - Banco de dados SQLite (`data/users.db`)
   - Funções de hash de senha seguras

2. **`auth_ui.py`** - Componentes de UI
   - `show_login_page()` - Página de login
   - `show_user_menu()` - Menu do usuário na sidebar
   - `show_user_management()` - Painel de gerenciamento (admin)
   - `show_change_password()` - Formulário de alteração de senha

### 🔐 Credenciais Padrão

```
Usuário: admin
Senha: admin123
```

⚠️ **IMPORTANTE**: Altere a senha padrão após o primeiro login!

### 🚀 Como Integrar no app.py

Para integrar o sistema de autenticação no `app.py`, adicione as seguintes linhas:

#### 1. Imports (após as importações existentes, linha ~26)

```python
from auth import AuthManager
from auth_ui import show_login_page, show_user_menu, show_user_management, show_change_password
```

#### 2. Inicialização (após as funções auxiliares, antes da sidebar, linha ~160)

```python
# Inicializar sistema de autenticação
auth_manager = AuthManager()

# Verificar autenticação
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
    st.session_state['user'] = None

# Se não estiver autenticado, mostrar página de login
if not st.session_state['authenticated']:
    show_login_page(auth_manager)
    st.stop()

# Usuário autenticado - continuar com a aplicação
current_user = st.session_state['user']
```

#### 3. Atualizar Menu de Navegação (na sidebar, linha ~191)

```python
# Menu de navegação
menu_options = ["📊 Dashboard", "➕ Nova Consulta", "📋 Histórico", "⚙️ Configurações"]

# Adicionar opção de gerenciamento de usuários para admins
if current_user['role'] == 'admin':
    menu_options.append("👥 Usuários")

menu = st.radio(
    "Navegação",
    menu_options,
    label_visibility="collapsed"
)
```

#### 4. Adicionar Menu do Usuário (na sidebar, após as métricas, linha ~205)

```python
# Informações do usuário e botão de logout
show_user_menu(current_user)
```

#### 5. Adicionar Página de Gerenciamento (no conteúdo principal, após as outras páginas)

```python
elif menu == "👥 Usuários":
    show_user_management(auth_manager, current_user)
```

#### 6. Adicionar Alteração de Senha (na página de Configurações)

Dentro da página "⚙️ Configurações", adicione uma nova aba:

```python
with st.tabs(["...", "🔒 Alterar Senha"]):
    # ... outras abas ...
    
    with tab_senha:
        show_change_password(auth_manager, current_user)
```

### 📊 Estrutura do Banco de Dados

**Tabela: users**
- id (PK)
- username (UNIQUE)
- password_hash
- salt
- full_name
- email
- role (user/admin)
- is_active (0/1)
- created_at
- last_login
- created_by

**Tabela: login_attempts**
- id (PK)
- username
- success (0/1)
- ip_address
- timestamp

### 🎨 Recursos de UI

- Página de login com gradiente roxo moderno
- Formulários de gerenciamento intuitivos
- Tabela de histórico de logins
- Indicadores visuais de status (🟢 ativo / 🔴 inativo)
- Mensagens de feedback claras

### 🔧 Próximos Passos Sugeridos

1. **Integrar no app.py** seguindo as instruções acima
2. **Testar o login** com as credenciais padrão
3. **Criar usuários adicionais** via painel admin
4. **Alterar senha padrão** do admin
5. **Testar níveis de acesso** (admin vs user)

### 📝 Notas Técnicas

- O banco de dados é criado automaticamente em `data/users.db`
- As senhas nunca são armazenadas em texto plano
- O sistema usa PBKDF2 com 100.000 iterações para máxima segurança
- Soft delete preserva histórico de usuários
- Login attempts são registrados para auditoria

### 🐛 Troubleshooting

**Erro: "No module named 'auth'"**
- Certifique-se de que `auth.py` e `auth_ui.py` estão no diretório raiz do projeto

**Erro: "Unable to open database file"**
- Verifique se o diretório `data/` existe e tem permissões de escrita

**Esqueci a senha do admin**
- Delete o arquivo `data/users.db` - um novo admin será criado automaticamente

### 📚 Exemplo de Uso

```python
# Criar novo usuário
auth_manager.create_user(
    username="joao",
    password="senha123",
    full_name="João Silva",
    email="joao@clinica.com",
    role="user"
)

# Autenticar
user = auth_manager.authenticate("joao", "senha123")
if user:
    print(f"Bem-vindo, {user['full_name']}!")

# Alterar senha
auth_manager.change_password("joao", "senha123", "novaSenha456")

# Desativar usuário
auth_manager.delete_user(user_id=2)
```

---

**Desenvolvido para BadiLab - Sistema de Documentação Veterinária**
**Versão 1.7 - Authentication System**
