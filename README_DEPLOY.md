# 🚀 README - Opções de Deploy

**Importante:** Leia este arquivo antes de fazer deploy!

---

## ⚠️ ATENÇÃO: Dois Arquivos de Requirements

Este projeto tem **2 arquivos de requirements** diferentes:

### 1. `requirements.txt` (LOCAL/DOCKER)
```
✅ Usa Whisper (transcrição de áudio)
✅ Para desenvolvimento local
✅ Para deploy com Docker (Railway, Render, Fly.io)
❌ NÃO funciona no Streamlit Cloud
```

### 2. `requirements-streamlit-cloud.txt` (STREAMLIT CLOUD)
```
❌ SEM Whisper (sem transcrição de áudio)
✅ Para deploy no Streamlit Cloud
✅ Apenas transcrição manual (colar texto)
✅ Funciona no plano grátis
```

---

## 🎯 Qual Usar?

### Use `requirements.txt` se:
- ✅ Vai rodar localmente no seu PC
- ✅ Vai fazer deploy com Docker (Railway, Render, etc)
- ✅ Quer transcrição de áudio funcionando
- ✅ Tem orçamento para servidor ($5-7/mês)

### Use `requirements-streamlit-cloud.txt` se:
- ✅ Vai fazer deploy no Streamlit Cloud (grátis)
- ✅ Não precisa de transcrição de áudio
- ✅ Apenas texto manual é suficiente
- ✅ Quer economizar dinheiro

---

## 🚀 Deploy Rápido

### Opção A: Streamlit Cloud (Grátis, SEM áudio)

```bash
# 1. Renomear requirements
mv requirements.txt requirements-local.txt
mv requirements-streamlit-cloud.txt requirements.txt

# 2. Commit e push
git add .
git commit -m "Deploy: Streamlit Cloud (sem áudio)"
git push

# 3. No Streamlit Cloud:
# - Restart app
# - Adicionar ANTHROPIC_API_KEY nos secrets
# - Pronto!
```

---

### Opção B: Railway (Pago, COM áudio) - **RECOMENDADO**

```bash
# Não precisa mudar nada! Use requirements.txt original

# 1. Criar conta: https://railway.app
# 2. New Project → Deploy from GitHub
# 3. Selecionar: veterinary-transcription
# 4. Settings → Variables:
#    ANTHROPIC_API_KEY = sua-chave-aqui
# 5. Deploy automático!
# 6. Railway detecta Dockerfile e usa ele ✅
```

**Custo:** $5/mês (hobby plan)

---

### Opção C: Render (Pago, COM áudio)

```bash
# Não precisa mudar nada! Use requirements.txt original

# 1. Criar conta: https://render.com
# 2. New Web Service → Connect GitHub
# 3. Environment: Docker
# 4. Dockerfile path: ./Dockerfile
# 5. Add environment variable:
#    ANTHROPIC_API_KEY = sua-chave-aqui
# 6. Deploy!
```

**Custo:** $7/mês (starter plan)

---

## 📊 Comparação Rápida

| Plataforma | Áudio? | Custo | Facilidade | Recomendado |
|------------|--------|-------|------------|-------------|
| **Streamlit Cloud** | ❌ | Grátis | ⭐⭐⭐⭐⭐ | Teste/Demo |
| **Railway** | ✅ | $5/mês | ⭐⭐⭐⭐⭐ | **MELHOR** |
| **Render** | ✅ | $7/mês | ⭐⭐⭐⭐ | Bom |
| **Fly.io** | ✅ | Grátis* | ⭐⭐⭐ | Técnicos |

*Free tier com limitações

---

## 🔧 Troubleshooting

### Erro no Streamlit Cloud: "installer returned non-zero exit code"

**Causa:** Você está usando `requirements.txt` com Whisper

**Solução:**
```bash
# Use requirements-streamlit-cloud.txt:
mv requirements.txt requirements-local.txt
mv requirements-streamlit-cloud.txt requirements.txt
git commit -am "fix: Use requirements para Streamlit Cloud"
git push
```

---

### Erro no Railway/Render: "Cannot find Dockerfile"

**Solução:**
```bash
# Verificar se Dockerfile existe:
ls -la Dockerfile

# Se não existir, está no branch errado!
git checkout main
```

---

## 📝 Links Úteis

**Guias detalhados:**
- [GUIA_DEPLOY_STREAMLIT_CLOUD.md](GUIA_DEPLOY_STREAMLIT_CLOUD.md) - Guia completo
- [GUIA_DOCKER.md](GUIA_DOCKER.md) - Entender Docker

**Plataformas:**
- [Streamlit Cloud](https://share.streamlit.io) - Deploy grátis
- [Railway](https://railway.app) - Deploy com Docker
- [Render](https://render.com) - Deploy com Docker
- [Fly.io](https://fly.io) - Deploy com Docker

---

## ✅ Checklist de Deploy

### Streamlit Cloud (sem áudio):
- [ ] Renomear requirements para usar versão cloud
- [ ] Push para GitHub
- [ ] Configurar ANTHROPIC_API_KEY no Streamlit Cloud
- [ ] Restart app
- [ ] Testar funcionalidade de texto

### Railway/Render (com áudio):
- [ ] Criar conta na plataforma
- [ ] Conectar repositório GitHub
- [ ] Configurar ANTHROPIC_API_KEY
- [ ] Aguardar build do Docker
- [ ] Testar upload de áudio

---

## 🎯 Recomendação

**Para sua situação:**

**Se tem orçamento ($5-7/mês):**
→ **Railway** é a melhor opção
   - Deploy em 5 minutos
   - Tudo funciona
   - Muito fácil de usar

**Se quer grátis:**
→ **Streamlit Cloud** para começar
   - Sem transcrição de áudio
   - Apenas texto manual
   - Upgrade depois para Railway

---

**Criado:** 10/11/2025
**Versão:** 1.0
