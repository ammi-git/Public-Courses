# Séance 2 — Prise en main de l'environnement et cas d'usage de l'IA
**Urbanisation des SI à l'ère de l'IA** · Master 2 CPI · Université Paris 8<br>
**Enseignant :** Pr Mehdi Ammi — Laboratoire LIASD (EA 4383)

*Note sur l'usage de l'IA : la progression pédagogique et le scénario ont été définis par l'auteur. Claude (Anthropic) a été utilisé pour la rédaction des exercices et la mise en forme des supports.*

## Contenu du dossier

```
seance2/
├── README.md                 ce fichier
├── S2_environnement_cas_usage.ipynble notebook de la séance
├── requirements.txt          bibliothèques à installer
├── .env.example              modèle de configuration du LLM
├── .gitignore                empêche de publier vos clés (.env)
├── livrables/                créé par le notebook (cartographie de la séance)
└── common/
    ├── llm.py                accès au LLM (local ou API)
    ├── embeddings.py         embeddings (sentence-transformers ou Ollama)
    ├── si.py                 SI simulé de la Ville de Saint-Denis
    ├── carto.py              cartographie du SI
    ├── rag.py                outils RAG (code de la séance 3)
    ├── outils.py             outils des agents (code de la séance 5)
    ├── serveur_mcp.py        serveur MCP du SI (séance 5)
    ├── check_setup.py        vérification de l'installation
    └── si_data/              données fictives : applications, familles, corpus documentaire
```

## Installation

```bash
cd seance2
python -m venv .venv && source .venv/bin/activate    # Windows : .venv\Scripts\activate
python -m pip install -r requirements.txt
cp .env.example .env          # puis choisir l'option A (local) ou B (API)
python common/check_setup.py  # doit afficher « OK »
jupyter lab S2_environnement_cas_usage.ipynb
```

Le fichier `.env` doit se trouver **dans le dossier de la séance**, à côté de `common/`. Il contient vos clés : **ne le commitez jamais**.

## Livrable

Le **Livrable 2** (en fin de notebook) est à déposer sur **Moodle**, dans l'espace « Livrable 2 » du cours, **à la fin de la séance**. Un dépôt par groupe.
