# 06 — Guide technique

[← Retour au README](../README.md)

## Installation

Travaillez dans un **environnement dédié**, sinon l'installation peut modifier des bibliothèques partagées par vos autres projets.

```bash
conda create -n analyste python=3.11 -y
conda activate analyste
python -m pip install -r requirements.txt
cp .env.example .env
python src/check_setup.py
```

Dans Jupyter ou VS Code, choisissez le noyau **analyste**.

> Les messages `pip's dependency resolver ... incompatible` sont des **avertissements** : l'installation a réussi si la dernière ligne n'est pas `ERROR: Could not install`.

## Modèle

| Option | Configuration dans `.env` | Remarque |
| --- | --- | --- |
| Local (Ollama) | `LLM_BASE_URL=http://localhost:11434/v1`, `LLM_MODEL=qwen2.5:7b` | lancer `ollama serve` ; un modèle de 7 à 8 milliards de paramètres est nettement plus fiable qu'un modèle de 3 milliards pour les outils et les sorties structurées |
| API | `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL` du fournisseur | activer un plafond de dépense |

## Versions MCP

`langchain-mcp-adapters` ne fonctionne pas encore avec `mcp` 2.x. Les versions testées ensemble sont fixées dans `requirements.txt` : `mcp==1.30.0` et `langchain-mcp-adapters==0.3.2`. Le serveur s'écrit avec la classe `FastMCP` du SDK officiel :

```python
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("analyste")

@mcp.tool()          # avec les parenthèses
def mon_outil(...): ...
```

## Erreurs fréquentes

| Erreur | Cause | Solution |
| --- | --- | --- |
| `McpError: Connection closed` | le serveur MCP plante au démarrage | le lancer à la main (`python src/mcp_server.py`) pour lire son erreur |
| `ImportError: cannot import name 'RequestContext'` | `mcp` en version 2.x | `pip install "mcp==1.30.0"`, puis redémarrer le noyau |
| Le serveur MCP ne trouve pas ses bibliothèques | il est lancé avec un autre Python | lancer le serveur avec `sys.executable` et un chemin absolu |
| `UnsupportedOperation: fileno` (Windows, dans Jupyter) | la sortie d'erreur du notebook n'est pas un vrai fichier, or le client MCP en a besoin pour lancer le serveur | avant de créer le client : `sys.stderr = open("mcp_stderr.log", "a", encoding="utf-8")` |
| `APIConnectionError: Connection error` | le LLM ne répond pas | lancer Ollama (`ollama serve`) ou vérifier `LLM_BASE_URL` |
| `LLM_MODEL est vide` | `.env` absent ou non relu | créer `.env` à la racine du projet, redémarrer le noyau |
| `ValidationError` sur une sortie structurée | le modèle répond dans un mauvais format | utiliser `src/sortie.py` (`structurer`), qui réessaie et valide |
| Cellule qui ne se termine pas | génération sans fin d'un petit modèle | `max_tokens` et `timeout` sont fixés dans `src/llm.py` ; interrompre et vérifier le modèle |
| `print` dans le serveur MCP casse le dialogue | stdout est le canal du protocole | ne jamais utiliser `print` dans le serveur ; écrire dans un fichier de log ou sur stderr |

## Exécution isolée du code généré

Principe minimal attendu :

```python
INTERDITS = ("import os", "import sys", "subprocess", "open(", "__import__", "eval(", "exec(", "socket")
AUTORISES = ("import pandas", "import plotly", "from plotly")   # déjà fournis dans l'espace de noms

def executer_isole(code: str, df):
    if any(motif in code for motif in INTERDITS):
        return None, "Code refusé : instruction interdite."
    # les imports autorisés sont retirés : pd, px et go sont fournis directement
    code = "\n".join(l for l in code.splitlines() if not l.strip().startswith(AUTORISES))
    if any(l.strip().startswith(("import ", "from ")) for l in code.splitlines()):
        return None, "Code refusé : import non autorisé."
    builtins_surs = {"len": len, "range": range, "min": min, "max": max, "sum": sum,
                     "sorted": sorted, "round": round, "list": list, "dict": dict, "str": str}
    espace = {"df": df.copy(), "pd": pd, "px": px, "go": go}
    try:
        exec(code, {"__builtins__": builtins_surs, **espace}, espace)
        return espace.get("fig"), None
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"
```

C'est une isolation **pédagogique**, pas une protection contre un attaquant. Pour aller plus loin : exécution dans un sous-processus avec un délai maximal (vu en séance 1 d'Agentic AI).

## Streamlit

```bash
streamlit run src/app.py
```

Le graphe est asynchrone si vous utilisez les outils MCP : dans Streamlit, appelez-le avec `asyncio.run(graphe.ainvoke(...))`.
