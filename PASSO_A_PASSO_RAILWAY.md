# 🚂 PASSO A PASSO: Configurar Railway com Docker

**PROBLEMA:** Railway está usando Railpack (Python 3.13) em vez de Docker (Python 3.11)

**SOLUÇÃO:** Configurar manualmente o Railway para usar Docker

---

## ✅ Arquivos Prontos no Repositório

Já temos tudo configurado:
- ✅ `Dockerfile` (Python 3.11 + FFmpeg)
- ✅ `railway.toml` (configuração Docker)
- ✅ `mise.toml` (backup)

---

## 📋 PASSO A PASSO COMPLETO

### PASSO 1: Verificar Branch no Railway

1. **Abrir Railway Dashboard:**
   - Acesse: https://railway.app
   - Clique no seu projeto

2. **Verificar qual branch está deployado:**
   - No topo da página, procure o nome do branch
   - Deve estar usando: `claude/evaluate-veterinary-trans-011CUyXjp9zMfhT3GYJ5zEXX`
   - OU: `main` (se você já fez merge)

3. **Se estiver no branch errado:**
   - Clique em "Settings" (⚙️)
   - Em "Source" → "Branch"
   - Selecione o branch correto: `claude/evaluate-veterinary-trans-011CUyXjp9zMfhT3GYJ5zEXX`
   - Clique "Update"

---

### PASSO 2: Configurar Builder para Docker

**IMPORTANTE:** Railway tem duas formas de detectar o builder. Vamos forçar Docker manualmente.

#### Opção A: Via Railway Dashboard (RECOMENDADO)

1. **Abrir Configurações:**
   - No Railway Dashboard, clique no seu serviço/projeto
   - Clique em "Settings" (⚙️) no menu lateral

2. **Configurar Builder:**
   - Role até encontrar a seção **"Build"** ou **"Builder"**
   - Procure por: **"Build Method"** ou **"Builder Type"**
   - Se houver opção, selecione: **"Dockerfile"**

3. **Configurar Dockerfile Path:**
   - Ainda em Settings → Build
   - Procure: **"Dockerfile Path"**
   - Digite: `Dockerfile` (exatamente assim, com D maiúsculo)

4. **Salvar:**
   - Clique em "Save" ou "Update"

#### Opção B: Deletar Variáveis de Build Automático

Se Railway tiver variáveis que forçam Railpack:

1. **Settings → Variables**
2. **Procurar e DELETAR** estas variáveis (se existirem):
   - `NIXPACKS_BUILD_CMD`
   - `NIXPACKS_INSTALL_CMD`
   - `NIXPACKS_PYTHON_VERSION`
3. **Salvar**

---

### PASSO 3: Adicionar Variável de Ambiente

1. **Abrir Variables:**
   - Settings → **"Variables"** ou **"Environment Variables"**

2. **Adicionar ANTHROPIC_API_KEY:**
   - Clique em **"New Variable"** ou **"+ Add Variable"**
   - **Key (Nome):** `ANTHROPIC_API_KEY`
   - **Value (Valor):** Sua chave da Anthropic (começa com `sk-ant-`)
   - Clique **"Add"** ou **"Save"**

---

### PASSO 4: Fazer Deploy

1. **Deletar Deploy Anterior (Limpar Cache):**
   - No Railway, vá em **"Deployments"**
   - Encontre o último deployment
   - Clique nos **três pontos (⋯)**
   - Selecione **"Remove"** ou **"Delete"**

2. **Fazer Novo Deploy:**
   - Clique em **"Deploy"** (botão principal)
   - OU clique em **"Redeploy"**
   - OU simplesmente faça um novo commit no GitHub (Railway auto-deploya)

---

### PASSO 5: Verificar Build Logs

**MUITO IMPORTANTE:** Agora verifique se Railway está usando Docker!

1. **Abrir Logs:**
   - Clique em **"Deployments"**
   - Clique no deployment mais recente
   - Veja os **"Build Logs"**

