# 🎨 Branch de Desenvolvimento: UX Improvements

## 📋 Informações da Branch

- **Nome:** `feature/ux-improvements`
- **Objetivo:** Aprimoramentos de experiência do usuário (UX/UI)
- **Status:** Em desenvolvimento
- **Criada em:** 02/12/2025

## 🎯 Objetivos das Melhorias

Esta branch foi criada para implementar melhorias na interface e experiência do usuário sem afetar a versão em produção. As alterações incluem:

- [ ] Melhorias visuais na interface
- [ ] Otimização de fluxos de trabalho
- [ ] Aprimoramento de feedback visual
- [ ] Refinamento de componentes UI
- [ ] Testes de usabilidade

## 🚀 Como Trabalhar Nesta Branch

### 1️⃣ Setup Inicial (Primeira Vez)

#### Em Qualquer Máquina/IDE:

```bash
# Clonar o repositório (se ainda não tiver)
git clone https://github.com/silvaj1zero/veterinary-transcription.git
cd veterinary-transcription

# Mudar para a branch de desenvolvimento
git checkout feature/ux-improvements

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar .env (IMPORTANTE!)
# Copie o arquivo .env.example e renomeie para .env
# Adicione suas chaves de API:
```

**Conteúdo do `.env` (criar manualmente em cada máquina):**
```env
ANTHROPIC_API_KEY=sua_chave_anthropic_aqui
GOOGLE_API_KEY=AIzaSyD777yiJsYyjNQAftLkJZ2payzN3TjIlhA
SUPABASE_URL=sua_url_supabase
SUPABASE_KEY=sua_chave_supabase
SUPABASE_SERVICE_KEY=sua_service_key_supabase
DATABASE_PROVIDER=supabase
WHISPER_MODEL=base
```

### 2️⃣ Workflow Diário

```bash
# Sempre começar atualizando a branch
git checkout feature/ux-improvements
git pull origin feature/ux-improvements

# Fazer suas alterações...
# Testar localmente
streamlit run app.py

# Commitar suas mudanças
git add .
git commit -m "feat(ux): descrição da melhoria"

# Enviar para o GitHub
git push origin feature/ux-improvements
```

### 3️⃣ Sincronizar Entre Máquinas/IDEs

**Máquina A (ex: Desktop):**
```bash
git add .
git commit -m "feat(ux): nova melhoria"
git push origin feature/ux-improvements
```

**Máquina B (ex: Notebook):**
```bash
git checkout feature/ux-improvements
git pull origin feature/ux-improvements
# Continuar trabalhando...
```

## 📝 Convenções de Commit

Use commits semânticos para facilitar o rastreamento:

- `feat(ux):` - Nova funcionalidade de UX
- `fix(ux):` - Correção de bug visual
- `style(ux):` - Mudanças de estilo (cores, fontes, etc)
- `refactor(ux):` - Refatoração de código UI
- `docs(ux):` - Documentação

**Exemplos:**
```bash
git commit -m "feat(ux): adicionar animações de transição"
git commit -m "style(ux): atualizar paleta de cores"
git commit -m "fix(ux): corrigir alinhamento do header"
```

## 🧪 Testes Antes de Merge

Antes de fazer merge para produção, certifique-se de:

- [ ] Testar em diferentes resoluções de tela
- [ ] Verificar responsividade mobile
- [ ] Testar todos os fluxos principais
- [ ] Validar com usuários (se possível)
- [ ] Verificar performance
- [ ] Revisar código

## 🔄 Merge para Produção

Quando as melhorias estiverem prontas e testadas:

```bash
# 1. Atualizar a branch com as últimas mudanças
git checkout feature/ux-improvements
git pull origin feature/ux-improvements

# 2. Voltar para main e atualizar
git checkout main
git pull origin main

# 3. Fazer merge da branch de UX
git merge feature/ux-improvements

# 4. Resolver conflitos (se houver)
# Edite os arquivos com conflito, depois:
git add .
git commit -m "chore: merge feature/ux-improvements into main"

# 5. Enviar para produção (dispara deploy automático no Railway)
git push origin main

# 6. Opcional: Deletar a branch após merge
git branch -d feature/ux-improvements
git push origin --delete feature/ux-improvements
```

## 🖥️ IDEs Recomendadas

Esta branch pode ser trabalhada em qualquer IDE. Configurações recomendadas:

### VS Code
- Extensões: Python, Pylance, GitLens
- Settings: Auto-save habilitado

### PyCharm
- Configurar interpretador Python para o venv
- Habilitar Git integration

### Cursor / Windsurf
- Configurar Python interpreter
- Usar AI assistant para sugestões de UX

## 🔒 Segurança

**IMPORTANTE:** O arquivo `.env` **NÃO** está no Git por segurança. Você precisa:
1. Criar manualmente em cada máquina
2. Nunca commitar este arquivo
3. Usar `.env.example` como referência

## 📊 Status do Desenvolvimento

Acompanhe o progresso em: [GitHub Issues](https://github.com/silvaj1zero/veterinary-transcription/issues)

## 🆘 Problemas Comuns

### Erro: "Branch não encontrada"
```bash
git fetch origin
git checkout feature/ux-improvements
```

### Erro: "Conflitos de merge"
```bash
git status  # Ver arquivos em conflito
# Editar arquivos manualmente
git add .
git commit -m "fix: resolver conflitos"
```

### Erro: "Mudanças não commitadas"
```bash
# Salvar mudanças temporariamente
git stash

# Atualizar branch
git pull origin feature/ux-improvements

# Recuperar mudanças
git stash pop
```

## 📞 Suporte

Para dúvidas ou problemas, consulte:
- [README.md](README.md)
- [CHANGELOG.md](CHANGELOG.md)
- GitHub Issues

---

**Última atualização:** 02/12/2025
**Responsável:** BadiLab Team
