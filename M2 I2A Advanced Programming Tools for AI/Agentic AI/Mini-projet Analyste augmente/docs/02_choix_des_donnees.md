# 02 — Choix des données

[← Retour au README](../README.md)

Vous choisissez un **domaine** (transport, santé publique, emploi, climat, sport, culture…) et réunissez **deux sources liées à ce domaine**.

## Exigences minimales

| Source | Exigences | Rôle dans le projet |
| --- | --- | --- |
| **Dataset tabulaire** (CSV ou Parquet) | au moins **1 000 lignes** ; au moins **3 colonnes numériques** et **2 catégorielles** ; licence ouverte | analyse et visualisation |
| **Corpus documentaire** (PDF ou texte) | au moins **20 pages** : dictionnaire de données, rapport, articles, documentation officielle | recherche documentaire (RAG) |

Les deux sources doivent **se répondre** : la documentation aide à comprendre ou à interpréter le dataset.

## Où chercher

- [data.gouv.fr](https://www.data.gouv.fr) — datasets publics français, souvent accompagnés d'une documentation ;
- [INSEE](https://www.insee.fr) — statistiques et notes méthodologiques ;
- [Kaggle](https://www.kaggle.com/datasets) — vérifier la licence et la présence d'une documentation ;
- [Inside Airbnb](http://insideairbnb.com) — annonces par ville, avec dictionnaire de données ;
- sites des agences publiques (transport, santé, environnement) pour les rapports.

## Exemples de couples dataset / corpus

| Domaine | Dataset | Corpus |
| --- | --- | --- |
| Mobilité | historique des locations de vélos en libre-service | rapports annuels de l'opérateur, dictionnaire de données |
| Logement | annonces Inside Airbnb d'une ville | dictionnaire Inside Airbnb, études sur le logement touristique |
| Emploi | offres d'emploi (`job_postings.csv`) | référentiels de métiers, études de l'APEC |
| Climat | relevés météorologiques historiques | rapports de synthèse du GIEC, notes de Météo-France |

## Fiche de choix — à faire valider avant de commencer

Recopiez [templates/fiche_choix_donnees.md](../templates/fiche_choix_donnees.md), remplissez-la et déposez-la pour validation. Elle contient :

1. le domaine ;
2. le dataset : lien, nombre de lignes, colonnes numériques et catégorielles, licence ;
3. le corpus : liens, nombre de pages ;
4. **trois exemples de questions** : une pour la documentation, une pour l'analyse, une pour la visualisation.

**Motifs de refus fréquents :** dataset trop petit ou sans colonnes catégorielles ; corpus sans lien avec le dataset ; questions qui ne mobilisent pas les deux sources.
