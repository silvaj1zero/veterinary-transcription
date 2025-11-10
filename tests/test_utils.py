"""
Testes para o módulo utils
"""
import pytest
from pathlib import Path
import time
from unittest.mock import Mock, patch, MagicMock
from utils import (
    setup_ffmpeg,
    validate_patient_info,
    retry_with_backoff,
    _is_valid_date,
    _should_retry,
    cleanup_temp_files
)


# ============================================================================
# Testes para setup_ffmpeg
# ============================================================================

@pytest.mark.unit
def test_setup_ffmpeg_already_in_path():
    """Testa quando FFmpeg já está no PATH"""
    with patch('utils.shutil.which', return_value='/usr/bin/ffmpeg'):
        # Não deve levantar exceção
        setup_ffmpeg()


@pytest.mark.unit
def test_setup_ffmpeg_not_found():
    """Testa quando FFmpeg não é encontrado"""
    with patch('utils.shutil.which', return_value=None):
        with patch('utils.os.name', 'posix'):  # Linux/Mac
            with pytest.raises(EnvironmentError, match="FFmpeg não encontrado"):
                setup_ffmpeg()


# ============================================================================
# Testes para validate_patient_info
# ============================================================================

@pytest.mark.unit
def test_validate_patient_info_valid(sample_patient_info):
    """Testa validação com informações válidas"""
    # Não deve levantar exceção
    validate_patient_info(sample_patient_info)


@pytest.mark.unit
def test_validate_patient_info_missing_name():
    """Testa validação com nome faltando"""
    info = {
        'paciente_nome': '',  # Vazio
        'paciente_especie': 'Cão',
        'paciente_raca': 'Yorkshire',
        'paciente_idade': '5 anos',
        'tutor_nome': 'Dr. Silva',
        'motivo_retorno': 'Consulta'
    }
    with pytest.raises(ValueError, match="Nome do paciente"):
        validate_patient_info(info)


@pytest.mark.unit
def test_validate_patient_info_missing_species():
    """Testa validação com espécie faltando"""
    info = {
        'paciente_nome': 'Bob',
        'paciente_especie': '',  # Vazio
        'paciente_raca': 'Yorkshire',
        'paciente_idade': '5 anos',
        'tutor_nome': 'Dr. Silva',
        'motivo_retorno': 'Consulta'
    }
    with pytest.raises(ValueError, match="Espécie do paciente"):
        validate_patient_info(info)


@pytest.mark.unit
def test_validate_patient_info_invalid_date():
    """Testa validação com data inválida"""
    info = {
        'paciente_nome': 'Bob',
        'paciente_especie': 'Cão',
        'paciente_raca': 'Yorkshire',
        'paciente_idade': '5 anos',
        'tutor_nome': 'Dr. Silva',
        'motivo_retorno': 'Consulta',
        'data_consulta': '32/13/2025'  # Data inválida
    }
    with pytest.raises(ValueError, match="Data inválida"):
        validate_patient_info(info)


@pytest.mark.unit
def test_validate_patient_info_whitespace_only():
    """Testa validação com campos contendo apenas espaços"""
    info = {
        'paciente_nome': '   ',  # Apenas espaços
        'paciente_especie': 'Cão',
        'paciente_raca': 'Yorkshire',
        'paciente_idade': '5 anos',
        'tutor_nome': 'Dr. Silva',
        'motivo_retorno': 'Consulta'
    }
    with pytest.raises(ValueError, match="Nome do paciente"):
        validate_patient_info(info)


# ============================================================================
# Testes para _is_valid_date
# ============================================================================

@pytest.mark.unit
@pytest.mark.parametrize("date_str,expected", [
    ("10/11/2025", True),
    ("01/01/2000", True),
    ("31/12/2099", True),
    ("32/01/2025", False),  # Dia inválido
    ("01/13/2025", False),  # Mês inválido
    ("10-11-2025", False),  # Formato errado
    ("2025/11/10", False),  # Ordem errada
    ("10/11/25", False),    # Ano com 2 dígitos
    ("abc", False),         # Texto aleatório
    ("", False),            # String vazia
])
def test_is_valid_date(date_str, expected):
    """Testa validação de data com vários formatos"""
    assert _is_valid_date(date_str) == expected


# ============================================================================
# Testes para retry_with_backoff
# ============================================================================

