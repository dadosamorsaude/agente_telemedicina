from contextvars import ContextVar
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain_core.tools import tool
from app.core.config import settings

# ContextVar para capturar os resultados retornados pelo RAG para auditorias/observabilidade posterior
rag_results_context: ContextVar[list] = ContextVar("rag_results", default=[])

def get_pgvector_store():
    """Inicializa e retorna o PGVector store conectado ao Supabase."""
    connection_string = settings.DATABASE_URL
    if connection_string.startswith("postgresql://"):
        connection_string = connection_string.replace("postgresql://", "postgresql+psycopg://", 1)
        
    embeddings = OpenAIEmbeddings(
        api_key=settings.OPENAI_API_KEY,
        model="text-embedding-3-large",
        dimensions=3072
    )
    
    return PGVector(
        embeddings=embeddings,
        collection_name=settings.RAG_COLLECTION_NAME,
        connection=connection_string,
        use_jsonb=True
    )

def format_docs(docs) -> str:
    """Formata os documentos recuperados com metadados estruturados."""
    if not docs:
        return ""

    formatted = []
    for i, doc in enumerate(docs, start=1):
        metadata = doc.metadata or {}
        fonte = metadata.get("fonte", "Fonte não informada")
        pagina = metadata.get("pagina", "N/A")
        
        header = (
            f"[Trecho {i}]\n"
            f"Fonte: {fonte} (Página {pagina})\n"
        )
        formatted.append(f"{header}Conteúdo:\n{doc.page_content}")

    return "\n\n---\n\n".join(formatted)

@tool
def search_telemedicina_rules(query: str) -> str:
    """
    OBRIGATÓRIO: Use esta ferramenta para pesquisar regras de negócio da Telemedicina, diretrizes de envio,
    conformidade com a LGPD (Lei Geral de Proteção de Dados), sigilo médico, regras operacionais do sistema VIDA, 
    definição de 'atendimento realizado' ou 'não realizado', critérios de disponibilidade de documentos (receitas,
    atestados, exames e orientações) e regras de liberação/autorização de envio para a equipe de operação.
    """
    try:
        store = get_pgvector_store()
        # Executa busca semântica para os top 5 resultados mais similares
        docs = store.similarity_search(query, k=5)
        
        # Registra os resultados no contexto para auditorias/evaluator
        captured = rag_results_context.get([])
        rag_results_context.set(
            captured + [
                {
                    "source": "Regras Telemedicina (pgvector)",
                    "collection": settings.RAG_COLLECTION_NAME,
                    "query": query,
                    "chunks": [d.page_content for d in docs],
                    "metadata": [d.metadata for d in docs]
                }
            ]
        )
        
        if not docs:
            return "Nenhuma regra de negócio ou diretriz de telemedicina encontrada para esta busca."
            
        return format_docs(docs)
    except Exception as e:
        return f"Erro ao realizar busca no RAG de Telemedicina: {str(e)}"
