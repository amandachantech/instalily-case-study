# backend/llm/llm_api.py
# Function: Unified routing for LLM calls (OpenAI / DeepSeek) and providing embeddings (for RAG)

import os
from openai import OpenAI  # Only used for embeddings
from .openai_api import call_openai
from .deepseek_api import call_deepseek  

# Default provider is OpenAI; to switch to DeepSeek, change to "deepseek"
DEFAULT_PROVIDER = "deepseek"              # "openai" or "deepseek"
DEFAULT_DEEPSEEK_MODEL = "deepseek-chat"   # or "deepseek-reasoner"

def call_llm(prompt: str, provider: str | None = None, allow_free_answer: bool = True) -> str:
    """
    Call the appropriate LLM based on provider.
    - provider: "openai" / "deepseek"; if None, uses DEFAULT_PROVIDER
    - allow_free_answer:
        True  → Allow the model to answer freely (for fallback / maintenance advice, etc.)
        False → Strictly follow the provided context (for RAG answers)
    """
    selected = (provider or DEFAULT_PROVIDER).lower()

    if selected == "deepseek":
        return call_deepseek(
            prompt,
            model=DEFAULT_DEEPSEEK_MODEL,
            allow_free_answer=allow_free_answer
        )

    # Default: OpenAI
    return call_openai(prompt, allow_free_answer=allow_free_answer)

def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Generate text embeddings (for RAG use).
    Currently uses OpenAI embeddings (DeepSeek does not have official embeddings yet).
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    return [item.embedding for item in resp.data]
