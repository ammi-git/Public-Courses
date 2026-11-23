"""Indexation et recherche documentaire — À COMPLÉTER.

    python src/rag.py      # indexe data/corpus/ dans chroma_db/
Voir docs/03_architecture.md, section 5.
"""
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
TAILLE, RECOUVREMENT = 800, 150   # TODO : à justifier dans le rapport


def extraire_textes(dossier: Path) -> list[dict]:
    """Renvoie [{"texte", "source", "page"}] pour chaque page des PDF et fichiers .txt du dossier."""
    raise NotImplementedError


def decouper(texte: str, taille: int = TAILLE, recouvrement: int = RECOUVREMENT) -> list[str]:
    """Découpe un texte en morceaux qui se recouvrent."""
    raise NotImplementedError


def indexer(dossier: Path = RACINE / "data" / "corpus") -> int:
    """Découpe, calcule les embeddings et stocke les morceaux dans ChromaDB ; renvoie le nombre de morceaux."""
    raise NotImplementedError


def chercher(requete: str, k: int = 4) -> list[dict]:
    """Renvoie les k passages les plus proches : [{"texte", "source", "page", "score"}]."""
    raise NotImplementedError


if __name__ == "__main__":
    print(indexer(), "morceaux indexés")
