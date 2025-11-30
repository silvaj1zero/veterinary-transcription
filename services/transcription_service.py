import os
import logging
import whisper
import google.generativeai as genai
from pathlib import Path
import config
from abc import ABC, abstractmethod

class TranscriptionService(ABC):
    @abstractmethod
    def transcribe(self, audio_path: Path) -> dict:
        pass

class WhisperTranscriptionService(TranscriptionService):
    def __init__(self, model_name=config.WHISPER_MODEL):
        self.model_name = model_name
        self.model = None

    def _load_model(self):
        if self.model is None:
            logging.info(f"Carregando modelo Whisper '{self.model_name}'...")
            self.model = whisper.load_model(self.model_name)

    def transcribe(self, audio_path: Path) -> dict:
        self._load_model()
        logging.info(f"Iniciando transcrição Whisper: {audio_path.name}")
        
        try:
            result = self.model.transcribe(
                str(audio_path),
                language=config.DEFAULT_LANGUAGE,
                verbose=False,
                fp16=False,
                beam_size=1,
                best_of=1,
                temperature=0.0
            )
            return result
        except Exception as e:
            logging.error(f"Erro na transcrição Whisper: {e}")
            raise

class GeminiTranscriptionService(TranscriptionService):
    def __init__(self, api_key=config.GOOGLE_API_KEY):
        if not api_key:
            raise ValueError("GOOGLE_API_KEY não configurada")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(config.GEMINI_MODEL_FLASH)

    def transcribe(self, audio_path: Path) -> dict:
        logging.info(f"Iniciando transcrição Gemini: {audio_path.name}")
        
        try:
            # Upload do arquivo para o Gemini
            logging.info("Fazendo upload do áudio para o Gemini...")
            audio_file = genai.upload_file(path=audio_path)
            
            # Prompt para transcrição
            prompt = "Transcreva este áudio de consulta veterinária fielmente em português."
            
            response = self.model.generate_content([prompt, audio_file])
            
            # Limpeza (opcional, mas boa prática deletar arquivos da nuvem se não precisar)
            # audio_file.delete() 
            
            return {'text': response.text}
            
        except Exception as e:
            logging.error(f"Erro na transcrição Gemini: {e}")
            raise

def get_transcription_service():
    provider = config.TRANSCRIPTION_PROVIDER
    
    if provider == "google_gemini":
        logging.info("Usando provedor de transcrição: Google Gemini")
        return GeminiTranscriptionService()
    else:
        logging.info("Usando provedor de transcrição: OpenAI Whisper (Local)")
        return WhisperTranscriptionService()
