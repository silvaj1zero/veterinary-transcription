"""
Testes para a classe VeterinaryTranscription
"""
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, mock_open
from transcribe_consult import VeterinaryTranscription
import anthropic


# ============================================================================
# Testes de Inicialização
# ============================================================================

@pytest.mark.unit
def test_init_with_api_key(mock_env_vars, setup_test_dirs, mock_anthropic_client):
    """Testa inicialização com API key válida"""
    with patch('transcribe_consult.anthropic.Anthropic', return_value=mock_anthropic_client):
        system = VeterinaryTranscription(load_whisper=False)

        assert system.whisper_model is None
        assert system.anthropic_client is not None
        assert system.prompt_template is not None


@pytest.mark.unit
def test_init_without_api_key(setup_test_dirs):
    """Testa inicialização sem API key"""
    import config
    original_key = config.ANTHROPIC_API_KEY

    try:
        config.ANTHROPIC_API_KEY = ""

        with pytest.raises(ValueError, match="ANTHROPIC_API_KEY não encontrada"):
            VeterinaryTranscription(load_whisper=False)
    finally:
        config.ANTHROPIC_API_KEY = original_key


@pytest.mark.unit
def test_init_missing_template(mock_env_vars, setup_test_dirs):
    """Testa inicialização com template faltando"""
    import config

    # Remover arquivo de template
    config.PROMPT_TEMPLATE_FILE.unlink()

    with pytest.raises(FileNotFoundError, match="Template não encontrado"):
        VeterinaryTranscription(load_whisper=False)


# ============================================================================
# Testes de Validação de Paciente
# ============================================================================

@pytest.mark.unit
def test_collect_patient_info_valid(mock_env_vars, setup_test_dirs, sample_patient_info):
    """Testa coleta de informações válidas do paciente"""
    with patch('transcribe_consult.anthropic.Anthropic'):
        system = VeterinaryTranscription(load_whisper=False)

    # Simular inputs do usuário
    inputs = [
        sample_patient_info['paciente_nome'],
        sample_patient_info['paciente_especie'],
        sample_patient_info['paciente_raca'],
        sample_patient_info['paciente_idade'],
        sample_patient_info['tutor_nome'],
        sample_patient_info['data_consulta'],
        sample_patient_info['motivo_retorno'],
        sample_patient_info['tipo_atendimento']
    ]

    with patch('builtins.input', side_effect=inputs):
        result = system.collect_patient_info()

    assert result['paciente_nome'] == sample_patient_info['paciente_nome']
    assert result['paciente_especie'] == sample_patient_info['paciente_especie']
    assert 'data_consulta' in result


@pytest.mark.unit
def test_collect_patient_info_invalid_then_cancel(mock_env_vars, setup_test_dirs):
    """Testa coleta de informações inválidas seguida de cancelamento"""
    with patch('transcribe_consult.anthropic.Anthropic'):
        system = VeterinaryTranscription(load_whisper=False)

    # Primeira tentativa: dados inválidos
    # Segunda tentativa: usuário cancela
    inputs = [
        '',      # paciente_nome (vazio - inválido)
        'Cão',   # paciente_especie
        'York',  # paciente_raca
        '5 anos', # paciente_idade
        'Dr. Silva', # tutor_nome
        '10/11/2025', # data_consulta
        'Consulta',   # motivo_retorno
        'Presencial', # tipo_atendimento
        'n'      # não tentar novamente
    ]

    with patch('builtins.input', side_effect=inputs):
        with pytest.raises(ValueError):
            system.collect_patient_info()


# ============================================================================
# Testes de Geração de Relatório
# ============================================================================

