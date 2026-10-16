"""Accès unique au LLM pour tout le cours.

Le même code fonctionne avec Ollama (local) ou une API compatible OpenAI :
seul le fichier .env change.
"""
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


def get_llm(temperature: float = 0.0, **kwargs) -> ChatOpenAI:
    """Retourne le modèle de chat configuré dans le fichier .env."""
    model = os.getenv("LLM_MODEL")
    if not model:
        raise RuntimeError("LLM_MODEL est vide : copiez .env.example en .env et complétez-le.")
    return ChatOpenAI(
        base_url=os.getenv("LLM_BASE_URL"),
        api_key=os.getenv("LLM_API_KEY", "ollama"),
        model=model,
        temperature=temperature,
        **kwargs,
    )
