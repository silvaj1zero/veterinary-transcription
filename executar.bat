@echo off
chcp 65001 >nul
echo ╔═══════════════════════════════════════════════════════════╗
echo ║   SISTEMA DE DOCUMENTAÇÃO DE CONSULTAS VETERINÁRIAS      ║
echo ║                      BadiLab - 2025                       ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

"C:\Users\Zero\AppData\Local\Programs\Python\Python312\python.exe" "%~dp0transcribe_consult.py"

pause
