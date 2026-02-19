# La uso para descargar desde .env las variables usadas para conectar con la BD
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    DEBUG: bool = True

    class Config:
        env_file = ".env"

settings = Settings()