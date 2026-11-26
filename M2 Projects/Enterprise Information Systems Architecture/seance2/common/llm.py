"""Accès unique au modèle de langage pour tout le cours.

Le même code fonctionne avec un modèle local (Ollama) ou une API compatible
OpenAI (GitHub Models, Mistral...) : seul le fichier .env change.
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Le fichier .env est cherché dans le dossier de la séance (parent de common/),
# puis dans le dossier courant et ses parents.
DOSSIER_SEANCE = Path(__file__).resolve().parent.parent
load_dotenv(DOSSIER_SEANCE / ".env", override=True)  # le .env de la séance est prioritaire
load_dotenv()


def get_llm(temperature: float = 0.0, **kwargs) -> ChatOpenAI:
    """Retourne le modèle de chat configuré dans le fichier .env."""
    model = os.getenv("LLM_MODEL")
    if not model:
        raise RuntimeError(
            f"LLM_MODEL est vide : aucun fichier .env valide dans {DOSSIER_SEANCE}. "
            "Copiez .env.example en .env, complétez-le, puis redémarrez le noyau."
        )
    return ChatOpenAI(
        base_url=os.getenv("LLM_BASE_URL"),
        api_key=os.getenv("LLM_API_KEY", "ollama"),
        model=model,
        temperature=temperature,
        **kwargs,
    )


def description_modele() -> str:
    """Indique le modèle utilisé et s'il est local ou distant."""
    url = os.getenv("LLM_BASE_URL", "")
    lieu = "local (Ollama)" if ("localhost" in url or "127.0.0.1" in url) else f"API distante ({url})"
    return f"{os.getenv('LLM_MODEL')} — {lieu}"


def get_llm_alternatif(temperature: float = 0.0, **kwargs) -> ChatOpenAI | None:
    """Second modèle (variables LLM2_* du .env), pour comparer local et API. None s'il n'est pas configuré."""
    model = os.getenv("LLM2_MODEL")
    if not model:
        return None
    return ChatOpenAI(base_url=os.getenv("LLM2_BASE_URL"), api_key=os.getenv("LLM2_API_KEY", "ollama"),
                      model=model, temperature=temperature, **kwargs)
