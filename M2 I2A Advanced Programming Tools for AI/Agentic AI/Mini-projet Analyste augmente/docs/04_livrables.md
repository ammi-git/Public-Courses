# 04 — Livrables

[← Retour au README](../README.md)

À déposer sur **Moodle** à la date indiquée dans le README :

1. le **lien de votre dépôt Git** (public, ou partagé avec l'enseignant) ;
2. le **rapport** en PDF ;
3. l'archive du dossier `scenarios/` si les traces sont volumineuses.

## 1. Le code

- Le dépôt suit la structure du squelette (`src/`, `data/`, `scenarios/`).
- `README.md` mis à jour : votre domaine, vos sources, **comment installer et lancer** le projet.
- `requirements.txt` à jour.
- **Aucune clé** dans le dépôt (`.env` est ignoré par Git).
- Si le dataset dépasse 50 Mo, ne le commitez pas : indiquez où le télécharger.

## 2. Les 5 scénarios de démonstration

Vous les définissez à partir de vos données. Pour chacun, déposez dans `scenarios/` la **trace complète** (messages, appels d'outils, réponses) et, pour la visualisation, le **dashboard HTML** produit. Modèle : [templates/scenarios.md](../templates/scenarios.md).

| # | Scénario imposé | Évalué pour |
| --- | --- | --- |
| S1 | une question sur la documentation, avec citation des sources | Agentic AI |
| S2 | une question chiffrée sur le dataset, résolue par l'agent d'analyse | Agentic AI |
| S3 | une demande de dashboard menée jusqu'à l'export | DataViz |
| S4 | un cas où la boucle de réparation corrige une erreur d'exécution | DataViz |
| S5 | un cas où l'humain refuse le résultat, fait une remarque, puis valide la version corrigée | Agentic AI |

## 3. Le rapport (3 pages)

Modèle : [templates/rapport.md](../templates/rapport.md).

**Partie DataViz (1,5 page)**
- le pipeline de visualisation : vos choix de résumé du dataset, de prompt, d'isolation ;
- **approche classique ou générée par LLM** : quand votre pipeline est-il préférable à un dashboard écrit à la main, et quand ne l'est-il pas ?
- une limite observée (hallucination, code faux, graphique trompeur…) et sa correction.

**Partie Agentic AI (1,5 page)**
- le schéma de votre graphe ;
- pour chaque branche : **workflow ou agent**, et pourquoi ;
- l'intérêt d'exposer les outils par **MCP** plutôt que de les définir dans l'agent ;
- votre **stratégie de découpage** du corpus et ce qui l'a motivée ;
- une limite observée et sa correction.
