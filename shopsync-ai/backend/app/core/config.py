"""Server-side configuration. No provider token is placed in the React bundle."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    demo_mode: bool = True
    shopsync_demo_owner_token: str = ""
    mongodb_uri: str | None = None
    mongodb_db: str = "shopsync_ai"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.5-flash-lite"
    gemini_synthetic_demo: bool = False


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Cache configuration per process; tests can clear this cache after env changes."""
    return Settings()