@pytest.mark.unit
@pytest.mark.requires_api
def test_generate_report_success(mock_env_vars, setup_test_dirs, sample_patient_info, sample_transcription):
    """Testa geração de relatório com sucesso"""
    mock_client = MagicMock()
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text="# Relatório Veterinário\n\nPaciente: Bob")]
    mock_message.usage = MagicMock(input_tokens=100, output_tokens=200)
    mock_client.messages.create.return_value = mock_message

    with patch('transcribe_consult.anthropic.Anthropic', return_value=mock_client):
        system = VeterinaryTranscription(load_whisper=False)
        report = system.generate_report(sample_transcription, sample_patient_info)

    assert "Relatório" in report
    assert mock_client.messages.create.called


@pytest.mark.unit
@pytest.mark.requires_api
def test_generate_report_rate_limit_error(mock_env_vars, setup_test_dirs, sample_patient_info, sample_transcription):
    """Testa tratamento de erro de rate limit"""
    mock_client = MagicMock()
    mock_client.messages.create.side_effect = anthropic.RateLimitError("Rate limit exceeded")

    with patch('transcribe_consult.anthropic.Anthropic', return_value=mock_client):
        system = VeterinaryTranscription(load_whisper=False)

        with pytest.raises(anthropic.RateLimitError):
            system.generate_report(sample_transcription, sample_patient_info)


@pytest.mark.unit
@pytest.mark.requires_api
def test_generate_report_api_error(mock_env_vars, setup_test_dirs, sample_patient_info, sample_transcription):
    """Testa tratamento de erro genérico da API"""
    mock_client = MagicMock()
    mock_client.messages.create.side_effect = anthropic.APIError("API Error")

    with patch('transcribe_consult.anthropic.Anthropic', return_value=mock_client):
        system = VeterinaryTranscription(load_whisper=False)

        with pytest.raises(anthropic.APIError):
            system.generate_report(sample_transcription, sample_patient_info)


# ============================================================================
# Testes de Salvamento de Relatório
# ============================================================================

@pytest.mark.unit
def test_save_report(mock_env_vars, setup_test_dirs):
    """Testa salvamento de relatório"""
    with patch('transcribe_consult.anthropic.Anthropic'):
        system = VeterinaryTranscription(load_whisper=False)

    report_text = "# Relatório\n\nPaciente: Bob"
    patient_name = "Bob"
    audio_filename = "consulta_20251110"

    report_path = system.save_report(report_text, patient_name, audio_filename)

    assert report_path.exists()
    assert report_path.suffix == '.md'
    assert 'Bob' in report_path.name

    # Verificar conteúdo
    content = report_path.read_text(encoding='utf-8')
    assert content == report_text


@pytest.mark.unit
def test_save_report_special_characters(mock_env_vars, setup_test_dirs):
    """Testa salvamento de relatório com caracteres especiais no nome"""
    with patch('transcribe_consult.anthropic.Anthropic'):
        system = VeterinaryTranscription(load_whisper=False)

    report_text = "# Relatório"
    patient_name = "Bob & Rex / Max"  # Caracteres especiais
    audio_filename = "consulta"

    report_path = system.save_report(report_text, patient_name, audio_filename)

    assert report_path.exists()
    # Verificar que caracteres especiais foram removidos/sanitizados
    assert '&' not in report_path.name
    assert '/' not in report_path.name


# ============================================================================
# Testes de Transcrição de Áudio
# ============================================================================

@pytest.mark.unit
@pytest.mark.slow
def test_transcribe_audio(mock_env_vars, setup_test_dirs, sample_audio_path, mock_whisper_model):
    """Testa transcrição de áudio"""
    with patch('transcribe_consult.anthropic.Anthropic'):
        with patch('transcribe_consult.whisper.load_model', return_value=mock_whisper_model):
            system = VeterinaryTranscription(load_whisper=True)
            system.whisper_model = mock_whisper_model

            result = system.transcribe_audio(sample_audio_path)

    assert 'text' in result
    assert mock_whisper_model.transcribe.called

    # Verificar que transcrição foi salva
    import config
    transcription_files = list(config.TRANSCRIPTION_DIR.glob("*.txt"))
    assert len(transcription_files) > 0


