# Données

- Placez votre dataset dans `data/` (par exemple `data/dataset.csv`) et indiquez son chemin dans `.env` (`DATASET_PATH`).
- Placez les documents du corpus dans `data/corpus/` (PDF ou `.txt`).
- Au-delà de 50 Mo, ne commitez pas le fichier : indiquez dans le README principal comment le télécharger.
- La base vectorielle (`chroma_db/`) est générée par `src/rag.py` et n'est pas commitée.
