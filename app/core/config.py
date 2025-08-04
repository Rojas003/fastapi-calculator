from pydantic_settings import BaseSettings
import logging

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str

    class Config:
        env_file = ".env"

settings = Settings()

# Debugging
logging.basicConfig(level=logging.DEBUG)
logging.debug(f"Loaded DATABASE_URL -> {settings.database_url}")
