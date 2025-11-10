# Script para iniciar o Sistema de Documentação Veterinária
# PowerShell Script

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "  Sistema de Documentação Veterinária v1.2" -ForegroundColor Cyan
Write-Host "  BadiLab - 2025" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se Python está instalado
Write-Host "Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python não encontrado!" -ForegroundColor Red
    Write-Host "Por favor, instale Python 3.8+ de: https://www.python.org/downloads/" -ForegroundColor Red
    pause
    exit 1
}

Write-Host ""

# Verificar se dependências estão instaladas
Write-Host "Verificando dependências..." -ForegroundColor Yellow
$modules = @("streamlit", "anthropic", "whisper", "pandas", "plotly")
$missingModules = @()

foreach ($module in $modules) {
    $installed = python -c "import $module" 2>&1
    if ($LASTEXITCODE -ne 0) {
        $missingModules += $module
    }
}

if ($missingModules.Count -gt 0) {
    Write-Host "✗ Dependências faltando: $($missingModules -join ', ')" -ForegroundColor Yellow
    Write-Host ""
    $install = Read-Host "Deseja instalar as dependências agora? (s/n)"

    if ($install -eq 's' -or $install -eq 'S') {
        Write-Host "Instalando dependências..." -ForegroundColor Yellow
        pip install -r requirements.txt

        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Dependências instaladas com sucesso!" -ForegroundColor Green
        } else {
            Write-Host "✗ Erro ao instalar dependências!" -ForegroundColor Red
            pause
            exit 1
        }
    } else {
        Write-Host "Instalação cancelada. Execute manualmente:" -ForegroundColor Red
        Write-Host "  pip install -r requirements.txt" -ForegroundColor Yellow
        pause
        exit 1
    }
} else {
    Write-Host "✓ Todas as dependências estão instaladas" -ForegroundColor Green
}

Write-Host ""

# Verificar API Key
Write-Host "Verificando API Key..." -ForegroundColor Yellow
if (Test-Path ".env") {
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "ANTHROPIC_API_KEY=sk-") {
        Write-Host "✓ API Key encontrada" -ForegroundColor Green
    } else {
        Write-Host "⚠ API Key pode estar incorreta no arquivo .env" -ForegroundColor Yellow
    }
} else {
    Write-Host "✗ Arquivo .env não encontrado!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Crie o arquivo .env com seu API Key:" -ForegroundColor Yellow
    Write-Host '  echo "ANTHROPIC_API_KEY=sua-chave-aqui" > .env' -ForegroundColor Cyan
    Write-Host ""
    $continue = Read-Host "Deseja continuar mesmo assim? (s/n)"
    if ($continue -ne 's' -and $continue -ne 'S') {
        exit 1
    }
}

Write-Host ""
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

# Menu de opções
Write-Host "Escolha uma opção:" -ForegroundColor Yellow
Write-Host "  1. Interface Web (Streamlit) [Recomendado]" -ForegroundColor White
Write-Host "  2. Interface CLI (Terminal)" -ForegroundColor White
Write-Host "  3. Executar Testes" -ForegroundColor White
Write-Host "  4. Sair" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Digite sua escolha (1-4)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "Iniciando interface web..." -ForegroundColor Green
        Write-Host "Acesse: http://localhost:8501" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Pressione Ctrl+C para parar o servidor" -ForegroundColor Yellow
        Write-Host ""
        streamlit run app.py
    }
    "2" {
        Write-Host ""
        Write-Host "Iniciando interface CLI..." -ForegroundColor Green
        Write-Host ""
        python transcribe_consult.py
    }
    "3" {
        Write-Host ""
        Write-Host "Executando testes..." -ForegroundColor Green

        # Verificar se pytest está instalado
        $pytestInstalled = python -c "import pytest" 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Instalando pytest..." -ForegroundColor Yellow
            pip install pytest pytest-cov pytest-mock
        }

        Write-Host ""
        pytest -v --cov --cov-report=term-missing
        Write-Host ""
        pause
    }
    "4" {
        Write-Host "Até logo!" -ForegroundColor Green
        exit 0
    }
    default {
        Write-Host "Opção inválida!" -ForegroundColor Red
        pause
        exit 1
    }
}
