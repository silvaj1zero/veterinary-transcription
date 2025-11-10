"""
Utilitários para o Sistema de Transcrição Veterinária
"""
import os
import shutil
import logging
from pathlib import Path
from functools import wraps
import time

# ============================================================================
# FFmpeg Detection
# ============================================================================

def setup_ffmpeg():
    """
    Detecta e configura o FFmpeg no PATH de forma cross-platform.

    Raises:
        EnvironmentError: Se FFmpeg não for encontrado
    """
    # Verificar se FFmpeg já está no PATH
    ffmpeg_path = shutil.which('ffmpeg')

    if ffmpeg_path:
        logging.info(f"FFmpeg encontrado: {ffmpeg_path}")
        return

    # Locais comuns do FFmpeg no Windows
    if os.name == 'nt':  # Windows
        common_paths = [
            r'C:\ffmpeg\bin',
            r'C:\Program Files\ffmpeg\bin',
            r'C:\Program Files (x86)\ffmpeg\bin',
        ]

        # Verificar também WinGet packages
        user_local_path = Path(os.environ.get('LOCALAPPDATA', ''))
        if user_local_path.exists():
            winget_packages = user_local_path / 'Microsoft' / 'WinGet' / 'Packages'
            if winget_packages.exists():
                # Procurar por FFmpeg nos pacotes WinGet
                for package in winget_packages.glob('*FFmpeg*'):
                    for ffmpeg_bin in package.rglob('bin'):
                        if (ffmpeg_bin / 'ffmpeg.exe').exists():
                            common_paths.append(str(ffmpeg_bin))

        # Tentar adicionar ao PATH
        for path in common_paths:
            if Path(path).exists() and (Path(path) / 'ffmpeg.exe').exists():
                os.environ['PATH'] = f"{path};{os.environ['PATH']}"
                logging.info(f"FFmpeg adicionado ao PATH: {path}")
                return

    # Se chegou aqui, FFmpeg não foi encontrado
    raise EnvironmentError(
        "FFmpeg não encontrado! Por favor, instale o FFmpeg:\n"
        "  Windows: winget install Gyan.FFmpeg\n"
        "  macOS: brew install ffmpeg\n"
        "  Linux: sudo apt-get install ffmpeg\n"
        "Ou adicione o diretório bin do FFmpeg ao PATH do sistema."
    )


# ============================================================================
# Input Validation
# ============================================================================

def validate_patient_info(info):
    """
    Valida as informações do paciente.

    Args:
        info (dict): Dicionário com informações do paciente

    Raises:
        ValueError: Se algum campo obrigatório estiver vazio ou inválido
    """
    required_fields = {
        'paciente_nome': 'Nome do paciente',
        'paciente_especie': 'Espécie do paciente',
        'paciente_raca': 'Raça do paciente',
        'paciente_idade': 'Idade/Peso do paciente',
        'tutor_nome': 'Nome do tutor',
        'motivo_retorno': 'Motivo do retorno/consulta'
    }

    for field, label in required_fields.items():
        if not info.get(field, '').strip():
            raise ValueError(f"Campo obrigatório não preenchido: {label}")

    # Validar data (se fornecida)
    if info.get('data_consulta'):
        data = info['data_consulta'].strip()
        if data and not _is_valid_date(data):
            raise ValueError(f"Data inválida: {data}. Use o formato DD/MM/AAAA")

    logging.info("Informações do paciente validadas com sucesso")


def _is_valid_date(date_str):
    """
    Verifica se a string é uma data válida no formato DD/MM/AAAA.

    Args:
        date_str (str): String com a data

    Returns:
        bool: True se válida, False caso contrário
    """
    import re
    from datetime import datetime

    # Verificar formato básico
    if not re.match(r'^\d{2}/\d{2}/\d{4}$', date_str):
        return False

    # Tentar parsear a data
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False


# ============================================================================
# API Retry Logic
# ============================================================================

def retry_with_backoff(max_retries=4, initial_delay=2.0, backoff_factor=2.0):
    """
    Decorator para adicionar retry com backoff exponencial.

    Args:
        max_retries (int): Número máximo de tentativas
        initial_delay (float): Delay inicial em segundos
        backoff_factor (float): Fator de multiplicação do delay

    Returns:
        function: Função decorada
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e

                    # Verificar se é um erro que vale a pena retry
                    if not _should_retry(e):
                        logging.warning(f"Erro não recuperável: {type(e).__name__}")
                        raise

                    if attempt < max_retries:
                        logging.warning(
                            f"Tentativa {attempt + 1}/{max_retries} falhou: {str(e)}. "
                            f"Tentando novamente em {delay:.1f}s..."
                        )
                        time.sleep(delay)
                        delay *= backoff_factor
                    else:
                        logging.error(f"Todas as {max_retries + 1} tentativas falharam")

            # Se chegou aqui, todas as tentativas falharam
            raise last_exception

        return wrapper
    return decorator


def _should_retry(exception):
    """
    Determina se um erro deve ser retentado.

    Args:
        exception: A exceção capturada

    Returns:
        bool: True se deve retentar, False caso contrário
    """
    # Importar aqui para evitar dependência circular
    try:
        import anthropic

        # Erros de rede/API que valem retry
        retry_errors = (
            anthropic.RateLimitError,
            anthropic.APIConnectionError,
            anthropic.APITimeoutError,
            anthropic.InternalServerError,
        )

        return isinstance(exception, retry_errors)
    except ImportError:
        # Se anthropic não estiver disponível, retentar apenas erros de rede genéricos
        return isinstance(exception, (ConnectionError, TimeoutError))


# ============================================================================
# Cleanup Utilities
# ============================================================================

def cleanup_temp_files(directory, pattern="*.tmp", max_age_hours=24):
    """
    Remove arquivos temporários antigos.

    Args:
        directory (Path): Diretório para limpar
        pattern (str): Padrão glob para arquivos temporários
        max_age_hours (int): Idade máxima em horas
    """
    import time

    directory = Path(directory)
    if not directory.exists():
        return

    current_time = time.time()
    max_age_seconds = max_age_hours * 3600

    for file_path in directory.glob(pattern):
        try:
            file_age = current_time - file_path.stat().st_mtime
            if file_age > max_age_seconds:
                file_path.unlink()
                logging.info(f"Arquivo temporário removido: {file_path.name}")
        except Exception as e:
            logging.warning(f"Erro ao remover {file_path.name}: {e}")
