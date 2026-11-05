from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    cors_origins: str = "http://localhost:3000"
    
    database_url: str = "postgresql+asyncpg://neondb_owner:npg_kt9KBSyx1rhW@ep-sparkling-shape-a1byyy3t.ap-southeast-1.aws.neon.tech/neondb?ssl=require"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
