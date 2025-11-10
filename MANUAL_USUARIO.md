# 📖 Manual Rápido do Usuário

## Sistema de Documentação de Consultas Veterinárias v1.2

**Desenvolvido por:** BadiLab
**Última atualização:** Novembro 2025

---

## 🎯 Visão Geral

O Sistema de Documentação Veterinária automatiza a transcrição de consultas e gera relatórios estruturados profissionais usando Inteligência Artificial.

**Principais Funcionalidades:**
- 🎤 Transcrição automática de áudio (Whisper AI)
- 📝 Processamento de texto existente
- 📊 Dashboard com estatísticas
- 📋 Histórico de consultas
- 📄 Exportação em MD, TXT e PDF

---

## 🚀 Iniciando o Sistema

### Opção 1: Script PowerShell (Recomendado - Windows)

```powershell
.\iniciar_sistema.ps1
```

Escolha a opção:
- **1** - Interface Web (Streamlit) ⭐ Recomendado
- **2** - Interface CLI (Terminal)
- **3** - Executar Testes

### Opção 2: Comando Direto

```powershell
streamlit run app.py
```

**Acesse:** http://localhost:8501

---

## 📱 Interface Web - Guia Completo

### 1️⃣ Dashboard

**O que você vê:**
- 📊 Métricas: Consultas hoje, total, custos
- 📋 Últimas consultas
- 📈 Gráficos de estatísticas

**Como usar:**
1. Visualize estatísticas gerais
2. Clique em **"Ver"** para abrir um relatório
3. Use **"⬅️ Voltar ao Dashboard"** para retornar

---

### 2️⃣ Nova Consulta

#### 🎤 Método 1: Processar Áudio

**Tempo estimado:** 5-10 minutos

**Passo a passo:**

1. **Fazer Upload do Áudio**
   - Clique em "Browse files"
   - Selecione o arquivo (MP3, WAV, M4A, OGG, FLAC)
   - Aguarde o upload completar

2. **Preencher Dados do Paciente**
   - **Nome do Paciente:** Ex: Bob
   - **Espécie:** Cão, Gato ou Outro
   - **Raça:** Ex: Yorkshire Terrier
   - **Idade e Peso:** Ex: 5 anos, 3.2kg
   - **Nome do Tutor:** Ex: Dr. Silva
   - **Data da Consulta:** Selecione no calendário
   - **Motivo:** Ex: Acompanhamento dermatite
   - **Tipo:** Presencial ou Videoconferência

3. **Gerar Relatório**
   - Clique em **"🚀 Gerar Relatório"**
   - Aguarde o processamento (5-10 min)
   - Relatório será exibido automaticamente

4. **Baixar Relatório**
   - Escolha o formato:
     - 📄 **MD** - Markdown (formato original)
     - 📝 **TXT** - Texto puro (compatível)
     - 📕 **PDF** - Documento formatado

---

#### 📝 Método 2: Usar Transcrição (MAIS RÁPIDO ⚡)

**Tempo estimado:** 30 segundos

**Passo a passo:**

1. **Colar Texto da Transcrição**
   - Clique na aba **"📝 Usar Transcrição"**
   - Cole ou digite o texto da consulta
   - Mínimo: 100 caracteres

2. **Preencher Dados do Paciente**
   - Igual ao método de áudio

3. **Gerar Relatório**
   - Clique em **"🚀 Gerar Relatório"**
   - Aguarde 30 segundos
   - Relatório pronto!

**💡 Dica:** Use este método quando já tiver a transcrição pronta (videoconferência, consulta online, etc.)

---

### 3️⃣ Histórico

**Como usar:**

1. **Buscar Consultas**
   - 🔍 Digite o nome do paciente
   - 📅 Filtre por data
   - 🔄 Ordene: Recentes, Antigos, Nome (A-Z)

2. **Visualizar Relatório**
   - Clique no nome da consulta para expandir
   - Clique em **"👁️ Visualizar"** para ver o conteúdo
   - Ou baixe diretamente (MD, TXT, PDF)

