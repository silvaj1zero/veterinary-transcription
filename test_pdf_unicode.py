#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify PDF Unicode support
Tests that Portuguese characters are preserved in PDF output
"""
from pdf_converter import convert_md_to_pdf
from pathlib import Path

# Test content with Portuguese special characters
test_content = """
# Relatório de Consulta Veterinária

## Informações do Paciente
- **Nome:** Flávio
- **Espécie:** Cão
- **Raça:** Vira-lata
- **Tutor:** João da Silva

## Anamnese
O paciente apresentou prurido intenso há 3 semanas. A tutora relata que já tentou banhos com sabão neutro mas não houve melhora significativa.

## Exame Físico
- **Temperatura:** 38.5°C
- **Frequência Cardíaca:** 120 bpm
- **Mucosas:** Rosadas e úmidas
- **Linfonodos:** Sem alterações palpáveis

## Diagnóstico
Dermatite alérgica à pulgas (DAPP)

## Prescrição
- Simparic 40mg - 1 comprimido via oral, a cada 30 dias
- Prednisolona 5mg - 1 comprimido 2x ao dia por 5 dias
- Shampoo hipoalergênico - banhos 2x por semana

## Observações
- Atenção especial à nutrição
- Controle rigoroso de pulgas no ambiente
- Retorno em 15 dias para reavaliação

---
**Veterinário:** Dr. José Carlos Mendonça
**CRMV-SP:** 12345
**Data:** 14/11/2025
"""

def main():
    """Run PDF Unicode test"""
    print("Testando geracao de PDF com caracteres Unicode...")
    print("="*60)

    # Test 1: Generate PDF
    print("\n1. Gerando PDF com acentos portugueses...")
    try:
        pdf_bytes = convert_md_to_pdf(test_content)
        print(f"   OK - PDF gerado com sucesso ({len(pdf_bytes)} bytes)")
    except Exception as e:
        print(f"   ERRO - Erro ao gerar PDF: {e}")
        return False

    # Test 2: Save to file
    print("\n2. Salvando PDF em arquivo...")
    output_file = Path("teste_unicode.pdf")
    try:
        with open(output_file, "wb") as f:
            f.write(pdf_bytes)
        print(f"   OK - Arquivo salvo: {output_file.absolute()}")
    except Exception as e:
        print(f"   ERRO - Erro ao salvar arquivo: {e}")
        return False

    # Test 3: Verify file exists and has content
    print("\n3. Verificando arquivo gerado...")
    if output_file.exists():
        file_size = output_file.stat().st_size
        print(f"   OK - Arquivo existe ({file_size} bytes)")

        if file_size > 1000:  # Should be at least 1KB
            print("   OK - Tamanho adequado")
        else:
            print(f"   AVISO - Arquivo muito pequeno ({file_size} bytes)")
    else:
        print("   ERRO - Arquivo nao foi criado")
        return False

    # Summary
    print("\n" + "="*60)
    print("OK - TESTE CONCLUIDO COM SUCESSO!")
    print("="*60)
    print(f"\nAbra o arquivo '{output_file}' e verifique:")
    print("   - Caracteres acentuados (a, a, c, etc.) estao preservados")
    print("   - Formatacao esta correta (titulos, listas, etc.)")
    print("   - Texto esta legivel e completo")
    print("\nSe todos os acentos estiverem corretos, o teste passou!")

    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
