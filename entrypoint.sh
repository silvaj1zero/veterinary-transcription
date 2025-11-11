#!/bin/bash
set -e

echo "======================================"
echo "Sistema de Transcrição Veterinária"
echo "======================================"

# Verificar variáveis de ambiente
echo "📋 Verificando configuração..."
echo "PORT: ${PORT:-8501}"
echo "ANTHROPIC_API_KEY: $([ -n "$ANTHROPIC_API_KEY" ] && echo "✅ Configurada" || echo "❌ Não configurada")"

# Criar diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p /app/audios /app/transcricoes /app/relatorios /app/templates /app/logs
echo "✅ Diretórios criados"

# Verificar dependências
echo "🔍 Verificando dependências..."
python3 -c "import whisper; import anthropic; import streamlit; print('✅ Dependências OK')"

# Configurar porta
export STREAMLIT_SERVER_PORT="${PORT:-8501}"
export STREAMLIT_SERVER_ADDRESS="0.0.0.0"
export STREAMLIT_SERVER_HEADLESS="true"
export STREAMLIT_BROWSER_GATHER_USAGE_STATS="false"

echo "🚀 Iniciando Streamlit..."
echo "Porta: $STREAMLIT_SERVER_PORT"
echo "Endereço: $STREAMLIT_SERVER_ADDRESS"
echo "======================================"

# Iniciar Streamlit com logs detalhados
exec streamlit run app.py \
  --server.port=$STREAMLIT_SERVER_PORT \
  --server.address=$STREAMLIT_SERVER_ADDRESS \
  --server.headless=true \
  --browser.gatherUsageStats=false \
  --logger.level=info
