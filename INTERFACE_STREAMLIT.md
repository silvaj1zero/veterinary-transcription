# 🎨 Interface Gráfica - Guia Completo

## ✨ Interface Streamlit - Instalada e Funcionando!

---

## 🚀 Como Iniciar

### Método 1: Clique Duplo (Mais Fácil)

```
Clique duas vezes em: iniciar_interface.bat
```

A interface abrirá automaticamente no seu navegador!

### Método 2: Linha de Comando

```bash
cd C:\Users\Zero\Desktop\veterinary-transcription
python -m streamlit run app.py
```

### Método 3: Atalho Customizado

Crie um atalho para `iniciar_interface.bat` na Área de Trabalho!

---

## 📱 Acessando a Interface

Depois de iniciar, abra no navegador:

```
http://localhost:8501
```

Se não abrir automaticamente, copie e cole este endereço no navegador.

---

## 🎯 Funcionalidades da Interface

### 1️⃣ Dashboard (📊)

**O que você vê:**
- 📊 Estatísticas em tempo real
  - Consultas de hoje
  - Total de consultas
  - Custos acumulados
  - Economia vs áudio
- 📋 Lista das últimas consultas
- 📈 Gráficos interativos
  - Tipo de atendimento (Pizza)
  - Consultas por dia (Barras)

**Para que serve:**
- Visão geral do sistema
- Acompanhar uso e custos
- Acesso rápido aos relatórios recentes

---

### 2️⃣ Nova Consulta (➕)

#### Opção A: 🎤 Processar Áudio

**Como usar:**
1. Clique em "Processar Áudio"
2. Arraste ou clique para escolher arquivo
3. Preencha dados do paciente
4. Clique "Gerar Relatório"
5. Aguarde ~5-10 minutos
6. Relatório pronto!

**Formatos aceitos:**
- MP3, WAV, M4A, OGG, FLAC

#### Opção B: 📝 Usar Transcrição

**Como usar:**
1. Clique em "Usar Transcrição"
2. Cole o texto da consulta
3. Preencha dados do paciente
4. Clique "Gerar Relatório"
5. Aguarde ~30 segundos ⚡
6. Relatório pronto!

**Vantagens:**
- 95% mais rápido
- Menor custo de processamento
- Perfeito para textos já digitados

#### Formulário do Paciente

**Campos obrigatórios (*):**
- Nome do Paciente
- Espécie (Cão/Gato/Outro)
- Raça
- Idade e Peso
- Nome do Tutor
- Motivo do Retorno
- Tipo de Atendimento

**Campos opcionais:**
- Data da Consulta (padrão = hoje)

---

### 3️⃣ Histórico (📋)

**Funcionalidades:**
- 🔍 **Buscar** por nome do paciente
- 📅 **Filtrar** por data
- 🔄 **Ordenar** (recentes, antigos, A-Z)
- 👁️ **Visualizar** relatórios
- ⬇️ **Baixar** em formato Markdown

**Como usar:**
1. Digite o nome no campo de busca
2. Selecione data (opcional)
3. Escolha ordenação
4. Expanda consulta desejada
5. Visualize ou baixe

---

### 4️⃣ Configurações (⚙️)

**O que configurar:**
- 🎤 Modelo Whisper (tiny, base, small, medium, large)
- 📊 Ver informações do sistema
- ℹ️ Ler documentação
- 🔧 Ações do sistema:
  - Limpar cache
  - Abrir pasta de relatórios
  - Ver documentação

**Informações exibidas:**
- Versão do Python
- Versão do Streamlit
- Status da API Claude
- Status do FFmpeg
- Pastas do sistema

---

## 💡 Dicas de Uso

### Dica 1: Atalho Rápido

Para consultas rápidas:
1. Abra interface
2. "Nova Consulta" → "Usar Transcrição"
3. Cole texto
4. Preencha formulário (dados salvos ficam preenchidos)
5. Gerar!

**Tempo total:** ~1 minuto

### Dica 2: Trabalho em Lote

Processando vários áudios:
1. Deixe interface aberta
2. Processe um por um
3. Use dashboard para acompanhar
4. Verifique histórico ao final

### Dica 3: Visualização Rápida

No dashboard:
- Clique em "Ver" ao lado da consulta
- Abre preview instantâneo
- Não precisa ir no histórico!

### Dica 4: Dark Mode

Quer tema escuro?
- Clique no ⚙️ no canto superior direito do Streamlit
- Settings → Theme → Dark
- Interface muda instantaneamente!

---

## 🎨 Aparência da Interface

### Tema Padrão (Light)
- Cores azuis profissionais
- Fundo branco limpo
- Cards com bordas coloridas
- Gráficos interativos

### Responsivo
- ✅ Desktop (tela grande)
- ✅ Laptop (1366x768+)
- ✅ Tablet (iPad, etc)
- ✅ Mobile (com limitações)

---

## ⚡ Performance

