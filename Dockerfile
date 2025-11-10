# Dockerfile para Sistema de Documentação Veterinária
# Baseado em Python 3.11 com FFmpeg

FROM python:3.11-slim

# Metadados
LABEL maintainer="BadiLab"
LABEL description="Sistema de Transcrição e Documentação de Consultas Veterinárias"
LABEL version="1.2"

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de dependências
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretórios necessários
RUN mkdir -p audios transcricoes relatorios templates logs

# Expor porta para Streamlit
EXPOSE 8501

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Comando padrão: interface web Streamlit
# Use shell form to support environment variable substitution
CMD streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0
