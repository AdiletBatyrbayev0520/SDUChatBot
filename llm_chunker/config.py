import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL: str = os.getenv("LLM_CHUNKER_MODEL", "gpt-4o-mini")


def get_openai_api_key() -> str | None:
    return os.getenv("OPENAI_API_KEY") or None


