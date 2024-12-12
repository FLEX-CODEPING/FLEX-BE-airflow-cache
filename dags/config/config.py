from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    flex_server: str
    redis_host: str
    redis_port: int
    redis_db: str
    redis_password: str

    model_config = SettingsConfigDict(
        env_file=(".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings(_env_file=".env")

print(f"Loaded settings: {settings.dict()}")