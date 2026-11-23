"""Graphe LangGraph de l'assistant — À COMPLÉTER. Évalué pour la note Agentic AI.

Voir docs/03_architecture.md, sections 1 à 8.
"""
import os
import sys
from pathlib import Path
from typing import Annotated, Literal, TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.types import Command, interrupt  # noqa: F401  (utilisés dans le nœud valider)
from langchain_mcp_adapters.client import MultiServerMCPClient
from pydantic import BaseModel, Field

SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC))
from llm import get_llm  # noqa: E402
from sortie import structurer  # noqa: E402,F401

CLIENT_MCP = MultiServerMCPClient({
    "analyste": {"command": sys.executable, "args": [str(SRC / "mcp_server.py")], "transport": "stdio"},
})


class Route(BaseModel):
    raisonnement: str = Field(description="En 2 phrases : ce que demande l'utilisateur et quelle source y répond")
    destination: Literal["documentation", "analyse", "visualisation"]


class EtatAssistant(TypedDict):
    messages: Annotated[list, add_messages]
    destination: str
    figures: list
    code: str
    journal: list[str]
    dashboard: str | None


async def construire_graphe():
    """Charge les outils MCP, crée les nœuds et compile le graphe avec un checkpointer."""
    llm = get_llm()
    outils = {o.name: o for o in await CLIENT_MCP.get_tools()}  # noqa: F841

    # TODO : nœud routeur (structurer(llm, Route, ...)) qui range la destination dans l'état
    # TODO : nœud documentation (agent RAG qui cite ses sources)
    # TODO : nœud analyse (create_agent + system prompt + recursion_limit)
    # TODO : nœud visualisation (appelle viz_pipeline.pipeline)
    # TODO : nœud valider (interrupt, puis Command(goto=...))
    # TODO : nœud de résumé de l'historique au-delà de N messages

    g = StateGraph(EtatAssistant)
    # TODO : g.add_node(...), g.add_edge(START, ...), g.add_conditional_edges(...)
    return g.compile(checkpointer=InMemorySaver())
