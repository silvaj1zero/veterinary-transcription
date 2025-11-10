"""
Fixtures compartilhadas para os testes
"""
import pytest
import os
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, MagicMock
import tempfile
import shutil


@pytest.fixture
def temp_dir():
    """Cria um diretório temporário para testes"""
    temp = tempfile.mkdtemp()
    yield Path(temp)
    shutil.rmtree(temp, ignore_errors=True)


@pytest.fixture
def sample_patient_info():
    """Retorna informações de paciente válidas para testes"""
    return {
        'paciente_nome': 'Bob',
        'paciente_especie': 'Cão',
        'paciente_raca': 'Yorkshire Terrier',
        'paciente_idade': '5 anos, 3.2kg',
        'tutor_nome': 'Dr. Silva',
        'data_consulta': datetime.now().strftime("%d/%m/%Y"),
        'motivo_retorno': 'Acompanhamento dermatite',
        'tipo_atendimento': 'Presencial'
    }


@pytest.fixture
def invalid_patient_info():
    """Retorna informações de paciente inválidas para testes"""
    return {
        'paciente_nome': '',  # Nome vazio (inválido)
        'paciente_especie': 'Cão',
        'paciente_raca': '',  # Raça vazia (inválido)
        'paciente_idade': '5 anos',
        'tutor_nome': 'Dr. Silva',
        'data_consulta': '32/13/2025',  # Data inválida
        'motivo_retorno': '',  # Motivo vazio (inválido)
        'tipo_atendimento': 'Presencial'
    }


@pytest.fixture
def sample_transcription():
    """Retorna uma transcrição de exemplo"""
    return """
    Paciente Bob, Yorkshire Terrier de 5 anos.
    Apresenta dermatite alérgica há 3 semanas.
    Prescrição: Prednisolona 5mg, 1 comprimido a cada 12h por 7 dias.
    Retorno em 15 dias para reavaliação.
    """


@pytest.fixture
def sample_audio_path(temp_dir):
    """Cria um arquivo de áudio falso para testes"""
    audio_file = temp_dir / "consulta_teste.mp3"
    audio_file.write_text("fake audio content")  # Não é um áudio real, apenas para testes de path
    return audio_file


@pytest.fixture
def mock_whisper_model():
    """Mock do modelo Whisper"""
    mock = MagicMock()
    mock.transcribe.return_value = {
        'text': 'Paciente apresenta sintomas de dermatite alérgica.',
        'language': 'pt'
    }
    return mock


@pytest.fixture
def mock_anthropic_client():
    """Mock do cliente Anthropic"""
    mock = MagicMock()

    # Mock da resposta da API
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text="# Relatório Veterinário\n\nPaciente: Bob\n\n## Diagnóstico\nDermatite alérgica")]
    mock_message.usage = MagicMock(input_tokens=100, output_tokens=200)

    mock.messages.create.return_value = mock_message

    return mock


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Configura variáveis de ambiente para testes"""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test-key-123456")


@pytest.fixture
def setup_test_dirs(temp_dir, monkeypatch):
    """Configura diretórios de teste"""
    # Criar diretórios necessários
    audio_dir = temp_dir / "audios"
    transcription_dir = temp_dir / "transcricoes"
    report_dir = temp_dir / "relatorios"
    template_dir = temp_dir / "templates"

    for d in [audio_dir, transcription_dir, report_dir, template_dir]:
        d.mkdir()

    # Criar template de prompt
    prompt_template = template_dir / "prompt_veterinario.txt"
    prompt_template.write_text("""
Transcrição: {transcricao}
Paciente: {paciente_nome}
Espécie: {paciente_especie}
Raça: {paciente_raca}
Idade: {paciente_idade}
Tutor: {tutor_nome}
Data: {data_consulta}
Motivo: {motivo_retorno}
Tipo: {tipo_atendimento}

Gere um relatório veterinário estruturado.
""")

    # Modificar config para usar diretórios de teste
    import config
    monkeypatch.setattr(config, 'AUDIO_DIR', audio_dir)
    monkeypatch.setattr(config, 'TRANSCRIPTION_DIR', transcription_dir)
    monkeypatch.setattr(config, 'REPORT_DIR', report_dir)
    monkeypatch.setattr(config, 'TEMPLATE_DIR', template_dir)
    monkeypatch.setattr(config, 'PROMPT_TEMPLATE_FILE', prompt_template)

    return {
        'audio_dir': audio_dir,
        'transcription_dir': transcription_dir,
        'report_dir': report_dir,
        'template_dir': template_dir
    }
