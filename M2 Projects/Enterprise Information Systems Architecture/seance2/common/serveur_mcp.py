"""Serveur MCP du SI simulé de Saint-Denis (séance 5).

Il expose quelques API du SI selon le protocole MCP, pour que n'importe quel
agent compatible puisse les utiliser. Lancé automatiquement par le notebook :
    python common/serveur_mcp.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mcp.server.fastmcp import FastMCP  # noqa: E402

from common import si  # noqa: E402

serveur = FastMCP("SI Ville de Saint-Denis")


@serveur.tool()
def consulter_famille(id_famille: str) -> dict:
    """Consulte le dossier d'une famille dans le portail famille (par exemple "FAM001")."""
    return si.cantine_consulter_famille(id_famille)


@serveur.tool()
def tarif_repas(quotient_familial: int | None) -> float:
    """Prix d'un repas de cantine (en euros) en 2026-2027 selon le quotient familial (null s'il n'est pas calculé)."""
    return si.cantine_tarif_repas(quotient_familial)


@serveur.tool()
def consulter_stationnement(id_resident: str) -> dict:
    """Consulte la situation d'un résident pour la carte de stationnement (par exemple "RES001")."""
    return si.stationnement_consulter(id_resident)


if __name__ == "__main__":
    serveur.run()