### Velocidade:
- **Carregamento inicial:** ~2-3 segundos
- **Troca de página:** Instantâneo
- **Upload de arquivo:** Depende do tamanho
- **Geração de relatório:**
  - Texto: 30 segundos
  - Áudio: 5-10 minutos

### Cache Inteligente:
- Streamlit faz cache automático
- Dados são reprocessados apenas quando necessário
- Use "Limpar Cache" se houver problemas

---

## 🔧 Troubleshooting

### Problema: Interface não abre

**Solução:**
```bash
# Verificar se Streamlit foi instalado
python -m pip list | findstr streamlit

# Se não estiver, instalar
python -m pip install streamlit
```

### Problema: Erro ao processar consulta

**Solução:**
1. Verifique se API Key está configurada (.env)
2. Verifique conexão com internet
3. Veja logs no terminal

### Problema: Arquivos não aparecem no histórico

**Solução:**
- Verifique se relatórios estão em `relatorios/`
- Atualize a página (F5)
- Limpe cache (Configurações)

### Problema: Gráficos não carregam

**Solução:**
```bash
# Reinstalar plotly
python -m pip install --upgrade plotly
```

---

## 📊 Comparação: Interface vs Terminal

| Recurso | Terminal | **Interface Web** |
|---------|----------|-------------------|
| Facilidade de uso | ⭐⭐ | **⭐⭐⭐⭐⭐** |
| Visual | Texto | **Gráfico moderno** |
| Dashboard | ❌ | **✅** |
| Gráficos | ❌ | **✅** |
| Upload drag-drop | ❌ | **✅** |
| Preview relatório | ❌ | **✅** |
| Histórico visual | ❌ | **✅** |
| Busca/Filtros | ❌ | **✅** |
| Multi-janela | ❌ | **✅** |
| Mobile | ❌ | **✅** |

---

## 🌐 Acessar de Outro Computador

### Na mesma rede (LAN):

1. No computador servidor, descubra o IP:
```bash
ipconfig
# Anote o IPv4 (ex: 192.168.1.100)
```

2. Inicie a interface:
```bash
streamlit run app.py --server.address 0.0.0.0
```

3. Em outro computador na mesma rede:
```
http://192.168.1.100:8501
```

### Deploy Online (Futuro):

Opções gratuitas:
- Streamlit Cloud (https://streamlit.io/cloud)
- Heroku (https://heroku.com)
- Railway (https://railway.app)

---

## 🎯 Próximas Melhorias

Já incluídas na v1.3:
- ✅ Interface gráfica completa
- ✅ Dashboard com estatísticas
- ✅ Upload de áudio
- ✅ Input de texto
- ✅ Histórico com busca
- ✅ Preview de relatórios
- ✅ Download de arquivos
- ✅ Gráficos interativos

Planejadas para futuras versões:
- [ ] Autenticação de usuários
- [ ] Exportar para PDF
- [ ] Editar relatórios gerados
- [ ] Templates personalizáveis
- [ ] Notificações por email
- [ ] Backup automático
- [ ] API REST
- [ ] App mobile

---

## 📱 Screenshots (Descrição)

### Tela 1: Dashboard
```
┌──────────────────────────────────────────┐
│  🏥 Vet Docs                    [Menu]   │
├──────────────────────────────────────────┤
│  📊 Dashboard                            │
│                                          │
│  ┌──────┬──────┬──────┬──────┐          │
│  │ 📝 5 │ 📊127│ 💰$6 │ ⚡95%│          │
│  │ Hoje │Total │Custo │Econ. │          │
│  └──────┴──────┴──────┴──────┘          │
│                                          │
│  📋 Últimas Consultas                    │
│  ┌────────────────────────────────┐      │
│  │ 09/11 14:23 | Bob | Retorno   │[Ver] │
│  │ 09/11 10:15 | Rex | Vacinação │[Ver] │
│  └────────────────────────────────┘      │
│                                          │
│  📈 Gráficos [Pizza] [Barras]           │
└──────────────────────────────────────────┘
```

### Tela 2: Nova Consulta
```
┌──────────────────────────────────────────┐
│  ➕ Nova Consulta                        │
├──────────────────────────────────────────┤
│  [🎤 Áudio] [📝 Texto]                   │
│                                          │
│  📝 Cole ou digite a transcrição:        │
│  ┌────────────────────────────────────┐  │
│  │ Olá, Dr. João aqui...              │  │
│  │ (texto da consulta)                │  │
│  └────────────────────────────────────┘  │
│                                          │
│  📋 Dados do Paciente                    │
│  Nome: [Bob          ]  Raça: [Yorkshire│
│  Espécie: [Cão ▼]       Idade: [5 anos] │
│                                          │
│  [🚀 Gerar Relatório]                    │
└──────────────────────────────────────────┘
```

---

**Versão:** 1.3 (Production Ready)
**Última atualização:** Novembro 2025
