from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    database_url: str = Field(env="DATABASE_URL")

    class Config:
        env_file = ".env"  # Specify the .env file to load

settings = Settings()
