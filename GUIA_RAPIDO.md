# 🚀 Guia Rápido de Início

## Configuração Inicial (faça apenas uma vez)

### 1. Obter sua API Key

1. Acesse: https://console.anthropic.com/
2. Faça login
3. Vá em **Settings → API Keys**
4. Clique em **Create Key**
5. Copie a chave

### 2. Configurar a API Key

Crie um arquivo `.env` na raiz do projeto com:

```
ANTHROPIC_API_KEY=sua_chave_aqui
```

**Pronto! Agora você está pronto para usar.**

---

## Uso Diário

### Método 1: Processar áudio (completo)

1. Clique duas vezes em **executar.bat**
2. Escolha opção **1** (arquivo específico) ou **2** (todos)
3. Siga as instruções na tela

### Método 2: Usar transcrição existente (rápido!)

1. Clique duas vezes em **executar.bat**
2. Escolha opção **3** (transcrição existente)
3. Cole o texto OU escolha um arquivo .txt
4. Preencha dados do paciente
5. Relatório pronto em segundos!

### Método 3: Linha de comando

1. Abra o terminal nesta pasta
2. Execute:
   ```bash
   python transcribe_consult.py
   ```

---

## Fluxo de Trabalho

```
1. Colocar áudio → audios/
         ↓
2. Executar sistema
         ↓
3. Preencher dados do paciente
         ↓
4. Aguardar processamento
         ↓
5. Relatório em → relatorios/
```

---

## Exemplo Passo a Passo

**Passo 1:** Copie seu arquivo de áudio
```
consulta.mp3 → pasta audios/
```

**Passo 2:** Execute
```
Clique em executar.bat
```

**Passo 3:** Escolha a opção
```
Escolha uma opção (1-3): 1
```

**Passo 4:** Selecione o arquivo
```
Arquivos disponíveis:
1. consulta.mp3
Escolha: 1
```

**Passo 5:** Preencha os dados
```
Nome do paciente: Rex
Espécie: Cão
Raça: Labrador
Idade e Peso: 4 anos, 28kg
Nome do tutor: João Silva
Data da consulta: [Enter para hoje]
Motivo do retorno: Acompanhamento pós-cirurgia
Tipo: Presencial
```

**Passo 6:** Aguarde
```
🎤 Transcrevendo...
🤖 Gerando relatório...
✅ Pronto!
```

**Passo 7:** Abra o relatório
```
Vá em: relatorios/
Abra o arquivo .md gerado
```

---

## Dicas

💡 **Áudios mais curtos** = processamento mais rápido
💡 **Use o modelo 'base'** para testes rápidos
💡 **Processar em lote** durante a noite (opção 2)
💡 **Já tem transcrição?** Use opção 3 (95% mais rápido!)
💡 **Custo típico:** ~5 centavos por consulta

## Atalho Rápido ⚡

Para consultas com transcrição já disponível:
1. **executar.bat** → **3** → **1** (colar texto)
2. Cole a transcrição
3. Digite **FIM**
4. Preencha dados
5. Pronto em 30 segundos!

---

## Problemas Comuns

❌ **"API key não encontrada"**
→ Verifique se criou o arquivo `.env` com a chave

❌ **"Nenhum áudio encontrado"**
→ Certifique-se que o arquivo está em `audios/`

❌ **Transcrição com erros**
→ Use o modelo `medium` para melhor precisão em português

---

## Precisa de Ajuda?

Leia o **README.md** para documentação completa.

---

**Versão Rápida:** 1.0
