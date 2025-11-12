# 🧪 ROTEIRO DE TESTES - Sistema Veterinário

**Data:** 11/11/2025
**Ambiente:** Railway Production

---

## 📋 TESTE 1: Verificar Dashboard Inicial

### **Objetivo:** Confirmar que a aplicação carrega

**Passos:**
1. Acesse a URL do Railway
2. Aguarde carregamento (5-10 segundos)

**Resultado esperado:**
- ✅ Página carrega com título "🏥 Sistema Veterinário"
- ✅ Menu lateral aparece
- ✅ Dashboard principal visível
- ✅ Sem erros na página

**Prints úteis:**
- Tire print da tela inicial

---

## 📋 TESTE 2: Verificar Configuração (API Claude)

### **Objetivo:** Confirmar que ANTHROPIC_API_KEY está funcionando

**Passos:**
1. No menu lateral, clique em **"⚙️ Configurações"**
2. Procure por **"API Claude"**

**Resultado esperado:**
- ✅ Mostra: "API Claude: Configurada ✅"
- ❌ Se mostrar "Não configurada ❌": ANTHROPIC_API_KEY não está no Railway

**Se falhar:**
1. Railway Dashboard → Settings → Variables
2. Add Variable: `ANTHROPIC_API_KEY` = `sk-ant-...`
3. Redeploy

---

## 📋 TESTE 3: Transcrição Manual (SEM Áudio)

### **Objetivo:** Testar geração de relatório com texto manual

**Passos:**
1. No menu lateral, clique em **"📝 Nova Consulta"**
2. Selecione: **"Texto Manual"** (não "Upload de Áudio")
3. Preencha os campos:

   **Informações do Paciente:**
   ```
   Nome do Animal: Rex
   Espécie: Cão
   Raça: Labrador
   Idade: 5 anos
   Tutor: João Silva
   Contato: (11) 98765-4321
   ```

4. **Texto da Consulta (cole este exemplo):**
   ```
   Paciente apresentou vômitos há 2 dias.
   Apetite reduzido. Sem diarreia.
   Exame físico: temperatura 38.5°C, mucosas rosadas.
   Palpação abdominal: leve desconforto.
   Diagnóstico: possível gastrite.
   Prescrição: omeprazol 20mg, 1x ao dia por 7 dias.
   Retorno em 1 semana.
   ```

5. Clique em **"Gerar Relatório"**

**Resultado esperado:**
- ✅ Barra de progresso aparece
- ✅ Mensagem: "Gerando relatório com Claude AI..."
- ✅ Após 10-30 segundos: "✅ Relatório gerado com sucesso!"
- ✅ Relatório aparece formatado com:
  - Cabeçalho (nome, espécie, tutor)
  - Anamnese
  - Exame físico
  - Diagnóstico
  - Prescrição

**Se falhar:**
- Anotar mensagem de erro exata
- Verificar se API Claude está configurada
- Verificar logs do Railway

---

## 📋 TESTE 4: Download de Relatório

### **Objetivo:** Testar exportação em diferentes formatos

**Passos:**
1. Após gerar o relatório (Teste 3)
2. Procure pelos botões de download:
   - **"📄 Download MD"** (Markdown)
   - **"📄 Download TXT"** (Texto)
   - **"📄 Download PDF"**

3. Clique em cada um

**Resultado esperado:**
- ✅ Arquivo baixa automaticamente
- ✅ Arquivo abre corretamente
- ✅ Conteúdo está formatado

**Verificar:**
- MD: Markdown com # ## formatação
- TXT: Texto puro legível
- PDF: Formatado com parágrafos (sem caracteres estranhos)

**Se PDF falhar:**
- Verificar se há caracteres especiais (á, é, ç)
- Deve converter para (a, e, c) automaticamente

---

## 📋 TESTE 5: Dashboard de Estatísticas

### **Objetivo:** Verificar histórico e estatísticas

**Passos:**
1. No menu lateral, clique em **"📊 Dashboard"**

**Resultado esperado:**
- ✅ Mostra métricas:
  - Total de Relatórios
  - Relatórios Hoje
  - Custo Total
  - Custo Hoje
  - Tempo Médio

- ✅ Gráficos (se houver dados):
  - Relatórios por Dia
  - Distribuição de Espécies
  - Custo por Consulta

**Se não mostrar dados:**
- Normal se é primeiro uso
- Dados aparecem após criar primeiro relatório

---

## 📋 TESTE 6: Histórico de Relatórios

### **Objetivo:** Verificar listagem de consultas anteriores

**Passos:**
1. No menu lateral, clique em **"📋 Histórico"**

**Resultado esperado:**
- ✅ Lista de relatórios salvos
- ✅ Filtros: data, espécie, tutor
- ✅ Cada item mostra:
  - Data/Hora
  - Paciente
  - Espécie
  - Tutor
- ✅ Botões: Ver, Download

**Testar:**
1. Clique em **"Ver"** em algum relatório
2. Relatório abre em modal/nova página
3. Clique em **"Download"**
4. Arquivo baixa corretamente

---

## 📋 TESTE 7: Upload de Áudio (PRINCIPAL!)

### **Objetivo:** Testar transcrição com Whisper

**Passos:**
1. **Primeiro, prepare um áudio de teste:**
   - Grave um áudio no celular (30-60 segundos)
   - Fale algo como:
     ```
     "O paciente Rex, um Labrador de 5 anos,
     foi trazido pelo tutor João Silva.
     Apresenta vômitos há 2 dias.
     Temperatura está em 38 graus e meio.
     Vou prescrever omeprazol."
     ```
   - Salve como MP3 ou M4A