@pytest.mark.unit
def test_retry_with_backoff_success_first_try():
    """Testa retry quando a função funciona na primeira tentativa"""
    mock_func = Mock(return_value="sucesso")
    decorated = retry_with_backoff(max_retries=3)(mock_func)

    result = decorated()

    assert result == "sucesso"
    assert mock_func.call_count == 1


@pytest.mark.unit
def test_retry_with_backoff_success_after_retries():
    """Testa retry quando a função funciona após algumas tentativas"""
    # Simular erro nas primeiras 2 tentativas, sucesso na 3ª
    mock_func = Mock(side_effect=[
        ConnectionError("Erro 1"),
        ConnectionError("Erro 2"),
        "sucesso"
    ])

    with patch('utils._should_retry', return_value=True):
        decorated = retry_with_backoff(max_retries=3, initial_delay=0.01)(mock_func)
        result = decorated()

    assert result == "sucesso"
    assert mock_func.call_count == 3


@pytest.mark.unit
def test_retry_with_backoff_max_retries_exceeded():
    """Testa retry quando todas as tentativas falham"""
    mock_func = Mock(side_effect=ConnectionError("Erro persistente"))

    with patch('utils._should_retry', return_value=True):
        decorated = retry_with_backoff(max_retries=2, initial_delay=0.01)(mock_func)

        with pytest.raises(ConnectionError, match="Erro persistente"):
            decorated()

    assert mock_func.call_count == 3  # 1 tentativa inicial + 2 retries


@pytest.mark.unit
def test_retry_with_backoff_non_retryable_error():
    """Testa que erros não recuperáveis não são retentados"""
    mock_func = Mock(side_effect=ValueError("Erro não recuperável"))

    with patch('utils._should_retry', return_value=False):
        decorated = retry_with_backoff(max_retries=3)(mock_func)

        with pytest.raises(ValueError, match="Erro não recuperável"):
            decorated()

    assert mock_func.call_count == 1  # Não tenta novamente


# ============================================================================
# Testes para _should_retry
# ============================================================================

@pytest.mark.unit
def test_should_retry_with_anthropic_errors():
    """Testa _should_retry com erros da API Anthropic"""
    import anthropic

    # Erros que devem ser retentados
    assert _should_retry(anthropic.RateLimitError("Rate limit")) == True
    assert _should_retry(anthropic.APIConnectionError("Connection error")) == True
    assert _should_retry(anthropic.APITimeoutError("Timeout")) == True
    assert _should_retry(anthropic.InternalServerError("Server error")) == True

    # Erros que não devem ser retentados
    assert _should_retry(anthropic.AuthenticationError("Auth error")) == False
    assert _should_retry(ValueError("Value error")) == False


@pytest.mark.unit
def test_should_retry_with_generic_errors():
    """Testa _should_retry com erros genéricos"""
    # Erros de rede genéricos (devem ser retentados)
    assert _should_retry(ConnectionError("Connection failed")) == True
    assert _should_retry(TimeoutError("Timeout")) == True

    # Outros erros (não devem ser retentados)
    assert _should_retry(ValueError("Value error")) == False
    assert _should_retry(TypeError("Type error")) == False


# ============================================================================
# Testes para cleanup_temp_files
# ============================================================================

@pytest.mark.unit
def test_cleanup_temp_files(temp_dir):
    """Testa limpeza de arquivos temporários antigos"""
    # Criar arquivos temporários
    old_file = temp_dir / "old.tmp"
    new_file = temp_dir / "new.tmp"
    other_file = temp_dir / "other.txt"

    old_file.write_text("old")
    new_file.write_text("new")
    other_file.write_text("other")

    # Modificar tempo de modificação do arquivo antigo
    old_time = time.time() - (25 * 3600)  # 25 horas atrás
    import os
    os.utime(old_file, (old_time, old_time))

    # Limpar arquivos com mais de 24 horas
    cleanup_temp_files(temp_dir, pattern="*.tmp", max_age_hours=24)

    # Verificar que apenas o arquivo antigo foi removido
    assert not old_file.exists()
    assert new_file.exists()
    assert other_file.exists()


@pytest.mark.unit
def test_cleanup_temp_files_nonexistent_dir(temp_dir):
    """Testa limpeza em diretório inexistente"""
    nonexistent = temp_dir / "nonexistent"

    # Não deve levantar exceção
    cleanup_temp_files(nonexistent, pattern="*.tmp")
