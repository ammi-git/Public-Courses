"""Vérifie l'installation (fourni) : python src/check_setup.py"""
import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
PAQUETS = ["langgraph", "langchain", "langchain_openai", "pydantic", "dotenv", "pandas", "plotly",
           "streamlit", "chromadb", "pypdf", "mcp", "langchain_mcp_adapters"]

manquants = [p for p in PAQUETS if importlib.util.find_spec(p) is None]
if manquants:
    sys.exit(f"[manquant] {', '.join(manquants)} -> python -m pip install -r requirements.txt")

from llm import get_llm  # noqa: E402

try:
    print("Réponse du modèle :", get_llm().invoke("Réponds uniquement par le mot OK.").content)
    print("OK : l'environnement est prêt.")
except Exception as e:  # noqa: BLE001
    print("[erreur] appel au modèle impossible :", e)
