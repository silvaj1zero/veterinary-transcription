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

# Carregar variáveis de ambiente IMEDIATAMENTE antes de qualquer import local
load_dotenv()

import json
import re

# Import new modular services
from services import StatsService, ReportService
from converters import convert_md_to_txt
from pdf_converter import convert_md_to_pdf
import anthropic
import config

# Seleção dinâmica do provedor de autenticação
# Agora config.DATABASE_PROVIDER terá o valor correto pois load_dotenv já rodou
if config.DATABASE_PROVIDER == "supabase":
    try:
        from auth_supabase import SupabaseAuthManager as AuthManager
        logging.info("🔄 Usando Supabase para autenticação")
    except ImportError as e:
        logging.error(f"Erro ao importar SupabaseAuthManager: {e}. Revertendo para SQLite.")
        from auth import AuthManager
else:
    from auth import AuthManager
    logging.info("🔄 Usando SQLite para autenticação")

from auth_ui import show_login_page, show_user_menu, show_user_management, show_change_password

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

# Initialize services
@st.cache_resource
def get_stats_service():
    """Get cached stats service instance"""
    return StatsService(config.REPORT_DIR)

@st.cache_resource
def get_report_service():
    """Get cached report service instance"""
    return ReportService(config.REPORT_DIR)

# Funções auxiliares
@st.cache_data(ttl=60)  # Cache for 60 seconds
def get_stats():
    """Obtém estatísticas do sistema (cached)"""
    stats_service = get_stats_service()
    return stats_service.get_stats()

@st.cache_data(ttl=30, show_spinner=False)  # Cache for 30 seconds
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


# ==================== AUTHENTICATION ====================
# Inicializar sistema de autenticação
auth_manager = AuthManager()

# Verificar autenticação
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
    st.session_state['user'] = None

# Se não estiver autenticado, mostrar página de login
if not st.session_state['authenticated']:
    show_login_page(auth_manager)
    st.stop()

