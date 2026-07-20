from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

load_dotenv(override = True)

class Settings(BaseSettings):
    #AWS ATHENA Settings
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str
    ATHENA_S3_STAGING_DIR: str
    ATHENA_DATABASE: str

    #LLM Settings:
    OPENAI_API_KEY: str
    OPENAI_MODEL: str
    ANTHROPIC_API_KEY: str
    ANTHROPIC_MODEL: str

    #DATABASE SETTINGS:
    DATABASE_URL: str

    # RAG Settings:
    RAG_COLLECTION_NAME: str = "regras_telemedicina"

    # API Security:
    API_KEY: Optional[str] = None

    model_config = SettingsConfigDict(env_file='.env', extra='ignore', env_file_encoding='utf-8')

settings = Settings()