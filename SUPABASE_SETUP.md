# 🚀 Guia Completo de Setup Supabase

**Sistema de Documentação Veterinária v1.8**
**Migração de SQLite para Supabase**

---

## 📋 Índice

1. [Por que Supabase?](#por-que-supabase)
2. [Criar Projeto no Supabase](#criar-projeto-no-supabase)
3. [Configurar Banco de Dados](#configurar-banco-de-dados)
4. [Configurar Storage (Opcional)](#configurar-storage-opcional)
5. [Configurar Variáveis de Ambiente](#configurar-variáveis-de-ambiente)
6. [Migrar Dados do SQLite](#migrar-dados-do-sqlite)
7. [Ativar Supabase no Sistema](#ativar-supabase-no-sistema)
8. [Testar Integração](#testar-integração)
9. [Troubleshooting](#troubleshooting)

---

## 🎯 Por que Supabase?

### Vantagens sobre SQLite:

| Recurso | SQLite | Supabase |
|---------|--------|----------|
| **Escalabilidade** | ~100 users | Ilimitado |
| **Backup Automático** | ❌ Manual | ✅ Automático (7-30 dias) |
| **Perda de Dados (Railway)** | ❌ Risco em redeploy | ✅ Seguro (cloud) |
| **Concorrência** | ⚠️ Limitada | ✅ Alta |
| **Auth Nativo** | ❌ Implementar | ✅ Pronto (OAuth, 2FA, etc) |
| **Storage** | ❌ Não incluído | ✅ 1GB grátis |
| **Realtime** | ❌ | ✅ Websockets |
| **Dashboard** | ❌ | ✅ Visual completo |
| **Custo** | $0 | $0 (Free tier) / $25 (Pro) |

---

## 🆕 1. Criar Projeto no Supabase

### Passo 1.1: Criar Conta

1. Acesse: https://supabase.com
2. Clique em **"Start your project"**
3. Faça login com GitHub (recomendado) ou email

### Passo 1.2: Criar Novo Projeto

1. Clique em **"New Project"**
2. Preencha:
   - **Name:** `veterinary-transcription` (ou outro nome)
   - **Database Password:** Gere uma senha forte (guarde bem!)
   - **Region:** Escolha o mais próximo (ex: `South America (São Paulo)`)
   - **Pricing Plan:** `Free` (suficiente para começar)
3. Clique em **"Create new project"**
4. ⏳ Aguarde 2-3 minutos (provisionando infraestrutura)

### Passo 1.3: Obter Credenciais

Após o projeto ser criado:

1. Vá em **Settings** → **API**
2. Copie as seguintes informações:

```
Project URL: https://xxxxxxxxxxx.supabase.co
anon/public key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
service_role key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

⚠️ **IMPORTANTE:**
- `anon/public key` → Usar no frontend/backend (seguro para expor)
- `service_role key` → Apenas backend (NUNCA expor ao cliente)

---

## 🗄️ 2. Configurar Banco de Dados

### Passo 2.1: Executar Schema SQL

1. No dashboard do Supabase, vá em **SQL Editor** (ícone 📝)
2. Clique em **"+ New query"**
3. Copie TODO o conteúdo de `supabase_schema.sql`
4. Cole no editor
5. Clique em **"Run"** (▶️)
6. Verifique se aparece: ✅ **"Success. No rows returned"**

### Passo 2.2: Verificar Tabelas Criadas

1. Vá em **Table Editor** (ícone 📋)
2. Você deve ver:
   - ✅ `user_profiles`
   - ✅ `login_attempts`
   - ✅ `reports`
   - ✅ `transcriptions`

### Passo 2.3: Criar Primeiro Usuário Admin

**Opção A: Via Supabase Dashboard (Recomendado)**

1. Vá em **Authentication** → **Users**
2. Clique em **"Add user"** → **"Create new user"**
3. Preencha:
   - **Email:** seu-email@exemplo.com
   - **Password:** Senha forte
   - **Auto Confirm User:** ✅ Marque (pula verificação de email)
4. Clique em **"Create user"**
5. Copie o **User UID** (formato: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

6. Vá em **SQL Editor** e execute:

```sql
-- Substitua USER_ID_AQUI pelo UID copiado
UPDATE public.user_profiles
SET role = 'admin', full_name = 'Administrador'
WHERE user_id = 'USER_ID_AQUI';
```

**Opção B: Via Python (depois de configurar .env)**

```bash
python -c "
from auth_supabase import SupabaseAuthManager
auth = SupabaseAuthManager()
auth.signup('admin@exemplo.com', 'senha123', 'Administrador', 'admin')
print('Admin criado!')
"
```

---

## 📦 3. Configurar Storage (Opcional)

Se quiser armazenar áudios e relatórios no Supabase Storage:

### Passo 3.1: Criar Buckets

1. Vá em **Storage** (ícone 🗄️)
2. Clique em **"Create a new bucket"**
3. Criar 2 buckets:

**Bucket 1: audios**
- **Name:** `audios`
- **Public:** ❌ Não (privado)
- Clique em **"Create bucket"**

**Bucket 2: relatorios**
- **Name:** `relatorios`
- **Public:** ❌ Não (privado)
- Clique em **"Create bucket"**

### Passo 3.2: Configurar Políticas de Acesso

Para cada bucket, vá em **Policies** e adicione:

```sql
-- Policy: Usuários podem fazer upload
CREATE POLICY "Users can upload own files"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (bucket_id = 'audios' AND auth.uid()::text = (storage.foldername(name))[1]);

-- Policy: Usuários podem baixar próprios arquivos
CREATE POLICY "Users can download own files"
ON storage.objects FOR SELECT
TO authenticated
USING (bucket_id = 'audios' AND auth.uid()::text = (storage.foldername(name))[1]);
```

Repita para bucket `relatorios`.

---

## ⚙️ 4. Configurar Variáveis de Ambiente

### Passo 4.1: Atualizar `.env`

Edite o arquivo `.env` na raiz do projeto:

```bash
# API Keys existentes
ANTHROPIC_API_KEY=sua_chave_claude

# Supabase (NOVO)
SUPABASE_URL=https://xxxxxxxxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...  # anon key
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...  # service_role key

# Ativar Supabase
DATABASE_PROVIDER=supabase

# Outros (opcionais)
GOOGLE_API_KEY=sua_chave_gemini
TRANSCRIPTION_PROVIDER=openai_whisper
LLM_PROVIDER=anthropic_claude
```

### Passo 4.2: Configurar no Railway (se estiver usando)

1. Railway Dashboard → Seu Projeto → **Variables**
2. Adicionar:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `SUPABASE_SERVICE_KEY`
   - `DATABASE_PROVIDER=supabase`
3. **Deploy** → Aguardar redeploy automático

---

## 🔄 5. Migrar Dados do SQLite

Se você já tem usuários no SQLite local:

### Passo 5.1: Instalar Dependências

```bash
pip install supabase psycopg2-binary
```

### Passo 5.2: Executar Script de Migração

```bash
python migrate_sqlite_to_supabase.py
```

O script irá:
1. Ler usuários do `data/users.db`
2. Solicitar email e nova senha para cada usuário
3. Criar usuários no Supabase Auth
4. Criar perfis na tabela `user_profiles`

⚠️ **Notas:**
- Senhas NÃO podem ser migradas (são hashes)
- Você define novas senhas durante migração
- SQLite não é alterado (fazer backup antes de deletar)

---

## ✅ 6. Ativar Supabase no Sistema

### Passo 6.1: Atualizar `app.py`

O sistema já está preparado para usar Supabase. Basta garantir que:

```python
# Em app.py, trocar:
# from auth import AuthManager
# auth_manager = AuthManager()

# Por:
from auth_supabase import SupabaseAuthManager
import config

# Usar provider baseado em config
if config.DATABASE_PROVIDER == "supabase":
    auth_manager = SupabaseAuthManager()
else:
    from auth import AuthManager
    auth_manager = AuthManager()
```

Mas isso já deve estar implementado na versão atualizada do app.py.

### Passo 6.2: Reiniciar Aplicação

```bash
# Parar Streamlit atual (Ctrl+C)

# Reiniciar
streamlit run app.py
```

---

## 🧪 7. Testar Integração

### Teste 1: Login

1. Acesse: http://localhost:8501
2. Faça login com usuário admin criado
3. Verificar se login funciona
4. Verificar se nome e role aparecem corretamente

### Teste 2: Criar Usuário

1. Login como admin
2. Ir em **"👥 Usuários"**
3. Criar novo usuário
4. Logout e login com novo usuário
5. Verificar permissões

### Teste 3: Auditoria

1. No Supabase Dashboard → **Table Editor**
2. Abrir tabela `login_attempts`
3. Verificar se tentativas de login estão sendo registradas

### Teste 4: Criar Relatório

1. Criar uma consulta/relatório
2. Verificar se aparece em **Histórico**
3. No Supabase → Tabela `reports`
4. Verificar se registro foi criado

---

## 🐛 8. Troubleshooting

### Erro: "SUPABASE_URL e SUPABASE_KEY devem estar configurados"

**Solução:**
```bash
# Verificar se .env existe
cat .env

# Verificar se variáveis estão definidas
python -c "import config; print(config.SUPABASE_URL)"
```

Se vazio, revisar Passo 4.

---

### Erro: "Invalid API key"

**Causa:** Chave incorreta ou expirada

**Solução:**
1. Supabase Dashboard → Settings → API
2. Copiar novamente `anon key` e `service_role key`
3. Atualizar no `.env`

---

### Erro: "relation 'public.user_profiles' does not exist"

**Causa:** Schema SQL não foi executado

**Solução:**
1. Supabase → SQL Editor
2. Executar `supabase_schema.sql` novamente
3. Verificar mensagens de erro no console

---

### Erro: "row-level security policy"

**Causa:** RLS ativado mas sem policies corretas

**Solução:**
O schema já inclui policies. Verificar se foram criadas:

```sql
-- Verificar policies
SELECT * FROM pg_policies WHERE tablename = 'user_profiles';
```

---

### Performance Lenta

**Causa:** Region distante

**Solução:**
1. Criar novo projeto em region mais próxima
2. Migrar dados
3. Atualizar `.env`

Regions disponíveis:
- 🇧🇷 South America (São Paulo) - RECOMENDADO para Brasil
- 🇺🇸 East US (Virginia)
- 🇪🇺 West EU (Ireland)

---

## 📊 9. Monitoramento

### Dashboard do Supabase

**Verificar regularmente:**

1. **Database** → Database Health
   - Conexões ativas
   - Tamanho do banco
   - Queries lentas

2. **Auth** → Users
   - Usuários ativos
   - Últimos logins

3. **Logs** → Logs Explorer
   - Erros de API
   - Queries com erro

### Limites do Plano Free:

| Recurso | Free Tier | Pro Tier |
|---------|-----------|----------|
| Database | 500 MB | 8 GB |
| Storage | 1 GB | 100 GB |
| Bandwidth | 2 GB | 200 GB |
| Auth Users | Unlimited | Unlimited |
| Backups | 7 days | 30 days |

Se ultrapassar limites: Upgrade para Pro ($25/mês)

---

## ✨ 10. Recursos Avançados

### Email Templates

Personalizar emails de:
- Verificação de conta
- Recuperação de senha
- Magic Links

**Como:**
1. Supabase → Authentication → Email Templates
2. Editar HTML/CSS
3. Adicionar logo da clínica

### OAuth Providers

Habilitar login com:
- Google
- GitHub
- Microsoft
- Apple

**Como:**
1. Authentication → Providers
2. Ativar provider desejado
3. Configurar Client ID/Secret

### Webhooks

Receber notificações quando:
- Novo usuário se registra
- Relatório é criado
- Erro ocorre

**Como:**
1. Database → Webhooks
2. Configurar URL de callback
3. Selecionar eventos

---

## 🎓 Recursos de Aprendizado

- 📚 [Docs Oficiais](https://supabase.com/docs)
- 🎥 [Supabase YouTube](https://www.youtube.com/c/supabase)
- 💬 [Discord Community](https://discord.supabase.com)
- 🐦 [Twitter @supabase](https://twitter.com/supabase)

---

## 📞 Suporte

**Problemas com Supabase:**
- Free: Discord community
- Pro: Email support

**Problemas com a Integração:**
- Verificar logs: `veterinary_system_web.log`
- Executar testes: `python test_auth_system.py`
- Revisar este guia

---

**Versão:** 1.8 - Supabase Integration
**Última atualização:** Dezembro 2025
**Desenvolvido por:** BadiLab
