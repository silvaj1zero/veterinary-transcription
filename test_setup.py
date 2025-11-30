#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para testar se o ambiente está configurado corretamente"""

import sys
import os

def test_environment():
    print("=" * 50)
    print("TESTE DE CONFIGURACAO DO AMBIENTE")
    print("=" * 50)

    # Versão do Python
    print(f"\n[OK] Python Version: {sys.version}")
    print(f"[OK] Python Path: {sys.executable}")

    # Testar imports das principais bibliotecas
    print("\n--- Testando Imports ---")

    try:
        import whisper
        print("[OK] openai-whisper instalado")
    except ImportError as e:
        print(f"[ERRO] openai-whisper: {e}")

    try:
        import anthropic
        print("[OK] anthropic instalado")
    except ImportError as e:
        print(f"[ERRO] anthropic: {e}")

    try:
        import streamlit
        print("[OK] streamlit instalado")
    except ImportError as e:
        print(f"[ERRO] streamlit: {e}")

    try:
        import pandas
        print("[OK] pandas instalado")
    except ImportError as e:
        print(f"[ERRO] pandas: {e}")

    try:
        import plotly
        print("[OK] plotly instalado")
    except ImportError as e:
        print(f"[ERRO] plotly: {e}")

    try:
        from fpdf import FPDF
        print("[OK] fpdf2 instalado")
    except ImportError as e:
        print(f"[ERRO] fpdf2: {e}")

    # Verificar arquivo .env
    print("\n--- Verificando Configuracoes ---")
    if os.path.exists('.env'):
        print("[OK] Arquivo .env encontrado")
    else:
        print("[AVISO] Arquivo .env nao encontrado - voce precisara criar um com suas API keys")

    print("\n" + "=" * 50)
    print("TESTE CONCLUÍDO!")
    print("=" * 50)

if __name__ == "__main__":
    test_environment()
