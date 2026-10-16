"""Embeddings du cours (séances 2 et 3).

Deux moteurs au choix, réglés dans le fichier .env :

- EMBEDDING_BACKEND=sentence-transformers (par défaut)
  modèle local paraphrase-multilingual-MiniLM-L12-v2, via PyTorch ;
- EMBEDDING_BACKEND=ollama
  modèle paraphrase-multilingual servi par Ollama, sans PyTorch
  (utile sur Mac Intel) : ollama pull paraphrase-multilingual

Les deux modèles sont multilingues et produisent des vecteurs normalisés.
"""
import os
from pathlib import Path

import numpy as np
import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)
load_dotenv()

BACKEND = os.getenv("EMBEDDING_BACKEND", "sentence-transformers").strip().lower()
MODELE_ST = "paraphrase-multilingual-MiniLM-L12-v2"
MODELE_OLLAMA = os.getenv("EMBEDDING_MODEL", "paraphrase-multilingual")
URL_OLLAMA = os.getenv("OLLAMA_URL", "http://localhost:11434")

_modele_st = None
_ollama_ok = False


def _verifier_ollama() -> None:
    """Vérifie une fois qu'Ollama répond et que le modèle d'embedding est téléchargé."""
    global _ollama_ok
    if _ollama_ok:
        return
    try:
        modeles = requests.get(f"{URL_OLLAMA}/api/tags", timeout=5).json().get("models", [])
    except requests.RequestException as e:
        raise RuntimeError(f"Ollama ne répond pas sur {URL_OLLAMA} : lancez « ollama serve ».") from e
    noms = {m["name"].split(":")[0] for m in modeles}
    if MODELE_OLLAMA.split(":")[0] not in noms:
        raise RuntimeError(f"Modèle absent : lancez « ollama pull {MODELE_OLLAMA} » dans un terminal.")
    _ollama_ok = True


def encoder(textes: list[str]) -> np.ndarray:
    """Renvoie une matrice (n_textes, dimension) de vecteurs normalisés."""
    textes = list(textes)
    if BACKEND == "ollama":
        _verifier_ollama()
        r = requests.post(f"{URL_OLLAMA}/api/embed",
                          json={"model": MODELE_OLLAMA, "input": textes}, timeout=(5, 120))
        r.raise_for_status()
        vecteurs = np.array(r.json()["embeddings"], dtype=float)
    else:
        global _modele_st
        if _modele_st is None:
            from sentence_transformers import SentenceTransformer
            _modele_st = SentenceTransformer(MODELE_ST)
        vecteurs = np.asarray(_modele_st.encode(textes), dtype=float)
    return vecteurs / np.linalg.norm(vecteurs, axis=1, keepdims=True)


def chroma_embedding_function():
    """Fonction d'embedding à passer à ChromaDB (create_collection(..., embedding_function=...))."""
    if BACKEND != "ollama":
        from chromadb.utils import embedding_functions
        return embedding_functions.SentenceTransformerEmbeddingFunction(MODELE_ST)

    from chromadb import Documents, EmbeddingFunction, Embeddings

    class OllamaEF(EmbeddingFunction):
        def __init__(self):
            pass

        def __call__(self, input: Documents) -> Embeddings:
            return encoder(input).tolist()

    return OllamaEF()
