#!/usr/bin/env python3
"""
Script de migração de dados do SQLite para Supabase
Migra usuários existentes do auth.py (SQLite) para auth_supabase.py
"""

import sqlite3
from pathlib import Path
import sys
from getpass import getpass

try:
    from auth_supabase import SupabaseAuthManager
except ImportError:
    print("❌ Erro: Instale as dependências do Supabase primeiro")
    print("   pip install supabase psycopg2-binary")
    sys.exit(1)

def migrate_users():
    """Migrar usuários do SQLite para Supabase"""

    print("\n" + "=" * 60)
    print("MIGRAÇÃO: SQLite → Supabase")
    print("=" * 60)

    # Verificar se banco SQLite existe
    sqlite_db = Path("data/users.db")
    if not sqlite_db.exists():
        print("\n❌ Banco de dados SQLite não encontrado: data/users.db")
        print("   Nada para migrar.")
        return

    # Conectar ao SQLite
    print("\n📂 Conectando ao SQLite...")
    conn = sqlite3.connect(sqlite_db)
    cursor = conn.cursor()

    # Buscar usuários
    cursor.execute("""
        SELECT id, username, password_hash, salt, full_name, email, role, is_active, created_at
        FROM users
        WHERE is_active = 1
        ORDER BY created_at
    """)

    users = cursor.fetchall()
    conn.close()

    if not users:
        print("   ⚠️  Nenhum usuário ativo encontrado no SQLite")
        return

    print(f"   ✅ Encontrados {len(users)} usuário(s) ativo(s)")

    # Confirmar migração
    print("\n⚠️  ATENÇÃO:")
    print("   - Esta migração criará novos usuários no Supabase")
    print("   - Senhas NÃO podem ser migradas (são hashes)")
    print("   - Você precisará definir novas senhas para cada usuário")
    print("   - O banco SQLite não será alterado")

    confirm = input("\n   Deseja continuar? (s/N): ").strip().lower()
    if confirm != 's':
        print("\n❌ Migração cancelada")
        return

    # Inicializar Supabase
    print("\n🚀 Conectando ao Supabase...")
    try:
        auth = SupabaseAuthManager()
    except Exception as e:
        print(f"❌ Erro ao conectar ao Supabase: {e}")
        print("   Verifique se SUPABASE_URL e SUPABASE_KEY estão configurados no .env")
        return

    # Migrar cada usuário
    print("\n👤 Migrando usuários...")
    migrated = 0
    skipped = 0

    for user in users:
        user_id, username, pwd_hash, salt, full_name, email, role, is_active, created_at = user

        print(f"\n   • {username} ({full_name})")
        print(f"     Email: {email or 'N/A'}")
        print(f"     Role: {role}")

        # Se não tiver email, solicitar
        if not email or email == "":
            email = input(f"     Digite o email para {username}: ").strip()
            if not email:
                print("     ⏭️  Pulando (email obrigatório)")
                skipped += 1
                continue

        # Solicitar nova senha
        print(f"     Digite uma NOVA senha para {username}:")
        password = getpass("     Senha: ")
        password_confirm = getpass("     Confirme: ")

        if password != password_confirm:
            print("     ❌ Senhas não coincidem. Pulando usuário.")
            skipped += 1
            continue

        if len(password) < 6:
            print("     ❌ Senha muito curta (mínimo 6 caracteres). Pulando usuário.")
            skipped += 1
            continue

        # Criar usuário no Supabase
        try:
            result = auth.signup(
                email=email,
                password=password,
                full_name=full_name,
                role=role
            )

            if result:
                print("     ✅ Migrado com sucesso!")
                migrated += 1
            else:
                print("     ❌ Falha ao criar usuário")
                skipped += 1

        except Exception as e:
            print(f"     ❌ Erro: {e}")
            skipped += 1

    # Resumo
    print("\n" + "=" * 60)
    print("RESUMO DA MIGRAÇÃO")
    print("=" * 60)
    print(f"   ✅ Migrados: {migrated}")
    print(f"   ⏭️  Pulados: {skipped}")
    print(f"   📊 Total: {len(users)}")

    if migrated > 0:
        print("\n✅ Migração concluída!")
        print("\n📋 Próximos passos:")
        print("   1. Teste o login com os usuários migrados")
        print("   2. Atualize DATABASE_PROVIDER=supabase no .env")
        print("   3. Reinicie a aplicação")
        print("   4. Faça backup do SQLite antes de deletá-lo")
    else:
        print("\n⚠️  Nenhum usuário foi migrado")

def main():
    """Função principal"""
    try:
        migrate_users()
    except KeyboardInterrupt:
        print("\n\n❌ Migração cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
