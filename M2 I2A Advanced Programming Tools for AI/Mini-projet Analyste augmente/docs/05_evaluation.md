# 05 — Évaluation

[← Retour au README](../README.md)

Le projet donne **deux notes indépendantes sur 20**. Chaque composant compte pour un seul cours.

> Le pipeline de visualisation peut être démontré **seul** (appelé hors du graphe) : un graphe incomplet ne pénalise pas la note DataViz.

## Note Agentic DataViz (sur 20)

| Critère | Points | Attendu pour la totalité des points |
| --- | --- | --- |
| Données et résumé du dataset | 3 | sources conformes aux exigences ; résumé adapté à la fenêtre de contexte (schéma, statistiques, échantillon), sans envoyer les données brutes |
| Recommandation JSON avec raisonnement | 3 | sortie JSON validée ; raisonnement écrit avant la recommandation ; recommandation réellement exploitée par la suite du pipeline |
| Génération, extraction, exécution isolée | 4 | code Plotly généré à partir du résumé ; extraction fiable ; exécution dans un espace de noms restreint ; code dangereux refusé |
| Boucle de réparation | 3 | erreur réinjectée au LLM ; 3 essais au maximum ; journal des essais ; scénario S4 démontré |
| Dashboard | 3 | plusieurs figures dans un seul HTML ; graphiques adaptés aux données et à la question ; titres, axes et unités lisibles |
| Interface Streamlit | 2 | saisie, affichage de la réponse et du dashboard ; utilisable sans toucher au code |
| Rapport, partie DataViz | 2 | choix argumentés ; comparaison approche classique / générée par LLM ; une limite et sa correction |

## Note Agentic AI (sur 20)

| Critère | Points | Attendu pour la totalité des points |
| --- | --- | --- |
| Serveur MCP et conception des outils | 4 | au moins 3 outils fonctionnels ; docstrings précises ; arguments bornés ; erreurs renvoyées comme messages lisibles ; aucun outil défini hors du serveur |
| RAG | 4 | découpage justifié ; recherche pertinente ; sources citées (fichier, page) ; réponse honnête quand rien n'est trouvé ; scénario S1 |
| Graphe et routeur | 4 | `StateGraph` correct (état, nœuds, arêtes conditionnelles) ; routeur en sortie Pydantic avec raisonnement ; bon routage des scénarios |
| Agent d'analyse | 3 | agent ReAct multi-outils ; system prompt qui interdit les chiffres non calculés ; `recursion_limit` ; scénario S2 |
| Validation humaine | 2 | `interrupt` avant exécution ou export ; reprise avec `Command` ; scénario S5 |
| Mémoire | 2 | conversation par `thread_id` ; résumé de l'historique au-delà de N messages |
| Rapport, partie Agentic AI | 1 | schéma du graphe ; choix workflow / agent justifiés ; intérêt de MCP ; limite et correction |

## Barème indicatif par critère

| Niveau | Part des points |
| --- | --- |
| Absent ou ne fonctionne pas | 0 % |
| Présent mais incomplet, ou fonctionne partiellement | 50 % |
| Conforme à l'attendu | 100 % |

## Démonstration

Les points sont **confirmés lors de la démonstration** : l'enseignant pose ses propres questions à l'assistant, puis interroge l'étudiant sur son code et ses choix. Un critère dont le fonctionnement ou la compréhension n'est pas démontré peut être ramené à 50 % ou à 0 % de ses points. Exemples de questions : [08 — Démonstration et questions](08_demonstration.md).

## Notions évaluées

| Cours | Notions |
| --- | --- |
| **Agentic DataViz** | chain-of-thought ; sortie JSON forcée ; résumé et échantillonnage du dataset ; pipeline données → visualisation ; génération de code Plotly ; exécution isolée ; boucle de réparation ; dashboard multi-figures ; Streamlit ; approche classique ou générée par LLM |
| **Agentic AI** | sortie structurée (Pydantic) ; boucle ReAct ; conception d'outils ; agent multi-outils ; system prompt ; mémoire et contexte long ; embeddings ; découpage ; RAG agentique ; `StateGraph` ; routeur ; patterns ; workflow ou agent ; validation humaine ; MCP (serveur, client, `stdio`) |
