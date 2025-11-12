#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface Gráfica do Sistema de Documentação Veterinária
Powered by Streamlit
"""

import streamlit as st
import os
import sys
import logging
from pathlib import Path
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
import json
import re
from fpdf import FPDF

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging para Streamlit
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('veterinary_system_web.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Configurar FFmpeg (cross-platform)
from utils import setup_ffmpeg, validate_patient_info
try:
    setup_ffmpeg()
    logging.info("FFmpeg configurado com sucesso")
except EnvironmentError as e:
    logging.error(f"Erro ao configurar FFmpeg: {e}")
    st.error(f"⚠️ Erro ao configurar FFmpeg: {e}")
    st.info("Por favor, instale o FFmpeg e tente novamente.")

# Importar sistema
import config
from transcribe_consult import VeterinaryTranscription

# Configuração da página
st.set_page_config(
    page_title="Sistema Veterinário",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
</style>
""", unsafe_allow_html=True)

# Funções auxiliares
def get_stats():
    """Obtém estatísticas do sistema"""
    stats = {
        'total_relatorios': 0,
        'relatorios_hoje': 0,
        'custo_total': 0.0,
        'custo_hoje': 0.0,
        'tempo_medio': 0
    }

    # Contar relatórios
    if config.REPORT_DIR.exists():
        reports = list(config.REPORT_DIR.glob("*.md"))
        stats['total_relatorios'] = len(reports)

        # Relatórios de hoje
        hoje = datetime.now().strftime("%Y%m%d")
        stats['relatorios_hoje'] = sum(1 for r in reports if r.stem.startswith(hoje))

        # Estimativa de custos ($0.05 por relatório)
        stats['custo_total'] = stats['total_relatorios'] * 0.05
        stats['custo_hoje'] = stats['relatorios_hoje'] * 0.05

    return stats

def convert_md_to_txt(md_content):
    """Converte conteúdo Markdown para texto puro"""
    # Remove cabeçalhos (#)
    txt = re.sub(r'^#+\s+', '', md_content, flags=re.MULTILINE)

    # Remove negrito/itálico
    txt = re.sub(r'\*\*(.+?)\*\*', r'\1', txt)
    txt = re.sub(r'\*(.+?)\*', r'\1', txt)

    # Remove links markdown [texto](url)
    txt = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', txt)

    # Remove tabelas markdown (converte para texto simples)
    txt = re.sub(r'\|', ' ', txt)
    txt = re.sub(r'^[-:\s]+$', '', txt, flags=re.MULTILINE)

    # Remove emojis se houver
    txt = re.sub(r'[\U0001F000-\U0001FFFF]+', '', txt)

    # Remove linhas vazias extras
    txt = re.sub(r'\n{3,}', '\n\n', txt)

    return txt.strip()

