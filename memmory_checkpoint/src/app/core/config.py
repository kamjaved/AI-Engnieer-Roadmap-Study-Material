from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed application configuration, sourced from environment variables / .env.

    Centralizing config here — instead of scattering os.getenv() calls across
    the codebase — buys you three things that actually matter once this stops
    being a toy:
      1. Fail-fast validation: a missing DATABASE_URL raises at process
         startup, not three requests later when the DB code finally runs.
      2. A single, greppable source of truth for everything the app depends on.
      3. Easy overriding in tests: Settings(database_url="...") bypasses the
         real environment entirely — no monkeypatching os.environ.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    database_url: str = Field(
        ...,  # "..." = required, no default. Missing env var -> ValidationError at startup.
        description="SQLAlchemy async connection string, e.g. postgresql+psycopg://...",
    )
    psycopg_database_url: str = Field(
        ...,
        description="Raw psycopg connection string for LangGraph checkpointer, e.g. postgresql://...",
    )
    openai_api_key: str = Field(
        ...,
        description="OpenAI API key consumed by langchain-openai's ChatOpenAI",
    )
    app_env: str = Field(default="local", description="local | staging | production")


@lru_cache
def get_settings() -> Settings:
    """Process-wide cached singleton.

    Without @lru_cache, every call to get_settings() would re-read and
    re-validate .env from disk. FastAPI will call this once per request
    (via Depends), so the caching isn't a micro-optimization — it's the
    difference between parsing .env once at startup vs. on every request.
    """
    return Settings()
