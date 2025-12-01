#!/usr/bin/env python3
"""
Script de teste do sistema de autenticação
"""

import sys
from pathlib import Path

# Adicionar diretório ao path
sys.path.insert(0, str(Path(__file__).parent))

from auth import AuthManager

def test_authentication_system():
    """Testar funcionalidades principais do sistema de autenticação"""

    print("=" * 60)
    print("TESTE DO SISTEMA DE AUTENTICAÇÃO")
    print("=" * 60)

    # 1. Inicializar AuthManager
    print("\n1. Inicializando AuthManager...")
    auth = AuthManager()
    print("   ✅ AuthManager inicializado")

    # 2. Verificar se admin padrão foi criado
    print("\n2. Verificando usuário admin padrão...")
    if auth.user_exists("admin"):
        print("   ✅ Usuário 'admin' existe")
    else:
        print("   ❌ Usuário 'admin' não foi criado")
        return False

    # 3. Testar autenticação com credenciais corretas
    print("\n3. Testando autenticação com credenciais corretas...")
    user = auth.authenticate("admin", "admin123")
    if user:
        print(f"   ✅ Login bem-sucedido!")
        print(f"   - Username: {user['username']}")
        print(f"   - Nome: {user['full_name']}")
        print(f"   - Role: {user['role']}")
        print(f"   - Email: {user['email']}")
    else:
        print("   ❌ Falha no login com credenciais corretas")
        return False

    # 4. Testar autenticação com senha incorreta
    print("\n4. Testando autenticação com senha incorreta...")
    user = auth.authenticate("admin", "senha_errada")
    if not user:
        print("   ✅ Falha esperada com senha incorreta")
    else:
        print("   ❌ Sistema aceitou senha incorreta!")
        return False

    # 5. Criar novo usuário
    print("\n5. Criando novo usuário de teste...")
    success = auth.create_user(
        username="teste_user",
        password="senha123",
        full_name="Usuário de Teste",
        email="teste@exemplo.com",
        role="user",
        created_by="admin"
    )
    if success:
        print("   ✅ Usuário 'teste_user' criado com sucesso")
    else:
        print("   ❌ Falha ao criar usuário")
        return False

    # 6. Testar login do novo usuário
    print("\n6. Testando login do novo usuário...")
    user = auth.authenticate("teste_user", "senha123")
    if user:
        print(f"   ✅ Login do usuário de teste bem-sucedido!")
        print(f"   - Username: {user['username']}")
        print(f"   - Role: {user['role']}")
    else:
        print("   ❌ Falha no login do usuário de teste")
        return False

    # 7. Listar todos os usuários
    print("\n7. Listando todos os usuários...")
    users = auth.get_all_users()
    print(f"   ✅ Total de usuários: {len(users)}")
    for u in users:
        status = "Ativo" if u['is_active'] else "Inativo"
        print(f"   - {u['username']} ({u['role']}) - {status}")

    # 8. Alterar senha
    print("\n8. Testando alteração de senha...")
    success = auth.change_password("teste_user", "senha123", "nova_senha456")
    if success:
        print("   ✅ Senha alterada com sucesso")

        # Verificar se nova senha funciona
        user = auth.authenticate("teste_user", "nova_senha456")
        if user:
            print("   ✅ Login com nova senha bem-sucedido")
        else:
            print("   ❌ Falha ao fazer login com nova senha")
            return False
    else:
        print("   ❌ Falha ao alterar senha")
        return False

    # 9. Desativar usuário
    print("\n9. Testando desativação de usuário...")
    success = auth.update_user("teste_user", is_active=False)
    if success:
        print("   ✅ Usuário desativado")

        # Tentar login com usuário desativado
        user = auth.authenticate("teste_user", "nova_senha456")
        if not user:
            print("   ✅ Login bloqueado para usuário desativado")
        else:
            print("   ❌ Sistema permitiu login de usuário desativado")
            return False
    else:
        print("   ❌ Falha ao desativar usuário")
        return False

    # 10. Verificar histórico de logins
    print("\n10. Verificando histórico de logins...")
    history = auth.get_login_history("admin", limit=5)
    if history:
        print(f"   ✅ Histórico encontrado: {len(history)} registros")
        for h in history[:3]:
            status = "✅ Sucesso" if h['success'] else "❌ Falha"
            print(f"   - {h['timestamp']} - {status}")
    else:
        print("   ⚠️  Nenhum histórico encontrado")

    # 11. Verificar banco de dados
    print("\n11. Verificando arquivo do banco de dados...")
    db_path = Path("data/users.db")
    if db_path.exists():
        size = db_path.stat().st_size
        print(f"   ✅ Banco de dados criado: {db_path}")
        print(f"   - Tamanho: {size} bytes")
    else:
        print("   ❌ Arquivo do banco não encontrado")
        return False

    print("\n" + "=" * 60)
    print("✅ TODOS OS TESTES PASSARAM COM SUCESSO!")
    print("=" * 60)

    return True

if __name__ == "__main__":
    try:
        success = test_authentication_system()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERRO NO TESTE: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
