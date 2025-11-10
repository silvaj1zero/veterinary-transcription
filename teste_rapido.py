#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste rápido do sistema
Demonstra a funcionalidade de transcrição existente
"""

import os
import sys
import io
from pathlib import Path
from dotenv import load_dotenv

# Configurar encoding UTF-8 para saída
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configurar caminho do FFmpeg
os.environ['PATH'] = r'C:\Users\Zero\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0-full_build\bin;' + os.environ['PATH']

# Carregar variáveis de ambiente
load_dotenv()

# Importar sistema
from transcribe_consult import VeterinaryTranscription

def teste_transcricao_existente():
    """
    Teste da funcionalidade de transcrição existente
    """
    print("="*70)
    print("TESTE RAPIDO DO SYSTEM - v1.1")
    print("="*70)
    print("\nTestando funcionalidade: Processar transcricao existente\n")

    # Ler arquivo de exemplo
    exemplo_path = Path("exemplo_transcricao.txt")

    if not exemplo_path.exists():
        print("[ERRO] Arquivo de exemplo nao encontrado!")
        return

    with open(exemplo_path, 'r', encoding='utf-8') as f:
        transcricao = f.read()

    print(f"[OK] Transcricao de exemplo carregada ({len(transcricao)} caracteres)\n")

    # Dados do paciente para teste
    patient_info = {
        'paciente_nome': 'Bob',
        'paciente_especie': 'Cão',
        'paciente_raca': 'Yorkshire Terrier',
        'paciente_idade': '5 anos, 3.2kg',
        'tutor_nome': 'Dr. Silva',
        'data_consulta': '09/11/2025',
        'motivo_retorno': 'Acompanhamento dermatite alérgica',
        'tipo_atendimento': 'Presencial'
    }

    print("Dados do paciente:")
    for key, value in patient_info.items():
        print(f"   {key}: {value}")

    print("\n" + "-"*70)

    # Inicializar sistema (sem carregar Whisper para ser mais rápido)
    print("\nInicializando sistema (modo rapido - sem Whisper)...")
    system = VeterinaryTranscription(load_whisper=False)

    # Processar transcrição
    print("\nProcessando transcricao...\n")
    report_path = system.process_from_text(
        transcricao,
        patient_info,
        source_name="teste_exemplo"
    )

    print("\n" + "="*70)
    print("[SUCESSO] TESTE CONCLUIDO!")
    print("="*70)
    print(f"\nRelatorio gerado: {report_path}")
    print(f"Localizacao: {report_path.absolute()}")

    # Mostrar preview do relatório
    print("\n" + "-"*70)
    print("PREVIEW DO RELATORIO (primeiras linhas):")
    print("-"*70 + "\n")

    with open(report_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()[:25]  # Primeiras 25 linhas
        print(''.join(lines))
        if len(f.readlines()) > 25:
            print("\n[... continua ...]\n")

    print("-"*70)
    print(f"\nAbra o arquivo completo em: {report_path.name}")
    print("\nSistema funcionando perfeitamente!\n")

if __name__ == "__main__":
    try:
        teste_transcricao_existente()
    except Exception as e:
        print(f"\n[ERRO] Erro durante o teste: {str(e)}")
        import traceback
        traceback.print_exc()