def convert_md_to_pdf(md_content, output_filename):
    """Converte conteúdo Markdown para PDF"""
    pdf = FPDF()
    pdf.add_page()

    # Configurar fonte com suporte a UTF-8
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(left=10, top=10, right=10)

    # Processar conteúdo linha por linha
    lines = md_content.split('\n')

    for line in lines:
        original_line = line
        line = line.strip()

        # Linha vazia - adicionar espaço
        if not line:
            pdf.ln(3)
            continue

        # Pular linhas separadoras de tabelas que são APENAS traços (---)
        if re.match(r'^[\-]{3,}$', line):
            continue

        # Pular separadores de colunas de tabela (| --- | --- |)
        if re.match(r'^[\|\s\-:]+$', line) and '|' in line:
            continue

        # Detectar tipo de linha e configurar fonte
        text = line

        if line.startswith('# '):
            pdf.set_font('Helvetica', 'B', 14)
            text = line[2:]  # Remove "# "
        elif line.startswith('## '):
            pdf.set_font('Helvetica', 'B', 12)
            text = line[3:]  # Remove "## "
        elif line.startswith('### '):
            pdf.set_font('Helvetica', 'B', 11)
            text = line[4:]  # Remove "### "
        elif line.startswith('- ') or line.startswith('* '):
            pdf.set_font('Helvetica', '', 9)
            text = '  ' + line  # Mantém o marcador
        elif line.startswith('|') and line.endswith('|'):
            # Linha de tabela
            pdf.set_font('Helvetica', '', 7)
            # Remover pipes no início e fim
            cells = [cell.strip() for cell in line.split('|') if cell.strip()]
            text = ' | '.join(cells)
            # Truncar se muito longo
            if len(text) > 150:
                text = text[:147] + '...'
        else:
            # Texto normal - pode ter negrito
            pdf.set_font('Helvetica', '', 9)
            # Se tiver **, tornar negrito mas manter o texto
            if '**' in line:
                # Remover ** mas manter o conteúdo
                text = line.replace('**', '')
                if text.strip():  # Se ainda tem conteúdo depois de remover **
                    pdf.set_font('Helvetica', 'B', 9)

        # Remover emojis
        text = re.sub(r'[\U0001F000-\U0001FFFF]+', '', text)

        # Remover outros caracteres Unicode problemáticos (setas, símbolos especiais, etc)
        text = re.sub(r'[\u2000-\u2FFF]+', '', text)  # Remove símbolos gerais e pontuação

        # Normalizar caracteres acentuados para compatibilidade com latin-1
        # Mapear caracteres problemáticos comuns
        replacements = {
            'á': 'a', 'à': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a',
            'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
            'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
            'ó': 'o', 'ò': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o',
            'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
            'ç': 'c', 'ñ': 'n',
            'Á': 'A', 'À': 'A', 'Â': 'A', 'Ã': 'A', 'Ä': 'A',
            'É': 'E', 'È': 'E', 'Ê': 'E', 'Ë': 'E',
            'Í': 'I', 'Ì': 'I', 'Î': 'I', 'Ï': 'I',
            'Ó': 'O', 'Ò': 'O', 'Ô': 'O', 'Õ': 'O', 'Ö': 'O',
            'Ú': 'U', 'Ù': 'U', 'Û': 'U', 'Ü': 'U',
            'Ç': 'C', 'Ñ': 'N',
            '"': '"', '"': '"', ''': "'", ''': "'"
        }
        for old_char, new_char in replacements.items():
            text = text.replace(old_char, new_char)

        # Pular se não tem texto após limpeza
        if not text.strip():
            continue

        # Converter para latin-1 safe (remover qualquer caractere que não seja latin-1)
        try:
            # Tentar encode/decode para verificar se é latin-1 compatível
            text = text.encode('latin-1', errors='ignore').decode('latin-1')
        except:
            # Se falhar, usar apenas ASCII
            text = text.encode('ascii', 'ignore').decode('ascii')

        if not text.strip():
            continue

        # Adicionar o texto ao PDF
        try:
            # Para linhas muito longas, quebrar em palavras
            if len(text) > 120:
                words = text.split()
                current_line = ""
                for word in words:
                    test_line = current_line + (" " if current_line else "") + word
                    if len(test_line) <= 120:
                        current_line = test_line
                    else:
                        if current_line:
                            pdf.multi_cell(0, 5, current_line, align='L')
                        current_line = word
                if current_line:
                    pdf.multi_cell(0, 5, current_line, align='L')
            else:
                pdf.multi_cell(0, 5, text, align='L')
        except Exception as e:
            # Última tentativa: remover tudo que não é ASCII básico
            try:
                text_ascii = text.encode('ascii', 'ignore').decode('ascii')
                if text_ascii.strip():
                    pdf.multi_cell(0, 5, text_ascii, align='L')
            except:
                pass  # Ignorar linha problemática

    # Retornar bytes do PDF usando dest='S' para retornar string
    # Isso evita problemas de encoding no Windows
    pdf_output = pdf.output(dest='S')
    if isinstance(pdf_output, str):
        return pdf_output.encode('latin-1')
    return bytes(pdf_output)

