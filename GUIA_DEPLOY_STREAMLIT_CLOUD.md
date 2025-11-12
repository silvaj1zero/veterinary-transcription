# 🚀 Guia de Deploy no Streamlit Cloud

**Data:** 10/11/2025
**Status:** ⚠️ **LIMITAÇÕES IMPORTANTES**

---

## ⚠️ PROBLEMA IDENTIFICADO

O erro que você recebeu:
```
❗️ installer returned a non-zero exit code
❗️ Error during processing dependencies!
```

**Causa:** O Streamlit Cloud **NÃO suporta Whisper** porque:
- ❌ Não tem FFmpeg instalado
- ❌ Não permite instalar pacotes do sistema
- ❌ Recursos limitados (RAM/CPU)
- ❌ Ambiente isolado e restrito

---

## 🔍 Por que Whisper não funciona?

```python
# requirements.txt original:
openai-whisper==20231117  # ❌ ERRO!

# Whisper precisa de:
- FFmpeg (não disponível)
- torch (muito pesado)
- Modelos grandes (769 MB para medium)
- RAM significativa (4GB+)
- GPU para performance (não disponível)
```

---

## 💡 SOLUÇÕES

### Opção 1: Deploy no Streamlit Cloud SEM Whisper (Recomendado para teste)

**Funcionalidades disponíveis:**
- ✅ Transcrição manual (colar texto)
- ✅ Geração de relatórios com Claude
- ✅ Dashboard e histórico
- ✅ Downloads MD/TXT/PDF
- ❌ Upload e transcrição de áudio

**Vantagens:**
- ✅ Grátis
- ✅ Deploy rápido (5 minutos)
- ✅ HTTPS automático
- ✅ Fácil de usar

**Desvantagens:**
- ❌ Sem transcrição de áudio
- ❌ Recursos limitados
- ❌ Pode ficar lento com muitos usuários

#### Passo a passo:

**1. Renomear/substituir arquivos:**

```bash
# No seu repositório GitHub:

# Renomear requirements.txt original
git mv requirements.txt requirements-local.txt

# Usar requirements otimizado para cloud
git mv requirements-streamlit-cloud.txt requirements.txt

# Commit
git add .
git commit -m "fix: Otimizar requirements para Streamlit Cloud"
git push
```

**2. Configurar Streamlit Cloud:**

```
1. Acesse: https://share.streamlit.io
2. Login com GitHub
3. New app → Escolha seu repositório
4. Main file: app.py
5. Advanced settings:
   - ANTHROPIC_API_KEY = sua-chave-aqui
6. Deploy!
```

**3. Aviso para usuários:**

Adicione aviso no README ou na interface informando que **transcrição de áudio não está disponível na versão cloud**.

---

### Opção 2: Deploy com Docker (Railway/Render) - Funcionalidade Completa ✅

**Funcionalidades disponíveis:**
- ✅ Upload e transcrição de áudio (Whisper)
- ✅ Transcrição manual
- ✅ Geração de relatórios com Claude
- ✅ Dashboard e histórico
- ✅ Downloads MD/TXT/PDF
- ✅ **TUDO FUNCIONA!**

#### A. Deploy no Railway (Recomendado)

**Vantagens:**
- ✅ Suporta Docker
- ✅ FFmpeg disponível
- ✅ 500 horas grátis/mês
- ✅ Deploy automático do GitHub
- ✅ Muito fácil de configurar

**Passo a passo:**

1. **Criar conta no Railway:**
   ```
   https://railway.app
   Login com GitHub
   ```

2. **Novo projeto:**
   ```
   New Project → Deploy from GitHub repo
   Escolher: veterinary-transcription
   ```

3. **Configurar variáveis:**
   ```
   Settings → Variables:
   ANTHROPIC_API_KEY = sua-chave-aqui
   ```

4. **Railway detecta Dockerfile automaticamente!**
   ```
   ✅ Vai usar docker-compose.yml
   ✅ Já configurado com FFmpeg
   ✅ Deploy automático
   ```

5. **Acessar:**
   ```
   Railway gera URL pública:
   https://seu-app.railway.app
   ```

**Custo:**
- Grátis: 500 horas/mês ($0)
- Hobby: $5/mês (ilimitado)

---

#### B. Deploy no Render

**Vantagens:**
- ✅ Suporta Docker
- ✅ FFmpeg disponível
- ✅ $0/mês no plano free
- ✅ Muito estável

**Passo a passo:**

1. **Criar conta no Render:**
   ```
   https://render.com
   Login com GitHub
   ```

2. **Novo Web Service:**
   ```
   New → Web Service
   Connect repository: veterinary-transcription
   ```

3. **Configurar:**
   ```
   Name: vet-transcription
   Environment: Docker
   Dockerfile path: ./Dockerfile

   Environment Variables:
   ANTHROPIC_API_KEY = sua-chave-aqui
   ```

4. **Deploy:**
   ```
   Create Web Service
   Aguardar build (~10 minutos)
   ```

5. **Acessar:**
   ```
   Render gera URL:
   https://vet-transcription.onrender.com
   ```

**Custo:**
- Free: $0/mês (mas serviço "hiberna" após inatividade)
- Starter: $7/mês (sempre ativo)

---

#### C. Deploy no Fly.io

**Vantagens:**
- ✅ Suporta Docker
- ✅ Global deployment
- ✅ $0/mês no plano free
- ✅ Muito rápido

**Passo a passo:**

