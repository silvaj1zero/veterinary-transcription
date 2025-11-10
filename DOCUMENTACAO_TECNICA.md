# 🔧 Documentação Técnica

## Sistema de Documentação de Consultas Veterinárias v1.2

**Versão:** 1.2 (Production Ready)
**Data:** Novembro 2025
**Desenvolvedor:** BadiLab

---

## 📑 Índice

1. [Arquitetura do Sistema](#arquitetura-do-sistema)
2. [Estrutura de Arquivos](#estrutura-de-arquivos)
3. [Módulos e Componentes](#módulos-e-componentes)
4. [APIs e Integrações](#apis-e-integrações)
5. [Fluxos de Dados](#fluxos-de-dados)
6. [Configuração](#configuração)
7. [Testes](#testes)
8. [Deployment](#deployment)
9. [Segurança](#segurança)
10. [Manutenção](#manutenção)

---

## 1. Arquitetura do Sistema

### 1.1 Visão Geral

```
┌─────────────────────────────────────────────────────────┐
│                    INTERFACE USUÁRIO                     │
│  ┌──────────────────┐         ┌──────────────────┐     │
│  │  Interface Web   │         │  Interface CLI   │     │
│  │   (Streamlit)    │         │    (Console)     │     │
│  └────────┬─────────┘         └────────┬─────────┘     │
└───────────┼──────────────────────────────┼──────────────┘
            │                              │
            └──────────────┬───────────────┘
                           │
            ┌──────────────▼──────────────┐
            │     CAMADA DE APLICAÇÃO     │
            │  (transcribe_consult.py)    │
            │                              │
            │  - VeterinaryTranscription   │
            │  - Validação de dados        │
            │  - Orquestração workflow     │
            └──────────────┬───────────────┘
                           │
            ┌──────────────┼──────────────┐
            │              │               │
    ┌───────▼────────┐ ┌──▼────┐ ┌──────▼────────┐
    │  Whisper AI    │ │ Utils │ │  Claude API   │
    │  (Transcrição) │ │       │ │  (Relatórios) │
    └────────────────┘ └───────┘ └───────────────┘
            │                              │
            │                              │
    ┌───────▼──────────────────────────────▼───────┐
    │           CAMADA DE PERSISTÊNCIA             │
    │  - audios/           (entrada)               │
    │  - transcricoes/     (intermediário)         │
    │  - relatorios/       (saída)                 │
    │  - logs/             (auditoria)             │
    └──────────────────────────────────────────────┘
```

### 1.2 Princípios de Design

- **Separação de Responsabilidades:** Módulos distintos para transcrição, validação e geração
- **Modularidade:** Componentes independentes e testáveis
- **Resiliência:** Retry automático com backoff exponencial
- **Observabilidade:** Logging estruturado em todas as operações
- **Portabilidade:** Compatível com Windows, macOS e Linux

---

## 2. Estrutura de Arquivos

```
veterinary-transcription/
│
├── Core Application
│   ├── transcribe_consult.py    (451 linhas) - Lógica principal
│   ├── app.py                   (840 linhas) - Interface Streamlit
│   ├── config.py                (30 linhas)  - Configurações
│   └── utils.py                 (233 linhas) - Utilitários
│
├── Configuration
│   ├── .env                     - Variáveis de ambiente (API keys)
│   ├── .env.example             - Template de configuração
│   └── pytest.ini               - Configuração de testes
│
├── Docker
│   ├── Dockerfile               - Containerização
│   ├── docker-compose.yml       - Orquestração
│   └── .dockerignore            - Exclusões de build
│
├── Tests
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py          (143 linhas) - Fixtures
│   │   ├── test_utils.py        (263 linhas) - Testes utils
│   │   └── test_transcription.py (350 linhas) - Testes core
│
├── Scripts
│   ├── iniciar_sistema.ps1      - Launcher Windows
│   ├── executar.bat             - CLI Windows
│   └── iniciar_interface.bat    - Web Windows
│
├── Data Directories
│   ├── audios/                  - Arquivos de entrada
│   ├── transcricoes/            - Transcrições geradas
│   ├── relatorios/              - Relatórios finais
│   └── logs/                    - Arquivos de log
│
├── Templates
│   └── templates/
│       └── prompt_veterinario.txt - Template do prompt
│
└── Documentation
    ├── README.md                - Guia principal
    ├── MANUAL_USUARIO.md        - Manual do usuário
    ├── DOCUMENTACAO_TECNICA.md  - Esta documentação
    ├── IMPROVEMENTS.md          - Melhorias v1.2
    ├── GUIA_RAPIDO.md          - Início rápido
    ├── CHANGELOG.md            - Histórico de versões
    └── USO_TRANSCRICAO_MANUAL.md - Guia de transcrição
```

---

## 3. Módulos e Componentes

### 3.1 Core: `transcribe_consult.py`

**Classe Principal:** `VeterinaryTranscription`

#### Métodos Públicos

```python
__init__(load_whisper: bool = True)
    """Inicializa o sistema com logging e clientes API"""

transcribe_audio(audio_path: Path) -> dict
    """Transcreve áudio usando Whisper AI"""

collect_patient_info() -> dict
    """Coleta informações do paciente interativamente"""

generate_report(transcription_text: str, patient_info: dict) -> str
    """Gera relatório estruturado via Claude API com retry"""

save_report(report_text: str, patient_name: str, audio_filename: str) -> Path
    """Salva relatório em arquivo markdown"""

process_consultation(audio_path: Path, patient_info: dict = None) -> Path
    """Workflow completo: áudio → transcrição → relatório"""

process_from_text(transcription_text: str, patient_info: dict = None,
                 source_name: str = "transcrição_manual") -> Path
    """Workflow: texto → relatório (sem Whisper)"""

get_transcription_from_user() -> str
    """Interface para colar/ler transcrição existente"""

batch_process()
    """Processa todos os áudios na pasta audios/"""
```

#### Métodos Privados

```python
_ensure_whisper_loaded()
    """Carregamento lazy do modelo Whisper"""

_load_prompt_template() -> str
    """Carrega template do prompt"""
```

#### Decorators

```python
@retry_with_backoff(max_retries=4, initial_delay=2.0, backoff_factor=2.0)
```
- Aplicado em `generate_report()`
- Retry automático para erros de API
- Backoff exponencial: 2s, 4s, 8s, 16s

---

### 3.2 Interface Web: `app.py`

**Framework:** Streamlit

#### Componentes Principais

**1. Dashboard** (linhas 315-425)
- Métricas de estatísticas
- Lista de consultas recentes
- Visualização de relatórios
- Gráficos (pizza e barras)

**2. Nova Consulta** (linhas 426-644)
- Tab 1: Upload de áudio
- Tab 2: Transcrição de texto
- Formulário de dados do paciente
- Geração e preview de relatório
- Download em múltiplos formatos

**3. Histórico** (linhas 645-740)
- Busca por nome
- Filtro por data
- Ordenação (recentes, antigos, A-Z)
- Visualização inline
- Download em lote

**4. Configurações** (linhas 742-839)
- Informações do sistema
- Status do Whisper e API
- Ações: limpar cache, abrir pastas

#### Funções Auxiliares

```python
get_stats() -> dict
    """Calcula estatísticas de uso"""

convert_md_to_txt(md_content: str) -> str
    """Converte Markdown para texto puro"""

convert_md_to_pdf(md_content: str, output_filename: str) -> bytes
    """Gera PDF a partir de Markdown"""

get_recent_reports(limit: int = 10) -> list
    """Obtém lista de relatórios recentes"""
```

---

### 3.3 Utilitários: `utils.py`

#### 1. Detecção de FFmpeg

```python
setup_ffmpeg()
    """
    Detecta FFmpeg automaticamente:
    - Windows: WinGet packages, paths comuns
    - macOS: Homebrew
    - Linux: apt/yum

    Raises:
        EnvironmentError: Se FFmpeg não for encontrado
    """
```

**Estratégia de Busca (Windows):**
1. Verificar se já está no PATH
2. Procurar em `C:\ffmpeg\bin`
3. Procurar em Program Files
4. Buscar em pacotes WinGet
5. Adicionar ao PATH se encontrado

#### 2. Validação de Entrada

```python
validate_patient_info(info: dict)
    """
    Valida campos obrigatórios:
    - paciente_nome, paciente_especie, paciente_raca
    - paciente_idade, tutor_nome, motivo_retorno
    - data_consulta (formato DD/MM/AAAA)

    Raises:
        ValueError: Se validação falhar
    """

_is_valid_date(date_str: str) -> bool
    """Valida formato de data DD/MM/AAAA"""
```

#### 3. Retry Logic

```python
retry_with_backoff(max_retries=4, initial_delay=2.0, backoff_factor=2.0)
    """
    Decorator para retry com backoff exponencial

    Erros retentados:
    - anthropic.RateLimitError
    - anthropic.APIConnectionError
    - anthropic.APITimeoutError
    - anthropic.InternalServerError
    - ConnectionError, TimeoutError
    """

_should_retry(exception: Exception) -> bool
    """Determina se erro deve ser retentado"""
```

#### 4. Limpeza

```python
cleanup_temp_files(directory: Path, pattern: str = "*.tmp",
                  max_age_hours: int = 24)
    """Remove arquivos temporários antigos"""
```

---

### 3.4 Configuração: `config.py`

```python
# Diretórios
BASE_DIR = Path(__file__).parent
AUDIO_DIR = BASE_DIR / "audios"
TRANSCRIPTION_DIR = BASE_DIR / "transcricoes"
REPORT_DIR = BASE_DIR / "relatorios"
TEMPLATE_DIR = BASE_DIR / "templates"

# Modelo Whisper
WHISPER_MODEL = "medium"  # tiny, base, small, medium, large

# API
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Processamento
AUDIO_EXTENSIONS = ['.mp3', '.wav', '.m4a', '.ogg', '.flac']
DEFAULT_LANGUAGE = "pt"

# Template
PROMPT_TEMPLATE_FILE = TEMPLATE_DIR / "prompt_veterinario.txt"
```

---

## 4. APIs e Integrações

### 4.1 Whisper AI (OpenAI)

**Biblioteca:** `openai-whisper==20231117`

**Modelo Usado:** `medium` (769 MB)
- Otimizado para português
- Trade-off: precisão vs velocidade

**Configuração:**
```python
whisper.load_model("medium")
result = model.transcribe(
    audio_path,
    language="pt",
    verbose=False
)
```

**Opções de Modelo:**
| Modelo | Tamanho | Velocidade | Precisão | Uso |
|--------|---------|------------|----------|-----|
| tiny | 39 MB | ⚡⚡⚡⚡⚡ | ⭐⭐ | Testes |
| base | 74 MB | ⚡⚡⚡⚡ | ⭐⭐⭐ | Geral |
| small | 244 MB | ⚡⚡⚡ | ⭐⭐⭐⭐ | Qualidade |
| **medium** | 769 MB | ⚡⚡ | ⭐⭐⭐⭐⭐ | **Português** |
| large | 1550 MB | ⚡ | ⭐⭐⭐⭐⭐ | Máximo |

---

### 4.2 Claude API (Anthropic)

**Biblioteca:** `anthropic==0.39.0`

**Modelo:** `claude-sonnet-4-20250514`

**Configuração:**
```python
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4000,
    temperature=0.3,  # Consistência
    messages=[{"role": "user", "content": prompt}]
)
```

**Parâmetros:**
- `max_tokens`: 4000 (suficiente para relatórios completos)
- `temperature`: 0.3 (baixa = mais consistente)
- `model`: Claude Sonnet 4 (última versão)

**Custos:**
- Input: $3 por 1M tokens
- Output: $15 por 1M tokens
- **Média por consulta:** $0.05

**Tracking de Tokens:**
```python
usage = message.usage
input_tokens = usage.input_tokens
output_tokens = usage.output_tokens
```

---

### 4.3 Dependências Externas

```
# Core
openai-whisper==20231117    # Transcrição
anthropic==0.39.0           # IA Generativa
python-dotenv==1.0.0        # Env vars
tqdm==4.66.1                # Progress bars
pydub==0.25.1               # Áudio

# Web
streamlit                   # Interface
pandas                      # Dados
plotly                      # Gráficos
fpdf                        # PDF

# Testing
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0

# Dev (opcional)
black                       # Formatação
flake8                      # Linting
mypy                        # Type checking
```

---

## 5. Fluxos de Dados

### 5.1 Workflow: Áudio → Relatório

```
┌─────────────┐
│ Upload Áudio│
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Salvar em       │
│ audios/         │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Whisper AI      │
│ Transcrição     │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Salvar em       │
│ transcricoes/   │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Coletar Dados   │
│ do Paciente     │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Validar Dados   │
│ (utils.py)      │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Montar Prompt   │
│ com Template    │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Claude API      │
│ (com retry)     │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Gerar Relatório │
│ Markdown        │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Salvar em       │
│ relatorios/     │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Log de Sucesso  │
└─────────────────┘
```

**Tempo Total:** 5-10 minutos

---

### 5.2 Workflow: Texto → Relatório (Fast Path)

```
┌─────────────┐
│ Colar Texto │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Validar > 100   │
│ caracteres      │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Coletar Dados   │
│ do Paciente     │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Validar Dados   │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Claude API      │
│ (com retry)     │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Salvar Relatório│
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Exibir Preview  │
└─────────────────┘
```

**Tempo Total:** 30 segundos ⚡

---

### 5.3 Fluxo de Retry

```
┌─────────────────┐
│ Chamar API      │
└──────┬──────────┘
       │
       ▼
   ┌────────┐
   │Sucesso?│
   └───┬─┬──┘
       │ │
   Sim │ │ Não
       │ │
       │ ▼
       │ ┌────────────┐
       │ │Erro Retry? │
       │ └─────┬──┬───┘
       │       │  │
       │   Sim │  │ Não
       │       │  │
       │       │  └──────► [Erro Final]
       │       │
       │       ▼
       │  ┌─────────────┐
       │  │ Aguardar    │
       │  │ 2^n segundos│
       │  └──────┬──────┘
       │         │
       │         ▼
       │  ┌─────────────┐
       │  │Max retries? │
       │  └──────┬──┬───┘
       │         │  │
       │     Não │  │ Sim
       │         │  │
       │         │  └──────► [Erro Final]
       │         │
       │         └──────► [Tentar Novamente]
       │
       ▼
  [Retornar Resultado]
```

**Delays:** 2s → 4s → 8s → 16s

---

## 6. Configuração

### 6.1 Variáveis de Ambiente

**Arquivo:** `.env`

```bash
# API Keys
ANTHROPIC_API_KEY=sk-ant-v4-xxxxxxxxxxxxx

# Opcional: Configurações adicionais
# WHISPER_MODEL=medium
# LOG_LEVEL=INFO
```

**Criação:**
```bash
# Copiar template
cp .env.example .env

# Editar
nano .env  # ou notepad .env no Windows
```

---

### 6.2 Configuração de Logs

**Localização:** Configurado em `transcribe_consult.py` e `app.py`

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('veterinary_system.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
```

**Níveis de Log:**
- `INFO` - Operações normais
- `WARNING` - Avisos (validação falhou, retry)
- `ERROR` - Erros que impedem operação

**Arquivos Gerados:**
- `veterinary_system.log` - CLI
- `veterinary_system_web.log` - Streamlit

---

### 6.3 Configuração do Whisper

**Alterar Modelo:**

Edite `config.py`:
```python
WHISPER_MODEL = "base"  # ou "tiny", "small", "medium", "large"
```

**Trade-offs:**
- `tiny/base`: Mais rápido, menos preciso
- `medium`: **Recomendado para português**
- `large`: Mais lento, máxima precisão

---

## 7. Testes

### 7.1 Estrutura de Testes

**Framework:** pytest

**Cobertura:** 70%+

**Arquivos:**
```
tests/
├── __init__.py              # Init
├── conftest.py              # Fixtures compartilhadas
├── test_utils.py            # 15 testes (utils)
└── test_transcription.py    # 14 testes (core)
```

### 7.2 Fixtures Disponíveis

```python
# conftest.py

@pytest.fixture
def temp_dir():
    """Diretório temporário para testes"""

@pytest.fixture
def sample_patient_info():
    """Dados de paciente válidos"""

@pytest.fixture
def invalid_patient_info():
    """Dados inválidos para testes de validação"""

@pytest.fixture
def sample_transcription():
    """Transcrição de exemplo"""

@pytest.fixture
def sample_audio_path(temp_dir):
    """Arquivo de áudio fake"""

@pytest.fixture
def mock_whisper_model():
    """Mock do Whisper"""

@pytest.fixture
def mock_anthropic_client():
    """Mock da API Claude"""

@pytest.fixture
def setup_test_dirs(temp_dir, monkeypatch):
    """Configuração completa de diretórios"""
```

### 7.3 Executar Testes

```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov --cov-report=html

# Apenas unitários
pytest -m unit

# Apenas integração
pytest -m integration

# Verbose
pytest -v

# Um arquivo específico
pytest tests/test_utils.py

# Um teste específico
pytest tests/test_utils.py::test_validate_patient_info_valid
```

### 7.4 Marcadores (Markers)

```python
@pytest.mark.unit          # Teste unitário
@pytest.mark.integration   # Teste de integração
@pytest.mark.slow          # Teste lento
@pytest.mark.requires_api  # Requer API keys
```

### 7.5 Cobertura Atual

```
tests/test_utils.py ..................... [ 15/29 ] 52%
tests/test_transcription.py ............. [ 29/29 ] 100%

Total: 29 testes, 70%+ cobertura
```

---

## 8. Deployment

### 8.1 Deployment Local (Manual)

```bash
# 1. Clonar repositório
git clone https://github.com/silvaj1zero/veterinary-transcription.git
cd veterinary-transcription

# 2. Instalar Python 3.8+
# Verificar: python --version

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Instalar FFmpeg
# Windows: winget install Gyan.FFmpeg
# macOS: brew install ffmpeg
# Linux: sudo apt-get install ffmpeg

# 5. Configurar API Key
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env

# 6. Executar
streamlit run app.py
```

---

### 8.2 Deployment com Docker

**Vantagens:**
- Ambiente isolado
- FFmpeg pré-instalado
- Portável entre sistemas
- Fácil de replicar

#### Dockerfile

```dockerfile
FROM python:3.11-slim

# Instalar FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Copiar aplicação
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Expor porta
EXPOSE 8501

# Executar
CMD ["streamlit", "run", "app.py"]
```

#### docker-compose.yml

```yaml
version: '3.8'

services:
  vet-docs-web:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./audios:/app/audios
      - ./transcricoes:/app/transcricoes
      - ./relatorios:/app/relatorios
      - ./.env:/app/.env:ro
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    restart: unless-stopped
```

#### Comandos

```bash
# Build
docker-compose build

# Iniciar
docker-compose up -d vet-docs-web

# Logs
docker-compose logs -f

# Parar
docker-compose down

# CLI
docker-compose run --rm vet-docs-cli
```

---

### 8.3 Deployment em Servidor

**Opções:**

1. **VPS (DigitalOcean, Linode, AWS EC2)**
   ```bash
   # Instalar Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh

   # Deploy
   docker-compose up -d
   ```

2. **Streamlit Cloud**
   - Grátis para projetos públicos
   - Deploy automático via GitHub
   - Limitações: CPU/memória

3. **Heroku**
   - Deploy via Git
   - Adicionar buildpack Python
   - Configurar variáveis de ambiente

---

## 9. Segurança

### 9.1 Proteção de Secrets

✅ **Implementado:**
- API keys em `.env` (não commitado)
- `.gitignore` configurado
- Variáveis de ambiente

❌ **Não Implementado:**
- Criptografia de dados em repouso
- Autenticação de usuários
- Rate limiting local

### 9.2 Validação de Entrada

✅ **Implementado:**
- Validação de campos obrigatórios
- Validação de formato de data
- Sanitização de nomes de arquivo

### 9.3 Tratamento de Erros

✅ **Implementado:**
- Try-except em operações críticas
- Logging de erros
- Mensagens de erro amigáveis
- Retry automático para falhas temporárias

### 9.4 Conformidade LGPD

⚠️ **Considerações:**
- Dados armazenados localmente
- Sem compartilhamento de dados
- Necessário: consentimento dos tutores
- Implementar: política de retenção de dados

### 9.5 Recomendações de Segurança

1. **Backup Regular:**
   ```bash
   # Backup de relatórios
   tar -czf backup_relatorios_$(date +%Y%m%d).tar.gz relatorios/
   ```

2. **Rotação de API Keys:**
   - Trocar chaves a cada 90 dias
   - Monitorar uso na console Anthropic

3. **Logs:**
   - Não loggar dados sensíveis
   - Implementar rotação de logs
   - Revisar logs regularmente

4. **Acesso:**
   - Restringir acesso ao servidor
   - Usar HTTPS em produção
   - Implementar autenticação (futuro)

---

## 10. Manutenção

### 10.1 Atualização do Sistema

```bash
# 1. Backup
tar -czf backup_$(date +%Y%m%d).tar.gz relatorios/ transcricoes/

# 2. Pull de atualizações
git pull

# 3. Atualizar dependências
pip install -r requirements.txt --upgrade

# 4. Reiniciar serviço
# Se usando systemd:
sudo systemctl restart veterinary-docs

# Se usando Docker:
docker-compose down
docker-compose build
docker-compose up -d
```

### 10.2 Monitoramento

**Métricas a Acompanhar:**
- Número de consultas/dia
- Tempo médio de processamento
- Taxa de erro da API
- Uso de tokens
- Custo total

**Logs a Revisar:**
```bash
# Erros recentes
grep ERROR veterinary_system_web.log | tail -n 50

# Estatísticas de uso
grep "Relatório gerado com sucesso" veterinary_system_web.log | wc -l
```

### 10.3 Troubleshooting

**Problema: Alto uso de memória**
- Solução: Usar modelo Whisper menor (`base` ou `small`)
- Alternativa: Processar áudios fora do horário de pico

**Problema: API muito lenta**
- Verificar: Logs de retry
- Solução: Aumentar timeout
- Alternativa: Processar em lote assíncrono

**Problema: Logs muito grandes**
- Implementar rotação:
  ```python
  from logging.handlers import RotatingFileHandler
  handler = RotatingFileHandler('app.log', maxBytes=10MB, backupCount=5)
  ```

### 10.4 Limpeza Periódica

```bash
# Remover transcrições antigas (>30 dias)
find transcricoes/ -type f -mtime +30 -delete

# Remover áudios processados (>7 dias)
find audios/ -type f -mtime +7 -delete

# Comprimir logs antigos
find . -name "*.log" -mtime +7 -exec gzip {} \;
```

---

## 📊 Métricas de Qualidade

| Métrica | Valor | Meta |
|---------|-------|------|
| Cobertura de Testes | 70%+ | 80% |
| Linhas de Código | 1.934 | - |
| Módulos | 15 | - |
| Dependências | 22 | <30 |
| Documentação | 9 arquivos | - |
| Tempo de Resposta (texto) | 30s | <60s |
| Tempo de Resposta (áudio) | 5-10min | <15min |
| Taxa de Erro API | <1% | <5% |

---

## 🔄 Roadmap Técnico

### Curto Prazo (1-3 meses)
- [ ] Aumentar cobertura de testes para 80%+
- [ ] Implementar CI/CD com GitHub Actions
- [ ] Adicionar type hints completos
- [ ] Implementar cache de transcrições

### Médio Prazo (3-6 meses)
- [ ] Banco de dados (SQLite/PostgreSQL)
- [ ] API REST com FastAPI
- [ ] Autenticação e autorização
- [ ] Rate limiting local

### Longo Prazo (6-12 meses)
- [ ] Multi-tenancy
- [ ] Processamento assíncrono com Celery
- [ ] Suporte a vídeo
- [ ] Mobile app (React Native)

---

## 📞 Suporte Técnico

**Desenvolvedor:** BadiLab
**Versão:** 1.2 (Production Ready)
**Repositório:** https://github.com/silvaj1zero/veterinary-transcription

**Logs de Debug:**
```bash
# Habilitar modo debug
export LOG_LEVEL=DEBUG

# Ver logs em tempo real
tail -f veterinary_system_web.log
```

---

**Última atualização:** Novembro 2025
**Próxima revisão:** Dezembro 2025
