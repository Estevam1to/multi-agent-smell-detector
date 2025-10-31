"""Configurações do projeto."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações carregadas do .env."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str
    OPENROUTER_API_MODEL: str


settings = Settings()
