# Séance 2 — Mémoire, RAG agentique et premier graphe
**Agentic AI** · Master 2 I2A · Université Paris 8<br>
**Enseignant :** Pr Mehdi Ammi — Laboratoire LIASD (EA 4383)

*Note sur l'usage de l'IA : le contenu pédagogique (objectifs, progression, exercices, solutions) a été conçu par l'auteur. Claude Code (Anthropic) a été utilisé pour la mise en forme des supports.*

## Contenu du dossier

```
seance2/
├── README.md                 ce fichier
├── S2_memoire_rag_graphe.ipynb  le notebook de la séance
├── data/
│   ├── corpus/               articles téléchargés par le notebook
│   └── livrable2/            PDF du livrable 2
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
cd seance2
python -m venv .venv && source .venv/bin/activate    # Windows : .venv\Scripts\activate
python -m pip install -r requirements.txt
cp ../seance1/.env .env   # réutiliser la configuration de la séance précédente
                              # (ou : cp .env.example .env, puis choisir l'option A ou B)
python common/check_setup.py  # doit afficher « OK »
jupyter lab S2_memoire_rag_graphe.ipynb
```

Le fichier `.env` doit se trouver **dans le dossier de la séance**, à côté de `common/`. Il contient vos clés : **ne le commitez jamais**.

## Moteur d'embeddings (Mac Intel)

Par défaut, les embeddings sont calculés avec `sentence-transformers` (PyTorch). Sur un **Mac à processeur Intel**, PyTorch est bloqué en version 2.2.2 et l'import de `sentence_transformers` peut échouer (erreur NumPy ou `name 'nn' is not defined`). Utilisez alors Ollama, sans PyTorch :

```bash
ollama pull paraphrase-multilingual
echo "EMBEDDING_BACKEND=ollama" >> .env
```

puis redémarrez le noyau du notebook. Le choix est lu par `common/embeddings.py`.

## Livrable

Le **Livrable 2** (en fin de notebook) est à déposer sur **Moodle**, dans l'espace « Livrable 2 » du cours, **à la fin de la journée**.
