"""
Configurações do Sistema de Transcrição Veterinária
"""
import os
import logging
from pathlib import Path

# Diretórios
BASE_DIR = Path(__file__).parent
AUDIO_DIR = BASE_DIR / "audios"
TRANSCRIPTION_DIR = BASE_DIR / "transcricoes"
REPORT_DIR = BASE_DIR / "relatorios"
TEMPLATE_DIR = BASE_DIR / "templates"

# Criar diretórios se não existirem
for directory in [AUDIO_DIR, TRANSCRIPTION_DIR, REPORT_DIR, TEMPLATE_DIR]:
    directory.mkdir(exist_ok=True)

# Modelo Whisper (opções: tiny, base, small, medium, large)
# base = rápido e preciso para produção (5-10x mais rápido que medium)
# medium = mais preciso mas MUITO mais lento em CPU (use apenas com GPU)
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")  # Permite override via env var

# API Keys (será carregada do arquivo .env)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Configuração de Provedores
# Opções: "openai_whisper" (local), "google_gemini" (nuvem)
TRANSCRIPTION_PROVIDER = os.getenv("TRANSCRIPTION_PROVIDER", "google_gemini")

# Opções: "anthropic_claude", "google_gemini"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "google_gemini")

# Modelos Gemini
GEMINI_MODEL_FLASH = "gemini-2.5-flash" 
GEMINI_MODEL_PRO = "gemini-2.5-pro"

# Configurações de processamento
AUDIO_EXTENSIONS = ['.mp3', '.wav', '.m4a', '.ogg', '.flac']
DEFAULT_LANGUAGE = "pt"

# Template do prompt
# Template do prompt
PROMPT_TEMPLATE_FILE = TEMPLATE_DIR / "prompt_veterinario.txt"

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")  # anon/public key
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")  # service_role key (admin)

# Database Provider: "sqlite" (local) ou "supabase" (cloud)
DATABASE_PROVIDER = os.getenv("DATABASE_PROVIDER", "sqlite")

# ============================================================================
# SEGURANÇA: Filtro de Logs para Redação de API Keys
# ============================================================================

class APIKeyFilter(logging.Filter):
    """Filtro para remover API keys dos logs"""
    def filter(self, record):
        if hasattr(record, 'msg'):
            msg = str(record.msg)
            # Redact Anthropic API keys
            if ANTHROPIC_API_KEY and ANTHROPIC_API_KEY in msg:
                msg = msg.replace(ANTHROPIC_API_KEY, '***ANTHROPIC_KEY_REDACTED***')
            # Redact Google API keys
            if GOOGLE_API_KEY and GOOGLE_API_KEY in msg:
                msg = msg.replace(GOOGLE_API_KEY, '***GOOGLE_KEY_REDACTED***')
            # Redact Supabase keys
            if SUPABASE_KEY and SUPABASE_KEY in msg:
                msg = msg.replace(SUPABASE_KEY, '***SUPABASE_KEY_REDACTED***')
            if SUPABASE_SERVICE_KEY and SUPABASE_SERVICE_KEY in msg:
                msg = msg.replace(SUPABASE_SERVICE_KEY, '***SUPABASE_SERVICE_KEY_REDACTED***')
            record.msg = msg
        return True

# Aplicar filtro a todos os handlers de log existentes
def apply_api_key_filter():
    """Aplica o filtro de API keys a todos os handlers de log"""
    api_filter = APIKeyFilter()
    for handler in logging.root.handlers:
        handler.addFilter(api_filter)

# Aplicar filtro automaticamente quando o módulo é importado
apply_api_key_filter()
