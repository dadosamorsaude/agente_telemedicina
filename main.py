import os
from fastapi import FastAPI, HTTPException, Security, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from app.agents.workflow import agent
from app.services.memory import get_session_history
from app.core.config import settings


app = FastAPI()

# Configuração da chave de API
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)):
    """Verifica se a chave de API fornecida no header coincide com a configurada."""
    if settings.API_KEY and api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Chave de API inválida ou ausente.",
        )
    return api_key

# Configuração de CORS para permitir acesso de qualquer origem (essencial para o Chat UI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatQuery(BaseModel):
    question: str
    thread_id: str


@app.get("/", response_class=HTMLResponse)
async def root_chat_ui():
    """Retorna o painel da interface gráfica do Chat UI para o agente."""
    template_path = os.path.join(os.path.dirname(__file__), "app", "templates", "index.html")
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Chat UI Template Not Found</h1>", status_code=404)


@app.post("/api/chat")
async def chat_endpoint(query: ChatQuery, api_key: str = Security(verify_api_key)):
    history = None
    try:
        history = get_session_history(query.thread_id)
        recent_messages = list(history.messages)[-10:]
        input_messages = recent_messages + [HumanMessage(content=query.question)]
        response = await agent.ainvoke({"messages": input_messages})
        final_content =  {"answer": response["messages"][-1].content}
        history.add_user_message(query.question)
        history.add_ai_message(final_content["answer"])
        return final_content
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Garante o fechamento da conexão com o banco de dados para evitar leaks
        if history and hasattr(history, "sync_connection") and history.sync_connection:
            try:
                history.sync_connection.close()
            except Exception:
                pass

