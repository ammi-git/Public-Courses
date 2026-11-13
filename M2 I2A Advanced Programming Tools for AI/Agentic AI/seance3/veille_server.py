# ✏️ À COMPLÉTER
import arxiv
from mcp.server.fastmcp import FastMCP  # SDK MCP officiel

mcp = FastMCP("veille")


@mcp.tool()
def search_arxiv(query: str, max_results: int = 5) -> list[dict]:
    """TODO : reprendre la docstring de votre outil de la séance 1."""
    ...  # TODO : reprendre le corps de votre search_arxiv de la séance 1


if __name__ == "__main__":
    mcp.run()
