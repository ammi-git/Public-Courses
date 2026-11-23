# Mini-projet — Assistant d'analyse de données ouvertes

**Évaluation :** démo, revue de code et questions orales

---

## 1. Objectif

Construire un assistant conversationnel qui répond en langage naturel à des questions sur **un jeu de données que tu choisis**, et qui affiche les résultats sous forme de graphiques.

Le projet doit démontrer que tu sais :

- exposer des données via un **serveur MCP** (FastMCP) ;
- créer un **agent ReAct** (LangGraph) qui choisit et enchaîne des tools ;
- produire une **visualisation Plotly** à partir d'un tool local ;
- présenter le tout dans une **interface Streamlit** ;
- explorer et nettoyer des données de manière documentée.

---

## 2. Cahier des charges — choix du jeu de données

### 2.1 Critères obligatoires

| Critère | Exigence |
|---|---|
| Volume | ≥ 500 lignes et ≥ 5 colonnes exploitables |
| Format | CSV, Excel, JSON ou base SQLite, lisible sans infrastructure lourde |
| Source | URL d'origine et date de téléchargement citées |
| Usage | Permet de répondre à au moins 3 questions d'analyse différentes |
| Données personnelles | Aucune donnée nominative ni identifiante ; données agrégées ou anonymisées |

### 2.2 Critères de qualité (à justifier dans le README et le notebook)

- **Pertinence** : le jeu correspond à un besoin concret, avec un utilisateur qui a une question précise.
- **Couverture** : la période et le périmètre du jeu sont décrits.
- **Limites** : valeurs manquantes et biais de collecte identifiés et expliqués.
- **Nettoyage** : les étapes de nettoyage (types, doublons, valeurs manquantes) sont listées et justifiées.

### 2.3 Interdits

- Un jeu déjà utilisé dans le cours ou à l'épreuve.
- Un jeu qui doit être téléchargé à chaque lancement sans script documenté.
- Une API payante, ou une API nécessitant une clé qui serait exposée dans le code.

### 2.4 Où chercher

**Portails généraux**

- data.gouv.fr (France)
- data.europa.eu (Union européenne)
- INSEE (France)
- Eurostat (Europe)
- Our World in Data (monde)
- Banque mondiale, Open Data (monde)
- OpenFoodFacts (produits alimentaires)
- Open-Meteo (météo historique, API)
- OpenStreetMap (données géographiques)

**Catalogues et dépôts**

- Kaggle
- Hugging Face Datasets
- UCI Machine Learning Repository
- Zenodo (jeux de données de recherche)
- Google Dataset Search

Vérifie chaque adresse et la taille du jeu sur sa page avant de le retenir.

---

## 3. Livrable : dépôt GitHub

### 3.1 Arborescence attendue

```
nom-prenom-projet/
├── README.md                     # documentation du projet (voir section 4)
├── requirements.txt              # dépendances
├── data/
│   ├── <jeu>.csv                 # données, ou script de téléchargement documenté
│   └── SOURCE.md                 # URL, date de récupération, description des colonnes
├── notebooks/
│   └── 01_exploration.ipynb      # exploration, nettoyage, tests des tools et de l'agent
├── mcp_<nom>_server.py           # serveur MCP (FastMCP, au moins 3 tools)
├── viz.py                        # tool make_dashboard (@tool, au moins 2 graphiques)
├── agent.py                      # agent ReAct, system prompt, mémoire
├── app.py                        # interface Streamlit
└── assets/
    ├── architecture.png          # schéma d'architecture
    └── dashboard.html            # dashboard généré
```

Le découpage en `agent.py` et `viz.py` est recommandé. Il permet de tester chaque composant séparément dans le notebook.

### 3.2 Serveur MCP (`mcp_<nom>_server.py`)

- Au moins **3 tools** décorés `@mcp.tool()`, avec une docstring claire.
- Chaque tool **retourne une `str`** : pas de DataFrame, pas d'objet Plotly.
- Les requêtes SQL utilisent des **paramètres liés**, jamais une f-string construite à partir de l'entrée de l'utilisateur ou du LLM.
- Les chemins sont relatifs au fichier (`os.path.dirname(__file__)`).
- Gestion d'erreur : un tool qui échoue retourne un message lisible, sans planter le serveur.

### 3.3 Tool local (`viz.py`)

- Une fonction `make_dashboard` décorée `@tool` (LangChain).
- Elle produit une figure Plotly avec **au moins 2 graphiques** (`make_subplots` ou figures séparées).
- Elle enregistre le résultat en HTML dans `assets/` et retourne une `str` (chemin du fichier et résumé).

### 3.4 Agent (`agent.py`)