2. **Verificar se mostra Docker:**

   **✅ CORRETO** (deve aparecer):
   ```
   Building with Dockerfile...
   FROM python:3.11-slim
   Step 1/10 : FROM python:3.11-slim
   Step 2/10 : WORKDIR /app
   ...
   Installing FFmpeg
   Successfully installed openai-whisper
   ```

   **❌ ERRADO** (se ainda aparecer):
   ```
   ╭─────────────────╮
   │ Railpack 0.10.0 │  ← AINDA ERRADO!
   ╰─────────────────╯
   ```

---

## 🔧 Solução se AINDA usar Railpack

Se após seguir todos os passos Railway **ainda** usar Railpack:

### Opção 1: Criar .railwayignore

```bash
# No terminal local:
cd veterinary-transcription

# Criar arquivo .railwayignore
echo "mise.toml" > .railwayignore
echo "nixpacks.toml" >> .railwayignore

# Commit
git add .railwayignore
git commit -m "fix: Ignore mise files to force Docker"
git push
```

### Opção 2: Renomear railway.toml para railway.json

Railway pode preferir JSON:

```bash
# No terminal local:
cd veterinary-transcription

# Criar railway.json
cat > railway.json << 'EOF'
{
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "startCommand": "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0",
    "healthcheckPath": "/_stcore/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
EOF

# Commit
git add railway.json
git commit -m "fix: Add railway.json config"
git push
```

### Opção 3: Configurar via CLI do Railway

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link ao projeto
railway link

# Forçar Docker
railway up --dockerfile Dockerfile
```

---

## 📊 Checklist Final

Antes de tentar novamente, verifique:

- [ ] Railway está usando o branch correto (`claude/evaluate-veterinary-trans-011CUyXjp9zMfhT3GYJ5zEXX`)
- [ ] Settings → Build → Builder = "Dockerfile"
- [ ] Settings → Build → Dockerfile Path = "Dockerfile"
- [ ] Settings → Variables → ANTHROPIC_API_KEY está configurada
- [ ] Deletou o deployment anterior (limpar cache)
- [ ] Fez novo deploy
- [ ] Build logs mostram "Building with Dockerfile"

---

## ❓ Se NADA Funcionar

Se Railway insiste em usar Railpack, temos 2 alternativas:

### Alternativa 1: Usar Render (MAIS FÁCIL)

Render respeita Dockerfile por padrão:

1. **Criar conta:** https://render.com
2. **New → Web Service**
3. **Connect GitHub** → selecionar repositório
4. **Environment:** Docker
5. **Dockerfile path:** `Dockerfile`
6. **Add environment variable:**
   - Key: `ANTHROPIC_API_KEY`
   - Value: sua chave
7. **Create Web Service**

**Custo:** $7/mês

### Alternativa 2: Usar Fly.io

```bash
# Instalar flyctl
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Launch app
flyctl launch
# Responda: Yes para Docker
# Configure região: US

# Adicionar secret
flyctl secrets set ANTHROPIC_API_KEY=sua-chave-aqui

# Deploy
flyctl deploy
```

**Custo:** Grátis (com limitações)

---

## 🎯 Resumo Executivo

**O que está acontecendo:**
- Railway detecta automaticamente Python e usa Railpack
- Railpack usa Python 3.13 (não compatível com Whisper)
- Precisamos forçar Railway a usar Dockerfile (Python 3.11)

**Solução:**
1. Configurar manualmente Builder = Dockerfile no Railway Dashboard
2. Ou usar plataforma alternativa (Render/Fly.io)

---

## 📞 Próximo Passo

**ME AVISE:**
1. Qual branch Railway está usando
2. Se consegue ver opção "Builder" ou "Build Method" em Settings
3. Se após configurar Dockerfile, os logs ainda mostram Railpack
4. Se quer tentar Render/Fly.io como alternativa

---

**Criado:** 10/11/2025
**Status:** Aguardando configuração no Railway Dashboard
