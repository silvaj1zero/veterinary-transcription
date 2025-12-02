# 🚀 Quick Start - Branch UX Improvements

## Setup Rápido (Nova Máquina/IDE)

```bash
# 1. Clonar repositório
git clone https://github.com/silvaj1zero/veterinary-transcription.git
cd veterinary-transcription

# 2. Mudar para branch de UX
git checkout feature/ux-improvements

# 3. Configurar ambiente
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 4. Criar .env (copiar de .env.example)
# Adicionar suas chaves de API

# 5. Testar
streamlit run app.py
```

## Workflow Diário

```bash
# Atualizar
git pull origin feature/ux-improvements

# Trabalhar...
# Testar: streamlit run app.py

# Salvar
git add .
git commit -m "feat(ux): descrição"
git push origin feature/ux-improvements
```

## Merge para Produção

```bash
git checkout main
git pull origin main
git merge feature/ux-improvements
git push origin main  # ← Deploy automático!
```

## 📖 Documentação Completa
Ver: [BRANCH_UX_GUIDE.md](BRANCH_UX_GUIDE.md)
