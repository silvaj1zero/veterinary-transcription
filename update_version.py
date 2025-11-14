#!/usr/bin/env python3
"""Script para atualizar versão de 1.2 para 1.3 em todos os arquivos .md"""

import os
import re
from pathlib import Path

# Diretório base
base_dir = Path(__file__).parent

# Padrões a substituir
replacements = [
    (r'Versão:?\s*1\.2\s*\(Production Ready\)', 'Versão: 1.3 (Production Ready)'),
    (r'v1\.2\s*-\s*Production Ready', 'v1.3 - Production Ready'),
    (r'Veterinárias v1\.2', 'Veterinárias v1.3'),
    (r'## Sistema de Documentação de Consultas Veterinárias v1\.2', '## Sistema de Documentação de Consultas Veterinárias v1.3'),
]

# Encontrar todos os arquivos .md
md_files = list(base_dir.glob('*.md'))

print(f"Encontrados {len(md_files)} arquivos .md")

updated_count = 0

for md_file in md_files:
    try:
        # Ler conteúdo
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Aplicar todas as substituições
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)

        # Se houve mudanças, salvar
        if content != original_content:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[OK] Atualizado: {md_file.name}")
            updated_count += 1
        else:
            print(f"[SKIP] Sem mudancas: {md_file.name}")

    except Exception as e:
        print(f"[ERROR] Erro em {md_file.name}: {e}")

print(f"\nTotal de arquivos atualizados: {updated_count}/{len(md_files)}")