1. **Instalar flyctl:**
   ```bash
   # Windows (PowerShell):
   iwr https://fly.io/install.ps1 -useb | iex

   # macOS/Linux:
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login:**
   ```bash
   fly auth login
   ```

3. **Criar app:**
   ```bash
   cd veterinary-transcription
   fly launch

   # Responda:
   App name: vet-transcription
   Region: São Paulo (gru)
   Database: No
   Deploy: Yes
   ```

4. **Configurar secrets:**
   ```bash
   fly secrets set ANTHROPIC_API_KEY=sua-chave-aqui
   ```

5. **Acessar:**
   ```
   https://vet-transcription.fly.dev
   ```

**Custo:**
- Free: $0/mês (3GB RAM, suficiente)
- Pro: $1.94/mês (mais RAM)

---

### Opção 3: Deploy em VPS/Cloud (Controle Total)

**Para produção séria:**

#### AWS/Google Cloud/Azure

```bash
# Criar VM
# Instalar Docker
sudo apt update
sudo apt install docker.io docker-compose

# Clonar projeto
git clone seu-repo
cd veterinary-transcription

# Configurar
echo "ANTHROPIC_API_KEY=sua-chave" > .env

# Iniciar
docker-compose up -d

# Configurar domínio e HTTPS (Nginx + Let's Encrypt)
```

---

## 📊 Comparação de Opções

| Serviço | Whisper? | Custo | Facilidade | Performance | Recomendado? |
|---------|----------|-------|------------|-------------|--------------|
| **Streamlit Cloud** | ❌ Não | Grátis | ⭐⭐⭐⭐⭐ | ⭐⭐ | ✅ Para TESTE |
| **Railway** | ✅ Sim | $5/mês | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅✅ **RECOMENDADO** |
| **Render** | ✅ Sim | $7/mês | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ Boa opção |
| **Fly.io** | ✅ Sim | Grátis | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ Técnicos |
| **VPS** | ✅ Sim | $5-50/mês | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⏳ Futuro |

---

## ✅ SOLUÇÃO RÁPIDA (AGORA)

### Para Streamlit Cloud (sem áudio):

```bash
# 1. No seu repositório local:
cd veterinary-transcription

# 2. Backup do requirements original
cp requirements.txt requirements-local.txt

# 3. Usar requirements otimizado
cp requirements-streamlit-cloud.txt requirements.txt

# 4. Adicionar aviso no README
echo "⚠️ Versão Streamlit Cloud: Apenas transcrição manual" >> README.md

# 5. Commit e push
git add .
git commit -m "fix: Otimizar para Streamlit Cloud (sem Whisper)"
git push

# 6. No Streamlit Cloud:
# - Restart app
# - Deve funcionar agora!
```

### Para Railway (com áudio):

```bash
# 1. Criar conta: https://railway.app
# 2. New Project → GitHub repo
# 3. Adicionar variável: ANTHROPIC_API_KEY
# 4. Deploy automático!
# 5. Pronto! ✅
```

---

## 🐛 Troubleshooting

### Erro: "Module not found"

**Solução:**
```bash
# Verificar requirements.txt está correto:
cat requirements.txt

# Deve ter versões específicas:
anthropic==0.39.0
streamlit==1.51.0
# NÃO deve ter: openai-whisper
```

---

### Erro: "Memory limit exceeded"

**Causa:** Whisper é muito pesado para Streamlit Cloud

**Solução:** Use Railway/Render com Docker

---

### App fica lento

**Streamlit Cloud:**
- É grátis, tem recursos limitados
- Normal ficar lento com muitos usuários

**Solução:**
- Migre para Railway/Render
- Otimize código (cache, lazy loading)

---

## 📝 Arquivos Criados Para Você

```
✅ requirements-streamlit-cloud.txt
   → Requirements SEM Whisper (para Streamlit Cloud)

✅ requirements-local.txt
   → Seu requirements original (para desenvolvimento local)

✅ packages.txt
   → Pacotes do sistema (vazio, Streamlit Cloud não precisa)

✅ app-streamlit-cloud.py
   → Versão do app SEM funcionalidade de áudio

✅ GUIA_DEPLOY_STREAMLIT_CLOUD.md
   → Este guia
```

---

## 🎯 Recomendação Final

**Para TESTE/DEMO rápido:**
→ Use **Streamlit Cloud** (sem áudio, só texto)

**Para PRODUÇÃO:**
→ Use **Railway** ($5/mês, tudo funciona)

**Para HOBBY/Economia:**
→ Use **Fly.io** (grátis, técnico)

---

## 🚀 Próximos Passos

1. **Decidir:** Com ou sem transcrição de áudio?

2. **Se SEM áudio (Streamlit Cloud):**
   ```bash
   cp requirements-streamlit-cloud.txt requirements.txt
   git add . && git commit -m "fix: Deploy Streamlit Cloud"
   git push
   # Restart app no Streamlit Cloud
   ```

3. **Se COM áudio (Railway):**
   ```bash
   # Criar conta: https://railway.app
   # Deploy from GitHub
   # Adicionar ANTHROPIC_API_KEY
   # Pronto!
   ```

---

## ❓ FAQ

**P: Posso usar Whisper no Streamlit Cloud?**
R: ❌ Não, é tecnicamente impossível. Use Railway/Render.

**P: Quanto custa Railway?**
R: Grátis por 500 horas/mês, ou $5/mês ilimitado.

**P: É difícil migrar depois?**
R: ❌ Não! Docker funciona em qualquer lugar.

**P: Preciso mudar código?**
R: ❌ Não! Docker usa o código original.

---

**Criado por:** Claude Code
**Data:** 10/11/2025
**Versão:** 1.0

🎉 **Boa sorte com o deploy!**
