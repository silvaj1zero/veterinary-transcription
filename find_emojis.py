#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys
import io

# Configurar UTF-8 para output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Ler arquivo
with open('transcribe_consult.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Padrão de emojis (ranges Unicode)
emoji_pattern = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags
    "\U00002702-\U000027B0"  # dingbats
    "\U000024C2-\U0001F251"  # enclosed characters
    "\U0001F900-\U0001F9FF"  # supplemental symbols
    "\U0001FA00-\U0001FA6F"  # chess symbols
    "\U0001FA70-\U0001FAFF"  # symbols and pictographs extended-a
    "\U00002600-\U000026FF"  # miscellaneous symbols
    "]+",
    flags=re.UNICODE
)

# Encontrar emojis
found_emojis = []
for i, line in enumerate(lines, 1):
    emojis = emoji_pattern.findall(line)
    if emojis:
        found_emojis.append((i, line.strip(), emojis))
        print(f"Linha {i}: {emojis} -> {line.strip()[:80]}")

print(f"\nTotal de linhas com emojis: {len(found_emojis)}")
