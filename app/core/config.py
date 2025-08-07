from pydantic_settings import BaseSettings
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Settings(BaseSettings):
    database_url: str = "sqlite:///./test.db"
    secret_key: str = "a-string-secret-at-least-256-bits-long"
    algorithm: str = "HS256"

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

# Debug log to confirm config is loaded
logging.debug(f"Loaded DATABASE_URL -> {settings.database_url}")
logging.debug(f"Loaded DATABASE_URL -> {settings.database_url}")