2. **Na aplicação:**
   - Clique em **"📝 Nova Consulta"**
   - Selecione: **"Upload de Áudio"**
   - Clique em **"Browse files"**
   - Selecione seu áudio
   - Aguarde upload

3. **Preencha informações do paciente:**
   ```
   Nome: Rex
   Espécie: Cão
   Raça: Labrador
   Idade: 5 anos
   Tutor: João Silva
   Contato: (11) 98765-4321
   ```

4. Clique em **"Transcrever e Gerar Relatório"**

**Resultado esperado:**
- ✅ Upload completa (barra de progresso)
- ✅ Mensagem: "Transcrevendo áudio com Whisper..."
- ✅ Transcrição aparece (pode demorar 30-120 segundos)
- ✅ Texto transcrito mostra o que você falou
- ✅ Geração de relatório automática
- ✅ Relatório final gerado

**Possíveis tempos:**
- Áudio 30s: ~30-60s para transcrever
- Áudio 60s: ~60-120s para transcrever
- Geração relatório: +10-30s

**Se falhar:**
- Anotar erro exato
- Verificar tamanho do áudio (max 200MB)
- Verificar formato (MP3, WAV, M4A, OGG, FLAC)

---

## 📋 TESTE 8: Teste de Carga (Opcional)

### **Objetivo:** Verificar estabilidade

**Passos:**
1. Gerar 3-5 relatórios consecutivos
2. Verificar se:
   - Todos geram corretamente
   - Não há degradação de performance
   - Dashboard atualiza estatísticas

**Resultado esperado:**
- ✅ Todos relatórios gerados
- ✅ Dashboard mostra números corretos
- ✅ Histórico lista todas consultas

---

## 🐛 PROBLEMAS COMUNS E SOLUÇÕES

### **Problema: Página não carrega**

**Sintomas:**
- Erro 502 Bad Gateway
- Erro 503 Service Unavailable
- Página em branco

**Soluções:**
1. Aguardar 30-60 segundos e recarregar
2. Verificar status no Railway Dashboard
3. Fazer Restart do deployment
4. Verificar logs do Railway

---

### **Problema: "API Claude não configurada"**

**Sintomas:**
- Mensagem de erro ao gerar relatório
- API mostra "❌ Não configurada"

**Solução:**
1. Railway Dashboard → Settings → Variables
2. Add: `ANTHROPIC_API_KEY` = `sk-ant-api-xxx...`
3. Redeploy

---

### **Problema: PDF com caracteres estranhos**

**Sintomas:**
- PDF mostra "?" no lugar de á, é, ç

**Status:**
- ✅ Já corrigido no código (normalização de caracteres)
- Se ainda ocorrer, me avisar

---

### **Problema: Upload de áudio falha**

**Possíveis causas:**
1. **Arquivo muito grande:** Max 200MB
2. **Formato não suportado:** Use MP3, WAV, M4A, OGG, FLAC
3. **Timeout:** Áudio muito longo (>10 minutos)

**Soluções:**
1. Comprimir áudio
2. Converter para MP3
3. Dividir áudio em partes menores

---

### **Problema: Transcrição em branco ou errada**

**Causas:**
- Áudio com muito ruído
- Volume muito baixo
- Idioma não é português

**Solução:**
- Regravar áudio com melhor qualidade
- Aumentar volume
- Falar claramente

---

## ✅ CHECKLIST DE SUCESSO

Marque conforme testa:

**Básico (obrigatório):**
- [ ] Aplicação carrega
- [ ] API Claude configurada
- [ ] Gera relatório com texto manual
- [ ] Download MD/TXT/PDF funciona
- [ ] Dashboard mostra estatísticas
- [ ] Histórico lista relatórios

**Avançado (desejável):**
- [ ] Upload de áudio funciona
- [ ] Transcrição com Whisper funciona
- [ ] Relatório gerado a partir de áudio
- [ ] Múltiplos relatórios consecutivos
- [ ] Performance estável

**Extra (opcional):**
- [ ] Teste com áudios longos (5-10 min)
- [ ] Teste com diferentes formatos (MP3, WAV, M4A)
- [ ] Teste de carga (10+ relatórios)

---

## 📊 RELATÓRIO DE TESTES

**Ao terminar, me envie:**

```
AMBIENTE: Railway Production
URL: https://[sua-url].railway.app

TESTES EXECUTADOS:
✅ Teste 1: Dashboard - OK
✅ Teste 2: API Claude - OK
✅ Teste 3: Relatório manual - OK
✅ Teste 4: Downloads - OK
✅ Teste 5: Dashboard stats - OK
✅ Teste 6: Histórico - OK
✅ Teste 7: Upload áudio - OK (ou FALHOU com erro X)
✅ Teste 8: Carga - OK

PROBLEMAS ENCONTRADOS:
[Liste aqui qualquer problema]

OBSERVAÇÕES:
[Comentários adicionais]
```

---

## 🎉 SUCESSO TOTAL

**Se todos os testes passarem:**

🎊 **PARABÉNS!** 🎊

Seu sistema está **100% funcional** em produção no Railway!

**Próximos passos:**
1. Compartilhar URL com usuários
2. Monitorar uso e performance
3. Configurar domínio customizado (opcional)
4. Fazer backup dos relatórios periodicamente

---

**Criado:** 11/11/2025
**Autor:** Claude Code
**Status:** Pronto para testes

🚀 **Boa sorte nos testes!**
