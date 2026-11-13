"""Accès unique au LLM pour tout le cours.

Le même code fonctionne avec Ollama (local) ou une API compatible OpenAI :
seul le fichier .env change.
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
