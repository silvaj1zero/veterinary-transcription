#!/usr/bin/env python3
"""
Sistema de Transcrição e Documentação de Consultas Veterinárias
Autor: BadiLab
Versão: 1.3
"""

import whisper
import anthropic
from pathlib import Path
from datetime import datetime
from tqdm import tqdm
import sys
import json
import os
from dotenv import load_dotenv
import config

# Configurar caminho do FFmpeg
os.environ['PATH'] = r'C:\Users\Zero\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0-full_build\bin;' + os.environ['PATH']

# Carregar variáveis de ambiente
load_dotenv()

class VeterinaryTranscription:
    """
    Classe principal para processamento de consultas veterinárias
    """

    def __init__(self, load_whisper=True):
        """
        Inicializa o sistema

        Args:
            load_whisper (bool): Se True, carrega o modelo Whisper.
                                 Se False, carrega apenas o cliente Anthropic
        """
        print("Inicializando sistema...")

        # Whisper será carregado sob demanda
        self.whisper_model = None
        self.load_whisper_enabled = load_whisper

        # Inicializar cliente Anthropic
        if not config.ANTHROPIC_API_KEY:
            raise ValueError("ERRO - ANTHROPIC_API_KEY não encontrada! Configure no arquivo .env")

        self.anthropic_client = anthropic.Anthropic(
            api_key=config.ANTHROPIC_API_KEY
        )
        print("OK - Cliente Anthropic inicializado!")

        # Carregar template de prompt
        self.prompt_template = self._load_prompt_template()

    def _ensure_whisper_loaded(self):
        """Carrega o modelo Whisper se ainda não estiver carregado"""
        if self.whisper_model is None:
            print(f"Carregando modelo Whisper '{config.WHISPER_MODEL}'...")
            self.whisper_model = whisper.load_model(config.WHISPER_MODEL)
            print("OK - Modelo Whisper carregado!")

    def _load_prompt_template(self):
        """Carrega o template de prompt"""
        if config.PROMPT_TEMPLATE_FILE.exists():
            with open(config.PROMPT_TEMPLATE_FILE, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise FileNotFoundError(
                f"ERRO - Template não encontrado: {config.PROMPT_TEMPLATE_FILE}"
            )

    def transcribe_audio(self, audio_path):
        """
        Transcreve áudio usando Whisper

        Args:
            audio_path (Path): Caminho do arquivo de áudio

        Returns:
            dict: Resultado da transcrição
        """
        print(f"\nTranscrevendo: {audio_path.name}")

        # Garantir que o Whisper está carregado
        self._ensure_whisper_loaded()

        result = self.whisper_model.transcribe(
            str(audio_path),
            language=config.DEFAULT_LANGUAGE,
            verbose=False
        )

        # Salvar transcrição
        transcription_file = config.TRANSCRIPTION_DIR / f"{audio_path.stem}_transcricao.txt"
        with open(transcription_file, 'w', encoding='utf-8') as f:
            f.write(result['text'])

        print(f"OK - Transcrição salva: {transcription_file.name}")

        return result

    def collect_patient_info(self):
        """
        Coleta informações do paciente de forma interativa

        Returns:
            dict: Dicionário com informações do paciente
        """
        print("\n" + "="*60)
        print("COLETA DE INFORMACOES DO PACIENTE")
        print("="*60)

        info = {
            'paciente_nome': input("Nome do paciente: ").strip(),
            'paciente_especie': input("Espécie (Cão/Gato/Outro): ").strip(),
            'paciente_raca': input("Raça: ").strip(),
            'paciente_idade': input("Idade e Peso (ex: 3 anos, 8kg): ").strip(),
            'tutor_nome': input("Nome do tutor: ").strip(),
            'data_consulta': input("Data da consulta (DD/MM/AAAA) [Enter=hoje]: ").strip(),
            'motivo_retorno': input("Motivo do retorno: ").strip(),
            'tipo_atendimento': input("Tipo (Presencial/Videoconferência): ").strip()
        }

        # Data padrão = hoje
        if not info['data_consulta']:
            info['data_consulta'] = datetime.now().strftime("%d/%m/%Y")

        return info

    def generate_report(self, transcription_text, patient_info):
        """
        Gera relatório estruturado usando Claude API

        Args:
            transcription_text (str): Texto da transcrição
            patient_info (dict): Informações do paciente

        Returns:
            str: Relatório formatado
        """
        print("\nGerando relatorio com Claude API...")

        # Montar prompt com dados do paciente
        prompt = self.prompt_template.format(
            transcricao=transcription_text,
            **patient_info
        )

        # Chamar API Claude
        try:
            message = self.anthropic_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                temperature=0.3,  # Baixa temperatura para maior consistência
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            report = message.content[0].text

            # Estatísticas de uso
            usage = message.usage
            print(f"Stats: Tokens usados: {usage.input_tokens} input, {usage.output_tokens} output")

            return report

        except Exception as e:
            print(f"ERRO - Erro ao gerar relatório: {str(e)}")
            raise

    def save_report(self, report_text, patient_name, audio_filename):
        """
        Salva o relatório em arquivo

        Args:
            report_text (str): Texto do relatório
            patient_name (str): Nome do paciente
            audio_filename (str): Nome do arquivo de áudio original
        """
        # Nome do arquivo: data_paciente_audio.md
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_patient_name = "".join(c for c in patient_name if c.isalnum() or c in (' ', '-', '_')).strip()

        report_filename = f"{timestamp}_{safe_patient_name}_{audio_filename}.md"
        report_path = config.REPORT_DIR / report_filename

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_text)

        print(f"OK - Relatório salvo: {report_path.name}")
        return report_path

    def process_consultation(self, audio_path, patient_info=None):
        """
        Processa uma consulta completa: transcrição + relatório

        Args:
            audio_path (Path): Caminho do arquivo de áudio
            patient_info (dict, optional): Informações do paciente. Se None, coleta interativamente
        """
        print("\n" + "="*60)
        print(f"PROCESSANDO CONSULTA: {audio_path.name}")
        print("="*60)

        # Passo 1: Coletar informações (se necessário)
        if patient_info is None:
            patient_info = self.collect_patient_info()

        # Passo 2: Transcrever áudio
        transcription_result = self.transcribe_audio(audio_path)

        # Passo 3: Gerar relatório
        report = self.generate_report(
            transcription_result['text'],
            patient_info
        )

        # Passo 4: Salvar relatório
        report_path = self.save_report(
            report,
            patient_info['paciente_nome'],
            audio_path.stem
        )

        print("\n" + "="*60)
        print("OK - PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
        print("="*60)
        print(f"Relatorio: {report_path}")

        return report_path

    def batch_process(self):
        """
        Processa todos os áudios na pasta audios/
        """
        audio_files = []
        for ext in config.AUDIO_EXTENSIONS:
            audio_files.extend(config.AUDIO_DIR.glob(f"*{ext}"))

        if not audio_files:
            print(f"AVISO - Nenhum áudio encontrado em {config.AUDIO_DIR}")
            return

        print(f"\nEncontrados {len(audio_files)} arquivo(s) de audio")

        for audio_file in audio_files:
            try:
                self.process_consultation(audio_file)
            except Exception as e:
                print(f"ERRO - Erro ao processar {audio_file.name}: {str(e)}")
                continue

    def process_from_text(self, transcription_text, patient_info=None, source_name="transcrição_manual"):
        """
        Processa relatório a partir de texto de transcrição já existente

        Args:
            transcription_text (str): Texto da transcrição
            patient_info (dict, optional): Informações do paciente. Se None, coleta interativamente
            source_name (str): Nome de referência para o arquivo
        """
        print("\n" + "="*60)
        print("PROCESSANDO TRANSCRICAO EXISTENTE")
        print("="*60)

        # Passo 1: Coletar informações (se necessário)
        if patient_info is None:
            patient_info = self.collect_patient_info()

        # Passo 2: Salvar transcrição fornecida
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        transcription_file = config.TRANSCRIPTION_DIR / f"{timestamp}_{source_name}_transcricao.txt"
        with open(transcription_file, 'w', encoding='utf-8') as f:
            f.write(transcription_text)
        print(f"OK - Transcrição salva: {transcription_file.name}")

        # Passo 3: Gerar relatório
        report = self.generate_report(
            transcription_text,
            patient_info
        )

        # Passo 4: Salvar relatório
        report_path = self.save_report(
            report,
            patient_info['paciente_nome'],
            source_name
        )

        print("\n" + "="*60)
        print("OK - PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
        print("="*60)
        print(f"Relatorio: {report_path}")

        return report_path

    def get_transcription_from_user(self):
        """
        Obtém texto de transcrição do usuário
        Permite colar texto ou ler de arquivo
        """
        print("\n" + "="*60)
        print("FORNECER TRANSCRICAO")
        print("="*60)
        print("\nEscolha como fornecer a transcrição:")
        print("1. Colar/digitar o texto diretamente")
        print("2. Ler de um arquivo .txt")
        print("3. Voltar")

        choice = input("\nEscolha uma opção (1-3): ").strip()

        if choice == "1":
            print("\n" + "-"*60)
            print("Digite ou cole o texto da transcrição abaixo.")
            print("Quando terminar, digite 'FIM' em uma nova linha e pressione Enter:")
            print("-"*60 + "\n")

            lines = []
            while True:
                line = input()
                if line.strip().upper() == "FIM":
                    break
                lines.append(line)

            transcription = "\n".join(lines)

            if not transcription.strip():
                print("\nERRO - Nenhum texto fornecido!")
                return None

            print(f"\nOK - Transcrição capturada ({len(transcription)} caracteres)")
            return transcription

        elif choice == "2":
            # Listar arquivos .txt disponíveis
            txt_files = list(config.TRANSCRIPTION_DIR.glob("*.txt"))

            if not txt_files:
                # Procurar em outras pastas
                print("\nProcurando arquivos .txt...")
                txt_files = list(Path.cwd().glob("*.txt"))

            if not txt_files:
                print("\nAVISO - Nenhum arquivo .txt encontrado")
                file_path = input("\nDigite o caminho completo do arquivo: ").strip()
                if not file_path:
                    return None
                txt_files = [Path(file_path)]

            print("\nArquivos disponíveis:")
            for idx, file in enumerate(txt_files, 1):
                print(f"{idx}. {file.name}")

            try:
                file_choice = int(input("\nEscolha o número do arquivo: ")) - 1
                selected_file = txt_files[file_choice]

                with open(selected_file, 'r', encoding='utf-8') as f:
                    transcription = f.read()

                print(f"\nOK - Arquivo lido: {selected_file.name} ({len(transcription)} caracteres)")
                return transcription

            except (ValueError, IndexError) as e:
                print(f"\nERRO - Seleção inválida: {e}")
                return None
            except Exception as e:
                print(f"\nERRO - Erro ao ler arquivo: {e}")
                return None

        elif choice == "3":
            return None

        else:
            print("\nERRO - Opção inválida!")
            return None

def main():
    """Função principal"""
    print("""
===============================================================
   SISTEMA DE DOCUMENTACAO DE CONSULTAS VETERINARIAS
              BadiLab - 2025
===============================================================
    """)

    try:
        # Inicializar sistema
        system = VeterinaryTranscription()

        # Menu de opções
        print("\nOpções:")
        print("1. Processar arquivo de áudio específico")
        print("2. Processar todos os arquivos na pasta audios/")
        print("3. Usar transcrição existente (texto já disponível)")
        print("4. Sair")

        choice = input("\nEscolha uma opção (1-4): ").strip()

        if choice == "1":
            # Listar arquivos disponíveis
            audio_files = []
            for ext in config.AUDIO_EXTENSIONS:
                audio_files.extend(config.AUDIO_DIR.glob(f"*{ext}"))

            if not audio_files:
                print(f"\nAVISO - Nenhum áudio encontrado em {config.AUDIO_DIR}")
                print(f"   Coloque seus arquivos de áudio na pasta: {config.AUDIO_DIR.absolute()}")
                return

            print("\nArquivos disponíveis:")
            for idx, file in enumerate(audio_files, 1):
                print(f"{idx}. {file.name}")

            file_choice = int(input("\nEscolha o número do arquivo: ")) - 1
            selected_file = audio_files[file_choice]

            system.process_consultation(selected_file)

        elif choice == "2":
            system.batch_process()

        elif choice == "3":
            # Opção de usar transcrição existente
            transcription = system.get_transcription_from_user()

            if transcription:
                system.process_from_text(transcription)
            else:
                print("\nAVISO - Operação cancelada")

        elif choice == "4":
            print("\nAte logo!")
            return
        else:
            print("\nERRO - Opção inválida!")

    except KeyboardInterrupt:
        print("\n\nAVISO - Operação cancelada pelo usuário")
    except Exception as e:
        print(f"\nERRO - Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
