# Séance 3 — Patterns, validation humaine, MCP et multi-agents
**Agentic AI** · Master 2 I2A · Université Paris 8<br>
**Enseignant :** Pr Mehdi Ammi — Laboratoire LIASD (EA 4383)

*Note sur l'usage de l'IA : le contenu pédagogique (objectifs, progression, exercices, solutions) a été conçu par l'auteur. Claude Code (Anthropic) a été utilisé pour la mise en forme des supports.*

## Contenu du dossier

```
seance3/
├── README.md                 ce fichier
├── S3_patterns_mcp_multiagents.ipynb  le notebook de la séance
├── mcp_server_demo.py      serveur MCP de démonstration
├── agenda_server.py        squelette du serveur du livrable 3
├── agenda.json             données de l'agenda
├── requirements.txt          bibliothèques à installer
├── .env.example              modèle de configuration du LLM
├── .gitignore                empêche de publier vos clés (.env)
└── common/
    ├── llm.py                accès au LLM (local ou API)
    ├── embeddings.py         embeddings (sentence-transformers ou Ollama)
    └── check_setup.py        vérification de l'installation
```

## Installation

```bash
cd seance3
python -m venv .venv && source .venv/bin/activate    # Windows : .venv\Scripts\activate
python -m pip install -r requirements.txt
cp ../seance2/.env .env   # réutiliser la configuration de la séance précédente
                              # (ou : cp .env.example .env, puis choisir l'option A ou B)
python common/check_setup.py  # doit afficher « OK »
jupyter lab S3_patterns_mcp_multiagents.ipynb
```

## Environnement dédié (recommandé)

Installez le cours dans un **environnement séparé** de vos autres projets : sinon, l'installation met à jour des bibliothèques partagées (`mcp`, `numpy`, `protobuf`…) et peut casser d'autres outils.

```bash
# Avec conda (Anaconda)
conda create -n agentic python=3.11 -y
conda activate agentic
python -m pip install -r requirements.txt ipykernel
```

Puis choisissez le noyau **agentic** dans Jupyter ou VS Code (*Select Kernel*). Avec `venv`, utilisez la commande `python -m venv .venv` ci-dessus.

> Les messages `pip's dependency resolver ... incompatible` sont des **avertissements** sur d'autres paquets de l'environnement : l'installation a réussi si la dernière ligne n'est pas `ERROR: Could not install`.


Le fichier `.env` doit se trouver **dans le dossier de la séance**, à côté de `common/`. Il contient vos clés : **ne le commitez jamais**.

## Tester un serveur MCP

```bash
npx @modelcontextprotocol/inspector python mcp_server_demo.py   # ouvre l'inspecteur MCP dans le navigateur (nécessite Node.js)
```

## Livrable

Le **Livrable 3** (en fin de notebook) est à déposer sur **Moodle**, dans l'espace « Livrable 3 » du cours, **à la fin de la journée**.
