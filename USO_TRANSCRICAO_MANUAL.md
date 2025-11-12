# 📝 Usar Transcrição Existente

## Nova Funcionalidade: Opção 3

Agora você pode gerar relatórios **sem processar áudio**, usando transcrições que você já tem disponíveis!

---

## ✨ Vantagens

- ⚡ **Mais rápido** - Não precisa processar áudio
- 💰 **Economiza recursos** - Whisper não é carregado
- 🔄 **Flexível** - Use transcrições de qualquer fonte
- ♻️ **Reprocessar** - Gere novos relatórios de transcrições antigas

---

## 🚀 Como Usar

### Passo 1: Execute o sistema

```bash
python transcribe_consult.py
```

Ou clique em **executar.bat**

### Passo 2: Escolha a Opção 3

```
Opções:
1. Processar arquivo de áudio específico
2. Processar todos os arquivos na pasta audios/
3. Usar transcrição existente (texto já disponível)  ← ESCOLHA ESTA
4. Sair

Escolha uma opção (1-4): 3
```

### Passo 3: Escolha o método

Você tem duas opções:

#### Opção A: Colar/Digitar o texto

```
============================================================
📝 FORNECER TRANSCRIÇÃO
============================================================

Escolha como fornecer a transcrição:
1. Colar/digitar o texto diretamente  ← ESTA
2. Ler de um arquivo .txt
3. Voltar

Escolha uma opção (1-3): 1
```

Depois cole seu texto e digite `FIM` quando terminar:

```
Digite ou cole o texto da transcrição abaixo.
Quando terminar, digite 'FIM' em uma nova linha e pressione Enter:
------------------------------------------------------------

Olá, Dr. João Silva aqui. Hoje atendi o Rex, labrador de 4 anos...
(seu texto aqui)
FIM

✅ Transcrição capturada (523 caracteres)
```

#### Opção B: Ler de arquivo .txt

```
Escolha como fornecer a transcrição:
1. Colar/digitar o texto diretamente
2. Ler de um arquivo .txt  ← ESTA
3. Voltar

Escolha uma opção (1-3): 2
```

O sistema vai procurar arquivos .txt e listar para você escolher.

### Passo 4: Preencha os dados do paciente

Como sempre:
```
============================================================
📋 COLETA DE INFORMAÇÕES DO PACIENTE
============================================================
Nome do paciente: Rex
Espécie (Cão/Gato/Outro): Cão
Raça: Labrador
Idade e Peso (ex: 3 anos, 8kg): 4 anos, 28kg
Nome do tutor: João Silva
Data da consulta (DD/MM/AAAA) [Enter=hoje]:
Motivo do retorno: Revisão pós-operatória
Tipo (Presencial/Videoconferência): Presencial
```

### Passo 5: Pronto!

```
🤖 Gerando relatório com Claude API...
📊 Tokens usados: 4523 input, 1654 output

✅ Relatório salvo: 20251109_154523_Rex_transcrição_manual.md

============================================================
✅ PROCESSAMENTO CONCLUÍDO COM SUCESSO!
============================================================
📄 Relatório: relatorios/20251109_154523_Rex_transcrição_manual.md
```

---

## 📋 Casos de Uso

### 1. Já tem transcrições de outro sistema

Se você usa outro serviço de transcrição, pode importar o texto:

```
1. Copie o texto do outro sistema
2. Use opção 3 → 1 (colar texto)
3. Cole o texto
4. Digite FIM
5. Gere o relatório!
```

### 2. Transcrição manual (digitada)

Para consultas curtas ou notas já digitadas:

```
1. Digite suas notas da consulta
2. Use opção 3 → 1
3. Cole/digite suas notas
4. FIM
5. Relatório gerado!
```

### 3. Reprocessar transcrições antigas

Quer gerar um novo relatório de uma consulta antiga?

```
1. Vá na pasta transcricoes/
2. Encontre o arquivo .txt da consulta
3. Use opção 3 → 2 (ler arquivo)
4. Selecione o arquivo
5. Novo relatório gerado!
```

