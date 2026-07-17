from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from app.core.config import settings

def get_llm(provider: str, temperature: float = 0.0):
    """
    Retorna a instância do modelo de linguagem (LLM) baseado no .env
    """
    if provider.lower() == "openai":
        return ChatOpenAI(
            model = settings.OPENAI_MODEL,
            temperature = temperature,
            api_key = settings.OPENAI_API_KEY
        )
    elif provider.lower() == "anthropic":
        return ChatAnthropic(
            model = settings.ANTHROPIC_MODEL,
            temperature = temperature,
            api_key = settings.ANTHROPIC_API_KEY
        )
    else:
        raise ValueError(f"Provedor de LLM '{provider}' não suportado.")