# Agente de Telemedicina - Gestão de Rede (Amor Saúde)

Este é o **Agente de Telemedicina**, um sistema multiagente desenvolvido em Python utilizando **FastAPI**, **LangGraph** e **AWS Athena**. O agente atua como um assistente analítico e operacional capaz de consultar a base de dados de telemedicina da Amor Saúde, extrair métricas de atendimentos, identificar registros clínicos (evoluções, receitas, atestados) e responder a perguntas complexas em linguagem natural.

---

## 🏗️ Arquitetura do Sistema

O sistema é construído sobre uma arquitetura multiagente orquestrada com **LangGraph**:

1. **Orquestrador Central (`app/agents/workflow.py`)**: Analisa as mensagens do usuário, gerencia saudações, direciona perguntas específicas de dados para o especialista correspondente e formata o JSON estruturado retornado em respostas amigáveis.
2. **Worker de Telemedicina (`app/agents/workers.py`)**: Um agente especialista em SQL (Athena/Presto). Ele é configurado com o schema exato do banco de dados, gera queries SQL inteligentes com colunas explícitas, valida os tipos de dados e responde no formato estruturado `TelemedicinaOutput`.

```mermaid
graph TD
    User([Usuário]) --> API[FastAPI /api/chat]
    API --> Orquestrador[Orquestrador Central]
    Orquestrador -->|Direciona Query| Worker[Worker de Telemedicina]
    Worker -->|Consulta SQL| Athena[(AWS Athena)]
    Athena -->|Retorna Dados| Worker
    Worker -->|Auto-Correção se Erro| Worker
    Worker -->|JSON Estruturado| Orquestrador
    Orquestrador -->|Resposta Formatada| User
```

---

## ⚡ Principais Recursos

- **Loop de Auto-Correção SQL (Self-Correction):** Caso o AWS Athena retorne um erro de execução (erro de sintaxe, alias reservado ou coluna inexistente), o agente intercepta o erro, reescreve a consulta e tenta novamente automaticamente (até 3 tentativas).
- **Persistência de Memória:** Histórico de chat persistido no **PostgreSQL** utilizando `PostgresChatMessageHistory` via `langchain-postgres`. Configurado com *autocommit* ativo para evitar conexões pendentes no Supabase.
- **Segurança (API Key):** Endpoints privados protegidos via cabeçalho `X-API-Key`.
- **CORS Habilitado:** Permitindo conexões diretas de qualquer origem para facilitar a integração com a Chat UI.
- **Pronto para Deploy:** Configurações declarativas prontas para deploy em nuvem (Docker + Render Blueprint).

---

## 📁 Estrutura de Pastas

```text
agente_telemedicina/
├── app/
│   ├── agents/
│   │   ├── workers.py       # Definição do especialista SQL e esquemas de saída
│   │   └── workflow.py      # Orquestrador LangGraph e fluxo de diálogo
│   ├── core/
│   │   └── config.py        # Configurações do Pydantic-Settings (.env)
│   ├── services/
│   │   ├── athena.py        # Serviço de conexão e execução no AWS Athena
│   │   ├── llm.py           # Fábrica de inicialização OpenAI/Anthropic
│   │   └── memory.py        # Conexão Postgres para histórico do chat
│   └── utils/               # Funções utilitárias auxiliares
├── Dockerfile               # Configuração do container Docker multi-stage (uv)
├── main.py                  # Servidor FastAPI e rotas do projeto
├── pyproject.toml           # Manifesto de dependências do Python (PEP 621)
├── render.yaml              # Blueprint declarativo para deploy no Render
├── tutor_guide.md           # Linha do tempo e guia pedagógico de desenvolvimento
└── uv.lock                  # Lockfile de dependências gerenciado pelo uv
```

---

## 🚀 Como Executar Localmente

### 1. Pré-requisitos
Recomenda-se o uso do **uv** (gerenciador rápido de dependências Python) ou Python 3.12+.

### 2. Instalar Dependências
```bash
# Sincroniza e cria o ambiente virtual (.venv) automaticamente
uv sync
```

### 3. Configurar Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto baseado nas seguintes variáveis:

```env
# AWS Athena
AWS_ACCESS_KEY_ID="seu_access_key"
AWS_SECRET_ACCESS_KEY="seu_secret_key"
AWS_REGION="us-east-1"
ATHENA_DATABASE="seu_athena_database"
ATHENA_STAGING_DIR="s3://seu-bucket-de-staging/"

# LLMs
OPENAI_API_KEY="sua_chave_openai"
OPENAI_MODEL="gpt-4o"
ANTHROPIC_API_KEY="sua_chave_anthropic"
ANTHROPIC_MODEL="claude-3-5-sonnet-latest"

# Banco de Dados de Memória
DATABASE_URL="postgresql://usuario:senha@host:porta/banco"

# Chave do Servidor para Segurança
API_KEY="uma_chave_aleatoria_segura"
```

### 4. Executar o Servidor FastAPI
```bash
uv run uvicorn main:app --reload
```
A API estará disponível em `http://localhost:8000`. O health check público pode ser testado acessando a rota raiz no navegador: `http://localhost:8000/`.

---

## 🌐 Deploy no Render.com

Este projeto inclui um arquivo `render.yaml` (Blueprint) que simplifica a publicação no Render:

1. Suba o código do repositório no seu GitHub.
2. Acesse a dashboard do Render, clique em **Blueprints** e conecte seu repositório.
3. O Render irá criar automaticamente:
   - Uma **Base de Dados PostgreSQL** para a memória persistente.
   - Um **Web Service (FastAPI)** rodando a partir do `Dockerfile`.
4. Preencha as chaves necessárias (AWS, LLMs, API_KEY) na tela de configuração e confirme o deploy.
