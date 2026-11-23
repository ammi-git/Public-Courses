# 01 — Cahier des charges

[← Retour au README](../README.md)

## 1. Objectif

Concevoir un assistant qui répond à des questions en langage naturel sur un domaine de votre choix. Selon la demande, il :

- **cherche dans une documentation** et cite ses sources ;
- **analyse le dataset** pour répondre à une question chiffrée ;
- **produit automatiquement un dashboard**.

Tous les outils de l'assistant sont servis par **votre serveur MCP**.

Exemples de demandes, pour un projet sur les vélos en libre-service :

| Demande | Branche |
| --- | --- |
| « Que signifie la colonne `capacity` ? » | documentation |
| « Quelle est la station la plus utilisée le dimanche ? » | analyse |
| « Montre l'évolution des locations par heure et par arrondissement » | visualisation |

## 2. Composants à réaliser

Chaque composant est rattaché **à un seul cours** : c'est lui qui compte pour la note de ce cours (voir [05 — Évaluation](05_evaluation.md)).

| # | Composant | Ce qui est demandé | Cours |
| --- | --- | --- | --- |
| 1 | Résumé du dataset | échantillonnage ou statistiques descriptives adaptés à la fenêtre de contexte | DataViz |
| 2 | Recommandation de graphiques | sortie **JSON** forcée, avec un champ de **raisonnement pas à pas** (chain-of-thought) écrit avant les recommandations | DataViz |
| 3 | Génération du code Plotly | génération par le LLM, extraction, **exécution isolée** | DataViz |
| 4 | Boucle de réparation | l'erreur d'exécution est réinjectée au LLM, **3 essais au maximum** | DataViz |
| 5 | Dashboard | fichier HTML **multi-figures**, graphiques pertinents et lisibles | DataViz |
| 6 | Interface | application **Streamlit** : saisie, réponse, affichage du dashboard | DataViz |
| 7 | Serveur MCP | au moins 3 outils : résumer le dataset, calculer des statistiques ou filtrer, chercher dans la documentation | Agentic AI |
| 8 | RAG | indexation du corpus avec un **découpage justifié**, recherche sémantique, **sources citées** | Agentic AI |
| 9 | Graphe et routeur | `StateGraph` ; routeur qui classe la demande en **sortie Pydantic** | Agentic AI |
| 10 | Agent d'analyse | agent **ReAct** multi-outils encadré par un **system prompt** | Agentic AI |
| 11 | Validation humaine | `interrupt` avant d'exécuter le code généré ou d'exporter le dashboard | Agentic AI |
| 12 | Mémoire | conversation suivie par `thread_id` ; résumé de l'historique quand il devient long | Agentic AI |

Le détail de chaque composant est dans [03 — Architecture](03_architecture.md).

## 3. Contraintes

- **Le pipeline de visualisation doit pouvoir s'appeler seul**, hors du graphe (`pipeline(df, demande)`). Il est ainsi évaluable pour la note DataViz même si le graphe ne fonctionne pas complètement.
- **Tous les outils passent par le serveur MCP** : aucun outil n'est défini dans le code de l'agent.
- **Toute boucle est bornée** : 3 essais de réparation, `recursion_limit` sur les agents, `max_tokens` sur les appels.
- **Le code généré par le LLM n'est jamais exécuté sans isolation** : espace de noms restreint, sans accès à `os`, `sys`, `open`, ni au réseau.
- **Aucun chiffre sans calcul** : l'agent d'analyse obtient tout chiffre par un outil, jamais de mémoire.

## 4. Ce qui est libre

- le domaine et les données (voir [02 — Choix des données](02_choix_des_donnees.md)) ;
- le modèle (local ou API) ;
- la stratégie de découpage, le type de graphiques, le style du dashboard ;
- l'organisation interne du code, tant que les composants demandés existent.
