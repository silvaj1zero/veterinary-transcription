# 🏥 Sistema Completo de Documentação Veterinária

Sistema automatizado de transcrição de consultas veterinárias e geração de relatórios estruturados usando Whisper AI e Claude API.

## 🆕 Versão 1.2 - Production Ready

Esta versão inclui melhorias significativas de qualidade, estabilidade e facilidade de implantação:

- ✅ **Compatibilidade Cross-Platform** - Funciona em Windows, macOS e Linux
- ✅ **Sistema de Logging Completo** - Rastreamento e auditoria de todas as operações
- ✅ **Retry Automático com Backoff** - Maior resiliência a falhas de rede/API
- ✅ **Validação Robusta de Entrada** - Previne erros antes do processamento
- ✅ **70%+ Cobertura de Testes** - 29 testes unitários e de integração
- ✅ **Docker & Docker Compose** - Implantação simplificada em 1 comando

📖 **[Ver detalhes completos das melhorias](IMPROVEMENTS.md)**

---

## 📦 Estrutura do Projeto

```
veterinary-transcription/
├── transcribe_consult.py          # Script principal
├── config.py                       # Configurações
├── requirements.txt                # Dependências
├── .env                            # API Keys (criar você mesmo)
├── .env.example                    # Exemplo de configuração
├── .gitignore                      # Arquivos ignorados pelo Git
├── README.md                       # Este arquivo
├── audios/                         # Pasta para áudios de entrada
├── transcricoes/                   # Transcrições geradas
├── relatorios/                     # Relatórios finais
└── templates/                      # Templates de prompt
    └── prompt_veterinario.txt
```

---

## 🎯 Funcionalidades

- ✅ **Transcrição automática** de áudios com Whisper AI
- ✅ **Geração de relatórios estruturados** com Claude API
- ✅ **Suporte a múltiplos formatos** de áudio (MP3, WAV, M4A, OGG, FLAC)
- ✅ **Processamento em lote** de múltiplos arquivos
- ✅ **Interface interativa** para coleta de dados do paciente
- ✅ **Relatórios em formato Markdown** profissionais
- ✅ **Histórico de transcrições** salvo automaticamente

---

## 🚀 Instalação Rápida

### Pré-requisitos

- Python 3.8 ou superior
- FFmpeg (já instalado no seu sistema)
- API Key da Anthropic (Claude)

### Passo 1: Obter API Key da Anthropic

1. Acesse: https://console.anthropic.com/
2. Faça login ou crie uma conta
3. Vá em **Settings → API Keys**
4. Clique em **Create Key**
5. Copie a chave gerada

### Passo 2: Configurar API Key

Crie um arquivo `.env` na raiz do projeto:

```bash
# Copiar o exemplo
cp .env.example .env

# Editar e adicionar sua API key
# ANTHROPIC_API_KEY=sua_chave_aqui
```

### Passo 3: Pronto para usar!

As dependências já foram instaladas. O sistema está pronto para uso!

---

## 📝 Como Usar

### Uso Básico

**1. Coloque seu áudio na pasta `audios/`**

```bash
# Formatos aceitos: mp3, wav, m4a, ogg, flac
# Exemplo: copiar um áudio
cp sua_consulta.mp3 audios/
```

**2. Execute o script**

```bash
python transcribe_consult.py
```

**3. Escolha a opção:**
- `1` = Processar arquivo específico
- `2` = Processar todos os arquivos
- `3` = Sair

**4. Preencha os dados do paciente**

O sistema vai solicitar:
- Nome do paciente
- Espécie (Cão/Gato/Outro)
- Raça
- Idade e Peso
- Nome do tutor
- Data da consulta (ou Enter para hoje)
- Motivo do retorno
- Tipo de atendimento

**5. Aguarde o processamento**

- Transcrição (pode levar alguns minutos)
- Geração do relatório (alguns segundos)

**6. Relatório pronto!**

O relatório estará em `relatorios/` no formato:
```
AAAAMMDD_HHMMSS_NomePaciente_arquivo.md
```

---

## 💡 Exemplos de Uso

### Exemplo 1: Processar um arquivo específico

