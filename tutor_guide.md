# Guia de Tutoria e Evolução do Projeto: Agente Gestor de Rede

Este documento serve como referência de diretrizes para o desenvolvimento do projeto **Agente Gestor de Rede** e registra o progresso da nossa colaboração.

---

## 🎓 Diretriz de Atuação (Tutor)
- **Papel do Assistente:** Atuar estritamente como **tutor e revisor técnico**.
- **Regra de Ouro:** O assistente **NÃO** deve escrever códigos no workspace, executar comandos ou criar arquivos diretamente, exceto se solicitado explicitamente pelo usuário. Toda a digitação de código e execução de comandos no terminal deve ser feita pelo usuário.
- **Instruções de Explicação:** O assistente **NÃO** deve fornecer blocos de código prontos para copiar e colar. Em vez disso, deve guiar o usuário com um **passo a passo** de como construir a lógica (exemplo: "Importe a biblioteca X", "Crie uma classe com tal nome", "Instancie a função Y", etc.), instigando o usuário a escrever e aprender.

---

## 📈 Evolução do Projeto (Linha do Tempo)

### Fase 1: Planejamento e Estrutura Inicial (Concluído)
- [x] Definição do escopo: Agente local sem MCP (inicialmente) focado em dados analíticos e operacionais dos profissionais da rede.
- [x] Criação do diretório do projeto: `agente_gestao_rede`.
- [x] Estruturação das pastas internas:
  - `app/core` (configurações)
  - `app/services` (banco de dados/Athena e LLM)
  - `app/agents` (orquestrador de IA e prompts)
  - `app/utils` (utilitários)
- [x] Inicialização do projeto Python utilizando o comando `uv init`.

### Fase 2: Configuração e Camada de Serviços (Concluído)
- [x] Instalação de dependências: FastAPI, Uvicorn, LangChain, LangGraph, Dotenv, PyAthena, Pydantic-Settings, LangChain-OpenAI, LangChain-Anthropic.
- [x] Criação do arquivo de ambiente `.env`.
- [x] Criação do arquivo de configuração centralizada `app/core/config.py` com Pydantic-Settings.
- [x] Criação do serviço de LLM `app/services/llm.py`.
- [x] Criação do serviço de conexão do AWS Athena `app/services/athena.py`.

### Fase 3: Orquestrador e Especialistas (Concluído)
- [x] Criação do prompt do especialista de SQL voltado para Gestão de Rede.
- [x] Desenvolvimento do agente com ReAct em `app/agents/workflow.py`.

### Fase 4: API de Exposição (Concluído)
- [x] Criação do servidor FastAPI para expor o agente.
- [x] Criação do endpoint POST `/api/chat` integrado com chamada assíncrona do agente.

### Fase 5: Persistência e Memória (Concluído)
- [x] Configuração de histórico de mensagens persistente em PostgreSQL (`PostgresChatMessageHistory` via `langchain-postgres`), alinhado com o padrão dos outros agentes.
- [x] Ajuste do endpoint da API para carregar, limitar (últimas 10 mensagens) e persistir as sessões utilizando o `thread_id`.

### Fase 6: Structured Output e Arquitetura Worker (Concluído)
- [x] Definição do schema Pydantic `TelemedicinaOutput` com os campos clínicos das consultas da base Athena.
- [x] Desenvolvimento do Worker de Telemedicina (`telemedicina_worker`) para encapsular o agente SQL especialista e retornar saídas em JSON estruturado.
- [x] Adaptação do arquivo `workflow.py` em um Orquestrador central que gerencia saudações e formata as saídas estruturadas do worker de forma amigável para o chat.
### Fase 7: Auto-Correção de Queries SQL e Configurações Render (Concluído)
- [x] Implementar captura de erros na execução do Athena com retorno amigável para o agente.
- [x] Permitir que o agente receba erros de SQL, interprete-os e reescreva/refine a query automaticamente.
- [x] Ajustar conexão do Postgres na persistência de memória para usar `autocommit=True` (psycopg3).
- [x] Criar `Dockerfile` multi-stage com `uv` e blueprint `render.yaml` para deploy simplificado.

---

## 📋 Próximos Passos (Plano de Trabalho)

### Fase 8: Interface Gráfica de Usuário (Chat UI)
- [ ] Desenvolver uma interface web minimalista (como um painel HTML/JS servido pelo próprio FastAPI ou via Streamlit) para interação em formato de chat.

