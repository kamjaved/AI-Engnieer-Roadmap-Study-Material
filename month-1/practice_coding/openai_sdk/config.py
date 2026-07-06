from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    default_model: str = "gpt-4o"
    default_max_tokens: int = 1000
    default_temprature: float = 0.7

    # ❌ Old (Pydantic v1 style — still works but deprecated in v2)
    # class Config:
    #     env_file = ".env"  # reads form .env automatically
    #     env_file_encoding = "utf-8"

    # ✅ Modern (Pydantic v2)
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
