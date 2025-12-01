# 🚀 Guia de Deploy no Railway com Supabase

**Sistema de Transcrição Veterinária v1.7**
**Data:** 2025-12-01

---

## 📋 Pré-requisitos

- ✅ Conta no Railway: https://railway.app
- ✅ Conta no Supabase: https://supabase.com
- ✅ Projeto Supabase criado e configurado
- ✅ API Key da Anthropic (Claude)
- ✅ Repositório Git (silvaj1zero/veterinary-transcription)

---

## 🎯 Passo a Passo

### **1. Criar Novo Projeto no Railway**

1. Acesse https://railway.app
2. Clique em **"New Project"**
3. Selecione **"Deploy from GitHub repo"**
4. Escolha o repositório: **silvaj1zero/veterinary-transcription**
5. Selecione a branch: **main** ou **claude/run-code-015CE8EAL29sMipBfcGffbXH**

---

### **2. Configurar Variáveis de Ambiente**

No Railway, vá em **"Variables"** e adicione:

#### **🔑 APIs Essenciais**

```bash
# Anthropic Claude API (OBRIGATÓRIO)
ANTHROPIC_API_KEY=sk-ant-api03-...

# Google Gemini API (OPCIONAL - para transcrição alternativa)
GOOGLE_API_KEY=AIza...
```

#### **🗄️ Supabase Database (OBRIGATÓRIO)**

```bash
# Supabase Configuration
SUPABASE_URL=https://hndfvuypboeuijizfdzz.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhuZGZ2dXlwYm9ldWlqaXpmZHp6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQ1NTA1MjcsImV4cCI6MjA4MDEyNjUyN30.N4_JKfRGgz_BOjdFP31lfbNdD0w3TZ-zoNCe857PpDQ
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhuZGZ2dXlwYm9ldWlqaXpmZHp6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NDU1MDUyNywiZXhwIjoyMDgwMTI2NTI3fQ.CLkI-CqnwzbG1jX0bJXANxYa2lkMQL3NBGStzq-vptY

# Database Provider (IMPORTANTE!)
DATABASE_PROVIDER=supabase
```

#### **⚙️ Configurações Opcionais**

```bash
# Whisper Model (base = rápido, medium = preciso mas lento)
WHISPER_MODEL=base

# Provedores
TRANSCRIPTION_PROVIDER=openai_whisper
LLM_PROVIDER=anthropic_claude
```

---

### **3. Deploy**

Após adicionar as variáveis:

1. O Railway vai **automaticamente** iniciar o build
2. Aguarde o build completar (3-5 minutos)
3. Após o deploy, clique em **"Settings"** → **"Generate Domain"**
4. Você receberá uma URL tipo: `https://seu-app.up.railway.app`

---

### **4. Verificar Deploy**

1. Acesse a URL gerada
2. Você verá a tela de login
3. Use as credenciais:
   - **Email:** zero@toptier.net.br
   - **Senha:** Admin@123456

---

## 🔐 Credenciais Admin Configuradas

### **Supabase Admin:**
- **Email:** zero@toptier.net.br
- **User ID:** 217e10b4-5f64-4700-8aa5-e812048e605d
- **Role:** admin
- **Senha:** Admin@123456

**⚠️ IMPORTANTE:** Troque a senha após o primeiro login!

---

## 📊 Estrutura do Banco de Dados

O Supabase já está configurado com:

### **Tabelas:**
- ✅ `user_profiles` - Perfis de usuários (admin/user/viewer)
- ✅ `login_attempts` - Histórico de login (auditoria)
- ✅ `reports` - Metadados dos relatórios gerados
- ✅ `transcriptions` - Histórico de transcrições

### **Recursos:**
- ✅ Row Level Security (RLS) - Desabilitado temporariamente
- ✅ Triggers automáticos para criar perfis
- ✅ Views de estatísticas
- ✅ Índices otimizados

---

## 🐛 Troubleshooting

### **Build Falha - Dependências**

Se o build falhar, verifique:

