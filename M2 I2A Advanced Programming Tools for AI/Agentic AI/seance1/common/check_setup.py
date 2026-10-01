"""Vérifie l'installation, depuis le dossier seance1 : python common/check_setup.py"""
import importlib
import sys

PACKAGES = ["langgraph", "langchain", "langchain_openai", "pydantic", "dotenv", "arxiv", "pypdf"]

ok = True
for p in PACKAGES:
    try:
        importlib.import_module(p)
    except ImportError:
        print(f"[manquant] {p} -> pip install -r requirements.txt")
        ok = False

if ok:
    sys.path.append(".")
    from common.llm import get_llm

    try:
        answer = get_llm().invoke("Réponds uniquement par le mot OK.").content
        print("Réponse du modèle :", answer)
        print("OK : l'environnement est prêt.")
    except Exception as e:  # noqa: BLE001
        print("[erreur] appel au modèle impossible :", e)
        print("Vérifiez le fichier .env (et qu'Ollama tourne si vous êtes en local).")
