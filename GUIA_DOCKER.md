# Guia Completo de Docker para o Sistema Veterinário

**Versão:** 1.0
**Data:** 10/11/2025
**Sistema:** Documentação Veterinária v1.2

---

## 📋 Índice

1. [O que é Docker?](#o-que-é-docker)
2. [Por que usar Docker?](#por-que-usar-docker)
3. [Quando usar Docker?](#quando-usar-docker)
4. [Quando NÃO usar Docker?](#quando-não-usar-docker)
5. [Docker no Projeto Atual](#docker-no-projeto-atual)
6. [Como Usar Docker](#como-usar-docker)
7. [Docker Compose](#docker-compose)
8. [Troubleshooting](#troubleshooting)
9. [Melhores Práticas](#melhores-práticas)

---

## 🐳 O que é Docker?

### Definição Simples

Docker é uma plataforma que **empacota sua aplicação e todas as suas dependências** em um "container" isolado que pode rodar em qualquer lugar.

**Analogia:** Imagina um container de navio 🚢
- O container tem TUDO que o aplicativo precisa dentro dele
- Pode ser movido de um lugar para outro
- Funciona da mesma forma em qualquer lugar
- Isolado de outros containers

### Componentes Principais

```
┌─────────────────────────────────────┐
│         Seu Computador              │
├─────────────────────────────────────┤
│  Docker Engine (Motor)              │
├─────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐        │
│  │Container │  │Container │        │
│  │   App 1  │  │   App 2  │        │
│  │          │  │          │        │
│  │ Python   │  │ Node.js  │        │
│  │ FFmpeg   │  │ MongoDB  │        │
│  │ Whisper  │  │ React    │        │
│  └──────────┘  └──────────┘        │
└─────────────────────────────────────┘
```

**Dockerfile:** Receita para construir o container
**Image:** Container "congelado" pronto para usar
**Container:** Image rodando (aplicação ativa)
**Docker Compose:** Orquestra múltiplos containers

---

## 🎯 Por que usar Docker?

### Problema SEM Docker

```
👨‍💻 Desenvolvedor:
"Funciona na minha máquina!"

👨‍🔧 DevOps:
"Mas não funciona no servidor..."

🤷‍♂️ Problemas:
- Python versão diferente
- FFmpeg não instalado
- Whisper não configurado
- Variáveis de ambiente erradas
- Dependências conflitantes
```

### Solução COM Docker

```
✅ Desenvolvedor:
"Funciona no meu container!"

✅ DevOps:
"Funciona no servidor também!"

🎉 Benefícios:
- Mesmo ambiente em todos os lugares
- Tudo já vem instalado e configurado
- Um comando para rodar
- Isolamento total
- Fácil de replicar
```

---

## 🚀 Benefícios do Docker

### 1. **Consistência de Ambiente**

**Sem Docker:**
```bash
# Desenvolvedor A (Windows)
Python 3.11 + FFmpeg 6.0 ✅

# Desenvolvedor B (macOS)
Python 3.9 + FFmpeg 5.0 ❌
# Não funciona igual!

# Servidor (Linux)
Python 3.10 + FFmpeg 7.0 ❌
# Comportamento diferente!
```

**Com Docker:**
```bash
# Todos usam:
Docker Image: vet-system:1.2 ✅
# EXATAMENTE o mesmo ambiente!
```

---

### 2. **Instalação Simplificada**

**Sem Docker:**
```bash
# 20+ passos:
1. Instalar Python 3.11
2. Instalar FFmpeg
3. Criar ambiente virtual
4. pip install -r requirements.txt
5. Baixar modelo Whisper
6. Configurar variáveis de ambiente
7. ...
# Se algo der errado, começar de novo! 😫
```

**Com Docker:**
```bash
# 2 passos:
1. docker-compose up -d
2. Pronto! ✅ 🎉
```

---

### 3. **Isolamento**

```
Sem Docker:
┌─────────────────────────────┐
│    Seu Computador           │
│                             │
│ Sistema Veterinário         │
│ + Outro projeto Python      │
│ + Banco de dados global     │
│                             │
│ 😱 TUDO MISTURADO           │
│ Conflitos de dependências   │
└─────────────────────────────┘

Com Docker:
┌─────────────────────────────┐
│    Seu Computador           │
│  ┌──────────┐  ┌──────────┐│
│  │Container1│  │Container2││
│  │   Vet    │  │  Outro   ││
│  │  System  │  │  Projeto ││
│  └──────────┘  └──────────┘│
│                             │
│ 🎉 ISOLADOS!                │
│ Zero conflitos              │
└─────────────────────────────┘
```

---

### 4. **Fácil de Replicar**

```bash
# Compartilhar com colega:

Sem Docker:
"Siga este tutorial de 50 páginas..."
📄📄📄📄📄

Com Docker:
git clone repo
docker-compose up
✅ Pronto em 2 comandos!
```

---

### 5. **Rollback Fácil**

```bash
# Algo deu errado?

Sem Docker:
"Preciso desinstalar tudo e reinstalar..." 😫

Com Docker:
docker-compose down
docker-compose up --build
✅ Volta ao estado anterior em segundos!
```

---

## ⏰ Quando usar Docker?

### ✅ Use Docker quando:

#### 1. **Deploy em Produção**
```
Cenário: Vai colocar em servidor/cloud

✅ Docker é ESSENCIAL
- Garante que funciona igual no servidor
- Fácil de atualizar
- Fácil de escalar
- Rollback rápido
```

#### 2. **Múltiplos Ambientes**
```
Cenário: Dev, Staging, Produção

✅ Docker MUITO recomendado
- Mesmo container em todos os ambientes
- Evita "funciona no meu PC"
- Testes confiáveis
```

#### 3. **Onboarding de Novos Desenvolvedores**
```
Cenário: Novo membro da equipe

Sem Docker:
"Siga estes 50 passos..." 📄
Tempo: 2-4 horas + troubleshooting

Com Docker:
"Clone o repo e rode docker-compose up"
Tempo: 5 minutos ✅
```

#### 4. **Dependências Complexas**
```
Cenário: FFmpeg + Whisper + Claude + Streamlit + ...

✅ Docker IDEAL
- Tudo já vem configurado
- Versões corretas garantidas
- Zero conflitos
```

#### 5. **CI/CD (Integração Contínua)**
```
Cenário: Testes automáticos + Deploy

✅ Docker NECESSÁRIO
- GitHub Actions usa containers
- Testes em ambiente idêntico à produção
- Deploy automatizado
```

#### 6. **Microservices**
```
Cenário: API + Frontend + Banco + Worker

✅ Docker + Compose PERFEITO
- Cada serviço em seu container
- Fácil escalar apenas o que precisa
- Isolamento total
```

---

## ❌ Quando NÃO usar Docker?

### ⚠️ Evite Docker quando:

#### 1. **Desenvolvimento Local Simples**
```
Cenário: Você é o único dev, trabalhando no seu PC

❌ Docker é OVERKILL
- Python virtual env é suficiente
- Mais rápido para testar mudanças
- Menos complexidade
```

#### 2. **Aplicações GUI Desktop Complexas**
```
Cenário: App Electron com UI nativa

❌ Docker não é ideal
- GUIs são complicadas no Docker
- Melhor rodar nativamente
```

#### 3. **Recursos Limitados**
```
Cenário: PC antigo com pouco RAM/CPU

❌ Docker pode ser pesado
- Overhead de virtualização
- Melhor rodar nativamente
```

#### 4. **Aprendizado Inicial**
```
Cenário: Você está aprendendo Python/Whisper

❌ Adiciona complexidade desnecessária
- Aprenda o básico primeiro
- Docker depois
```

---

## 🏗️ Docker no Projeto Atual

### Arquivos Docker Existentes

O projeto **JÁ TEM** Docker configurado! ✅

```
veterinary-transcription/
├── Dockerfile              # Receita do container
├── docker-compose.yml      # Orquestração
├── .dockerignore          # Arquivos a ignorar
└── requirements.txt       # Dependências Python
```

---

### Dockerfile Atual

```dockerfile
# Arquivo: Dockerfile
FROM python:3.11-slim

# Instalar FFmpeg e dependências do sistema
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Diretório de trabalho
WORKDIR /app

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretórios necessários
RUN mkdir -p audios transcricoes relatorios logs templates

# Expor porta do Streamlit
EXPOSE 8501

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Comando padrão: rodar Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**O que faz:**
1. ✅ Usa Python 3.11 (slim = versão menor)
2. ✅ Instala FFmpeg automaticamente
3. ✅ Instala todas as dependências Python
4. ✅ Copia seu código
5. ✅ Cria pastas necessárias
6. ✅ Expõe porta 8501 (Streamlit)
7. ✅ Configura healthcheck
8. ✅ Inicia Streamlit automaticamente

---

### docker-compose.yml Atual

```yaml
# Arquivo: docker-compose.yml
version: '3.8'

services:
  # Serviço principal: Interface Web
  vet-docs-web:
    build: .
    container_name: vet-docs-web
    ports:
      - "8501:8501"
    volumes:
      - ./audios:/app/audios
      - ./transcricoes:/app/transcricoes
      - ./relatorios:/app/relatorios
      - ./logs:/app/logs
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Serviço CLI (opcional)
  vet-docs-cli:
    build: .
    container_name: vet-docs-cli
    volumes:
      - ./audios:/app/audios
      - ./transcricoes:/app/transcricoes
      - ./relatorios:/app/relatorios
      - ./logs:/app/logs
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    command: python transcribe_consult.py
    profiles:
      - cli
```

**O que faz:**

**Serviço: vet-docs-web**
- ✅ Interface Streamlit
- ✅ Porta 8501 exposta
- ✅ Volumes para persistir dados
- ✅ Reinicia automaticamente se cair
- ✅ Healthcheck para monitorar saúde

**Serviço: vet-docs-cli** (opcional)
- ✅ Interface linha de comando
- ✅ Mesmo acesso aos dados
- ✅ Só inicia se você pedir (profile: cli)

---

## 🎮 Como Usar Docker

### Pré-requisitos

#### 1. Instalar Docker

**Windows:**
```bash
# Baixar Docker Desktop:
https://www.docker.com/products/docker-desktop

# Instalar e reiniciar
# Verificar:
docker --version
docker-compose --version
```

**macOS:**
```bash
# Baixar Docker Desktop:
https://www.docker.com/products/docker-desktop

# Verificar:
docker --version
docker-compose --version
```

**Linux:**
```bash
# Ubuntu/Debian:
sudo apt-get update
sudo apt-get install docker.io docker-compose

# Verificar:
docker --version
docker-compose --version

# Adicionar seu usuário ao grupo docker:
sudo usermod -aG docker $USER
# Fazer logout e login de novo
```

---

### Uso Básico

#### 1. **Primeira Execução (Build + Run)**

```bash
# Navegar até a pasta do projeto
cd C:\Users\Zero\Desktop\veterinary-transcription

# Criar arquivo .env com API key
echo "ANTHROPIC_API_KEY=sua-chave-aqui" > .env

# Construir e iniciar
docker-compose up -d

# Logs:
# Building vet-docs-web ...
# Creating vet-docs-web ... done
```

**O que acontece:**
1. 🔨 Docker lê `Dockerfile`
2. 📦 Baixa image Python 3.11
3. ⚙️ Instala FFmpeg
4. 📥 Instala dependências Python
5. 📋 Copia seu código
6. 🚀 Inicia container
7. ✅ Streamlit disponível em `localhost:8501`

**Tempo:** 5-10 minutos (primeira vez)

---

#### 2. **Acessar a Aplicação**

```bash
# Abrir navegador:
http://localhost:8501

# ✅ Streamlit está rodando no Docker!
```

---

#### 3. **Ver Logs**

```bash
# Ver logs em tempo real
docker-compose logs -f vet-docs-web

# Ver últimas 100 linhas
docker-compose logs --tail=100 vet-docs-web

# Ver logs de todos os serviços
docker-compose logs
```

---

#### 4. **Parar a Aplicação**

```bash
# Parar containers (mas não remove)
docker-compose stop

# Parar e remover containers
docker-compose down

# Parar, remover containers E volumes
docker-compose down -v
```

---

#### 5. **Atualizar Código**

```bash
# Você modificou app.py ou outro arquivo

# Opção 1: Rebuild completo
docker-compose down
docker-compose up -d --build

# Opção 2: Rebuild apenas se necessário
docker-compose up -d --build

# Opção 3: Restart rápido (sem rebuild)
docker-compose restart
```

---

#### 6. **Executar Comandos no Container**

```bash
# Entrar no container (modo interativo)
docker exec -it vet-docs-web bash

# Agora você está DENTRO do container!
# root@abc123:/app#

# Listar arquivos
ls -la

# Ver relatórios
ls relatorios/

# Executar script Python
python transcribe_consult.py

# Sair do container
exit
```

---

#### 7. **Usar CLI (opcional)**

```bash
# Iniciar serviço CLI
docker-compose --profile cli run --rm vet-docs-cli

# Vai abrir a interface CLI do transcribe_consult.py
```

---

### Comandos Úteis

```bash
# Ver containers rodando
docker ps

# Ver todos os containers (incluindo parados)
docker ps -a

# Ver images baixadas
docker images

# Ver uso de espaço
docker system df

# Limpar tudo que não está em uso
docker system prune -a

# Ver logs específicos
docker logs vet-docs-web

# Verificar saúde do container
docker inspect --format='{{.State.Health.Status}}' vet-docs-web

# Reiniciar container específico
docker restart vet-docs-web

# Parar container específico
docker stop vet-docs-web

# Remover container
docker rm vet-docs-web

# Remover image
docker rmi veterinary-transcription_vet-docs-web
```

---

## 🎼 Docker Compose

### O que é Docker Compose?

**Docker:** Gerencia 1 container
**Docker Compose:** Gerencia MÚLTIPLOS containers juntos

**Exemplo:**
```yaml
services:
  web:        # Container Streamlit
  api:        # Container FastAPI
  db:         # Container PostgreSQL
  redis:      # Container Redis (cache)
  worker:     # Container Celery (tarefas)
```

Compose **coordena** todos eles!

---

### Estrutura do docker-compose.yml

```yaml
version: '3.8'  # Versão do Compose

services:  # Lista de containers

  nome-servico:  # Nome do seu serviço
    build: .  # Onde está o Dockerfile
    # OU
    image: python:3.11  # Usar image pronta

    container_name: meu-container  # Nome do container

    ports:  # Mapear portas
      - "8501:8501"  # host:container

    volumes:  # Montar pastas
      - ./local:/container

    environment:  # Variáveis de ambiente
      - VAR=valor

    command: python app.py  # Comando a executar

    depends_on:  # Dependências
      - db
      - redis

    restart: unless-stopped  # Política de restart

    networks:  # Redes
      - minha-rede
```

---

### Exemplo: Adicionar Banco de Dados

```yaml
# docker-compose.yml (expandido)
version: '3.8'

services:
  # Aplicação Streamlit
  vet-docs-web:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./audios:/app/audios
      - ./relatorios:/app/relatorios
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - DATABASE_URL=postgresql://user:pass@db:5432/vetdb
    depends_on:
      - db
    restart: unless-stopped

  # Banco de dados PostgreSQL
  db:
    image: postgres:15-alpine
    container_name: vet-postgres
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=vetdb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  # Redis (cache)
  redis:
    image: redis:7-alpine
    container_name: vet-redis
    ports:
      - "6379:6379"
    restart: unless-stopped

volumes:
  postgres_data:  # Volume persistente
```

**Uso:**
```bash
docker-compose up -d

# Agora você tem:
# - Streamlit em localhost:8501
# - PostgreSQL em localhost:5432
# - Redis em localhost:6379
# Tudo conectado! 🎉
```

---

## 🔧 Troubleshooting

### Problema 1: "Port already in use"

```bash
# Erro:
# Bind for 0.0.0.0:8501 failed: port is already allocated

# Solução 1: Parar o que está usando a porta
# Ver o que está na porta 8501
netstat -ano | findstr :8501  # Windows
lsof -i :8501  # macOS/Linux

# Matar o processo
taskkill /PID <PID> /F  # Windows
kill -9 <PID>  # macOS/Linux

# Solução 2: Mudar a porta no docker-compose.yml
ports:
  - "8502:8501"  # Usar 8502 no host
```

---

### Problema 2: "Cannot connect to Docker daemon"

```bash
# Erro:
# Cannot connect to the Docker daemon

# Solução: Iniciar Docker Desktop
# Windows/macOS: Abrir Docker Desktop
# Linux:
sudo systemctl start docker
```

---

### Problema 3: Image build muito lenta

```bash
# Problema: Baixando tudo de novo sempre

# Solução: Usar cache do Docker

# Adicionar no Dockerfile:
# Cache de pip
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Rebuild com cache:
docker-compose build --no-cache  # Força rebuild completo
docker-compose build  # Usa cache (rápido)
```

---

### Problema 4: Container não inicia

```bash
# Ver logs detalhados
docker-compose logs vet-docs-web

# Ver status
docker ps -a

# Entrar no container para debug
docker run -it veterinary-transcription_vet-docs-web bash
```

---

### Problema 5: Mudanças no código não aparecem

```bash
# Problema: Código antigo ainda rodando

# Solução: Rebuild
docker-compose down
docker-compose up -d --build

# Ou com cache limpo:
docker-compose build --no-cache
docker-compose up -d
```

---

### Problema 6: Falta de espaço

```bash
# Ver uso
docker system df

# Limpar images não usadas
docker image prune

# Limpar containers parados
docker container prune

# Limpar volumes não usados
docker volume prune

# LIMPAR TUDO (cuidado!)
docker system prune -a --volumes
```

---

## 🎯 Melhores Práticas

### 1. **Use .dockerignore**

```bash
# .dockerignore
__pycache__/
*.pyc
.git/
.env
*.log
audios/*.mp3
relatorios/*.md
.vscode/
.idea/
```

**Por quê:** Evita copiar arquivos desnecessários para o container

---

### 2. **Multi-stage Builds (Avançado)**

```dockerfile
# Build stage
FROM python:3.11 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Production stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["streamlit", "run", "app.py"]
```

**Benefício:** Image final menor e mais segura

---

### 3. **Use Volumes para Dados**

```yaml
# ❌ Não faça:
# Dados dentro do container
# Se remover container, perde tudo!

# ✅ Faça:
volumes:
  - ./relatorios:/app/relatorios  # Dados no host
# Pode remover container, dados ficam!
```

---

### 4. **Variáveis de Ambiente**

```yaml
# ❌ Não faça:
environment:
  - ANTHROPIC_API_KEY=sk-ant-api03-1234567890  # Exposto!

# ✅ Faça:
environment:
  - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}  # Lê de .env
```

```bash
# .env
ANTHROPIC_API_KEY=sk-ant-api03-1234567890

# .gitignore
.env  # NÃO commitar!
```

---

### 5. **Healthchecks**

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

**Benefício:** Docker sabe se app está funcionando

---

### 6. **Restart Policies**

```yaml
restart: unless-stopped  # Reinicia sempre, exceto se você parar

# Opções:
# no: nunca reinicia
# always: sempre reinicia
# on-failure: só se falhar
# unless-stopped: sempre, exceto stop manual
```

---

### 7. **Nomeie Containers e Volumes**

```yaml
# ✅ Bom:
container_name: vet-docs-web
volumes:
  postgres_data:
    name: vet-postgres-data

# ❌ Evite:
# Nomes gerados automaticamente são confusos
```

---

## 📊 Comparação: Docker vs Nativo

| Aspecto | Nativo (sem Docker) | Docker |
|---------|---------------------|--------|
| **Setup inicial** | 20+ passos manuais | 2 comandos |
| **Consistência** | ❌ Varia por máquina | ✅ Idêntico em todas |
| **Isolamento** | ❌ Compartilha deps | ✅ Totalmente isolado |
| **Performance** | ✅✅ Nativa | ✅ Pequeno overhead |
| **Facilidade update** | ❌ Manual | ✅ Rebuild automático |
| **Rollback** | ❌ Difícil | ✅ Muito fácil |
| **Deploy** | ❌ Complexo | ✅ Muito simples |
| **Portabilidade** | ❌ Dificulta| ✅ Excelente |

---

## 🎓 Quando Usar Cada Abordagem

### Use **Nativo** (sem Docker):

```
✅ Desenvolvimento local solo
✅ Prototipagem rápida
✅ Aprendendo Python/Whisper
✅ Recursos limitados (PC fraco)
✅ Apenas você usa o código
```

### Use **Docker**:

```
✅ Deploy em produção
✅ Equipe com múltiplos devs
✅ CI/CD
✅ Múltiplos ambientes (dev/staging/prod)
✅ Onboarding de novos devs
✅ Microservices
✅ Dependências complexas
```

---

## ✅ Conclusão e Recomendação

### Para o seu projeto:

**Docker JÁ ESTÁ CONFIGURADO! ✅**

**Recomendação: USE DOCKER PARA:**

1. ✅ **Deploy em servidor/cloud**
   ```bash
   # No servidor:
   git clone repo
   echo "ANTHROPIC_API_KEY=..." > .env
   docker-compose up -d
   # Pronto! 🚀
   ```

2. ✅ **Compartilhar com colegas**
   ```bash
   # Colega:
   git clone repo
   docker-compose up -d
   # Funciona idêntico! 🎉
   ```

3. ✅ **Testes em ambiente limpo**
   ```bash
   # Testar sem mexer no seu ambiente:
   docker-compose up -d
   # Testa...
   docker-compose down
   # Volta tudo ao normal!
   ```

**Use NATIVO para:**
- Desenvolvimento diário no seu PC
- Testar mudanças rápidas
- Debug intensivo

**Workflow Híbrido (Ideal):**
```
1. Desenvolver nativo (rápido)
2. Testar no Docker (garantir funciona)
3. Push para Git
4. Deploy com Docker (produção)
```

---

## 🚀 Começar Agora

```bash
# 1. Instalar Docker Desktop
# https://www.docker.com/products/docker-desktop

# 2. No terminal:
cd C:\Users\Zero\Desktop\veterinary-transcription

# 3. Criar .env
echo "ANTHROPIC_API_KEY=sua-chave-aqui" > .env

# 4. Iniciar!
docker-compose up -d

# 5. Acessar
# http://localhost:8501

# 🎉 Pronto!
```

---

**Versão:** 1.0
**Última atualização:** 10/11/2025
**Autor:** Claude Code
