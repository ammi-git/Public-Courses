"""Livrable 3 — serveur MCP « agenda ».

À compléter : exposer list_events et add_event sur le fichier agenda.json.
Tester avec : fastmcp dev agenda_server.py
"""
import json
from pathlib import Path

from fastmcp import FastMCP

AGENDA = Path(__file__).parent / "agenda.json"
mcp = FastMCP("agenda")


# TODO : outil list_events(date_debut: str, date_fin: str) -> list[dict]
#        renvoie les événements entre deux dates (format AAAA-MM-JJ)


# TODO : outil add_event(date: str, debut: str, fin: str, titre: str) -> str
#        ajoute un événement s'il ne chevauche pas un événement existant,
#        sinon renvoie un message d'erreur lisible


if __name__ == "__main__":
    mcp.run()