3. **Exportar Relatório**
   - Botões **MD**, **TXT**, **PDF** disponíveis
   - Download instantâneo

---

### 4️⃣ Configurações

**Informações do Sistema:**
- Python version
- Streamlit version
- Modelo Whisper atual
- Status da API Claude
- Pasta de áudios

**Ações Disponíveis:**
- 🗑️ **Limpar Cache** - Libera memória
- 📁 **Abrir Pasta de Relatórios** - Acesso rápido
- 📚 **Ver Documentação** - Guias completos

---

## 💡 Dicas de Uso

### ✅ Boas Práticas

1. **Para Áudio:**
   - Use arquivos com boa qualidade de som
   - Evite ruídos de fundo excessivos
   - Tamanho máximo recomendado: 50 MB

2. **Para Texto:**
   - Inclua todos os detalhes da consulta
   - Seja específico sobre sintomas e diagnósticos
   - Mínimo 100 caracteres para bom resultado

3. **Dados do Paciente:**
   - Preencha todos os campos obrigatórios (*)
   - Use formato de data: DD/MM/AAAA
   - Seja consistente com nomes (facilita busca)

---

## 🔍 Solucionando Problemas Comuns

### ❌ Erro: "ANTHROPIC_API_KEY não encontrada"

**Solução:**
1. Verifique se o arquivo `.env` existe
2. Abra o `.env` e confirme:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```
3. Reinicie o Streamlit

---

### ❌ Erro: "FFmpeg não encontrado"

**Solução Windows:**
```powershell
winget install Gyan.FFmpeg
```

**Solução macOS:**
```bash
brew install ffmpeg
```

**Solução Linux:**
```bash
sudo apt-get install ffmpeg
```

---

### ❌ Transcrição muito lenta

**Soluções:**

1. **Use texto em vez de áudio** (30s vs 10min)
2. **Reduza tamanho do áudio:**
   - Converter para MP3 com menor qualidade
   - Usar ferramenta de compressão
3. **Altere modelo Whisper:**
   - Edite `config.py`: `WHISPER_MODEL = "base"`
   - Modelos: `tiny`, `base`, `small`, `medium`, `large`

---

### ❌ Erro ao validar dados do paciente

**Mensagens e soluções:**

- **"Campo obrigatório não preenchido"**
  → Preencha todos os campos com *

- **"Data inválida"**
  → Use formato DD/MM/AAAA (ex: 10/11/2025)

- **"Nome do paciente vazio"**
  → Digite um nome válido (não apenas espaços)

---

### ❌ Botão "Ver" não funciona no Dashboard

**Solução:**
```powershell
# Atualizar para última versão
git pull
streamlit run app.py
```

---

## 📊 Entendendo os Custos

### Estrutura de Custos (Claude API)

**Por consulta:**
- Input: ~6.000 tokens = $0,018
- Output: ~2.000 tokens = $0,030
- **Total: ~$0,05 (5 centavos)**

**Estimativas:**
- 10 consultas/dia = $0,50/dia = $15/mês
- 50 consultas/dia = $2,50/dia = $75/mês
- 100 consultas/dia = $5,00/dia = $150/mês

### Como Economizar

1. **Use transcrição de texto** (em vez de áudio)
   - Evita custos do Whisper
   - 10x mais rápido

2. **Revise antes de gerar**
   - Confirme dados do paciente
   - Evite gerar relatórios duplicados

3. **Monitore no Dashboard**
   - Acompanhe custos diários
   - Planeje seu uso

---

## 🎓 Casos de Uso

### 📌 Caso 1: Consulta Presencial com Gravação

1. Grave a consulta com gravador de voz
2. Transfira o arquivo MP3 para o computador
3. Use **"🎤 Processar Áudio"**
4. Aguarde 5-10 minutos
5. Relatório completo pronto!

**Vantagem:** Automação total

---

### 📌 Caso 2: Videoconferência com Transcrição

1. Use ferramenta de transcrição (Teams, Zoom, Google Meet)
2. Copie o texto da transcrição
3. Use **"📝 Usar Transcrição"**
4. Cole o texto
5. Relatório em 30 segundos!

**Vantagem:** Super rápido ⚡

---

### 📌 Caso 3: Consulta com Anotações Manuais

1. Digite suas anotações na caixa de texto
2. Inclua sintomas, diagnóstico, prescrições
3. Use **"📝 Usar Transcrição"**
4. Gere o relatório estruturado
5. Economize tempo de formatação!

**Vantagem:** Organização automática

---

### 📌 Caso 4: Processamento em Lote

1. Coloque vários arquivos de áudio na pasta `audios/`
2. Use a **Interface CLI**:
   ```powershell
   python transcribe_consult.py
   ```
3. Escolha opção **2** (processar todos)
4. Todos os relatórios serão gerados automaticamente

**Vantagem:** Processa múltiplas consultas de uma vez

---

## 📂 Organização de Arquivos

### Estrutura de Pastas

```
veterinary-transcription/
├── audios/              → Coloque arquivos de áudio aqui
├── transcricoes/        → Transcrições salvas automaticamente
├── relatorios/          → Relatórios finais (.md)
└── logs/                → Logs do sistema
```

### Nomenclatura de Relatórios

**Formato:** `AAAAMMDD_HHMMSS_NomePaciente_fonte.md`

**Exemplo:** `20251110_143025_Bob_consulta_teste.md`
- **20251110** - Data (10/11/2025)
- **143025** - Hora (14:30:25)
- **Bob** - Nome do paciente
- **consulta_teste** - Fonte/identificador

---

## 🔐 Segurança e Privacidade

### ✅ Dados Protegidos

- ✅ API Key armazenada localmente (`.env`)
- ✅ Áudios e relatórios ficam no seu computador
- ✅ Nenhum dado é compartilhado sem consentimento
- ✅ Logs não contêm informações sensíveis

### ⚠️ Cuidados Importantes

1. **Não compartilhe o arquivo `.env`**
   - Contém sua chave API
   - Mantenha em local seguro

2. **Faça backup dos relatórios**
   - Copie a pasta `relatorios/` regularmente
   - Use nuvem ou HD externo

3. **LGPD - Lei Geral de Proteção de Dados**
   - Obtenha consentimento dos tutores
   - Armazene dados de forma segura
   - Exclua dados quando solicitado

---

## 🆘 Suporte e Ajuda

### Documentação Completa

- 📖 **README.md** - Visão geral e instalação
- 📝 **GUIA_RAPIDO.md** - Início rápido
- 🔧 **IMPROVEMENTS.md** - Melhorias técnicas v1.2
- 📚 **USO_TRANSCRICAO_MANUAL.md** - Guia de transcrição

### Logs do Sistema

**Arquivos de log:**
- `veterinary_system.log` - CLI
- `veterinary_system_web.log` - Interface web

**Como verificar:**
```powershell
# Ver últimas linhas do log
Get-Content veterinary_system_web.log -Tail 50
```

---

## ✨ Atalhos de Teclado

**No navegador (Streamlit):**
- `R` - Recarregar aplicação
- `C` - Limpar cache
- `Ctrl + C` (terminal) - Parar servidor

---

## 📞 Informações de Contato

**Desenvolvedor:** BadiLab
**Versão:** 1.2 (Production Ready)
**Repositório:** GitHub - veterinary-transcription

---

## 🎉 Dicas Finais

1. **Comece simples:** Use transcrição de texto nas primeiras vezes
2. **Teste com dados fictícios:** Familiarize-se antes de usar dados reais
3. **Mantenha atualizado:** Execute `git pull` regularmente
4. **Monitore custos:** Acompanhe no Dashboard
5. **Faça backup:** Copie relatórios importantes

---

**🏥 Sistema de Documentação Veterinária v1.2**
Desenvolvido com ❤️ por BadiLab

**Tecnologias:**
- Whisper AI (OpenAI) - Transcrição
- Claude API (Anthropic) - Relatórios
- Streamlit - Interface Web
- Python 3.12
