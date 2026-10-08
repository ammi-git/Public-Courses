# Séance 1 — Du LLM à l'agent outillé
**Agentic AI** · Master 2 I2A · Université Paris 8<br>
**Enseignant :** Pr Mehdi Ammi — Laboratoire LIASD (EA 4383)

*Note sur l'usage de l'IA : le contenu pédagogique (objectifs, progression, exercices, solutions) a été conçu par l'auteur. Claude Code (Anthropic) a été utilisé pour la mise en forme des supports.*

## Contenu du dossier

```
seance1/
├── README.md                 ce fichier
├── S1_agent_outille.ipynb    le notebook de la séance
├── requirements.txt          bibliothèques à installer
├── .env.example              modèle de configuration du LLM
├── .gitignore                empêche de publier vos clés (.env)
└── common/
    ├── llm.py                accès au LLM (local ou API)
    └── check_setup.py        vérification de l'installation
```

## Installation

```bash
cd seance1
python -m venv .venv && source .venv/bin/activate    # Windows : .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # puis choisir l'option A ou B dans .env
python common/check_setup.py  # doit afficher « OK »
jupyter lab S1_agent_outille.ipynb
```

## Choisir son modèle

- **Option A — local (gratuit)** : installer [Ollama](https://ollama.com), puis `ollama pull qwen3:8b`. 16 Go de RAM conseillés.
- **Option B — API avec un compte personnel** : tout fournisseur compatible OpenAI. Activez un **plafond de dépense** sur votre compte.

Le fichier `.env` contient vos clés : **ne le commitez jamais**.

## Livrable

Le **Livrable 1** (en fin de notebook) est à déposer sur **Moodle**, dans l'espace « Livrable 1 » du cours, **à la fin de la journée**.
