# backend/llm/openai_api.py
# Function: Wrapper for OpenAI chat model calls

import os
from openai import OpenAI


_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_openai(prompt: str, allow_free_answer: bool = True) -> str:
    """
    Call the OpenAI Chat API (default model: gpt-4o-mini)
    - allow_free_answer=True: Allow the model to provide general maintenance/advice when no specific part/model/context is available
    - allow_free_answer=False: Restrict the model to only answer based on clear context/part/model (strict mode for RAG)
    """
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

    resp = _client.chat.completions.create(
        model="gpt-4o-mini",  
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=350,
    )
    return resp.choices[0].message.content.strip()
