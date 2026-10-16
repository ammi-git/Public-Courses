# Séance 2 — Mémoire, RAG agentique et premier graphe
**Agentic AI** · Master 2 I2A · Université Paris 8<br>
**Enseignant :** Pr Mehdi Ammi — Laboratoire LIASD (EA 4383)

*Note sur l'usage de l'IA : le contenu pédagogique (objectifs, progression, exercices, solutions) a été conçu par l'auteur. Claude Code (Anthropic) a été utilisé pour la mise en forme des supports.*

## Contenu du dossier

```
seance2/
├── README.md                 ce fichier
├── S2_memoire_rag_graphe.ipynble notebook de la séance
├── data/
│   ├── corpus/               articles téléchargés par le notebook
│   └── livrable2/            PDF du livrable 2
├── requirements.txt          bibliothèques à installer
├── .env.example              modèle de configuration du LLM
├── .gitignore                empêche de publier vos clés (.env)
└── common/
    ├── llm.py                accès au LLM (local ou API)
    └── check_setup.py        vérification de l'installation
```

## Installation

```bash
cd seance2
python -m venv .venv && source .venv/bin/activate    # Windows : .venv\Scripts\activate
python -m pip install -r requirements.txt
cp ../seance1/.env .env   # réutiliser la configuration de la séance précédente
                              # (ou : cp .env.example .env, puis choisir l'option A ou B)
python common/check_setup.py  # doit afficher « OK »
jupyter lab S2_memoire_rag_graphe.ipynb
```

Le fichier `.env` doit se trouver **dans le dossier de la séance**, à côté de `common/`. Il contient vos clés : **ne le commitez jamais**.

## Mac à processeur Intel

PyTorch s'arrête à la version 2.2.2 sur ces machines. Si l'import de `sentence_transformers` échoue (erreur NumPy ou `name 'nn' is not defined`) :

```bash
python -m pip install "numpy<2" "transformers<4.50" "sentence-transformers<4"
```

Au premier lancement, le modèle d'embedding (environ 500 Mo) est téléchargé puis mis en cache.

## Livrable

Le **Livrable 2** (en fin de notebook) est à déposer sur **Moodle**, dans l'espace « Livrable 2 » du cours, **à la fin de la journée**.