```bash
$ python transcribe_consult.py

╔═══════════════════════════════════════════════════════════╗
║   SISTEMA DE DOCUMENTAÇÃO DE CONSULTAS VETERINÁRIAS      ║
║              BadiLab - 2025               ║
╚═══════════════════════════════════════════════════════════╝

Opções:
1. Processar arquivo específico
2. Processar todos os arquivos na pasta audios/
3. Sair

Escolha uma opção (1-3): 1

Arquivos disponíveis:
1. consulta_bob_retorno.mp3

Escolha o número do arquivo: 1

============================================================
📋 COLETA DE INFORMAÇÕES DO PACIENTE
============================================================
Nome do paciente: Bob
Espécie (Cão/Gato/Outro): Cão
Raça: Yorkshire Terrier
Idade e Peso (ex: 3 anos, 8kg): 5 anos, 3.2kg
Nome do tutor: Dr. Silva
Data da consulta (DD/MM/AAAA) [Enter=hoje]:
Motivo do retorno: Acompanhamento dermatite
Tipo (Presencial/Videoconferência): Presencial

🎤 Transcrevendo: consulta_bob_retorno.mp3
✅ Transcrição salva: consulta_bob_retorno_transcricao.txt

🤖 Gerando relatório com Claude API...
📊 Tokens usados: 5847 input, 1923 output

✅ Relatório salvo: 20251109_142315_Bob_consulta_bob_retorno.md

============================================================
✅ PROCESSAMENTO CONCLUÍDO COM SUCESSO!
============================================================
```

### Exemplo 2: Processar múltiplos arquivos

```bash
$ python transcribe_consult.py
Escolha uma opção (1-3): 2

📦 Encontrados 3 arquivo(s) de áudio
# Processará todos automaticamente
```

---

## ⚙️ Configurações

### Modelos Whisper Disponíveis

Edite `config.py` para escolher o modelo:

```python
WHISPER_MODEL = "medium"  # Altere aqui
```

| Modelo | Velocidade | Precisão | Tamanho | Recomendado para |
|--------|-----------|----------|---------|------------------|
| tiny   | ⚡⚡⚡⚡⚡ | ⭐⭐ | 39 MB | Testes rápidos |
| base   | ⚡⚡⚡⚡ | ⭐⭐⭐ | 74 MB | Uso geral |
| small  | ⚡⚡⭐ | ⭐⭐⭐⭐ | 244 MB | Boa qualidade |
| **medium** | ⚡⚡ | ⭐⭐⭐⭐⭐ | 769 MB | **Português (Recomendado)** |
| large  | ⚡ | ⭐⭐⭐⭐⭐ | 1550 MB | Máxima precisão |

**Recomendação:** Use `medium` para português. Oferece o melhor custo-benefício.

**Recomendação:** Use `medium` para português. Oferece o melhor custo-benefício.

### Configurações de IA (Novo na v1.9)

Agora você pode escolher os provedores de inteligência artificial diretamente na sidebar:

1.  **Transcrição:**
    *   **OpenAI Whisper (Local):** Gratuito, roda no seu PC, funciona offline.
    *   **Google Gemini (Nuvem):** Rápido, requer chave de API (`GOOGLE_API_KEY`), processamento na nuvem.

2.  **Relatório (LLM):**
    *   **Anthropic Claude 3.5:** Recomendado para raciocínio clínico complexo.
    *   **Google Gemini 1.5 Pro:** Janela de contexto maior, alternativa robusta.

---

## 🔧 Troubleshooting

### Erro: "ANTHROPIC_API_KEY não encontrada"

**Solução:**
```bash
# Verifique se o arquivo .env existe
ls -la .env

# Se não existir, crie
echo "ANTHROPIC_API_KEY=sua_chave_aqui" > .env

# Verifique o conteúdo
cat .env
```

### Erro: "ffmpeg not found"

O FFmpeg já está instalado no seu sistema em:
```
C:\Users\Zero\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0-full_build\bin
```

O script já está configurado para usar este caminho.

### Transcrição muito lenta

**Opção 1:** Usar modelo menor (menos preciso, mais rápido)
```python
# Em config.py:
WHISPER_MODEL = "small"  # ou "base"
```

**Opção 2:** Processar em lote durante a noite
```bash
# Processar todos de uma vez
python transcribe_consult.py
# Escolher opção 2
```

### Erro: "Out of memory"

Use um modelo menor:
```python
# Em config.py:
WHISPER_MODEL = "base"  # ou "tiny"
```

---

## 📊 Custos da API Claude

### Estimativa de custos (Claude Sonnet 4):

- **Input:** $3 por 1M tokens
- **Output:** $15 por 1M tokens

**Exemplo típico por consulta:**
- Input: ~6.000 tokens = $0,018
- Output: ~2.000 tokens = $0,030
- **Total por consulta: ~$0,05 (5 centavos)**

### Monitoramento de custos

O sistema exibe os tokens usados:
```
📊 Tokens usados: 5847 input, 1923 output
```

