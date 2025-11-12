"""
Configurações do Sistema de Transcrição Veterinária
"""
import os
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

# Configurações de processamento
AUDIO_EXTENSIONS = ['.mp3', '.wav', '.m4a', '.ogg', '.flac']
DEFAULT_LANGUAGE = "pt"

# Template do prompt
PROMPT_TEMPLATE_FILE = TEMPLATE_DIR / "prompt_veterinario.txt"
