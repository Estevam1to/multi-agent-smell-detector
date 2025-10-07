from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configurações globais do projeto carregadas via variáveis de ambiente.

    Utiliza Pydantic para validar e carregar as variáveis do arquivo .env.

    Variáveis:
        ANTHROPIC_API_KEY: Chave de API para o serviço Anthropic
        ANTHROPIC_MODEL: Nome do modelo Anthropic a ser utilizado
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    ANTHROPIC_API_KEY: str
    ANTHROPIC_MODEL: str


settings = Settings()
