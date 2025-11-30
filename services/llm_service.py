import logging
import anthropic
import google.generativeai as genai
import config
from abc import ABC, abstractmethod
from utils import retry_with_backoff

class LLMService(ABC):
    @abstractmethod
    def generate_report(self, prompt: str, system_prompt: str = None) -> str:
        pass

class ClaudeLLMService(LLMService):
    def __init__(self, api_key=config.ANTHROPIC_API_KEY):
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY não configurada")
        self.client = anthropic.Anthropic(api_key=api_key)

    @retry_with_backoff(max_retries=3)
    def generate_report(self, prompt: str, system_prompt: str = None) -> str:
        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514", # Usando o modelo definido no código original
                max_tokens=4000,
                temperature=0.3,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return message.content[0].text
        except Exception as e:
            logging.error(f"Erro Claude API: {e}")
            raise

class GeminiLLMService(LLMService):
    def __init__(self, api_key=config.GOOGLE_API_KEY):
        if not api_key:
            raise ValueError("GOOGLE_API_KEY não configurada")
        genai.configure(api_key=api_key)
        # Usando Pro para melhor raciocínio na geração de relatórios
        self.model = genai.GenerativeModel(config.GEMINI_MODEL_PRO) 

    @retry_with_backoff(max_retries=3)
    def generate_report(self, prompt: str, system_prompt: str = None) -> str:
        try:
            # Gemini não usa system prompt separado da mesma forma que Claude em chamadas simples,
            # mas podemos concatenar ou usar config se necessário. Aqui vamos direto.
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logging.error(f"Erro Gemini API: {e}")
            raise

def get_llm_service():
    provider = config.LLM_PROVIDER
    
    if provider == "google_gemini":
        logging.info("Usando provedor LLM: Google Gemini")
        return GeminiLLMService()
    else:
        logging.info("Usando provedor LLM: Anthropic Claude")
        return ClaudeLLMService()