---

## 🎨 Personalização

### Modificar o template de relatório

Edite `templates/prompt_veterinario.txt` para:
- Adicionar/remover seções
- Mudar formatação
- Ajustar instruções para o Claude

### Adicionar novos formatos de áudio

Em `config.py`:
```python
AUDIO_EXTENSIONS = ['.mp3', '.wav', '.m4a', '.ogg', '.flac', '.aac']
```

---

## 📦 Integração com yt-dlp

Você já tem o `yt-dlp` instalado! Pode baixar áudios de consultas online:

```bash
# Baixar áudio de videoconferência gravada
yt-dlp -x --audio-format mp3 -o "audios/%(title)s.%(ext)s" "URL_DO_VIDEO"
```

---

## 🔐 Segurança

- ✅ `.env` está no `.gitignore` (não será commitado)
- ✅ Dados sensíveis ficam apenas localmente
- ✅ API Key nunca é exposta no código
- ⚠️ **Importante:** Não compartilhe seu arquivo `.env`

---

## 📄 Exemplo de Relatório Gerado

```markdown
# RELATÓRIO DE CONSULTA VETERINÁRIA - RETORNO

## 📋 DADOS DO ATENDIMENTO
- **Data:** 09/11/2025
- **Modalidade:** Presencial
- **Veterinário:** Dr. Antônio Laquierá

## 🐾 IDENTIFICAÇÃO DO PACIENTE
- **Paciente:** Bob | **Espécie:** Cão | **Raça:** Yorkshire Terrier
- **Idade/Peso:** 5 anos, 3.2kg
- **Tutor:** Dr. Silva

## 📝 SUMÁRIO EXECUTIVO
[Resumo da consulta...]

...
```

---

## 🐳 Instalação com Docker (Recomendado)

A forma mais fácil de executar o sistema é usando Docker:

### Pré-requisitos
- Docker e Docker Compose instalados

### Passo 1: Configurar API Key

Crie o arquivo `.env`:
```bash
echo "ANTHROPIC_API_KEY=sua-chave-aqui" > .env
```

### Passo 2: Iniciar o serviço

```bash
docker-compose up -d vet-docs-web
```

### Passo 3: Acessar

Abra o navegador em: **http://localhost:8501**

### Comandos Úteis

```bash
# Ver logs
docker-compose logs -f vet-docs-web

# Parar serviço
docker-compose down

# Usar CLI
docker-compose run --rm vet-docs-cli

# Atualizar imagem
docker-compose build
docker-compose up -d
```

### Benefícios do Docker
- ✅ FFmpeg já incluído
- ✅ Todas as dependências instaladas
- ✅ Ambiente isolado
- ✅ Fácil de replicar
- ✅ Pronto para produção

---

## 🧪 Executar Testes

O projeto inclui uma suite completa de testes (70%+ cobertura):

### Instalar dependências de teste

```bash
pip install pytest pytest-cov pytest-mock
```

### Executar todos os testes

```bash
pytest
```

### Com relatório de cobertura

```bash
pytest --cov --cov-report=html
```

### Apenas testes unitários

```bash
pytest -m unit
```

### Apenas testes de integração

```bash
pytest -m integration
```

### Tipos de Testes Incluídos

- **Testes Unitários (27 testes)**
  - Detecção de FFmpeg
  - Validação de entrada
  - Retry com backoff
  - Geração de relatórios
  - Salvamento de arquivos

- **Testes de Integração (2 testes)**
  - Workflow completo texto → relatório
  - Workflow completo áudio → relatório

### Ver Relatório de Cobertura

Após executar `pytest --cov --cov-report=html`, abra:
```
htmlcov/index.html
```

---

## 🆘 Suporte

Problemas? Sugestões?

1. Verifique a seção **Troubleshooting** acima
2. Revise os logs de erro
3. Confira se a API Key está correta

---

## 📜 Licença

Desenvolvido por **BadiLab - 2025**

---

## ✨ Próximas Funcionalidades

- [ ] Interface web (Flask/FastAPI)
- [ ] Suporte a vídeos
- [ ] Exportação para PDF
- [ ] Dashboard de estatísticas
- [ ] Integração com sistemas veterinários

---

**Versão:** 1.2 (Production Ready)
**Última atualização:** Novembro 2025

**Melhorias da v1.2:**
- Sistema de logging completo
- Retry automático com backoff exponencial
- Validação robusta de entrada
- 70%+ cobertura de testes
- Containerização Docker
- Compatibilidade cross-platform
