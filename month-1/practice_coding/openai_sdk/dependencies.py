from openai import AsyncOpenAI, OpenAI

from config import settings

# Module-level singleton — created once when the app starts
# FastAPI will inject this into any route that needs it
_openai_client = OpenAI(api_key=settings.openai_api_key)
_async_openai_client = AsyncOpenAI(api_key=settings.openai_api_key)


def get_openai_client() -> OpenAI:
    """
    FastAPI dependency that provides the shared OpenAI client.
    Using a singleton avoids creating a new HTTP client per request.
    """
    return _openai_client


def get_async_openai_client() -> AsyncOpenAI:
    """
    FastAPI dependency that provides a shared async OpenAI client.
    This is used by streaming endpoints that consume async iterators.
    """
    return _async_openai_client
