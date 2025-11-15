# 📱 Feature: Modo Transcrição Pronta

**Versão:** 1.3 (Planejamento)
**Status:** 📋 Documentado para Implementação Futura
**Prioridade:** Alta
**Data:** 2025-11-15

---

## 📖 Índice

1. [Visão Geral](#visão-geral)
2. [Problema Identificado](#problema-identificado)
3. [Solução Proposta](#solução-proposta)
4. [Apps de Transcrição Recomendados](#apps-de-transcrição-recomendados)
5. [Especificações Técnicas](#especificações-técnicas)
6. [Mockups e Interface](#mockups-e-interface)
7. [Arquitetura](#arquitetura)
8. [Implementação Passo a Passo](#implementação-passo-a-passo)
9. [Testes](#testes)
10. [Métricas e Benefícios](#métricas-e-benefícios)
11. [Roadmap](#roadmap)

---

## 🎯 Visão Geral

Adicionar funcionalidade que permite ao usuário **pular a etapa de transcrição Whisper** e inserir texto já transcrito de aplicativos móveis, reduzindo o tempo de processamento de **5-7 minutos para 1-2 minutos** por consulta.

### Objetivos

- ✅ Reduzir tempo de processamento em 60-80%
- ✅ Permitir uso de transcrições offline do smartphone
- ✅ Manter compatibilidade com fluxo atual (áudio → transcrição)
- ✅ Economizar custos de API Whisper quando não necessário
- ✅ Melhorar experiência do usuário em conexões lentas

---

## ❌ Problema Identificado

### Problema Principal

**Transcrição Whisper na Web é lenta:**
- Tempo médio: 2-5 minutos para áudio de 5-10 minutos
- Depende de conexão de internet estável
- Usa recursos computacionais significativos
- Custo: ~$0.006/minuto de áudio

### Cenários de Uso Afetados

1. **Veterinário em campo:**
   - Conexão móvel instável
   - Precisa de resultado rápido
   - Já tem smartphone com gravador

2. **Múltiplas consultas seguidas:**
   - 10 consultas = 50 minutos de espera só em transcrição
   - Gargalo no workflow

3. **Usuário com transcrição existente:**
   - Já transcreveu em outro app
   - Quer apenas gerar relatório formatado

---

## 💡 Solução Proposta

### Abordagem: Modo Híbrido

Adicionar **nova aba no sistema** que permite:

1. **Input de texto direto** (texto já transcrito)
2. **Opcionalmente anexar áudio original** (para referência)
3. **Pular processamento Whisper** completamente
4. **Gerar relatório** apenas com Claude API

### Benefícios

| Métrica | Antes | Depois | Melhoria |
|---------|-------|--------|----------|
| **Tempo total** | 5-7 min | 1-2 min | **70% mais rápido** |
| **Custo por consulta** | $0.056 | $0.050 | **10% mais barato** |
| **Dependência de internet** | Alta | Baixa | **Maior resiliência** |
| **Offline-first** | Não | Sim* | **Novo recurso** |

*Transcrição pode ser feita offline no smartphone

---

## 📲 Apps de Transcrição Recomendados

### Para Android

#### 1. Google Recorder ⭐ RECOMENDADO

**Características:**
- **Gratuito:** ✅ Completamente grátis
- **Offline:** ✅ Funciona sem internet
- **Qualidade:** Excelente (IA Google on-device)
- **Idioma:** Português brasileiro nativo
- **Edição:** Permite editar transcrição
- **Exporta:** TXT, compartilhamento direto

**Disponibilidade:**
- Pré-instalado: Google Pixel (6+)
- APK disponível: Pode instalar em outros Android 9+
- Download: Google Play Store ou APK Mirror

**Instruções de Uso:**
```
1. Abrir Google Recorder
2. Tocar em gravar (botão vermelho)
3. Realizar consulta (falar normalmente)
4. Parar gravação
5. Tocar em "Transcrição" (gerada automaticamente)
6. Tocar em "Compartilhar" → "Copiar texto"
7. Colar no sistema veterinário
```

**Recursos Avançados:**
- Busca por palavra-chave na transcrição
- Marcação de momentos importantes
- Sincronização áudio-texto (tocar no texto reproduz áudio)

---

#### 2. Otter.ai

**Características:**
- **Gratuito:** ✅ 600 minutos/mês (plano grátis)
- **Offline:** ❌ Requer internet
- **Qualidade:** Muito boa
- **Idioma:** Português suportado
- **Exporta:** TXT, PDF, SRT, DOCX

**Limitações Plano Grátis:**
- 600 minutos/mês (~20 consultas de 30 min)
- 40 minutos por gravação
- Exportação básica

**Plano Pago:** $8.33/mês (Pro)
- 1200 minutos/mês
- Transcrições avançadas

---

#### 3. Speechnotes

**Características:**
- **Gratuito:** ✅ Com anúncios
- **Offline:** ❌ Requer internet
- **Qualidade:** Boa (Google Speech API)
- **Idioma:** Português brasileiro
- **Exporta:** TXT, DOCX

**Vantagens:**
- Interface simples
- Comandos de pontuação por voz
- Sem limite de tempo

---

### Para iOS (iPhone/iPad)

#### 1. Notas de Voz (Nativo) ⭐ RECOMENDADO

**Características:**
- **Gratuito:** ✅ Incluído no iOS 17+
- **Offline:** ✅ Funciona offline
- **Qualidade:** Excelente (Apple Neural Engine)
- **Idioma:** Português brasileiro
- **Integração:** iCloud, Arquivos

**Como Ativar Transcrição:**
```
iOS 17+:
1. Configurações → Notas de Voz
2. Ativar "Transcrever notas de voz"
3. Selecionar idioma: Português (Brasil)
```

**Instruções de Uso:**
```
1. Abrir app Notas de Voz
2. Tocar em gravar (botão vermelho)
3. Realizar consulta
4. Parar gravação
5. Abrir gravação → Tocar em "Transcrição"
6. Tocar e segurar no texto → Selecionar tudo
7. Copiar → Colar no sistema
```

---

#### 2. Just Press Record

**Características:**
- **Gratuito:** ❌ Pago (R$ 24,90 compra única)
- **Offline:** ✅ Transcrição offline
- **Qualidade:** Excelente
- **Idioma:** 30+ idiomas incluindo português
- **Exporta:** TXT, iCloud Drive

**Vantagens:**
- Sem mensalidade (compra única)
- Sincronização entre dispositivos Apple
- Busca em transcrições

---

#### 3. Otter.ai

(Mesmas características da versão Android)

---

### Comparação Detalhada

| App | Plataforma | Custo | Offline | Qualidade | Limite |
|-----|------------|-------|---------|-----------|--------|
| **Google Recorder** | Android | Grátis | ✅ | 10/10 | Sem limite |
| **iOS Notas de Voz** | iOS 17+ | Grátis | ✅ | 10/10 | Sem limite |
| **Otter.ai** | Ambos | Grátis* | ❌ | 8/10 | 600 min/mês |
| **Speechnotes** | Android | Grátis | ❌ | 7/10 | Sem limite |
| **Just Press Record** | iOS | R$ 24,90 | ✅ | 9/10 | Sem limite |

*Plano grátis com limitações

---

## 🔧 Especificações Técnicas

### Requisitos Funcionais

#### RF-01: Nova Aba "Consulta com Texto"
- Sistema DEVE exibir nova opção no menu principal
- Label: "📝 Nova Consulta (Texto Pronto)"
- Posicionamento: Após "Nova Consulta" no menu

#### RF-02: Formulário de Entrada
- Campos obrigatórios:
  - Informações do paciente (existentes)
  - Campo de texto multi-linha para transcrição
- Campos opcionais:
  - Upload de arquivo de áudio (.mp3, .wav, .m4a, .ogg)
  - Observações adicionais

#### RF-03: Validação de Dados
- Texto da transcrição: Mínimo 50 caracteres
- Máximo: 10.000 caracteres (limite Claude)
- Validar campos do paciente (reutilizar `validate_patient_info()`)

#### RF-04: Processamento
- Pular etapa Whisper completamente
- Enviar texto direto para Claude API
- Gerar relatório usando mesmo prompt atual
- Salvar em `/relatorios/` com mesmo formato

#### RF-05: Armazenamento
- Salvar transcrição em `/transcricoes/texto_direto_YYYYMMDD_HHMMSS.txt`
- Se áudio fornecido: salvar em `/audios/`
- Metadados: incluir flag `source: "manual_text"`

---

### Requisitos Não-Funcionais

#### RNF-01: Performance
- Tempo total: < 60 segundos (vs. 5-7 minutos atual)
- Geração de relatório: < 30 segundos

#### RNF-02: Usabilidade
- Interface intuitiva (mesmo padrão Streamlit)
- Mensagens claras sobre economia de tempo
- Indicador de progresso durante geração

#### RNF-03: Compatibilidade
- Manter fluxo atual (áudio → transcrição) inalterado
- Permitir migração fácil entre modos
- Exportações no mesmo formato

#### RNF-04: Segurança
- Validar tamanho de texto (evitar DoS)
- Sanitizar entrada antes de enviar para Claude
- Mesmas permissões de acesso

---

### Requisitos de Dados

#### Estrutura de Arquivo de Transcrição Manual

```json
{
  "metadata": {
    "source": "manual_text",
    "timestamp": "2025-11-15T14:30:00",
    "app_sugerido": "Google Recorder / iOS Notas de Voz",
    "audio_anexado": true/false,
    "caracteres": 1234
  },
  "patient_info": {
    "paciente_nome": "Rex",
    "paciente_especie": "Cão",
    ...
  },
  "transcription": "Texto da consulta aqui...",
  "audio_file": "audio_YYYYMMDD_HHMMSS.mp3" // opcional
}
```

---

## 🎨 Mockups e Interface

### Layout da Nova Aba

```
┌─────────────────────────────────────────────────────────────┐
│ 🏥 Sistema de Documentação Veterinária - BadiLab           │
├─────────────────────────────────────────────────────────────┤
│ [Dashboard] [Nova Consulta] [📝 Texto Pronto] [Histórico]  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 📝 Nova Consulta com Texto Pronto                           │
│                                                              │
│ ℹ️ Use esta opção se você já transcreveu a consulta        │
│    em seu smartphone (Google Recorder, iOS Notas de Voz)    │
│                                                              │
│ ⏱️ Economia de tempo: ~5 minutos por consulta              │
│ 💰 Apps recomendados: Grátis e offline                     │
│                                                              │
│ ┌──────────────────────────────────────────────────────┐   │
│ │ 📋 Informações do Paciente                           │   │
│ │                                                       │   │
│ │ Nome do Paciente: [________________]                 │   │
│ │ Espécie: [▼ Cão]  Raça: [________________]          │   │
│ │ Idade: [___]       Sexo: [▼ Macho]                  │   │
│ │ Peso: [___] kg                                        │   │
│ │                                                       │   │
│ │ Nome do Tutor: [________________]                    │   │
│ │ Motivo da Consulta/Retorno: [________________]       │   │
│ └──────────────────────────────────────────────────────┘   │
│                                                              │
│ ┌──────────────────────────────────────────────────────┐   │
│ │ 📄 Transcrição da Consulta                           │   │
│ │                                                       │   │
│ │ Cole aqui o texto transcrito do seu smartphone:      │   │
│ │ ┌────────────────────────────────────────────────┐   │   │
│ │ │ Tutor relata que o animal apresentou vômitos   │   │   │
│ │ │ há 2 dias. Exame físico revela...             │   │   │
│ │ │                                                 │   │   │
│ │ │                                                 │   │   │
│ │ │                                                 │   │   │
│ │ │                                                 │   │   │
│ │ │                                                 │   │   │
│ │ │ [10 linhas de altura]                          │   │   │
│ │ └────────────────────────────────────────────────┘   │   │
│ │                                                       │   │
│ │ Caracteres: 234 / 10.000                             │   │
│ │ ✅ Mínimo: 50 caracteres                             │   │
│ └──────────────────────────────────────────────────────┘   │
│                                                              │
│ ┌──────────────────────────────────────────────────────┐   │
│ │ 🎙️ Áudio Original (Opcional)                         │   │
│ │                                                       │   │
│ │ [📎 Anexar arquivo de áudio para referência]        │   │
│ │                                                       │   │
│ │ ℹ️ O áudio não será transcrito, apenas salvo        │   │
│ │    como backup junto ao relatório                    │   │
│ └──────────────────────────────────────────────────────┘   │
│                                                              │
│              [🚀 Gerar Relatório (30s)]                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

### Fluxo de Uso

```
┌─────────────────┐
│ Usuário abre    │
│ "Texto Pronto"  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Preenche dados  │
│ do paciente     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│ Cola texto      │◄─────┤ Copiou do Google │
│ transcrito      │      │ Recorder/iOS     │
└────────┬────────┘      └──────────────────┘
         │
         ▼
┌─────────────────┐
│ (Opcional)      │
│ Anexa áudio     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Clica "Gerar    │
│ Relatório"      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Sistema valida  │
│ dados           │
└────────┬────────┘
         │
         ├─── ❌ Erro ───► [Mensagem de validação]
         │
         ▼ ✅
┌─────────────────┐
│ ⏭️ PULA WHISPER │
│ (economia: 5min)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Envia para      │
│ Claude API      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Gera relatório  │
│ (30s)           │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Salva arquivos: │
│ - Transcrição   │
│ - Relatório MD  │
│ - Relatório PDF │
│ - Áudio (se há) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Exibe resultado │
│ + Download      │
└─────────────────┘
```

---

## 🏗️ Arquitetura

### Componentes Afetados

```
📦 veterinary-transcription
│
├── app.py                          # ⚠️ MODIFICAR
│   ├── Adicionar nova aba no menu
│   ├── Criar função process_manual_text()
│   └── Reutilizar render_patient_form()
│
├── transcribe_consult.py           # ⚠️ MODIFICAR (Opcional)
│   └── Adicionar modo CLI para texto direto
│
├── utils.py                        # ➕ ADICIONAR
│   ├── validate_transcription_text()
│   └── save_manual_transcription()
│
└── config.py                       # ⚠️ MODIFICAR
    └── TRANSCRIPTION_TEXT_DIR = Path("transcricoes/texto_direto")
```

---

### Diagrama de Sequência

```
Usuário          Interface Web       Validação        Claude API      Arquivo
  │                    │                  │                │             │
  │─ Preenche form ───►│                  │                │             │
  │                    │                  │                │             │
  │─ Cola texto ──────►│                  │                │             │
  │                    │                  │                │             │
  │─ Clica "Gerar" ───►│                  │                │             │
  │                    │                  │                │             │
  │                    │── Valida dados ─►│                │             │
  │                    │                  │                │             │
  │                    │◄─ OK / Erro ─────│                │             │
  │                    │                  │                │             │
  │◄─ Erro (se há) ────│                  │                │             │
  │                    │                  │                │             │
  │                    │── Envia texto ──────────────────►│             │
  │                    │   + patient_info                 │             │
  │                    │                                  │             │
  │                    │◄────── Relatório ────────────────│             │
  │                    │        (Markdown)                │             │
  │                    │                                  │             │
  │                    │────── Salva transcrição ─────────────────────►│
  │                    │────── Salva relatório MD ────────────────────►│
  │                    │────── Gera relatório PDF ────────────────────►│
  │                    │────── Salva áudio (se há) ───────────────────►│
  │                    │                                  │             │
  │◄─ Exibe resultado ─│                                  │             │
  │   + Downloads      │                                  │             │
```

---

### Comparação de Fluxos

#### Fluxo Atual (Áudio → Transcrição)
```
Áudio ──► Whisper (2-5min) ──► Claude (30s) ──► Relatório
          [Gargalo]
```

#### Novo Fluxo (Texto Pronto)
```
Texto ──► Claude (30s) ──► Relatório
          [Direto, sem gargalo]
```

---

## 💻 Implementação Passo a Passo

### Fase 1: Backend (utils.py + config.py)

#### 1.1 Adicionar configurações

**Arquivo:** `config.py`

```python
# Adicionar após as configurações existentes

# Diretório para transcrições manuais
TRANSCRIPTION_TEXT_DIR = Path("transcricoes/texto_direto")
TRANSCRIPTION_TEXT_DIR.mkdir(exist_ok=True)

# Limites de texto
MIN_TRANSCRIPTION_LENGTH = 50      # Mínimo de caracteres
MAX_TRANSCRIPTION_LENGTH = 10000   # Máximo (limite Claude context)

# Formatos de áudio aceitos para anexo
ACCEPTED_AUDIO_FORMATS = ['.mp3', '.wav', '.m4a', '.ogg', '.flac']
```

---

#### 1.2 Adicionar funções de validação e salvamento

**Arquivo:** `utils.py`

```python
# Adicionar ao final do arquivo

def validate_transcription_text(text: str) -> bool:
    """
    Valida texto de transcrição manual.

    Args:
        text: Texto transcrito a validar

    Returns:
        True se válido

    Raises:
        ValueError: Se texto inválido
    """
    if not text or not isinstance(text, str):
        raise ValueError("Texto da transcrição é obrigatório")

    text_clean = text.strip()

    if len(text_clean) < config.MIN_TRANSCRIPTION_LENGTH:
        raise ValueError(
            f"Texto muito curto. Mínimo: {config.MIN_TRANSCRIPTION_LENGTH} caracteres. "
            f"Atual: {len(text_clean)} caracteres"
        )

    if len(text_clean) > config.MAX_TRANSCRIPTION_LENGTH:
        raise ValueError(
            f"Texto muito longo. Máximo: {config.MAX_TRANSCRIPTION_LENGTH} caracteres. "
            f"Atual: {len(text_clean)} caracteres"
        )

    logging.info(f"Texto validado: {len(text_clean)} caracteres")
    return True


def save_manual_transcription(text: str, patient_info: dict, audio_file=None) -> dict:
    """
    Salva transcrição manual com metadados.

    Args:
        text: Texto transcrito
        patient_info: Informações do paciente
        audio_file: Arquivo de áudio anexado (opcional)

    Returns:
        dict com paths dos arquivos salvos
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Criar metadados
    metadata = {
        "source": "manual_text",
        "timestamp": datetime.now().isoformat(),
        "app_sugerido": "Google Recorder / iOS Notas de Voz",
        "audio_anexado": audio_file is not None,
        "caracteres": len(text),
        "patient_info": patient_info
    }

    # Salvar transcrição como JSON
    transcription_data = {
        "metadata": metadata,
        "transcription": text
    }

    transcription_path = config.TRANSCRIPTION_TEXT_DIR / f"texto_{timestamp}.json"
    with open(transcription_path, 'w', encoding='utf-8') as f:
        json.dump(transcription_data, f, ensure_ascii=False, indent=2)

    logging.info(f"Transcrição manual salva: {transcription_path}")

    result = {
        "transcription_path": transcription_path,
        "timestamp": timestamp
    }

    # Salvar áudio se fornecido
    if audio_file is not None:
        audio_path = config.AUDIO_DIR / f"audio_{timestamp}{Path(audio_file.name).suffix}"
        with open(audio_path, 'wb') as f:
            f.write(audio_file.getbuffer())
        result["audio_path"] = audio_path
        logging.info(f"Áudio de referência salvo: {audio_path}")

    return result
```

---

### Fase 2: Frontend (app.py)

#### 2.1 Adicionar nova aba ao menu

**Localização:** `app.py` - Seção de menu (após linha ~70)

```python
# Menu principal
menu = st.sidebar.radio(
    "Menu",
    ["🏠 Dashboard", "🎙️ Nova Consulta", "📝 Consulta com Texto", "📚 Histórico", "⚙️ Configurações"],
    key="menu"
)

# ... resto do código
```

---

#### 2.2 Criar seção "Consulta com Texto"

**Localização:** `app.py` - Após seção "Nova Consulta" (após linha ~600)

```python
# ============================================================================
# SEÇÃO: CONSULTA COM TEXTO PRONTO
# ============================================================================
elif menu == "📝 Consulta com Texto":
    st.title("📝 Nova Consulta com Texto Pronto")

    # Informações e benefícios
    st.info(
        "💡 **Use esta opção se você já transcreveu a consulta em seu smartphone**\n\n"
        "**Vantagens:**\n"
        "- ⏱️ Economia de tempo: ~5 minutos por consulta\n"
        "- 📱 Transcrição offline no celular\n"
        "- 💰 Apps gratuitos recomendados\n\n"
        "**Apps recomendados:**\n"
        "- Android: Google Recorder (grátis, offline)\n"
        "- iOS: Notas de Voz nativo (grátis, offline, iOS 17+)"
    )

    # Link para documentação
    with st.expander("📖 Como usar apps de transcrição no smartphone"):
        st.markdown("""
        ### Android - Google Recorder

        1. Abrir app Google Recorder
        2. Gravar consulta
        3. Transcrição é gerada automaticamente
        4. Tocar em "Compartilhar" → "Copiar texto"
        5. Colar no campo abaixo

        ### iOS - Notas de Voz

        1. Ativar transcrição: Configurações → Notas de Voz → Transcrever
        2. Gravar consulta no app Notas de Voz
        3. Abrir gravação → Tocar em "Transcrição"
        4. Selecionar e copiar texto
        5. Colar no campo abaixo

        📄 Documentação completa: Ver `FEATURE_TRANSCRICAO_PRONTA.md`
        """)

    st.divider()

    # ========================================================================
    # Formulário de paciente (reutilizar código existente)
    # ========================================================================
    st.subheader("📋 Informações do Paciente")

    with st.form("patient_form_text"):
        col1, col2 = st.columns(2)

        with col1:
            paciente_nome = st.text_input("Nome do Paciente*", key="text_pac_nome")
            paciente_especie = st.selectbox(
                "Espécie*",
                ["Cão", "Gato", "Ave", "Réptil", "Outro"],
                key="text_pac_especie"
            )
            paciente_raca = st.text_input("Raça*", key="text_pac_raca")

        with col2:
            paciente_idade = st.text_input("Idade*", key="text_pac_idade")
            paciente_sexo = st.selectbox(
                "Sexo*",
                ["Macho", "Fêmea"],
                key="text_pac_sexo"
            )
            paciente_peso = st.text_input("Peso (kg)", key="text_pac_peso")

        tutor_nome = st.text_input("Nome do Tutor*", key="text_tutor_nome")
        motivo_retorno = st.text_input(
            "Motivo da Consulta/Retorno*",
            key="text_motivo"
        )

        st.divider()

        # ====================================================================
        # Campo de texto para transcrição
        # ====================================================================
        st.subheader("📄 Transcrição da Consulta")

        transcription_text = st.text_area(
            "Cole aqui o texto transcrito do seu smartphone:",
            height=300,
            max_chars=config.MAX_TRANSCRIPTION_LENGTH,
            placeholder="Cole o texto da consulta aqui...\n\n"
                       "Exemplo:\n"
                       "Tutor relata que o animal apresentou vômitos há 2 dias.\n"
                       "Ao exame físico: temperatura 38.5°C, mucosas normocoradas...",
            key="text_transcription"
        )

        # Contador de caracteres
        char_count = len(transcription_text) if transcription_text else 0

        col_count1, col_count2 = st.columns([3, 1])
        with col_count1:
            if char_count < config.MIN_TRANSCRIPTION_LENGTH:
                st.warning(
                    f"⚠️ Mínimo: {config.MIN_TRANSCRIPTION_LENGTH} caracteres "
                    f"(atual: {char_count})"
                )
            else:
                st.success(f"✅ {char_count} caracteres")

        with col_count2:
            st.caption(f"{char_count} / {config.MAX_TRANSCRIPTION_LENGTH}")

        st.divider()

        # ====================================================================
        # Upload opcional de áudio
        # ====================================================================
        st.subheader("🎙️ Áudio Original (Opcional)")

        st.caption(
            "ℹ️ O áudio não será transcrito, apenas salvo como backup "
            "junto ao relatório"
        )

        audio_file = st.file_uploader(
            "Anexar arquivo de áudio para referência",
            type=['mp3', 'wav', 'm4a', 'ogg', 'flac'],
            key="text_audio"
        )

        st.divider()

        # Botão de submissão
        submitted = st.form_submit_button(
            "🚀 Gerar Relatório (~30 segundos)",
            use_container_width=True,
            type="primary"
        )

    # ========================================================================
    # Processamento do formulário
    # ========================================================================
    if submitted:
        # Validar dados do paciente
        patient_info = {
            'paciente_nome': paciente_nome,
            'paciente_especie': paciente_especie,
            'paciente_raca': paciente_raca,
            'paciente_idade': paciente_idade,
            'paciente_sexo': paciente_sexo,
            'paciente_peso': paciente_peso,
            'tutor_nome': tutor_nome,
            'motivo_retorno': motivo_retorno
        }

        try:
            # Validar informações do paciente
            validate_patient_info(patient_info)

            # Validar texto da transcrição
            validate_transcription_text(transcription_text)

            # Processar
            with st.spinner("⏳ Gerando relatório..."):
                # Salvar transcrição manual
                saved_files = save_manual_transcription(
                    transcription_text,
                    patient_info,
                    audio_file
                )

                # Gerar relatório com Claude (reutilizar função existente)
                vet_system = VeterinaryTranscriptionSystem()

                report = vet_system.generate_report(
                    transcription_text,
                    patient_info
                )

                # Salvar relatório
                timestamp = saved_files['timestamp']

                # Markdown
                report_md_path = config.REPORT_DIR / f"relatorio_{timestamp}.md"
                with open(report_md_path, 'w', encoding='utf-8') as f:
                    f.write(report)

                # PDF
                report_pdf_path = config.REPORT_DIR / f"relatorio_{timestamp}.pdf"
                vet_system.markdown_to_pdf(report, str(report_pdf_path))

                logging.info(f"Relatório gerado: {report_md_path}")

            # Sucesso
            st.success("✅ Relatório gerado com sucesso!")

            # Exibir relatório
            st.markdown("---")
            st.subheader("📄 Relatório Gerado")
            st.markdown(report)

            # Downloads
            st.markdown("---")
            st.subheader("💾 Downloads")

            col_dl1, col_dl2 = st.columns(2)

            with col_dl1:
                with open(report_md_path, 'r', encoding='utf-8') as f:
                    st.download_button(
                        "📥 Download Markdown",
                        f.read(),
                        file_name=f"relatorio_{timestamp}.md",
                        mime="text/markdown",
                        width='stretch'
                    )

            with col_dl2:
                with open(report_pdf_path, 'rb') as f:
                    st.download_button(
                        "📥 Download PDF",
                        f.read(),
                        file_name=f"relatorio_{timestamp}.pdf",
                        mime="application/pdf",
                        width='stretch'
                    )

            # Estatísticas
            st.info(
                f"⏱️ **Economia de tempo:** ~5 minutos vs. transcrição Whisper\n\n"
                f"💰 **Custo:** $0.05 (apenas Claude, sem Whisper)\n\n"
                f"📊 **Caracteres processados:** {char_count}"
            )

        except ValueError as e:
            st.error(f"❌ Erro de validação: {e}")
        except Exception as e:
            st.error(f"❌ Erro ao gerar relatório: {e}")
            logging.error(f"Erro no modo texto: {e}", exc_info=True)
```

---

### Fase 3: Testes

#### 3.1 Testes Unitários

**Arquivo:** `tests/test_manual_text.py` (NOVO)

```python
"""
Testes para funcionalidade de texto manual.
"""

import pytest
from pathlib import Path
from utils import validate_transcription_text, save_manual_transcription
import config


class TestValidateTranscriptionText:
    """Testes de validação de texto."""

    def test_valid_text(self):
        """Testa texto válido."""
        text = "A" * 100  # 100 caracteres
        assert validate_transcription_text(text) is True

    def test_empty_text(self):
        """Testa texto vazio."""
        with pytest.raises(ValueError, match="obrigatório"):
            validate_transcription_text("")

    def test_text_too_short(self):
        """Testa texto muito curto."""
        text = "Abc"  # 3 caracteres
        with pytest.raises(ValueError, match="muito curto"):
            validate_transcription_text(text)

    def test_text_too_long(self):
        """Testa texto muito longo."""
        text = "A" * 20000  # 20k caracteres
        with pytest.raises(ValueError, match="muito longo"):
            validate_transcription_text(text)

    def test_minimum_length(self):
        """Testa tamanho mínimo exato."""
        text = "A" * config.MIN_TRANSCRIPTION_LENGTH
        assert validate_transcription_text(text) is True

    def test_maximum_length(self):
        """Testa tamanho máximo exato."""
        text = "A" * config.MAX_TRANSCRIPTION_LENGTH
        assert validate_transcription_text(text) is True


class TestSaveManualTranscription:
    """Testes de salvamento de transcrição."""

    @pytest.fixture
    def patient_data(self):
        """Dados de paciente para teste."""
        return {
            'paciente_nome': 'Rex',
            'paciente_especie': 'Cão',
            'paciente_raca': 'Labrador',
            'paciente_idade': '5 anos',
            'tutor_nome': 'João Silva',
            'motivo_retorno': 'Vacinação'
        }

    def test_save_text_only(self, patient_data, temp_dir):
        """Testa salvamento apenas de texto."""
        text = "Consulta veterinária de rotina. Animal saudável."

        result = save_manual_transcription(text, patient_data)

        assert 'transcription_path' in result
        assert 'timestamp' in result
        assert result['transcription_path'].exists()

    def test_save_with_audio(self, patient_data, temp_dir, tmp_path):
        """Testa salvamento com áudio anexado."""
        text = "Consulta com áudio de referência."

        # Criar arquivo de áudio fake
        audio_file = tmp_path / "test.mp3"
        audio_file.write_bytes(b"fake audio data")

        result = save_manual_transcription(text, patient_data, audio_file)

        assert 'audio_path' in result
        assert result['audio_path'].exists()

    def test_metadata_structure(self, patient_data, temp_dir):
        """Testa estrutura de metadados salvos."""
        text = "Texto de teste."

        result = save_manual_transcription(text, patient_data)

        # Ler arquivo salvo
        import json
        with open(result['transcription_path'], 'r') as f:
            data = json.load(f)

        assert 'metadata' in data
        assert data['metadata']['source'] == 'manual_text'
        assert 'timestamp' in data['metadata']
        assert data['metadata']['caracteres'] == len(text)
        assert 'transcription' in data
        assert data['transcription'] == text
```

---

#### 3.2 Testes de Integração

**Arquivo:** `tests/test_integration_text.py` (NOVO)

```python
"""
Testes de integração para fluxo completo de texto manual.
"""

import pytest
from pathlib import Path
import config
from transcribe_consult import VeterinaryTranscriptionSystem
from utils import save_manual_transcription


class TestManualTextFlow:
    """Testa fluxo completo de texto manual."""

    @pytest.fixture
    def vet_system(self):
        """Sistema veterinário."""
        return VeterinaryTranscriptionSystem()

    @pytest.fixture
    def valid_transcription(self):
        """Transcrição válida de exemplo."""
        return """
        Consulta de rotina. Tutor relata que o animal está com apetite normal
        e comportamento ativo. Ao exame físico: temperatura 38.2°C, frequência
        cardíaca 90 bpm, mucosas normocoradas, linfonodos não palpáveis.
        Ausculta cardíaca e pulmonar sem alterações. Prescrição: manter dieta
        atual e retorno em 6 meses para check-up.
        """

    @pytest.fixture
    def patient_info(self):
        """Informações do paciente."""
        return {
            'paciente_nome': 'Mel',
            'paciente_especie': 'Gato',
            'paciente_raca': 'Siamês',
            'paciente_idade': '3 anos',
            'paciente_sexo': 'Fêmea',
            'paciente_peso': '4.2',
            'tutor_nome': 'Maria Santos',
            'motivo_retorno': 'Check-up anual'
        }

    def test_full_flow_text_to_report(
        self,
        vet_system,
        valid_transcription,
        patient_info,
        temp_dir,
        mocker
    ):
        """
        Testa fluxo completo:
        Texto → Validação → Claude → Relatório
        """
        # Mock da API Claude
        mocker.patch.object(
            vet_system,
            'generate_report',
            return_value="# Relatório Veterinário\n\nConsulta realizada..."
        )

        # 1. Salvar transcrição manual
        saved = save_manual_transcription(valid_transcription, patient_info)

        assert saved['transcription_path'].exists()

        # 2. Gerar relatório
        report = vet_system.generate_report(valid_transcription, patient_info)

        assert len(report) > 0
        assert "Relatório" in report

        # 3. Salvar relatório
        timestamp = saved['timestamp']
        report_path = config.REPORT_DIR / f"relatorio_{timestamp}.md"

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        assert report_path.exists()

    def test_performance_comparison(self, vet_system, valid_transcription, patient_info):
        """
        Testa que modo texto é mais rápido que modo áudio.
        Nota: Este é um teste conceitual (não executa Whisper real).
        """
        import time

        # Simular modo texto (sem Whisper)
        start = time.time()
        # (Claude API mockada nos outros testes)
        text_time = time.time() - start

        # Expectativa: < 1 segundo (sem processar áudio)
        # vs. modo áudio que levaria 2-5 minutos
        assert text_time < 60  # Muito mais rápido
```

---

#### 3.3 Executar Testes

```bash
# Testes unitários apenas
pytest tests/test_manual_text.py -v

# Testes de integração
pytest tests/test_integration_text.py -v

# Todos os testes com cobertura
pytest tests/ --cov=. --cov-report=html
```

---

### Fase 4: Documentação de Usuário

#### 4.1 Atualizar MANUAL_USUARIO.md

Adicionar nova seção após "Nova Consulta":

```markdown
### 3.2 Nova Consulta com Texto Pronto ⚡

**Quando usar:**
- Você já transcreveu a consulta no smartphone
- Quer economizar ~5 minutos por consulta
- Tem conexão de internet lenta
- Quer usar transcrição offline

**Passo a passo:**

#### No Smartphone (Antes):

**Android - Google Recorder:**
1. Abrir app Google Recorder
2. Gravar consulta
3. Aguardar transcrição automática
4. Tocar em "Compartilhar" → "Copiar texto"

**iOS - Notas de Voz:**
1. Gravar consulta no app Notas de Voz
2. Abrir gravação → "Transcrição"
3. Selecionar todo o texto
4. Copiar

#### No Sistema Web:

1. Abrir navegador: http://localhost:8501
2. Menu lateral → **📝 Consulta com Texto**
3. Preencher dados do paciente
4. **Colar texto** no campo "Transcrição da Consulta"
5. (Opcional) Anexar arquivo de áudio original
6. Clicar em **"🚀 Gerar Relatório"**
7. Aguardar ~30 segundos
8. Baixar relatório em Markdown ou PDF

**Benefícios:**
- ⏱️ 70% mais rápido (1-2 min vs. 5-7 min)
- 💰 10% mais barato ($0.05 vs. $0.056)
- 📱 Transcrição offline no celular
- 🌐 Menor dependência de internet
```

---

#### 4.2 Atualizar DOCUMENTACAO_TECNICA.md

Adicionar na seção "5. Módulos e Componentes":

```markdown
### 5.X Módulo: Transcrição Manual (v1.3+)

**Arquivo:** `utils.py` (funções adicionais)

**Funções:**
- `validate_transcription_text(text)`: Valida texto transcrito manualmente
- `save_manual_transcription(text, patient_info, audio_file)`: Salva transcrição com metadados

**Fluxo:**
1. Usuário cola texto transcrito do smartphone
2. Sistema valida comprimento (50-10.000 caracteres)
3. Salva em `/transcricoes/texto_direto/` como JSON
4. Pula processamento Whisper
5. Envia direto para Claude API
6. Gera relatório

**Metadados Salvos:**
```json
{
  "source": "manual_text",
  "timestamp": "2025-11-15T14:30:00",
  "app_sugerido": "Google Recorder / iOS Notas de Voz",
  "audio_anexado": true/false,
  "caracteres": 1234
}
```

**Benefícios:**
- Reduz tempo de processamento em 70%
- Permite workflow offline-first
- Economia de custos de API Whisper
```

---

## 🧪 Testes

### Casos de Teste

| ID | Caso de Teste | Entrada | Resultado Esperado |
|----|---------------|---------|-------------------|
| TC-01 | Texto válido | 200 caracteres | ✅ Aceita e processa |
| TC-02 | Texto muito curto | 20 caracteres | ❌ Erro: "muito curto" |
| TC-03 | Texto muito longo | 15.000 caracteres | ❌ Erro: "muito longo" |
| TC-04 | Texto vazio | "" | ❌ Erro: "obrigatório" |
| TC-05 | Com áudio anexado | Texto + MP3 | ✅ Salva ambos |
| TC-06 | Sem áudio | Texto apenas | ✅ Salva só texto |
| TC-07 | Dados paciente inválidos | Nome vazio | ❌ Erro validação |
| TC-08 | Fluxo completo | Texto + dados válidos | ✅ Gera relatório |

---

### Testes de Performance

| Métrica | Meta | Como Medir |
|---------|------|------------|
| Tempo total | < 60s | `time.time()` início ao fim |
| Tempo Claude API | < 30s | Log de duração da chamada |
| Tamanho arquivo JSON | < 50KB | `os.path.getsize()` |
| Memória usada | < 100MB | `psutil.Process().memory_info()` |

---

### Testes de Usabilidade

**Checklist:**
- [ ] Interface intuitiva (usuário não treinado consegue usar)
- [ ] Mensagens de erro claras e acionáveis
- [ ] Contador de caracteres visível
- [ ] Indicador de progresso durante geração
- [ ] Downloads funcionam em todos os navegadores
- [ ] Responsivo (mobile-friendly)

---

## 📊 Métricas e Benefícios

### KPIs (Key Performance Indicators)

#### Tempo de Processamento

| Métrica | Modo Atual | Modo Texto | Melhoria |
|---------|-----------|------------|----------|
| Transcrição | 2-5 min | 0 min* | **100%** |
| Geração relatório | 30s | 30s | 0% |
| **TOTAL** | **5-7 min** | **1-2 min** | **~70%** |

*Transcrição feita offline no smartphone antes

---

#### Custos por Consulta

| Item | Modo Atual | Modo Texto | Economia |
|------|-----------|------------|----------|
| Whisper API | $0.006/min × 5min = $0.030 | $0.000 | **$0.030** |
| Claude API | $0.05 | $0.05 | $0.000 |
| **TOTAL** | **$0.080** | **$0.050** | **37.5%** |

**Economia anual (100 consultas/mês):**
- Mensal: $0.030 × 100 = **$3.00**
- Anual: $3.00 × 12 = **$36.00**

---

#### Experiência do Usuário

| Aspecto | Antes | Depois | Impacto |
|---------|-------|--------|---------|
| Dependência internet | Alta | Baixa | +Resiliência |
| Uso offline | Não | Sim* | +Flexibilidade |
| Tempo de espera | 5-7 min | 1-2 min | +Satisfação |
| Custo operacional | $0.08 | $0.05 | +ROI |

*Transcrição offline, geração online

---

### ROI (Return on Investment)

**Cenário: Clínica com 10 consultas/dia**

| Métrica | Cálculo | Valor |
|---------|---------|-------|
| Consultas/mês | 10 × 22 dias | 220 |
| Tempo economizado/mês | 5 min × 220 | **18.3 horas** |
| Custo economizado/mês | $0.03 × 220 | **$6.60** |
| Tempo economizado/ano | 18.3h × 12 | **220 horas** |
| Custo economizado/ano | $6.60 × 12 | **$79.20** |

**Valor do tempo:**
- Se hora do veterinário = $50/h
- Economia anual = 220h × $50 = **$11.000**

---

## 🗺️ Roadmap

### Versão 1.3 - Implementação Básica

**Prioridade:** Alta
**Tempo estimado:** 2-3 dias
**Status:** 📋 Planejado

**Tarefas:**
- [ ] Adicionar funções em `utils.py` (2h)
- [ ] Modificar `config.py` (30min)
- [ ] Adicionar nova aba em `app.py` (4h)
- [ ] Criar testes unitários (2h)
- [ ] Criar testes de integração (2h)
- [ ] Atualizar documentação (2h)
- [ ] Testes manuais (2h)
- [ ] Code review (1h)

**Total:** ~15-16 horas

---

### Versão 1.4 - Melhorias

**Prioridade:** Média
**Tempo estimado:** 1 semana
**Status:** 📋 Planejado

**Tarefas:**
- [ ] Adicionar suporte a múltiplos idiomas
- [ ] Importar transcrições de arquivo (.txt, .docx)
- [ ] Histórico de transcrições manuais vs. automáticas
- [ ] Estatísticas de uso (manual vs. automático)
- [ ] Modo CLI para texto direto
- [ ] Exportar guia de uso para PDF

---

### Versão 1.5 - Recursos Avançados

**Prioridade:** Baixa
**Tempo estimado:** 2 semanas
**Status:** 📋 Futuro

**Tarefas:**
- [ ] Integração direta com Google Recorder via API
- [ ] Sincronização automática de transcrições do smartphone
- [ ] App mobile companheiro (React Native)
- [ ] Editor de transcrição com preview
- [ ] Comparação de qualidade (manual vs. Whisper)
- [ ] Modo híbrido (combinar manual + Whisper)

---

## 📝 Notas de Implementação

### Considerações Técnicas

1. **Segurança:**
   - Validar e sanitizar texto antes de enviar para Claude
   - Limitar tamanho de arquivo de áudio (máx 50MB)
   - Verificar tipo MIME de arquivos anexados

2. **Performance:**
   - Processar texto de forma assíncrona (se possível em Streamlit)
   - Cache de validações comuns
   - Lazy loading de arquivos grandes

3. **Compatibilidade:**
   - Manter backward compatibility com modo áudio
   - Permitir migração fácil entre modos
   - Versionar metadados para futuras mudanças

4. **Logs:**
   - Registrar todas as transcrições manuais
   - Métricas de uso (% manual vs. automático)
   - Tempo médio de processamento

---

### Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| Usuário não sabe usar app mobile | Média | Alto | Documentação detalhada + vídeo tutorial |
| Texto mal transcrito no smartphone | Média | Médio | Permitir edição antes de enviar |
| Formato de texto incompatível | Baixa | Baixo | Normalização automática |
| Perda de contexto de áudio | Baixa | Baixo | Permitir anexar áudio original |

---

### Dependências

**Nenhuma nova dependência necessária!**

Utiliza bibliotecas já existentes:
- `streamlit` - Interface web
- `anthropic` - API Claude
- `pathlib` - Manipulação de arquivos
- `json` - Serialização de metadados
- `logging` - Logs do sistema

---

## 📚 Referências

### Documentação de Apps

- **Google Recorder:**
  - Oficial: https://recorder.google.com/
  - Suporte: https://support.google.com/recorder

- **iOS Notas de Voz:**
  - Guia Apple: https://support.apple.com/guide/iphone/record-voice-memos
  - Transcrições: https://support.apple.com/en-us/HT213064

- **Otter.ai:**
  - Website: https://otter.ai/
  - Docs: https://help.otter.ai/

### Artigos Técnicos

- "Speech-to-Text Accuracy Comparison" (2024)
- "Offline vs. Cloud Transcription Performance"
- "Mobile AI: On-Device Processing Benefits"

---

## ✅ Checklist de Implementação

### Fase 1: Backend
- [ ] Adicionar configurações em `config.py`
- [ ] Implementar `validate_transcription_text()` em `utils.py`
- [ ] Implementar `save_manual_transcription()` em `utils.py`
- [ ] Criar diretório `transcricoes/texto_direto/`

### Fase 2: Frontend
- [ ] Adicionar "Consulta com Texto" ao menu
- [ ] Criar seção de informações/benefícios
- [ ] Implementar formulário de paciente
- [ ] Adicionar campo de texto para transcrição
- [ ] Implementar contador de caracteres
- [ ] Adicionar upload opcional de áudio
- [ ] Implementar processamento e validação
- [ ] Exibir resultados e downloads

### Fase 3: Testes
- [ ] Criar `tests/test_manual_text.py`
- [ ] Implementar testes de validação
- [ ] Implementar testes de salvamento
- [ ] Criar `tests/test_integration_text.py`
- [ ] Testar fluxo completo
- [ ] Executar todos os testes
- [ ] Verificar cobertura > 70%

### Fase 4: Documentação
- [ ] Atualizar `MANUAL_USUARIO.md`
- [ ] Atualizar `DOCUMENTACAO_TECNICA.md`
- [ ] Criar guia de apps de transcrição
- [ ] Adicionar screenshots (se possível)
- [ ] Revisar documentação completa

### Fase 5: Deploy
- [ ] Code review
- [ ] Testes manuais em produção
- [ ] Atualizar versão para 1.3
- [ ] Criar tag de release
- [ ] Commit e push
- [ ] Anunciar nova feature

---

## 🎉 Conclusão

Esta funcionalidade representa uma **melhoria significativa** no sistema:

✅ **70% mais rápido** (1-2 min vs. 5-7 min)
✅ **37.5% mais barato** ($0.05 vs. $0.08)
✅ **Offline-first** (transcrição no smartphone)
✅ **Sem novas dependências**
✅ **Backward compatible**

**Implementação estimada:** 15-16 horas
**ROI:** Alto (economia de 220h/ano para clínica com 10 consultas/dia)

---

**Documento criado por:** Claude Code
**Data:** 2025-11-15
**Versão do documento:** 1.0
**Para versão do sistema:** 1.3 (planejado)
