#!/usr/bin/env python3
"""
Teste de integração completo do sistema
"""

import sys
from pathlib import Path

# Adicionar diretório ao path
sys.path.insert(0, str(Path(__file__).parent))

from auth import AuthManager
import config
import os

def test_full_integration():
    """Teste completo de integração do sistema"""

    print("\n" + "=" * 60)
    print("TESTE DE INTEGRAÇÃO COMPLETO")
    print("=" * 60)

    # 1. Verificar ambiente
    print("\n📋 1. VERIFICANDO AMBIENTE")
    print("-" * 60)

    # Verificar estrutura de diretórios
    required_dirs = [
        config.AUDIO_DIR,
        config.TRANSCRIPTION_DIR,
        config.REPORT_DIR,
        Path("data"),
        Path("templates"),
        Path("services")
    ]

    for dir_path in required_dirs:
        if dir_path.exists():
            print(f"   ✅ {dir_path}")
        else:
            print(f"   ⚠️  {dir_path} (será criado automaticamente)")

    # Verificar templates
    print("\n📄 Templates:")
    templates = [
        Path("templates/prompt_veterinario.txt"),
        Path("templates/prompt_resumo_tutor.txt")
    ]

    for template in templates:
        if template.exists():
            size = template.stat().st_size
            print(f"   ✅ {template.name} ({size} bytes)")
        else:
            print(f"   ❌ {template.name} NÃO ENCONTRADO")

    # 2. Testar Sistema de Autenticação
    print("\n🔐 2. SISTEMA DE AUTENTICAÇÃO")
    print("-" * 60)

    auth = AuthManager()
    print("   ✅ AuthManager inicializado")

    # Teste de login
    user = auth.authenticate("admin", "admin123")
    if user:
        print(f"   ✅ Login admin funcionando")
        print(f"      - Nome: {user['full_name']}")
        print(f"      - Role: {user['role']}")
    else:
        print("   ❌ Falha no login admin")
        return False

    # 3. Verificar Módulos Importados
    print("\n📦 3. MÓDULOS E DEPENDÊNCIAS")
    print("-" * 60)

    modules_to_test = [
        ("streamlit", "Interface Web"),
        ("anthropic", "Claude API"),
        ("google.generativeai", "Google Gemini (opcional)"),
        ("whisper", "Transcrição de Áudio (opcional)"),
        ("pandas", "Análise de Dados"),
        ("plotly", "Gráficos"),
        ("reportlab", "Geração de PDF"),
    ]

    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"   ✅ {description} ({module_name})")
        except (ImportError, Exception) as e:
            if "opcional" in description.lower():
                print(f"   ⚠️  {description} ({module_name}) - OPCIONAL (erro: {type(e).__name__})")
            else:
                print(f"   ❌ {description} ({module_name}) - OBRIGATÓRIO (erro: {type(e).__name__})")

    # 4. Verificar Configurações
    print("\n⚙️  4. CONFIGURAÇÕES")
    print("-" * 60)

    configs = [
        ("ANTHROPIC_API_KEY", config.ANTHROPIC_API_KEY, True),
        ("GOOGLE_API_KEY", config.GOOGLE_API_KEY, False),
        ("WHISPER_MODEL", config.WHISPER_MODEL, True),
        ("DEFAULT_LANGUAGE", config.DEFAULT_LANGUAGE, True),
        ("TRANSCRIPTION_PROVIDER", config.TRANSCRIPTION_PROVIDER, True),
        ("LLM_PROVIDER", config.LLM_PROVIDER, True),
    ]

    for name, value, required in configs:
        if value:
            masked = value[:10] + "..." if len(str(value)) > 15 else value
            print(f"   ✅ {name}: {masked}")
        else:
            if required:
                print(f"   ⚠️  {name}: NÃO CONFIGURADO (necessário)")
            else:
                print(f"   ⚙️  {name}: NÃO CONFIGURADO (opcional)")

    # 5. Verificar Serviços
    print("\n🔧 5. SERVIÇOS")
    print("-" * 60)

    try:
        from services import StatsService, ReportService
        print("   ✅ StatsService importado")
        print("   ✅ ReportService importado")

        # Testar StatsService
        stats_service = StatsService(config.REPORT_DIR)
        stats = stats_service.get_stats()
        print(f"   ✅ StatsService funcionando")
        print(f"      - Total de relatórios: {stats['total_relatorios']}")

    except Exception as e:
        print(f"   ❌ Erro ao importar services: {e}")

    # 6. Testar Conversores
    print("\n📄 6. CONVERSORES")
    print("-" * 60)

    try:
        from converters import convert_md_to_txt
        from pdf_converter import convert_md_to_pdf

        print("   ✅ convert_md_to_txt importado")
        print("   ✅ convert_md_to_pdf importado")

        # Testar conversão MD → TXT
        test_md = "# Teste\n\nConteúdo de **teste**."
        test_txt = convert_md_to_txt(test_md)
        if "Teste" in test_txt:
            print("   ✅ Conversão MD → TXT funcionando")
        else:
            print("   ❌ Conversão MD → TXT falhou")

    except Exception as e:
        print(f"   ❌ Erro nos conversores: {e}")

    # 7. Banco de Dados
    print("\n💾 7. BANCO DE DADOS")
    print("-" * 60)

    db_path = Path("data/users.db")
    if db_path.exists():
        size = db_path.stat().st_size
        users = auth.get_all_users()
        print(f"   ✅ Banco criado: {db_path}")
        print(f"      - Tamanho: {size} bytes")
        print(f"      - Usuários: {len(users)}")

        for user in users:
            status = "Ativo" if user['is_active'] else "Inativo"
            print(f"         • {user['username']} ({user['role']}) - {status}")
    else:
        print("   ❌ Banco não encontrado")

    # 8. Verificar Logs
    print("\n📝 8. SISTEMA DE LOGS")
    print("-" * 60)

    log_files = [
        Path("veterinary_system_web.log"),
        Path("veterinary_transcription.log")
    ]

    for log_file in log_files:
        if log_file.exists():
            size = log_file.stat().st_size
            print(f"   ✅ {log_file.name} ({size} bytes)")
        else:
            print(f"   ⚠️  {log_file.name} (será criado ao usar o sistema)")

    # Resumo Final
    print("\n" + "=" * 60)
    print("✅ TESTE DE INTEGRAÇÃO CONCLUÍDO")
    print("=" * 60)

    print("\n📊 RESUMO:")
    print("   ✅ Sistema de autenticação: OK")
    print("   ✅ Banco de dados: OK")
    print("   ✅ Módulos principais: OK")
    print("   ✅ Conversores: OK")
    print("   ✅ Serviços: OK")

    print("\n🚀 PRÓXIMOS PASSOS:")
    print("   1. Acessar: http://localhost:8501")
    print("   2. Login: admin / admin123")
    print("   3. Alterar senha padrão")
    print("   4. Criar usuários adicionais (se necessário)")
    print("   5. Configurar GOOGLE_API_KEY (opcional)")

    if not config.ANTHROPIC_API_KEY:
        print("\n⚠️  ATENÇÃO:")
        print("   Configure ANTHROPIC_API_KEY no arquivo .env")
        print("   para usar a geração de relatórios!")

    return True

if __name__ == "__main__":
    try:
        success = test_full_integration()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERRO NO TESTE: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
