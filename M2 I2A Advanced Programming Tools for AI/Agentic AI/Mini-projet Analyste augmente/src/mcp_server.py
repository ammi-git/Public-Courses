"""Serveur MCP du projet — À COMPLÉTER.

Il expose TOUS les outils de l'assistant. Lancé par le client en stdio :
    python src/mcp_server.py
Ne jamais utiliser print() ici : stdout est le canal du protocole MCP.
Voir docs/03_architecture.md, section 4.
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

RACINE = Path(__file__).resolve().parent.parent
load_dotenv(RACINE / ".env")

mcp = FastMCP("analyste")

# TODO : charger le dataset une seule fois au démarrage (chemin : os.getenv("DATASET_PATH"))


@mcp.tool()
def resumer_dataset(max_lignes: int = 10) -> str:
    """TODO : docstring précise pour le LLM — ce que l'outil renvoie et quand l'utiliser."""
    # TODO : borner max_lignes ; renvoyer schéma, types, statistiques descriptives et un échantillon
    raise NotImplementedError


@mcp.tool()
def statistiques(colonne: str, operation: str = "mean", groupe_par: str | None = None) -> str:
    """TODO : docstring précise (liste des opérations autorisées, format de la réponse)."""
    # TODO : vérifier que les colonnes existent et que l'opération fait partie d'une liste fermée ;
    #        en cas de problème, RENVOYER un message d'erreur lisible au lieu de lever une exception
    raise NotImplementedError


@mcp.tool()
def chercher_documentation(requete: str, k: int = 4) -> list[dict]:
    """TODO : docstring précise (contenu du corpus, langue de la requête, format des passages)."""
    # TODO : borner k ; appeler la recherche de src/rag.py ; chaque passage indique sa source (fichier, page)
    raise NotImplementedError


if __name__ == "__main__":
    mcp.run()
