import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    API_V1_STR: str = "/api/v1"
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN")

    class Config:
        case_sensitive = True


settings = Settings()
