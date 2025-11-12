#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface Gráfica do Sistema de Documentação Veterinária
VERSÃO STREAMLIT CLOUD (sem Whisper)
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

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Importar configurações
import config

# AVISO: Whisper não funciona no Streamlit Cloud!
WHISPER_AVAILABLE = False

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
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        border: 1px solid #ffc107;
        color: #856404;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# AVISO IMPORTANTE
st.markdown("""
<div class="warning-box">
⚠️ <strong>ATENÇÃO:</strong> Esta é a versão do Streamlit Cloud.<br>
A funcionalidade de <strong>transcrição de áudio</strong> não está disponível aqui.<br>
Use apenas a opção <strong>"📝 Usar Transcrição"</strong> (colar texto).
</div>
""", unsafe_allow_html=True)

# Importar funções do app.py original
from app import (
    convert_md_to_txt,
    convert_md_to_pdf,
    get_recent_reports,
    get_stats
)

# Sidebar
with st.sidebar:
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
    st.caption("v1.2 - Streamlit Cloud")

# Conteúdo principal - adaptar apenas a parte de Nova Consulta
if menu == "➕ Nova Consulta":
    st.markdown('<p class="main-header">➕ Nova Consulta Veterinária</p>', unsafe_allow_html=True)

    # APENAS tab de transcrição manual
    st.markdown("""
    <div class="info-box">
    <strong>📝 Transcrição Manual</strong><br>
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
        else:
            st.warning("⚠️ Texto muito curto. Adicione mais detalhes da consulta.")

    # Formulário de dados do paciente (resto do código igual ao app.py)
    # ... [copiar o resto do código do app.py]

else:
    # Para outros menus, importar diretamente do app.py
    st.info("Esta seção usa o código original do app.py")

st.markdown("---")
st.caption("🏥 Sistema de Documentação Veterinária v1.2 | Streamlit Cloud Version")
