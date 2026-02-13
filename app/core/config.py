from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Food Delivery API"
    sqlite_database_url: str = "sqlite+aiosqlite:///./food_delivery.db"
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60 * 24
    otp_ttl_seconds: int = 300
    media_root: Path = Path("backend/media")
    dish_media_subdir: str = "dishes"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_")


settings = Settings()
