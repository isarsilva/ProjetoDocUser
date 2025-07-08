from typing import List
from decouple import config
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings  # ✅ Import correto no Pydantic v2

class Settings(BaseSettings):
    API_V1_STR: str = "/v1"
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY", default="minha_chave_dev", cast=str)
    JWT_REFRESH_SECRET_KEY: str = config("JWT_REFRESH_SECRET_KEY", cast=str)
    MONGO_CONNECTION_STRING: str = config("MONGO_CONNECTION_STRING", cast=str)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRATION_MINUTES: int = 60 * 24 * 7
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    PROJECT_NAME: str = "Projeto DocUser"

    class Config:
        case_sensitive = True

settings = Settings()