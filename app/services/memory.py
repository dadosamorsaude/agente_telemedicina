from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_postgres import PostgresChatMessageHistory
import uuid
import psycopg
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

_memory_store: dict = {}

_tables_created = False


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    global _tables_created

    try:
        uuid.UUID(session_id)
        valid_session_id = session_id
    except ValueError:
        namespace = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')
        valid_session_id = str(uuid.uuid5(namespace, session_id))

    if settings.DATABASE_URL:
        try:
            # Estabelece a conexão síncrona com o PostgreSQL com autocommit habilitado
            conn = psycopg.connect(settings.DATABASE_URL, prepare_threshold=None, autocommit=True)
            
            # Garante que a tabela existe apenas uma vez por ciclo de vida
            if not _tables_created:
                try:
                    PostgresChatMessageHistory.create_tables(conn, "chat_history_telemedicina")
                    _tables_created = True
                    logger.info("Tabela de histórico 'chat_history_telemedicina' criada com sucesso.")
                except Exception as table_err:
                    logger.error(f"Erro ao criar tabelas no Postgres: {table_err}")
            
            # Cria a instância de histórico do LangChain vinculada a essa conexão
            history = PostgresChatMessageHistory(
                "chat_history_telemedicina",
                valid_session_id,
                sync_connection=conn,
            )
            return history
        except Exception as e:
            logger.warning(
                f"Falha ao conectar ao PostgreSQL para memória, usando in-memory: {e}"
            )

    # Fallback caso a conexão com o banco não funcione
    if valid_session_id not in _memory_store:
        _memory_store[valid_session_id] = ChatMessageHistory()
    return _memory_store[valid_session_id]


