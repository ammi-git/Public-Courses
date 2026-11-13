"""Serveur MCP minimal (démonstration en séance).

Tester :  fastmcp dev mcp_server_demo.py      (ouvre l'inspecteur MCP)
Lancer :  python mcp_server_demo.py           (transport stdio)
"""
from fastmcp import FastMCP

mcp = FastMCP("demo")


@mcp.tool
def compter_mots(texte: str) -> int:
    """Compte le nombre de mots d'un texte."""
    return len(texte.split())


if __name__ == "__main__":
    mcp.run()
