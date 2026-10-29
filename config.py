from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROMT: str
    API_KEY: str
    ENVIRONMENT: str
    LOG_LEVEL: str
    FRONT_URL: str

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache()
def get_settings() -> Settings:
    return Settings()