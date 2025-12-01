# 📋 Histórico de Alterações

## [1.8] - 01/12/2025

### 🎉 Novidades

- **Sistema de Autenticação Completo**
  - Login/Logout de usuários
  - Gerenciamento de usuários (somente admin)
  - Dois níveis de acesso: Admin e User
  - Senhas criptografadas (PBKDF2 + SHA256 + salt)
  - Histórico de tentativas de login para auditoria
  - Menu de usuário na sidebar com informações de perfil

- **Integração Supabase (Opcional)**
  - Suporte a PostgreSQL cloud via Supabase
  - Arquitetura dual database: SQLite (local) + Supabase (cloud)
  - Row Level Security (RLS) nativo
  - Schema SQL completo com 4 tabelas
  - Script de migração de dados do SQLite para Supabase
  - Views úteis para estatísticas (user_stats, report_stats)
  - Triggers automáticos para auditoria

- **Documentação Expandida**
  - `AUTH_SYSTEM.md` - Guia completo do sistema de autenticação
  - `ANALISE_SUPABASE.md` - Análise detalhada da integração Supabase
  - `RAILWAY_DEPLOY_GUIDE.md` - Guia completo de deploy no Railway
  - `RAILWAY_UPDATE_GUIDE.md` - Guia de atualização Railway
  - `SUPABASE_SETUP.md` - Setup passo a passo do Supabase
  - `SUPABASE_MIGRATION_SUMMARY.md` - Resumo técnico da migração

### 🔧 Melhorias

- Sistema agora requer login obrigatório antes de usar
- Dados de usuários persistidos em banco de dados
- Interface atualizada com informações do usuário logado
- Seleção dinâmica de provedor de banco (SQLite/Supabase)
- Página exclusiva para gerenciamento de usuários (admin)
- Opção de alteração de senha pelo próprio usuário

### 🔐 Segurança

- Implementação de autenticação obrigatória em todas as rotas
- Proteção de funcionalidades administrativas
- Auditoria completa de logins (sucesso e falhas)
- Senhas nunca armazenadas em texto plano
- Salt único por usuário no SQLite
- Row Level Security no Supabase

### ⚙️ Técnico

- Módulos `auth.py` e `auth_supabase.py` para abstração de banco
- Módulo `auth_ui.py` para componentes de interface
- Seleção automática de AuthManager baseada em `DATABASE_PROVIDER`
- Banco SQLite (`data/users.db`) com suporte a multi-usuário
- Integração completa com Supabase Auth API


---

## [1.1] - 09/11/2025

### ✨ Novidades

- **Opção 3: Usar Transcrição Existente**
  - Agora é possível gerar relatórios sem processar áudio
  - Suporte para colar texto diretamente
  - Suporte para ler de arquivos .txt
  - Economia de tempo e recursos (Whisper não é carregado)

### 🔧 Melhorias

- Whisper agora carrega sob demanda (lazy loading)
  - Mais rápido para usar transcrições existentes
  - Economiza memória quando não precisa transcrever
- Menu atualizado com 4 opções
- Melhor organização dos métodos da classe

### 📚 Documentação

- Novo arquivo: `USO_TRANSCRICAO_MANUAL.md`
- Arquivo de exemplo: `exemplo_transcricao.txt`
- README atualizado com nova funcionalidade

### 🐛 Correções

- Melhor tratamento de erros na entrada de texto
- Validação de arquivos .txt

---

## [1.0] - 09/11/2025

### 🎉 Lançamento Inicial

- Sistema completo de transcrição e documentação
- Integração com Whisper AI
- Integração com Claude API (Sonnet 4)
- Processamento de múltiplos formatos de áudio
- Geração automática de relatórios estruturados
- Processamento em lote
- Interface interativa
- Documentação completa

---

## 🚀 Próximas Versões

### [1.2] - Planejado

- [ ] Interface web (Flask)
- [ ] Exportação para PDF
- [ ] Dashboard de estatísticas
- [ ] Monitoramento de custos automático
- [ ] Templates customizáveis de relatório
- [ ] Integração com banco de dados
- [ ] API REST para integração com outros sistemas

### [2.0] - Futuro

- [ ] Suporte a vídeos
- [ ] Reconhecimento de múltiplos veterinários
- [ ] Análise de sentimento
- [ ] Sugestões automáticas de CID
- [ ] Integração com prontuários eletrônicos
- [ ] App mobile

---

**Convenções de Versionamento:**
- **Major (X.0.0):** Mudanças incompatíveis
- **Minor (0.X.0):** Novas funcionalidades compatíveis
- **Patch (0.0.X):** Correções de bugs
