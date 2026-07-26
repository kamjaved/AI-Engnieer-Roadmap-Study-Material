from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # This tells pydantic-settings WHERE to look besides real env vars:
    # read a local .env file if one exists. In production, you usually
    # won't ship a .env file at all — the platform (Docker, ECS, k8s,
    # Vercel, whatever) injects real env vars directly into the process.
    # env_file is a LOCAL DEV convenience, not a production requirement —
    # pydantic-settings checks actual os.environ first either way.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # ignore any stray env vars we didn't declare
    )
    OPENAI_API_KEY: str
    PINECONE_API_KEY: str
    PINECONE_INDEX_NAME: str
    # These two DO have defaults, matching the roadmap's .env —
    # a sensible fallback if the env var isn't set at all.
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    CHAT_MODEL: str = "gpt-4.1"


settings = Settings()
