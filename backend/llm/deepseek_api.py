# Function: Wrapper for DeepSeek Chat API calls (using OpenAI SDK, compatible format)
# Notes:
# - Must set environment variable first: export DEEPSEEK_API_KEY="your_key"
# - Optional settings (can be omitted to use defaults):
#     export DEEPSEEK_BASE="https://api.deepseek.com"
#     export DEEPSEEK_MODEL="deepseek-chat"    # or deepseek-reasoner
#
# - allow_free_answer=True: Allows general maintenance/advice when no clear context/part/model is available
# - allow_free_answer=False: Only answer based on context/part/model (used with strict RAG mode)

import os
from typing import Optional
from openai import OpenAI

# Read environment variables (provide defaults so it can run without explicit settings)
_DEEPSEEK_BASE = os.getenv("DEEPSEEK_BASE", "https://api.deepseek.com")
_DEFAULT_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

def _build_client() -> OpenAI:
    """Create a DeepSeek-specific OpenAI-compatible client (with base_url)"""
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("DeepSeek API key is missing. Please set DEEPSEEK_API_KEY.")
    return OpenAI(api_key=api_key, base_url=_DEEPSEEK_BASE)

def call_deepseek(
    prompt: str,
    model: Optional[str] = None,
    allow_free_answer: bool = True,
    temperature: float = 0.7,
    max_tokens: int = 350,
) -> str:
    """
    Call the DeepSeek Chat API (non-streaming)
    :param prompt: The final text to send to the model (already prepared upstream)
    :param model: Specify DeepSeek model; default is deepseek-chat, can be changed to deepseek-reasoner
    :param allow_free_answer: True → Free-form answer (fallback/general advice); False → Strict answer (RAG mode)
    :param temperature: Sampling temperature
    :param max_tokens: Maximum number of tokens to generate
    :return: English answer string (stripped)
    """
    client = _build_client()
    model = model or _DEFAULT_MODEL

    # Generate system prompt based on mode
    if allow_free_answer:
        system_prompt = (
            "You are a helpful assistant for PartSelect customers. "
            "You can answer questions about refrigerators and dishwashers, including parts, installation, "
            "maintenance tips, troubleshooting, detergent recommendations, and best practices. "
            "Always answer in plain English and be concise."
        )
    else:
        system_prompt = (
            "You are a support assistant for PartSelect refrigerator/dishwasher parts. "
            "Only use the provided context or concrete part/model details. "
            "If unsure, say you are not sure."
        )

    try:
        resp = client.chat.completions.create(
            model=model,  
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"DeepSeek request failed: {e}"
