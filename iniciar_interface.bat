@echo off
chcp 65001 >nul
echo.
echo ============================================================
echo    Interface Grafica do Sistema Veterinario
echo ============================================================
echo.
echo Iniciando servidor Streamlit...
echo.
echo A interface sera aberta automaticamente no navegador.
echo Para encerrar, pressione Ctrl+C nesta janela.
echo.
echo ============================================================
echo.

"C:\Users\Zero\AppData\Local\Programs\Python\Python312\python.exe" -m streamlit run "%~dp0app.py"

pause