@pytest.mark.unit
def test_ensure_whisper_loaded(mock_env_vars, setup_test_dirs, mock_whisper_model):
    """Testa carregamento lazy do modelo Whisper"""
    with patch('transcribe_consult.anthropic.Anthropic'):
        with patch('transcribe_consult.whisper.load_model', return_value=mock_whisper_model) as mock_load:
            system = VeterinaryTranscription(load_whisper=True)

            # Whisper não deve estar carregado ainda
            assert system.whisper_model is None

            # Forçar carregamento
            system._ensure_whisper_loaded()

            # Agora deve estar carregado
            assert system.whisper_model is not None
            assert mock_load.called


# ============================================================================
# Testes de Processamento de Texto
# ============================================================================

@pytest.mark.unit
def test_process_from_text(mock_env_vars, setup_test_dirs, sample_patient_info, sample_transcription):
    """Testa processamento a partir de texto existente"""
    mock_client = MagicMock()
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text="# Relatório")]
    mock_message.usage = MagicMock(input_tokens=100, output_tokens=200)
    mock_client.messages.create.return_value = mock_message

    with patch('transcribe_consult.anthropic.Anthropic', return_value=mock_client):
        system = VeterinaryTranscription(load_whisper=False)

        report_path = system.process_from_text(
            sample_transcription,
            sample_patient_info,
            source_name="teste_manual"
        )

    assert report_path.exists()
    assert report_path.suffix == '.md'

    # Verificar que transcrição foi salva
    import config
    transcription_files = list(config.TRANSCRIPTION_DIR.glob("*teste_manual*.txt"))
    assert len(transcription_files) > 0


# ============================================================================
# Testes de Integração (Workflow Completo)
# ============================================================================

@pytest.mark.integration
def test_full_workflow_from_text(mock_env_vars, setup_test_dirs, sample_patient_info, sample_transcription):
    """Testa workflow completo: texto -> relatório"""
    mock_client = MagicMock()
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text="# Relatório Veterinário\n\n## Paciente\nBob")]
    mock_message.usage = MagicMock(input_tokens=150, output_tokens=250)
    mock_client.messages.create.return_value = mock_message

    with patch('transcribe_consult.anthropic.Anthropic', return_value=mock_client):
        system = VeterinaryTranscription(load_whisper=False)

        # Processar
        report_path = system.process_from_text(
            sample_transcription,
            sample_patient_info,
            source_name="integration_test"
        )

        # Verificações
        assert report_path.exists()

        # Verificar conteúdo
        content = report_path.read_text(encoding='utf-8')
        assert "Relatório Veterinário" in content
        assert "Bob" in content

        # Verificar que transcrição foi salva
        import config
        transcription_files = list(config.TRANSCRIPTION_DIR.glob("*integration_test*.txt"))
        assert len(transcription_files) == 1


@pytest.mark.integration
@pytest.mark.slow
def test_full_workflow_from_audio(mock_env_vars, setup_test_dirs, sample_patient_info, sample_audio_path):
    """Testa workflow completo: áudio -> transcrição -> relatório"""
    # Mock Whisper
    mock_whisper = MagicMock()
    mock_whisper.transcribe.return_value = {
        'text': 'Consulta veterinária de acompanhamento',
        'language': 'pt'
    }

    # Mock Anthropic
    mock_client = MagicMock()
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text="# Relatório Completo")]
    mock_message.usage = MagicMock(input_tokens=100, output_tokens=200)
    mock_client.messages.create.return_value = mock_message

    with patch('transcribe_consult.anthropic.Anthropic', return_value=mock_client):
        with patch('transcribe_consult.whisper.load_model', return_value=mock_whisper):
            system = VeterinaryTranscription(load_whisper=True)
            system.whisper_model = mock_whisper

            # Processar
            report_path = system.process_consultation(
                sample_audio_path,
                sample_patient_info
            )

            # Verificações
            assert report_path.exists()

            # Verificar que transcrição foi criada
            import config
            transcription_files = list(config.TRANSCRIPTION_DIR.glob("*.txt"))
            assert len(transcription_files) > 0