- Agent ReAct créé avec `create_react_agent`, connecté au serveur MCP via `MultiServerMCPClient`.
- Le serveur est lancé avec `sys.executable`, jamais avec `"python"` en dur.
- **Ton propre system prompt**, qui impose un ordre d'appel des tools et interdit d'inventer des chiffres.
- Une fonction `async def run_agent(question, thread_id) -> (reponse, etapes)` utilisée par le notebook et par l'application.
- Mémoire : `MemorySaver` ou équivalent, de sorte qu'une question de suivi réutilise la réponse précédente.
- Modèle : `llama3.2` via Ollama (`http://localhost:11434/v1`). Un autre modèle est accepté s'il est justifié.

### 3.5 Interface Streamlit (`app.py`)

- Lancée avec `python -m streamlit run app.py`.
- Chat avec historique de conversation.
- Au moins **2 graphiques** affichés.
- Message d'erreur clair si Ollama ou le serveur MCP est indisponible.
- Aucune clé d'API dans le code.

### 3.6 Notebook (`notebooks/01_exploration.ipynb`)

Le notebook modèle fourni contient 10 sections et une checklist. Les cellules marquées `TODO` sont à compléter.

| # | Section | Contenu attendu |
|---|---|---|
| 0 | En-tête | Titre, auteur(s), date, description en 3 lignes |
| 1 | Contexte | Utilisateur visé et 3 questions métier |
| 2 | Source | URL, date de récupération, licence si connue, limites |
| 3 | Chargement | Lecture du fichier, dimensions, types, valeurs manquantes, aperçu |
| 4 | Nettoyage | Chaque transformation, sa justification et son effet |
| 5 | Analyse exploratoire | Au moins 3 graphiques Plotly, une phrase d'interprétation par graphique |
| 6 | Tests des tools MCP | Appel direct de chaque tool, sortie affichée |
| 7 | Test de l'agent | 3 questions : simple, multi-tools, suivi |
| 8 | Dashboard | Appel de `make_dashboard`, affichage du résultat |
| 9 | Limites | Au moins un cas où l'agent répond de façon fausse ou douteuse, avec correction |
| 10 | Conclusion | Réponses aux 3 questions métier, à partir du notebook |

**Règles de qualité du notebook**

- Il s'exécute **de haut en bas** après « Redémarrer et tout exécuter », sans erreur.
- Les sorties sont conservées.
- Les chemins sont relatifs au dossier du notebook.
- Les cellules qui appellent Ollama supposent que `ollama serve` tourne.
- Chaque tool et chaque prompt est écrit par l'étudiant. Aucun code n'est copié tel quel depuis les séances.

### 3.7 README.md du dépôt

1. Titre et description en une phrase
2. Jeu de données : source, licence, taille, colonnes principales
3. Questions auxquelles le projet répond
4. Architecture (schéma de `assets/architecture.png`)
5. Installation : `pip install -r requirements.txt` puis `ollama pull llama3.2`
6. Lancement : `python -m streamlit run app.py`
7. Exemples de questions testées, avec leurs réponses
8. Limites connues

---

## 4. Contrôles avant la démo

- [ ] `Redémarrer et tout exécuter` sur le notebook passe sans erreur
- [ ] Chaque tool MCP retourne une chaîne de caractères
- [ ] `python -m streamlit run app.py` démarre sans erreur
- [ ] `requirements.txt` permet de reproduire l'environnement
- [ ] Le dépôt ne contient aucune clé d'API

---

## 5. Grille d'évaluation (100 points)

| Critère | Points |
|---|---|
| Choix et justification du jeu de données | 10 |
| Serveur MCP (tools, retours en chaîne, requêtes sûres) | 20 |
| Agent (system prompt, ordre des tools, mémoire) | 20 |
| Visualisations (pertinence, lisibilité) | 15 |
| Interface Streamlit et gestion d'erreur | 10 |
| Démo qui fonctionne en direct | 10 |
| Oral : explication du code et réponses aux questions | 15 |

---

## 6. Déroulement de l'évaluation

1. **Démo** : l'étudiant pose 3 questions préparées, dont une question de suivi.
2. **Revue de code** : l'enseignant ouvre un tool MCP et `app.py`. L'étudiant explique un tool de son choix.
3. **Questions** : 2 ou 3 questions parmi celles de la section 7.

---

## 7. Questions possibles à l'oral

- « Montre le tool que l'agent a appelé pour cette réponse. Pourquoi celui-là ? »
- « Pose une question hors de ton jeu de données. Que se passe-t-il ? »
- « Pourquoi ton tool retourne-t-il une chaîne et pas un DataFrame ? »
- « Relance la question de suivi sans la mémoire. Qu'est-ce qui casse ? »
- « Ton agent a-t-il déjà inventé un chiffre ? Comment l'empêches-tu ? »
- « Ton jeu passe de 1 000 à 1 000 000 de lignes : qu'est-ce qui change ? »
- « Montre-moi comment ton SQL se protège contre une entrée malveillante. »
