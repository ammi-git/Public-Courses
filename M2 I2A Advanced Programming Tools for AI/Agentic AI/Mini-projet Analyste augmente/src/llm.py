"""Accès au LLM (fourni) : le même code fonctionne avec Ollama ou une API compatible OpenAI."""
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

RACINE = Path(__file__).resolve().parent.parent
load_dotenv(RACINE / ".env", override=True)


def get_llm(temperature: float = 0.0, **kwargs) -> ChatOpenAI:
    """Renvoie le modèle configuré dans .env. Les appels sont bornés en durée et en longueur."""
    kwargs.setdefault("timeout", 180)
    kwargs.setdefault("max_tokens", 1500)
    model = os.getenv("LLM_MODEL")
    if not model:
        raise RuntimeError(f"LLM_MODEL est vide : créez {RACINE / '.env'} à partir de .env.example.")
    return ChatOpenAI(base_url=os.getenv("LLM_BASE_URL"), api_key=os.getenv("LLM_API_KEY", "ollama"),
                      model=model, temperature=temperature, **kwargs)
