"""Vérifie l'installation, depuis le dossier seance2 : python common/check_setup.py"""
import importlib
import sys

PACKAGES = ['langchain', 'langchain_openai', 'pandas', 'matplotlib', 'dotenv']

ok = True
for p in PACKAGES:
    try:
        importlib.import_module(p)
    except ImportError:
        print(f"[manquant] {p} -> python -m pip install -r requirements.txt")
        ok = False

if ok:
    sys.path.append(".")
    from common.llm import get_llm, description_modele

    try:
        answer = get_llm().invoke("Réponds uniquement par le mot OK.").content
        print("Modèle :", description_modele())
        print("Réponse du modèle :", answer)
        print("OK : l'environnement est prêt.")
    except Exception as e:  # noqa: BLE001
        print("[erreur] appel au modèle impossible :", e)
        print("Vérifiez le fichier .env (et qu'Ollama tourne si vous êtes en local).")