def get_recent_reports(limit=10):
    """Obtém relatórios recentes"""
    if not config.REPORT_DIR.exists():
        return []

    reports = list(config.REPORT_DIR.glob("*.md"))
    reports.sort(key=lambda x: x.stat().st_mtime, reverse=True)

    result = []
    for report in reports[:limit]:
        # Parse do nome do arquivo: YYYYMMDD_HHMMSS_Nome_source.md
        parts = report.stem.split('_', 3)
        if len(parts) >= 3:
            date_str = parts[0]
            time_str = parts[1]
            paciente = parts[2] if len(parts) > 2 else "Desconhecido"

            # Formatar data
            try:
                dt = datetime.strptime(f"{date_str}{time_str}", "%Y%m%d%H%M%S")
                data_formatada = dt.strftime("%d/%m/%Y %H:%M")
            except:
                data_formatada = "Data inválida"

            # Ler primeira linha do relatório para pegar o motivo
            try:
                with open(report, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Procurar por motivo
                    if "Motivo do retorno:" in content:
                        motivo = "Retorno"
                    else:
                        motivo = "Consulta"
            except:
                motivo = "N/A"

            result.append({
                'data': data_formatada,
                'paciente': paciente,
                'motivo': motivo,
                'arquivo': report.name,
                'caminho': report
            })

    return result

# Sidebar
with st.sidebar:
    logo_path = Path(__file__).parent / "badi_logo.png"
    if logo_path.exists():
        st.image(str(logo_path), width=150)
    else:
        st.write("**BadiLab**")
    st.title("🏥 Vet Docs")
    st.markdown("---")

    # Menu de navegação
    menu = st.radio(
        "Navegação",
        ["📊 Dashboard", "➕ Nova Consulta", "📋 Histórico", "⚙️ Configurações"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Estatísticas resumidas na sidebar
    stats = get_stats()
    st.metric("Relatórios Hoje", stats['relatorios_hoje'])
    st.metric("Total de Relatórios", stats['total_relatorios'])
    st.metric("Custo Hoje", f"${stats['custo_hoje']:.2f}")

    st.markdown("---")
    st.caption("v1.1 - Interface Streamlit")

# Conteúdo principal
if menu == "📊 Dashboard":
    st.markdown('<p class="main-header">🏥 Dashboard do Sistema</p>', unsafe_allow_html=True)

    # Verificar se há um relatório para visualizar
    if 'view_report' in st.session_state and st.session_state['view_report']:
        report_path = st.session_state['view_report']

        st.markdown("---")
        st.subheader(f"📄 Visualizando: {report_path.name}")

        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()
                st.markdown(content)
        except Exception as e:
            st.error(f"Erro ao ler relatório: {e}")

        if st.button("⬅️ Voltar ao Dashboard"):
            del st.session_state['view_report']
            st.rerun()

        st.markdown("---")

    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            label="📝 Consultas Hoje",
            value=stats['relatorios_hoje'],
            delta=f"+{stats['relatorios_hoje']}" if stats['relatorios_hoje'] > 0 else "0"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            label="📊 Total de Consultas",
            value=stats['total_relatorios'],
            delta=None
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            label="💰 Custo Total",
            value=f"${stats['custo_total']:.2f}",
            delta=f"-${stats['custo_hoje']:.2f} hoje" if stats['custo_hoje'] > 0 else None
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            label="⚡ Economia",
            value="95%",
            delta="vs Áudio" if stats['relatorios_hoje'] > 0 else None,
            delta_color="normal"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Últimas consultas
    st.subheader("📋 Últimas Consultas")

    recent = get_recent_reports(10)

    if recent:
        df = pd.DataFrame(recent)

        # Tabela interativa
        for idx, row in df.iterrows():
            col1, col2, col3, col4 = st.columns([2, 2, 3, 1])

            with col1:
                st.write(f"**{row['data']}**")

            with col2:
                st.write(f"🐾 {row['paciente']}")

            with col3:
                st.write(f"📝 {row['motivo']}")

            with col4:
                if st.button("Ver", key=f"view_{idx}"):
                    st.session_state['view_report'] = row['caminho']
                    st.rerun()

    else:
        st.info("Nenhuma consulta registrada ainda. Crie sua primeira consulta!")

    # Gráfico de consultas ao longo do tempo (se houver dados)
    if stats['total_relatorios'] > 0:
        st.markdown("---")
        st.subheader("📈 Estatísticas")

        col1, col2 = st.columns(2)

        with col1:
            # Gráfico de pizza - tipo de atendimento (mock data por enquanto)
            fig_pie = go.Figure(data=[go.Pie(
                labels=['Presencial', 'Videoconferência', 'Retorno'],
                values=[60, 25, 15],
                hole=.3
            )])
            fig_pie.update_layout(
                title="Tipo de Atendimento",
                height=300
            )
            st.plotly_chart(fig_pie, width='stretch')

        with col2:
            # Gráfico de barras - consultas por dia (mock data)
            dias = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
            valores = [5, 8, 6, 12, 9, 3, 2]

            fig_bar = go.Figure(data=[go.Bar(
                x=dias,
                y=valores,
                marker_color='#1f77b4'
            )])
            fig_bar.update_layout(
                title="Consultas por Dia da Semana",
                height=300,
                yaxis_title="Quantidade"
            )
            st.plotly_chart(fig_bar, width='stretch')

elif menu == "➕ Nova Consulta":
    st.markdown('<p class="main-header">➕ Nova Consulta Veterinária</p>', unsafe_allow_html=True)

    # Escolher método
    st.subheader("Escolha o método de entrada")

    tab1, tab2 = st.tabs(["🎤 Processar Áudio", "📝 Usar Transcrição"])

    with tab1:
        st.markdown("""
        <div class="info-box">
        <strong>ℹ️ Processamento de Áudio</strong><br>
        Upload de arquivo de áudio para transcrição automática com Whisper AI.<br>
        <strong>Tempo estimado:</strong> 5-10 minutos
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")

        # Upload de áudio
        audio_file = st.file_uploader(
            "Escolha o arquivo de áudio",
            type=['mp3', 'wav', 'm4a', 'ogg', 'flac'],
            help="Formatos aceitos: MP3, WAV, M4A, OGG, FLAC"
        )

        if audio_file:
            st.audio(audio_file, format=f'audio/{audio_file.name.split(".")[-1]}')
            st.success(f"✅ Arquivo carregado: {audio_file.name} ({audio_file.size / 1024:.1f} KB)")

            # Salvar arquivo temporariamente
            temp_path = config.AUDIO_DIR / audio_file.name
            with open(temp_path, 'wb') as f:
                f.write(audio_file.getbuffer())

            st.session_state['audio_path'] = temp_path
            st.session_state['processing_mode'] = 'audio'

    with tab2:
        st.markdown("""
        <div class="info-box">
        <strong>ℹ️ Transcrição Existente</strong><br>
        Cole ou digite o texto da consulta diretamente.<br>
        <strong>Tempo estimado:</strong> 30 segundos ⚡
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")

        transcription_text = st.text_area(
            "Digite ou cole a transcrição da consulta:",
            height=300,
            placeholder="Cole aqui o texto da consulta veterinária...",
            help="Você pode colar texto de qualquer fonte: transcrições manuais, de videoconferências, etc."
        )

        if transcription_text:
            char_count = len(transcription_text)
            st.caption(f"📝 {char_count} caracteres")

            if char_count > 100:
                st.success("✅ Transcrição pronta para processar!")
                st.session_state['transcription'] = transcription_text
                st.session_state['processing_mode'] = 'text'
            else:
                st.warning("⚠️ Texto muito curto. Adicione mais detalhes da consulta.")

    # Formulário de dados do paciente
    if 'audio_path' in st.session_state or 'transcription' in st.session_state:
        st.markdown("---")
        st.subheader("📋 Dados do Paciente")

        with st.form("patient_form"):
            col1, col2 = st.columns(2)

            with col1:
                paciente_nome = st.text_input("Nome do Paciente *", placeholder="Ex: Bob")
                paciente_especie = st.selectbox("Espécie *", ["Cão", "Gato", "Outro"])
                paciente_raca = st.text_input("Raça *", placeholder="Ex: Yorkshire Terrier")
                paciente_idade = st.text_input("Idade e Peso *", placeholder="Ex: 5 anos, 3.2kg")

            with col2:
                tutor_nome = st.text_input("Nome do Tutor *", placeholder="Ex: Dr. Silva")
                data_consulta = st.date_input("Data da Consulta", value=datetime.now())
                motivo_retorno = st.text_input("Motivo do Retorno/Consulta *", placeholder="Ex: Acompanhamento dermatite")
                tipo_atendimento = st.selectbox("Tipo de Atendimento", ["Presencial", "Videoconferência"])

            # Dados do Veterinário (Opcionais)
            st.markdown("---")
            st.subheader("👨‍⚕️ Dados do Veterinário (Opcional)")

            col1, col2, col3 = st.columns(3)
            with col1:
                vet_nome = st.text_input("Nome Completo do Veterinário", placeholder="Ex: Dr. João Silva")
            with col2:
                vet_crmv = st.text_input("CRMV", placeholder="Ex: CRMV-SP 12345")
            with col3:
                vet_especialidade = st.text_input("Especialidade", placeholder="Ex: Dermatologia")

            # Exame Clínico (Opcional)
            st.markdown("---")
            st.subheader("🩺 Exame Físico Geral (Opcional)")
            st.caption("💡 Preencha apenas os campos que deseja que apareçam no relatório. Campos vazios serão extraídos da transcrição.")

            col1, col2, col3 = st.columns(3)
            with col1:
                exame_temperatura = st.text_input("Temperatura", placeholder="Ex: 38.5°C", key="temp")
                exame_fc = st.text_input("Frequência Cardíaca", placeholder="Ex: 120 bpm", key="fc")
                exame_fr = st.text_input("Frequência Respiratória", placeholder="Ex: 30 mpm", key="fr")
            with col2:
                exame_tpc = st.text_input("TPC", placeholder="Ex: < 2s", key="tpc")
                exame_mucosas = st.text_input("Mucosas", placeholder="Ex: Rosadas", key="mucosas")
                exame_hidratacao = st.text_input("Hidratação", placeholder="Ex: Normal", key="hidrat")
            with col3:
                exame_linfonodos = st.text_area("Linfonodos", placeholder="Ex: Sem alterações", height=100, key="linf")

            # Medicação e Exames (Opcional)
            st.markdown("---")
            st.subheader("💊 Medicação e Exames (Opcional)")
            st.caption("💡 Preencha se quiser adicionar/substituir medicação ou exames. Campos vazios serão extraídos da transcrição.")

            medicacao_info = st.text_area(
                "Medicação Prescrita",
                placeholder="Ex:\n- Omeprazol 20mg, 1x ao dia, 7 dias\n- Probiótico, 1 sachê 2x ao dia",
                height=100,
                key="med"
            )

            exames_complementares = st.text_area(
                "Resultados de Exames",
                placeholder="Ex:\n- Hemograma: dentro da normalidade\n- Ultrassom: sem alterações",
                height=100,
                key="exames"
            )

            st.markdown("---")

            # Botões de ação
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])

            with col_btn1:
                limpar = st.form_submit_button("🗑️ Limpar Formulário", type="secondary", use_container_width=True)

            with col_btn2:
                submitted = st.form_submit_button("🚀 Gerar Relatório", type="primary", use_container_width=True)

            with col_btn3:
                pass  # Espaço para futuro botão

            if limpar:
                # Limpar session state
                keys_to_clear = ['audio_path', 'transcription', 'processing_mode', 'show_result', 'last_report']
                for key in keys_to_clear:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()

            if submitted:
                # Preparar dados do paciente
                # LÓGICA SIMPLES: Se campo preenchido → usa, se vazio → extrai da transcrição
                patient_info = {
                    'paciente_nome': paciente_nome,
                    'paciente_especie': paciente_especie,
                    'paciente_raca': paciente_raca,
                    'paciente_idade': paciente_idade,
                    'tutor_nome': tutor_nome,
                    'data_consulta': data_consulta.strftime("%d/%m/%Y"),
                    'motivo_retorno': motivo_retorno,
                    'tipo_atendimento': tipo_atendimento,
                    # Campos opcionais: se preenchido, usa; se vazio, ignora (Claude extrai da transcrição)
                    'vet_nome': vet_nome.strip() if vet_nome else '',
                    'vet_crmv': vet_crmv.strip() if vet_crmv else '',
                    'vet_especialidade': vet_especialidade.strip() if vet_especialidade else '',
                    'exame_temperatura': exame_temperatura.strip() if exame_temperatura else '',
                    'exame_fc': exame_fc.strip() if exame_fc else '',
                    'exame_fr': exame_fr.strip() if exame_fr else '',
                    'exame_tpc': exame_tpc.strip() if exame_tpc else '',
                    'exame_mucosas': exame_mucosas.strip() if exame_mucosas else '',
                    'exame_hidratacao': exame_hidratacao.strip() if exame_hidratacao else '',
                    'exame_linfonodos': exame_linfonodos.strip() if exame_linfonodos else '',
                    'medicacao_info': medicacao_info.strip() if medicacao_info else '',
                    'exames_complementares': exames_complementares.strip() if exames_complementares else ''
                }

                # Validar campos usando a função de validação
                try:
                    validate_patient_info(patient_info)
                    logging.info(f"Formulário validado para paciente: {paciente_nome}")
                except ValueError as e:
                    st.error(f"❌ {str(e)}")
                    logging.warning(f"Validação falhou: {e}")
                    patient_info = None

                if patient_info:
                    # Processar
                    with st.spinner("🔄 Processando consulta..."):
                        try:
                            # Inicializar sistema
                            if st.session_state.get('processing_mode') == 'audio':
                                system = VeterinaryTranscription(load_whisper=True)
                                report_path = system.process_consultation(
                                    st.session_state['audio_path'],
                                    patient_info
                                )
                            else:  # text
                                system = VeterinaryTranscription(load_whisper=False)
                                report_path = system.process_from_text(
                                    st.session_state['transcription'],
                                    patient_info,
                                    source_name=f"{paciente_nome}_{motivo_retorno[:20]}"
                                )

                            st.session_state['last_report'] = report_path
                            st.session_state['show_result'] = True
                            logging.info(f"Relatório gerado com sucesso: {report_path.name}")

                            # Limpar dados temporários
                            if 'audio_path' in st.session_state:
                                del st.session_state['audio_path']
                            if 'transcription' in st.session_state:
                                del st.session_state['transcription']

                            st.rerun()

                        except Exception as e:
                            logging.error(f"Erro ao processar consulta: {e}")
                            st.error(f"❌ Erro ao processar: {str(e)}")

    # Mostrar resultado
    if st.session_state.get('show_result') and st.session_state.get('last_report'):
        st.markdown("---")
        st.markdown("""
        <div class="success-box">
        <h3>✅ Relatório Gerado com Sucesso!</h3>
        </div>
        """, unsafe_allow_html=True)

        report_path = st.session_state['last_report']

        st.markdown("")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("📄 Arquivo", report_path.name)
        with col2:
            st.metric("📁 Local", "relatorios/")
        with col3:
            st.write("**⬇️ Baixar Relatório:**")

        # Botões de download em múltiplos formatos
        st.markdown("---")
        col_md, col_txt, col_pdf = st.columns(3)

        with open(report_path, 'r', encoding='utf-8') as f:
            md_content = f.read()

        with col_md:
            st.download_button(
                label="📄 Baixar MD",
                data=md_content,
                file_name=report_path.name,
                mime="text/markdown",
                width='stretch'
            )

        with col_txt:
            txt_content = convert_md_to_txt(md_content)
            txt_filename = report_path.stem + '.txt'
            st.download_button(
                label="📝 Baixar TXT",
                data=txt_content,
                file_name=txt_filename,
                mime="text/plain",
                width='stretch'
            )

        with col_pdf:
            pdf_filename = report_path.stem + '.pdf'
            pdf_bytes = convert_md_to_pdf(md_content, pdf_filename)
            st.download_button(
                label="📕 Baixar PDF",
                data=pdf_bytes,
                file_name=pdf_filename,
                mime="application/pdf",
                width='stretch'
            )

        # Preview do relatório
        st.markdown("---")
        st.subheader("📖 Preview do Relatório")

        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
            st.markdown(content)

        if st.button("➕ Nova Consulta"):
            st.session_state['show_result'] = False
            del st.session_state['last_report']
            st.rerun()

elif menu == "📋 Histórico":
    st.markdown('<p class="main-header">📋 Histórico de Consultas</p>', unsafe_allow_html=True)

    # Modo de edição
    if st.session_state.get('edit_mode') and st.session_state.get('editing_report'):
        editing_report = st.session_state['editing_report']

        st.info(f"✏️ Editando relatório: **{editing_report['paciente']}**")

        # Ler conteúdo do relatório
        with open(editing_report['caminho'], 'r', encoding='utf-8') as f:
            current_content = f.read()

        # Editor de texto
        edited_content = st.text_area(
            "Edite o conteúdo do relatório:",
            value=current_content,
            height=500,
            help="Você pode editar o relatório diretamente aqui. Use Markdown para formatação."
        )

        col_cancel, col_save = st.columns(2)

        with col_cancel:
            if st.button("❌ Cancelar", use_container_width=True):
                del st.session_state['edit_mode']
                del st.session_state['editing_report']
                st.rerun()

        with col_save:
            if st.button("💾 Salvar Alterações", type="primary", use_container_width=True):
                # Salvar alterações
                try:
                    with open(editing_report['caminho'], 'w', encoding='utf-8') as f:
                        f.write(edited_content)
                    st.success(f"✅ Relatório atualizado com sucesso!")
                    logging.info(f"Relatório editado: {editing_report['arquivo']}")
                    del st.session_state['edit_mode']
                    del st.session_state['editing_report']
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao salvar: {str(e)}")
                    logging.error(f"Erro ao salvar edição: {e}")

        st.markdown("---")
        st.subheader("📖 Preview do Relatório Editado")
        st.markdown(edited_content)

    else:
        # Modo de visualização normal
        # Filtros
        col1, col2, col3 = st.columns(3)

        with col1:
            search_term = st.text_input("🔍 Buscar", placeholder="Nome do paciente...")

        with col2:
            filter_date = st.date_input("📅 Filtrar por data", value=None)

        with col3:
            sort_by = st.selectbox("🔄 Ordenar por", ["Mais recentes", "Mais antigos", "Nome (A-Z)"])

        st.markdown("---")

        # Obter relatórios
        recent = get_recent_reports(100)  # Todos

        # Aplicar filtros
        if search_term:
            recent = [r for r in recent if search_term.lower() in r['paciente'].lower()]

        if filter_date:
            date_str = filter_date.strftime("%d/%m/%Y")
            recent = [r for r in recent if date_str in r['data']]

        # Aplicar ordenação
        if sort_by == "Mais antigos":
            recent = list(reversed(recent))
        elif sort_by == "Nome (A-Z)":
            recent = sorted(recent, key=lambda x: x['paciente'])

        # Exibir resultados
        st.write(f"**Total: {len(recent)} consulta(s)**")

        if recent:
            for idx, report in enumerate(recent):
                with st.expander(f"🐾 {report['paciente']} - {report['data']} - {report['motivo']}"):
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        st.write(f"**Data:** {report['data']}")
                        st.write(f"**Paciente:** {report['paciente']}")
                        st.write(f"**Motivo:** {report['motivo']}")
                        st.write(f"**Arquivo:** {report['arquivo']}")

                    with col2:
                        # Botão de visualizar
                        if st.button("👁️ Visualizar", key=f"view_hist_{idx}", use_container_width=True):
                            with open(report['caminho'], 'r', encoding='utf-8') as f:
                                st.markdown(f.read())

                        # Botão de editar
                        if st.button("✏️ Editar", key=f"edit_hist_{idx}", use_container_width=True):
                            # Salvar relatório para edição no session_state
                            st.session_state['editing_report'] = {
                                'caminho': report['caminho'],
                                'paciente': report['paciente'],
                                'arquivo': report['arquivo']
                            }
                            st.session_state['edit_mode'] = True
                            st.rerun()

                        st.markdown("---")

                        # Botões de download em múltiplos formatos
                        st.write("**⬇️ Baixar:**")
                        col_md_h, col_txt_h, col_pdf_h = st.columns(3)

                        with open(report['caminho'], 'r', encoding='utf-8') as f:
                            md_content_h = f.read()

                        with col_md_h:
                            st.download_button(
                                label="MD",
                                data=md_content_h,
                                file_name=report['arquivo'],
                                mime="text/markdown",
                                key=f"download_md_hist_{idx}",
                                use_container_width=True
                            )

                        with col_txt_h:
                            txt_content_h = convert_md_to_txt(md_content_h)
                            txt_filename_h = Path(report['arquivo']).stem + '.txt'
                            st.download_button(
                                label="TXT",
                                data=txt_content_h,
                                file_name=txt_filename_h,
                                mime="text/plain",
                                key=f"download_txt_hist_{idx}",
                                use_container_width=True
                            )

                        with col_pdf_h:
                            pdf_filename_h = Path(report['arquivo']).stem + '.pdf'
                            pdf_bytes_h = convert_md_to_pdf(md_content_h, pdf_filename_h)
                            st.download_button(
                                label="PDF",
                                data=pdf_bytes_h,
                                file_name=pdf_filename_h,
                                mime="application/pdf",
                                key=f"download_pdf_hist_{idx}",
                                use_container_width=True
                            )
        else:
            st.info("Nenhuma consulta encontrada com os filtros aplicados.")

elif menu == "⚙️ Configurações":
    st.markdown('<p class="main-header">⚙️ Configurações do Sistema</p>', unsafe_allow_html=True)

    # Configurações do Whisper
    st.subheader("🎤 Whisper AI")

    current_model = config.WHISPER_MODEL

    model_options = {
        "tiny": "Tiny - Mais rápido, menos preciso (39 MB)",
        "base": "Base - Rápido e preciso para produção (74 MB) ⭐",
        "small": "Small - Boa precisão (244 MB)",
        "medium": "Medium - Mais preciso, lento em CPU (769 MB)",
        "large": "Large - Máxima precisão, muito lento (1550 MB)"
    }

    selected_model = st.selectbox(
        "Modelo Whisper",
        options=list(model_options.keys()),
        format_func=lambda x: model_options[x],
        index=list(model_options.keys()).index(current_model)
    )

    st.info(f"**Modelo atual:** {current_model}")

    if selected_model != current_model:
        if st.button("💾 Salvar Configuração"):
            st.warning("⚠️ Para alterar o modelo, edite o arquivo config.py manualmente.")

    st.markdown("---")

    # Informações do sistema
    st.subheader("📊 Informações do Sistema")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Python", f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        st.metric("Streamlit", st.__version__)
        st.metric("Modelo Whisper", config.WHISPER_MODEL)

    with col2:
        st.metric("API Claude", "Configurada ✅" if config.ANTHROPIC_API_KEY else "Não configurada ❌")
        st.metric("FFmpeg", "Disponível ✅")
        st.metric("Pasta de Áudios", str(config.AUDIO_DIR))

    st.markdown("---")

    # Sobre
    st.subheader("ℹ️ Sobre")

    st.markdown("""
    **Sistema de Documentação de Consultas Veterinárias**

    - **Versão:** 1.1 (Interface Streamlit)
    - **Desenvolvido por:** BadiLab
    - **Data:** Novembro 2025

    **Funcionalidades:**
    - ✅ Transcrição automática de áudios (Whisper AI)
    - ✅ Geração de relatórios estruturados (Claude API)
    - ✅ Processamento de transcrições existentes
    - ✅ Interface gráfica moderna (Streamlit)
    - ✅ Dashboard com estatísticas
    - ✅ Histórico de consultas

    **Documentação:**
    - README.md
    - GUIA_RAPIDO.md
    - USO_TRANSCRICAO_MANUAL.md
    """)

    st.markdown("---")

    # Ações
    st.subheader("🔧 Ações")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🗑️ Limpar Cache"):
            st.cache_data.clear()
            st.success("Cache limpo!")

    with col2:
        if st.button("📁 Abrir Pasta de Relatórios"):
            try:
                # Converter Path para string e abrir pasta
                folder_path = str(config.REPORT_DIR.resolve())

                # Usar método apropriado para cada sistema operacional
                if sys.platform == 'win32':
                    os.startfile(folder_path)
                elif sys.platform == 'darwin':  # macOS
                    os.system(f'open "{folder_path}"')
                else:  # Linux
                    os.system(f'xdg-open "{folder_path}"')

                st.success(f"Pasta aberta: {folder_path}")
                logging.info(f"Pasta de relatórios aberta: {folder_path}")
            except Exception as e:
                st.error(f"Erro ao abrir pasta: {e}")
                logging.error(f"Erro ao abrir pasta de relatórios: {e}")
                # Mostrar caminho alternativo
                st.info(f"Abra manualmente: {config.REPORT_DIR}")

    with col3:
        if st.button("📚 Ver Documentação"):
            readme_path = Path(__file__).parent / "README.md"
            if readme_path.exists():
                with open(readme_path, 'r', encoding='utf-8') as f:
                    st.markdown(f.read())

# Footer
st.markdown("---")
st.caption("🏥 Sistema de Documentação Veterinária v1.1 | Desenvolvido por BadiLab | Powered by Streamlit, Whisper AI & Claude API")
