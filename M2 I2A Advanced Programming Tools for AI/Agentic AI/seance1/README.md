# Séance 1 — Du LLM à l'agent outillé
### Cours « Agentic AI » — M2 I2A

**Auteur :** Mehdi Ammi — Université Paris 8, laboratoire LIASD<br>
**Conception :** cours conçu, élaboré et mis en place par Mehdi Ammi<br>
**Mise en forme :** réalisée avec l'assistance de Claude Code (Anthropic)

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
