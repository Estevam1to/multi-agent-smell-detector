from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configurações globais do projeto carregadas via variáveis de ambiente.

    Utiliza Pydantic para validar e carregar as variáveis do arquivo .env.

    Variáveis:
        OPENROUTER_API_KEY: Chave de API para o serviço OpenRouter
        OPENROUTER_BASE_URL: URL base do OpenRouter
        OPENROUTER_API_MODEL: Nome do modelo a ser utilizado
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str
    OPENROUTER_API_MODEL: str


settings = Settings()
