from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

EMBEDDING_DIM = 384


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    cors_origins: str = "http://localhost:3000"

    database_url: str = "postgresql+asyncpg://coach:coach@localhost:5432/coach"

    llm_api_key: SecretStr = SecretStr("")
    llm_base_url: str = "https://api.groq.com/openai/v1"
    llm_model: str = "openai/gpt-oss-120b"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
