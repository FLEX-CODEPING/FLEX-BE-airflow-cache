from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    flex_server: str
    redis_host: str
    redis_port: int
    redis_db: str

    model_config = SettingsConfigDict(
        env_file=(".env.local", ".env.dev", ".env.prod"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

env = os.getenv("APP_ENV", "local")
settings = Settings(_env_file=f".env.{env}")

print(f"Loaded settings: {settings.dict()}")