### 4. Editar transcrição antes de gerar relatório

```
1. Transcreva o áudio normalmente (opção 1)
2. Vá em transcricoes/ e abra o .txt gerado
3. Edite/corrija o que precisar
4. Salve o arquivo
5. Use opção 3 → 2 para ler o arquivo editado
6. Gere um relatório melhorado!
```

---

## 💡 Dicas

### Dica 1: Formato do texto

Não importa o formato, o Claude vai estruturar:

✅ **Aceita:**
- Texto corrido sem formatação
- Bullet points
- Parágrafos
- Notas soltas
- Transcrições com erros

O Claude vai organizar tudo no formato do relatório!

### Dica 2: Tamanho do texto

- **Mínimo:** ~100 caracteres (1-2 frases)
- **Ideal:** 500-5000 caracteres
- **Máximo:** ~20.000 caracteres

Textos muito curtos podem gerar relatórios incompletos.

### Dica 3: Economize tempo

Para consultas de retorno rápidas:

1. Fale suas notas no gravador do celular
2. Use transcrição automática do celular
3. Copie o texto
4. Cole na opção 3 → 1
5. Relatório pronto em segundos!

### Dica 4: Batch processing

Tem várias transcrições em .txt?

1. Coloque todos os .txt na pasta `transcricoes/`
2. Use opção 3 → 2 repetidas vezes
3. Ou crie um script para processar todos

---

## ⚡ Comparação de Velocidade

| Método | Tempo Estimado | Uso de Recursos |
|--------|----------------|-----------------|
| Áudio (opção 1) | 5-10 minutos | Alto (Whisper + Claude) |
| Transcrição (opção 3) | 10-30 segundos | Baixo (só Claude) |

**Economize até 95% do tempo!**

---

## 🔍 Exemplo Completo

### Entrada (texto colado):

```
Retorno do Bob, yorkshire de 5 anos. Tutor relata que a coceira diminuiu muito
após iniciar o tratamento com prednisolona 5mg. Ainda coça as orelhas mas bem
menos. Apetite normal, brincando normalmente. Exame físico: mucosas rosadas,
hidratação 8%, sem lesões novas na pele. Orelhas com leve eritema mas sem
secreção. Manter prednisolona por mais 7 dias e retornar para reavaliação.
```

### Saída (relatório gerado):

```markdown
# RELATÓRIO DE CONSULTA VETERINÁRIA - RETORNO

## 📋 DADOS DO ATENDIMENTO
- **Data:** 09/11/2025
- **Modalidade:** Presencial
- **Veterinário:** não mencionado

## 🐾 IDENTIFICAÇÃO DO PACIENTE
- **Paciente:** Bob | **Espécie:** Cão | **Raça:** Yorkshire
- **Idade/Peso:** 5 anos
- **Tutor:** João Silva

## 📝 SUMÁRIO EXECUTIVO
Retorno para acompanhamento de dermatite. Paciente apresentou excelente
resposta ao tratamento com prednisolona, com redução significativa do prurido...

[... resto do relatório estruturado ...]
```

---

## ❓ Perguntas Frequentes

**P: Posso usar transcrições de outros idiomas?**
R: Sim! O Claude processa múltiplos idiomas.

**P: Preciso formatar o texto antes?**
R: Não! Cole do jeito que está, o Claude organiza.

**P: O relatório fica igual ao de áudio?**
R: Sim! Mesma qualidade e estrutura.

**P: Posso editar a transcrição depois?**
R: Sim! Ela fica salva em `transcricoes/`.

**P: Quanto custa?**
R: Mesmo preço (~$0,05 por relatório).

---

## 🎯 Fluxo Completo

```
Texto/Transcrição disponível
        ↓
Executar sistema
        ↓
Opção 3 (transcrição existente)
        ↓
Escolher método (colar ou arquivo)
        ↓
Fornecer texto
        ↓
Preencher dados paciente
        ↓
Relatório gerado!
```

---

**Versão:** 1.3 (Production Ready)
**Atualizado:** Novembro 2025
