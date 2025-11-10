# Script para converter documentação Markdown para PDF
# Requer: pip install markdown2 pdfkit wkhtmltopdf

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Conversor de Documentação MD -> PDF" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se os arquivos existem
$manualUsuario = "MANUAL_USUARIO.md"
$docTecnica = "DOCUMENTACAO_TECNICA.md"

if (-not (Test-Path $manualUsuario)) {
    Write-Host "Erro: $manualUsuario não encontrado!" -ForegroundColor Red
    Write-Host "Execute 'git pull' primeiro" -ForegroundColor Yellow
    pause
    exit 1
}

if (-not (Test-Path $docTecnica)) {
    Write-Host "Erro: $docTecnica não encontrado!" -ForegroundColor Red
    Write-Host "Execute 'git pull' primeiro" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "✓ Arquivos encontrados:" -ForegroundColor Green
Write-Host "  - $manualUsuario"
Write-Host "  - $docTecnica"
Write-Host ""

# Menu
Write-Host "Escolha uma opção:" -ForegroundColor Yellow
Write-Host "  1. Abrir Manual do Usuário (Notepad)"
Write-Host "  2. Abrir Documentação Técnica (Notepad)"
Write-Host "  3. Abrir ambos (Notepad)"
Write-Host "  4. Copiar para Desktop"
Write-Host "  5. Sair"
Write-Host ""

$escolha = Read-Host "Digite sua escolha (1-5)"

switch ($escolha) {
    "1" {
        Write-Host "Abrindo Manual do Usuário..." -ForegroundColor Green
        notepad $manualUsuario
    }
    "2" {
        Write-Host "Abrindo Documentação Técnica..." -ForegroundColor Green
        notepad $docTecnica
    }
    "3" {
        Write-Host "Abrindo ambos os documentos..." -ForegroundColor Green
        notepad $manualUsuario
        Start-Sleep -Seconds 1
        notepad $docTecnica
    }
    "4" {
        $desktop = [Environment]::GetFolderPath("Desktop")
        Write-Host "Copiando para Desktop..." -ForegroundColor Green

        Copy-Item $manualUsuario -Destination "$desktop\MANUAL_USUARIO.md"
        Copy-Item $docTecnica -Destination "$desktop\DOCUMENTACAO_TECNICA.md"

        Write-Host "✓ Arquivos copiados para:" -ForegroundColor Green
        Write-Host "  $desktop\MANUAL_USUARIO.md"
        Write-Host "  $desktop\DOCUMENTACAO_TECNICA.md"

        # Abrir pasta Desktop
        explorer $desktop
    }
    "5" {
        Write-Host "Até logo!" -ForegroundColor Green
        exit 0
    }
    default {
        Write-Host "Opção inválida!" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Concluído!" -ForegroundColor Cyan
pause