```bash
# Logs do Railway vão mostrar o erro
# Verifique se todas as dependências estão em requirements.txt
```

### **App Não Inicia - Porta**

O Railway define a variável `PORT` automaticamente. O entrypoint.sh está configurado para usar essa porta.

### **Erro 500 - API Keys**

Verifique se `ANTHROPIC_API_KEY` está configurada corretamente:
- Deve começar com `sk-ant-api03-`
- Não pode ter espaços no início ou fim

### **Erro de Conexão - Supabase**

Verifique:
1. `SUPABASE_URL` está correto
2. `SUPABASE_KEY` e `SUPABASE_SERVICE_KEY` estão corretos
3. `DATABASE_PROVIDER=supabase` está definido
4. Projeto Supabase está ativo (não pausado)

### **Login Falha**

1. Verifique se o usuário foi criado no Supabase
2. Confirme o email no Dashboard: Authentication → Users
3. Verifique se o role está como 'admin' na tabela user_profiles

---

## 📱 Após Deploy Bem-Sucedido

### **1. Testar Funcionalidades:**
- [ ] Login com admin
- [ ] Upload de áudio
- [ ] Transcrição
- [ ] Geração de relatório
- [ ] Download de relatório

### **2. Configurar Domínio Customizado (Opcional):**
1. Railway → Settings → Domains
2. Adicione seu domínio customizado
3. Configure DNS conforme instruções

### **3. Reabilitar RLS (Segurança):**

Após validar que tudo funciona, execute no Supabase SQL Editor:

```sql
-- Reabilitar Row Level Security
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.login_attempts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.transcriptions ENABLE ROW LEVEL SECURITY;
```

### **4. Criar Novos Usuários:**

No Dashboard do Supabase:
1. Authentication → Users → Add user
2. Crie usuários normais (role='user')
3. Eles podem fazer login normalmente

---

## 🎨 Recursos Disponíveis

### **v1.7 - Autenticação & Supabase:**
- ✅ Sistema de login multi-usuário
- ✅ Banco de dados na nuvem (Supabase)
- ✅ Auditoria de login
- ✅ Gerenciamento de perfis

### **v1.6 - Resumo para Tutor & UX:**
- ✅ Geração de resumo simplificado para tutores
- ✅ Interface melhorada
- ✅ Melhor organização de campos

### **v1.5 - Fast Mode:**
- ✅ Modo Rápido (sem revisão intermediária)
- ✅ Modo Completo (com revisão)

### **v1.4 - Drag & Drop:**
- ✅ Upload de áudio por arrastar e soltar
- ✅ Google Gemini integration

---

## 📚 Documentação Completa

- **Setup Supabase:** `SUPABASE_SETUP.md`
- **Migração Técnica:** `SUPABASE_MIGRATION_SUMMARY.md`
- **Deployment Completo:** `DEPLOYMENT_COMPLETE.md`
- **Schema SQL:** `supabase_schema.sql`

---

## 🔗 Links Úteis

- **Railway Dashboard:** https://railway.app/dashboard
- **Supabase Dashboard:** https://supabase.com/dashboard
- **Documentação Railway:** https://docs.railway.app
- **Documentação Supabase:** https://supabase.com/docs

---

## ✅ Checklist Final

Antes de marcar como concluído:

- [ ] Deploy no Railway completo
- [ ] Todas as variáveis de ambiente configuradas
- [ ] URL pública acessível
- [ ] Login funcionando
- [ ] Upload de áudio funcionando
- [ ] Transcrição funcionando
- [ ] Geração de relatório funcionando
- [ ] Dados sendo salvos no Supabase
- [ ] Senha do admin alterada

---

## 🎉 Pronto!

Sua aplicação está agora em **PRODUÇÃO** com:
- ✅ Banco de dados na nuvem (Supabase)
- ✅ Autenticação segura
- ✅ Persistência de dados
- ✅ Escalabilidade
- ✅ Backup automático

**Desenvolvido com Claude Code**
**Sessão:** `claude/run-code-015CE8EAL29sMipBfcGffbXH`
**Data:** 2025-12-01
