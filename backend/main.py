# backend/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os


from agents.partselect_agent import chat_with_agent

app = FastAPI()

# === CORS settings (restrict allow_origins to your actual frontend source) ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # can change to ["http://localhost:3000"] or frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat_api(request: Request):
    """
    Receive { message, provider } from frontend:
      - message: User input message
      - provider: "openai" or "deepseek" (optional, default is openai)
    """
    data = await request.json()
    user_input = (data.get("message") or "").strip()
    provider = (data.get("provider") or "openai").lower()

    if not user_input:
        return {"response": "Please enter a question so I can answer!"}

    # —— Model provider switching strategy ——
    # 1) Set provider to environment variable; if llm_api reads DEFAULT_PROVIDER, it will take effect immediately
    os.environ["DEFAULT_PROVIDER"] = provider

    # 2) Try passing provider to the agent (if old version of chat_with_agent does not accept this param, fallback automatically)
    try:
        response = chat_with_agent(user_input, provider=provider)
    except TypeError:
        # Old signature: chat_with_agent(text) → still works
        response = chat_with_agent(user_input)

    return {"response": response}
