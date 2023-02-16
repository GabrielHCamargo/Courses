from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_URL: str = "/api/v1"
    DB_URL: str = "postgresql+asyncpg://postgres:123456@localhost:5432/fastapi"

    class Config:
        case_sensitive = True


settings: Settings = Settings()