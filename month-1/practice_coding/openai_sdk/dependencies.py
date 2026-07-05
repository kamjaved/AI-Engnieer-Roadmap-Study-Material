from openai import OpenAI

from config import settings

# Module-level singleton — created once when the app starts
# FastAPI will inject this into any route that needs it
_openai_client = OpenAI(api_key=settings.openai_api_key)


def get_openai_client() -> OpenAI:
    """
    FastAPI dependency that provides the shared OpenAI client.
    Using a singleton avoids creating a new HTTP client per request.
    """
    return _openai_client