# Usuário autenticado - continuar com a aplicação
current_user = st.session_state['user']
# ========================================================

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
    menu_options = ["📊 Dashboard", "➕ Nova Consulta", "📋 Histórico", "⚙️ Configurações"]
    
    # Adicionar opção de gerenciamento de usuários para admins
    if current_user['role'] == 'admin':
        menu_options.append("👥 Usuários")
    
    menu = st.radio(
        "Navegação",
        menu_options,
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Estatísticas resumidas na sidebar
    stats = get_stats()
    st.metric("Relatórios Hoje", stats['relatorios_hoje'])
    st.metric("Total de Relatórios", stats['total_relatorios'])
    st.metric("Custo Hoje", f"${stats['custo_hoje']:.2f}")

    # Informações do usuário e botão de logout
    show_user_menu(current_user)
    
    st.markdown("---")
    st.caption("v1.8 - Auth + Supabase Ready")

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

    # Botão de Limpar Tudo (fora do formulário, no topo)
    col_header1, col_header2 = st.columns([4, 1])
    with col_header2:
        if st.button("🗑️ Limpar Tudo", use_container_width=True, type="secondary"):
            # Limpar session state
            keys_to_clear = ['audio_path', 'transcription', 'processing_mode', 'show_result', 'last_report',
                           'tutor_summary', 'tutor_summary_path', 'last_patient_info']
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

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
        <strong>ℹ️ Transcrição Existente (Modo Rápido)</strong><br>
        Cole ou digite o texto da consulta diretamente.<br>
        <strong>Tempo estimado:</strong> 30 segundos ⚡<br>
        <strong>Economia:</strong> 70% mais rápido | 37% mais barato
        </div>
        """, unsafe_allow_html=True)

        # Apps recomendados
        with st.expander("📱 Apps de Transcrição Recomendados (Clique para ver)"):
            col_android, col_ios = st.columns(2)

            with col_android:
                st.markdown("""
                **🤖 Android**

                **⭐ Google Recorder** (Recomendado)
                - ✅ Grátis e offline
                - ✅ Excelente precisão
                - ✅ Tempo real
                - 📲 Disponível em Pixels

                **Otter.ai**
                - ✅ 600 min/mês grátis
                - ⚠️ Requer internet
                - ✅ Boa precisão
                """)

            with col_ios:
                st.markdown("""
                **🍎 iOS**

                **⭐ Notas de Voz** (Recomendado)
                - ✅ Grátis (iOS 17+)
                - ✅ Offline
                - ✅ Excelente precisão
                - 🔒 Privacidade total

                **Just Press Record**
                - 💰 R$ 24,90 (única vez)
                - ✅ Tempo real
                - ✅ Offline
                """)


            st.info("💡 **Dica:** Grave a consulta no smartphone e cole o texto aqui. Muito mais rápido!")

        st.markdown("")

        # Upload de arquivo de texto com drag and drop
        text_file = st.file_uploader(
            "Arraste e solte o arquivo de texto aqui",
            type=['txt'],
            help="Formatos aceitos: TXT",
            key="text_file_uploader"
        )

        # Inicializar texto da transcrição
        initial_text = ""
        
        if text_file:
            try:
                # Ler conteúdo do arquivo
                initial_text = text_file.read().decode('utf-8')
                st.success(f"✅ Arquivo carregado: {text_file.name} ({len(initial_text)} caracteres)")
            except Exception as e:
                st.error(f"❌ Erro ao ler arquivo: {e}")
                initial_text = ""

        transcription_text = st.text_area(
            "Digite ou cole a transcrição da consulta:",
            value=initial_text,
            height=300,
            placeholder="Cole aqui o texto da consulta veterinária...\n\nVocê pode usar:\n- Google Recorder (Android)\n- iOS Notas de Voz\n- Zoom/Google Meet (transcrição de videoconferência)\n- Ou digitar manualmente\n- Ou arrastar um arquivo .txt acima",
            help="Transcreva no smartphone durante a consulta e cole aqui. 70% mais rápido que processar áudio!"
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
            st.caption("💡 **Campos únicos:** Se preenchido, substitui o da transcrição. Se vazio, extrai da transcrição.")

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
            st.caption("💡 **Mesclagem inteligente:** Mesmo medicamento/exame → substitui. Adicional → mantém ambos (transcrição + preenchido).")

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

            # Botão de ação
            submitted = st.form_submit_button("🚀 Gerar Relatório Médico Completo", type="primary", use_container_width=True)

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
                            # Verificar API key antes de processar
                            if not config.ANTHROPIC_API_KEY:
                                st.error("❌ Erro: ANTHROPIC_API_KEY não configurada no arquivo .env")
                                logging.error("ANTHROPIC_API_KEY não encontrada")
                                patient_info = None
                            else:
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
                                st.session_state['last_patient_info'] = patient_info  # Salvar para usar no resumo
                                st.session_state['show_result'] = True
                                logging.info(f"Relatório gerado com sucesso: {report_path.name}")

                                # Limpar dados temporários
                                if 'audio_path' in st.session_state:
                                    del st.session_state['audio_path']
                                if 'transcription' in st.session_state:
                                    del st.session_state['transcription']

                                st.rerun()

                        except anthropic.RateLimitError as e:
                            error_msg = "Limite de requisições da API excedido. Por favor, aguarde alguns minutos antes de tentar novamente."
                            logging.error(f"Rate limit error: {e}")
                            st.error(f"❌ {error_msg}")
                        except anthropic.APIConnectionError as e:
                            error_msg = "Erro de conexão com a API Claude. Verifique sua conexão com a internet."
                            logging.error(f"API connection error: {e}")
                            st.error(f"❌ {error_msg}")
                        except anthropic.AuthenticationError as e:
                            error_msg = "Erro de autenticação. Verifique se sua ANTHROPIC_API_KEY está correta no arquivo .env"
                            logging.error(f"Authentication error: {e}")
                            st.error(f"❌ {error_msg}")
                        except FileNotFoundError as e:
                            error_msg = f"Arquivo não encontrado: {str(e)}"
                            logging.error(f"File not found: {e}")
                            st.error(f"❌ {error_msg}")
                        except ValueError as e:
                            error_msg = f"Erro de validação: {str(e)}"
                            logging.error(f"Validation error: {e}")
                            st.error(f"❌ {error_msg}")
                        except Exception as e:
                            error_msg = f"Erro inesperado ao processar: {str(e)}"
                            logging.error(f"Unexpected error processing consultation: {e}", exc_info=True)
                            st.error(f"❌ {error_msg}")
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
                use_container_width=True
            )

        with col_txt:
            txt_content = convert_md_to_txt(md_content)
            txt_filename = report_path.stem + '.txt'
            st.download_button(
                label="📝 Baixar TXT",
                data=txt_content,
                file_name=txt_filename,
                mime="text/plain",
                use_container_width=True
            )

        with col_pdf:
            pdf_filename = report_path.stem + '.pdf'
            pdf_bytes = convert_md_to_pdf(md_content, pdf_filename)
            st.download_button(
                label="📕 Baixar PDF",
                data=pdf_bytes,
                file_name=pdf_filename,
                mime="application/pdf",
                use_container_width=True
            )

        # Botão para gerar resumo para o tutor
        st.markdown("---")
        st.subheader("💬 Resumo para o Tutor")

        if 'tutor_summary' not in st.session_state:
            st.info("📱 **Novo:** Gere uma versão simplificada deste relatório para enviar ao tutor!")

            if st.button("✨ Gerar Resumo para o Tutor", type="primary", use_container_width=True):
                with st.spinner("🔄 Gerando resumo simplificado para o tutor..."):
                    try:
                        # Ler relatório completo
                        with open(report_path, 'r', encoding='utf-8') as f:
                            full_report = f.read()

                        # Inicializar sistema
                        system = VeterinaryTranscription(load_whisper=False)

                        # Recuperar patient_info do session_state
                        patient_info = st.session_state.get('last_patient_info', {})

                        # Gerar resumo
                        summary = system.generate_tutor_summary(full_report, patient_info)

                        # Salvar no session_state
                        st.session_state['tutor_summary'] = summary

                        # Salvar arquivo
                        summary_filename = report_path.stem + '_resumo_tutor.md'
                        summary_path = config.REPORT_DIR / summary_filename
                        with open(summary_path, 'w', encoding='utf-8') as f:
                            f.write(summary)

                        st.session_state['tutor_summary_path'] = summary_path
                        logging.info(f"Resumo para tutor gerado: {summary_filename}")

                        st.rerun()

                    except Exception as e:
                        st.error(f"❌ Erro ao gerar resumo: {str(e)}")
                        logging.error(f"Erro ao gerar resumo para tutor: {e}")
        else:
            # Mostrar resumo gerado
            st.success("✅ Resumo para o Tutor gerado com sucesso!")

            # Botões de download do resumo
            col_sum_md, col_sum_txt, col_sum_pdf = st.columns(3)

            summary_content = st.session_state['tutor_summary']
            summary_path = st.session_state.get('tutor_summary_path', report_path)

            with col_sum_md:
                st.download_button(
                    label="📄 Baixar Resumo MD",
                    data=summary_content,
                    file_name=f"{report_path.stem}_resumo_tutor.md",
                    mime="text/markdown",
                    use_container_width=True
                )

            with col_sum_txt:
                txt_summary = convert_md_to_txt(summary_content)
                st.download_button(
                    label="📝 Baixar Resumo TXT",
                    data=txt_summary,
                    file_name=f"{report_path.stem}_resumo_tutor.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            with col_sum_pdf:
                pdf_summary = convert_md_to_pdf(summary_content, f"{report_path.stem}_resumo_tutor.pdf")
                st.download_button(
                    label="📕 Baixar Resumo PDF",
                    data=pdf_summary,
                    file_name=f"{report_path.stem}_resumo_tutor.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

            # Preview do resumo
            st.markdown("---")
            st.subheader("📱 Preview do Resumo para o Tutor")
            st.markdown(summary_content)

        # Preview do relatório completo
        st.markdown("---")
        st.subheader("📖 Relatório Médico Completo (para prontuário)")

        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
            with st.expander("📄 Ver Relatório Completo", expanded=False):
                st.markdown(content)

        if st.button("➕ Nova Consulta"):
            st.session_state['show_result'] = False
            if 'last_report' in st.session_state:
                del st.session_state['last_report']
            if 'tutor_summary' in st.session_state:
                del st.session_state['tutor_summary']
            if 'tutor_summary_path' in st.session_state:
                del st.session_state['tutor_summary_path']
            if 'last_patient_info' in st.session_state:
                del st.session_state['last_patient_info']
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

elif menu == "👥 Usuários":
    show_user_management(auth_manager, current_user)


    # Configurações de Provedores (Admin)
    st.subheader("🛠️ Configuração de Provedores (Admin)")
    
    col_prov1, col_prov2 = st.columns(2)
    
    with col_prov1:
        transcription_options = {
            "openai_whisper": "OpenAI Whisper (Local)",
            "google_gemini": "Google Gemini (Nuvem)"
        }
        
        selected_transcription = st.selectbox(
            "Provedor de Transcrição",
            options=list(transcription_options.keys()),
            format_func=lambda x: transcription_options[x],
            index=list(transcription_options.keys()).index(config.TRANSCRIPTION_PROVIDER)
        )
        
        if selected_transcription != config.TRANSCRIPTION_PROVIDER:
            config.TRANSCRIPTION_PROVIDER = selected_transcription
            st.success(f"✅ Provedor de Transcrição alterado para: {transcription_options[selected_transcription]}")
            # Limpar cache para forçar recarregamento de serviços se necessário
            st.cache_resource.clear()

    with col_prov2:
        llm_options = {
            "anthropic_claude": "Anthropic Claude (Sonnet)",
            "google_gemini": "Google Gemini (Pro)"
        }
        
        selected_llm = st.selectbox(
            "Provedor de IA (LLM)",
            options=list(llm_options.keys()),
            format_func=lambda x: llm_options[x],
            index=list(llm_options.keys()).index(config.LLM_PROVIDER)
        )
        
        if selected_llm != config.LLM_PROVIDER:
            config.LLM_PROVIDER = selected_llm
            st.success(f"✅ Provedor de IA alterado para: {llm_options[selected_llm]}")
            # Limpar cache para forçar recarregamento de serviços se necessário
            st.cache_resource.clear()

    st.markdown("---")

    # Configurações do Whisper
    st.subheader("🎤 Configuração Whisper (se usado)")

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
            st.warning("⚠️ Para alterar o modelo permanentemente, edite o arquivo config.py ou .env.")

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

    - **Versão:** 1.6 - Resumo para Tutor & UX
    - **Desenvolvido por:** BadiLab
    - **Data:** Novembro 2025

    **Funcionalidades:**
    - ✅ Transcrição automática de áudios (Whisper AI)
    - ✅ Geração de relatórios estruturados (Claude API)
    - ✅ **NOVO:** Resumo para o Tutor (linguagem acessível)
    - ✅ **NOVO:** Botão Limpar Tudo (reinício rápido)
    - ✅ Processamento de transcrições existentes (Fast Mode)
    - ✅ Interface gráfica moderna (Streamlit)
    - ✅ Dashboard com estatísticas (cached)
    - ✅ Histórico de consultas
    - ✅ Edição de relatórios gerados
    - ✅ Campos opcionais com mesclagem inteligente
    - ✅ Exportação PDF com Unicode completo
    - ✅ Arquitetura modular e testável

    **Changelog v1.6:**
    - 💬 **Resumo para Tutor:** Versão simplificada do relatório em linguagem coloquial
    - 🗑️ **Limpar Tudo:** Botão para reiniciar entrada de dados rapidamente
    - 📋 **2 Documentos:** Relatório técnico (prontuário) + Resumo (tutor)
    - 🎨 **UX Melhorada:** Interface reorganizada com foco em produtividade

    **Changelog v1.5:**
    - 📱 **Modo Transcrição Pronta:** Interface melhorada com apps recomendados
    - 📊 **Economia:** 70% mais rápido, 37% mais barato que áudio
    - 📚 **Documentação:** Guia completo de apps Android/iOS

    **Changelog v1.4:**
    - 🎨 **PDF Unicode:** Suporte completo a acentos portugueses (á, ã, ç)
    - ⚡ **Performance:** Cache de estatísticas e relatórios (10x mais rápido)
    - 🏗️ **Arquitetura:** Módulos separados (services/, converters.py, pdf_converter.py)
    - 🐛 **Erros:** Tratamento específico (RateLimitError, APIConnectionError, etc.)
    - 🔒 **Segurança:** Validação de API key antes de processar
    - ⬆️ **Dependências:** Streamlit 1.41.1, pandas 2.2.3, anthropic 0.48.0

    **Documentação:**
    - README.md
    - RESUMO_VERSOES_1.3_a_1.6.md (NOVO)
    - CHANGELOG_v1.6.md (NOVO)
    - UPGRADE_GUIDE.md
    - GUIA_RAPIDO.md
    - USO_TRANSCRICAO_MANUAL.md
    - OTIMIZACOES_WHISPER.md
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
st.caption("🏥 Sistema de Documentação Veterinária v1.8 | Desenvolvido por BadiLab | Powered by Streamlit, Whisper AI & Claude API")
