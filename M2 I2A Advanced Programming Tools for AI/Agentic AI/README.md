# Agentic AI — M2 I2A

**Agentic AI** · Master 2 I2A · Université Paris 8<br>
**Enseignant :** Pr Mehdi Ammi — Laboratoire LIASD (EA 4383)

*Note sur l'usage de l'IA : le contenu pédagogique (objectifs, progression, exercices, solutions) a été conçu par l'auteur. Claude Code (Anthropic) a été utilisé pour la mise en forme des supports.*

Cours pratique en 4 séances de 6 h pour construire, pas à pas, un **assistant de veille scientifique** avec LangGraph.

| Séance | Notebook | Thème |
| --- | --- | --- |
| 1 | `seance1/S1_agent_outille.ipynb` | Du LLM à l'agent outillé : ReAct, `create_agent`, tool calling |
| 2 | `seance2/S2_memoire_rag_graphe.ipynb` | Mémoire, RAG agentique, premier `StateGraph` |
| 3 | `seance3/S3_patterns_mcp_multiagents.ipynb` | Patterns, validation humaine, MCP, multi-agents |
| 4 | `seance4/S4_evaluation_securite.ipynb` | Évaluation, sécurité, démos |

Chaque notebook contient : les notions, les exercices guidés, les exercices non guidés, le **livrable de fin de séance**, à déposer sur **Moodle à la fin de chaque journée**, et des **exercices d'approfondissement**.

## Installation

```bash
git clone <url-du-depot>
cd agentic-ai-m2/seance1          # chaque séance est un dossier autonome
python -m venv .venv && source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env              # puis choisir l'option A ou B
python common/check_setup.py
jupyter lab
```

## Choisir son modèle : local ou API

Tout le code passe par `common/llm.py` : changer de modèle se fait **uniquement** dans `.env`.

- **Option A — local (gratuit)** : installer [Ollama](https://ollama.com), puis `ollama pull qwen3:8b`. 16 Go de RAM conseillés.
- **Option B — API avec un compte personnel** : tout fournisseur compatible OpenAI. Activez un **plafond de dépense** sur votre compte.

## Règles

- Le fichier `.env` contient vos clés : il est dans `.gitignore`, **ne le commitez jamais**.
- Chaque agent a une limite d'itérations (`recursion_limit`).
- Travail individuel. Chaque séance se termine par un journal de bord (un échec, sa cause, sa correction).

## Structure

```
seance1/         notebook S1
seance2/         notebook S2 + data/ (corpus, PDF du livrable 2)
seance3/         notebook S3 + serveurs MCP (démo et squelette du livrable 3)
seance4/         notebook S4

Chaque dossier de séance est autonome : common/ (accès au LLM, vérification),
requirements.txt, .env.example, .gitignore et README.md. Le fichier .env se place
dans le dossier de la séance (copiez celui de la séance précédente).
```
