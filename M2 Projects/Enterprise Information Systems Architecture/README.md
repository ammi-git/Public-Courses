# Urbanisation des SI à l'ère de l'IA — M2 CPI

**Urbanisation des systèmes d'information** · Master 2 CPI · Université Paris 8<br>
**Enseignant :** Pr Mehdi Ammi — Laboratoire LIASD (EA 4383)

*Note sur l'usage de l'IA : la progression pédagogique et le scénario ont été définis par l'auteur. Claude (Anthropic) a été utilisé pour la rédaction des exercices et la mise en forme des supports.*

Cours pratique en 8 séances de 3 h. Après une introduction aux fondamentaux de l'urbanisation, les étudiants conçoivent, construisent et gouvernent un **guichet citoyen augmenté par l'IA** pour la Ville de Saint-Denis, et l'intègrent dans la cartographie de son SI.

> **Objectif du cours :** comprendre les principes de l'urbanisation des SI et savoir concevoir, intégrer et gouverner l'IA au sein du système d'information d'une organisation.

## Les trois niveaux d'articulation entre IA et SI

| Niveau | Ce que fait l'IA | Séances |
| --- | --- | --- |
| **L'IA s'appuie sur le SI** | Elle exploite les données et les documents (RAG) | S3, S4 |
| **L'IA agit dans le SI** | Des agents appellent les applications | S5, S6 |
| **L'IA transforme le SI** | Elle devient une couche à cartographier, gouverner et planifier | S1, S2, S7 |

## Les séances

| Séance | Dossier | Thème | Commande du jour |
| --- | --- | --- | --- |
| 1 | `seance1/` (support de cours) | IA et SI : quelle articulation ? Fondamentaux de l'urbanisation, fil rouge | La DGS : « Aidez-nous à y voir clair » |
| 2 | `seance2/S2_environnement_cas_usage.ipynb` | Prise en main de l'environnement, état des lieux du SI, priorisation des cas d'usage | La DGS : « Par où commencer ? » |
| 3 | `seance3/S3_rag_socle_documentaire.ipynb` | RAG (1) : audit du corpus, découpage, embeddings, base vectorielle | L'accueil : « 50 fois par jour les mêmes questions » |
| 4 | `seance4/S4_rag_assistant_evaluation.ipynb` | RAG (2) : assistant, évaluation, incident du tarif, local ou API | Une habitante : « Puis-je lui faire confiance ? » |
| 5 | `seance5/S5_agent_outils_si.ipynb` | Agents (1) : outils, agent, contrôles, MCP, traçabilité | Le DSI : « Traiter une demande, pas seulement répondre » |
| 6 | `seance6/S6_orchestration_guichet.ipynb` | Agents (2) : processus encadré, validation humaine, interopérabilité, guichet unique | La DGS : « De bout en bout, avec validation » |
| 7 | `seance7/S7_gouvernance_securite_trajectoire.ipynb` | Red teaming, garde-fous, conformité, coûts, cible et trajectoire | La DPO : « Je ne valide rien en l'état » |
| 8 | `seance8/` (consignes) | Soutenance devant le « conseil municipal » | L'élue au numérique |

Chaque notebook suit la même structure : 📩 la commande, des rappels de cours, des démonstrations à exécuter, des exercices guidés (✏️ À VOUS), un ⚡ rebondissement, des questions d'urbanisation 🏙️ et le 📦 livrable de fin de séance, à déposer sur **Moodle**. Le travail se fait en groupe de 4 ou 5.

Les exercices ne demandent **pas de programmer** : on modifie des consignes, des valeurs ou des listes, et on complète des lignes signalées par `...` ou `TODO`.

## Le fil rouge

La Ville de Saint-Denis veut ouvrir un guichet citoyen augmenté par l'IA. Son SI porte la trace de la **fusion avec Pierrefitte-sur-Seine** (applications en double) et partage des compétences avec **Plaine Commune** (voirie, propreté, éclairage). Les étudiants forment l'équipe projet et enrichissent la cartographie du SI à chaque séance.

> ⚠️ Le SI utilisé dans le cours est **fictif** : applications, données, documents et personnes ont été inventés pour le cours. Ils ne décrivent pas le SI réel de la commune.

## Installation

```bash
git clone <url-du-depot>
cd "M2 CPI Urbanisation des SI/seance2"   # chaque séance est un dossier autonome
python -m venv .venv && source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env                      # puis choisir l'option A ou B
python common/check_setup.py
jupyter lab
```

## Choisir son modèle : local ou API

Tout le code passe par `common/llm.py` : changer de modèle se fait **uniquement** dans `.env`.

- **Option A — local (gratuit)** : installer [Ollama](https://ollama.com), puis `ollama pull qwen2.5:7b` (16 Go de RAM conseillés) ou `qwen2.5:3b` pour une machine plus modeste.
- **Option B — API avec un compte personnel** : tout fournisseur compatible OpenAI (Mistral, OpenAI, Groq…). Activez un **plafond de dépense** sur votre compte.

Ce choix est aussi un sujet du cours : il est comparé en séance 4 et arbitré en séance 7 (qualité, coût, souveraineté).

## Règles

- Le fichier `.env` contient vos clés : il est dans `.gitignore`, **ne le commitez jamais**.
- Chaque agent a une limite d'étapes (`recursion_limit`).
- Gardez les dossiers des séances côte à côte : chaque notebook reprend la cartographie produite à la séance précédente.

## Structure

```
seance1/         support de cours et atelier de diagnostic (sans notebook)
seance2/ … seance7/
                 notebook de la séance + common/ (accès au LLM, SI simulé,
                 cartographie, RAG, outils des agents) + requirements.txt,
                 .env.example, .gitignore et README.md
seance8/         consignes et grille de la soutenance
```

Chaque dossier de séance est autonome. Les données du SI simulé (applications, familles, corpus documentaire) se trouvent dans `common/si_data/`.
