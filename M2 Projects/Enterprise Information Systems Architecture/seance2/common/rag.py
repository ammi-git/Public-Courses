"""Outils RAG du cours (séances 4 à 7).

Ce module range le code construit pas à pas en séance 3 :
charger le corpus, le découper, l'indexer, rechercher, puis répondre.
"""
import time
from pathlib import Path

import chromadb

from common.embeddings import chroma_embedding_function

DOSSIER_CORPUS = Path(__file__).resolve().parent / "si_data" / "corpus"

PROMPT_SYSTEME_DEFAUT = """Tu es l'assistant d'accueil de la Ville de Saint-Denis.
Tu réponds aux questions des habitants uniquement à partir des extraits fournis.
Si les extraits ne permettent pas de répondre, dis-le et oriente vers l'accueil de la mairie.
Réponds de façon courte et claire, dans la langue de la question."""


# ---------------------------------------------------------------- 1. Charger
def lire_document(chemin: Path) -> dict:
    """Lit un document Markdown et son en-tête (titre, service, date, statut)."""
    texte = chemin.read_text(encoding="utf-8")
    meta = {"source": chemin.name, "titre": chemin.stem, "service": "", "date": "", "statut": ""}
    if texte.startswith("---"):
        entete, texte = texte[3:].split("---", 1)
        for ligne in entete.strip().splitlines():
            if ":" in ligne:
                cle, valeur = ligne.split(":", 1)
                meta[cle.strip()] = valeur.strip()
    return {"texte": texte.strip(), **meta}


def charger_corpus(dossier: str | Path | None = None) -> list[dict]:
    """Charge tous les documents .md d'un dossier (par défaut : le corpus de la ville)."""
    dossier = Path(dossier) if dossier else DOSSIER_CORPUS
    return [lire_document(p) for p in sorted(dossier.glob("*.md"))]


# ---------------------------------------------------------------- 2. Découper
def decouper(documents: list[dict], taille: int = 600, chevauchement: int = 100) -> list[dict]:
    """Découpe chaque document en morceaux d'environ `taille` caractères.

    Les morceaux se chevauchent de `chevauchement` caractères pour ne pas couper
    une information en deux. Chaque morceau garde les métadonnées de son document.
    """
    morceaux = []
    for doc in documents:
        texte, debut, numero = doc["texte"], 0, 0
        while debut < len(texte):
            fin = min(debut + taille, len(texte))
            if fin < len(texte):  # couper de préférence à la fin d'une ligne
                coupure = texte.rfind("\n", debut + taille // 2, fin)
                fin = coupure if coupure != -1 else fin
            meta = {k: v for k, v in doc.items() if k != "texte"}
            morceaux.append({"id": f"{doc['source']}#{numero}", "texte": texte[debut:fin].strip(), **meta})
            numero += 1
            if fin >= len(texte):
                break
            debut = max(fin - chevauchement, debut + 1)
    return [m for m in morceaux if m["texte"]]


# ---------------------------------------------------------------- 3. Indexer
_client = None


def creer_index(morceaux: list[dict], nom: str = "corpus"):
    """Calcule les embeddings des morceaux et les range dans une base vectorielle (Chroma)."""
    global _client
    _client = _client or chromadb.EphemeralClient()
    try:
        _client.delete_collection(nom)
    except Exception:  # noqa: BLE001 — la collection n'existait pas
        pass
    index = _client.create_collection(nom, embedding_function=chroma_embedding_function(),
                                      metadata={"hnsw:space": "cosine"})
    index.add(ids=[m["id"] for m in morceaux],
              documents=[m["texte"] for m in morceaux],
              metadatas=[{k: v for k, v in m.items() if k not in ("id", "texte")} for m in morceaux])
    print(f"Index « {nom} » : {index.count()} morceaux indexés.")
    return index


def ajouter_documents(index, documents: list[dict], taille: int = 600, chevauchement: int = 100) -> None:
    """Ajoute de nouveaux documents à un index existant."""
    morceaux = decouper(documents, taille, chevauchement)
    index.add(ids=[m["id"] for m in morceaux], documents=[m["texte"] for m in morceaux],
              metadatas=[{k: v for k, v in m.items() if k not in ("id", "texte")} for m in morceaux])


# ---------------------------------------------------------------- 4. Rechercher
def rechercher(index, question: str, k: int = 4, filtre: dict | None = None) -> list[dict]:
    """Renvoie les k morceaux les plus proches de la question.

    filtre : condition sur les métadonnées, par exemple {"statut": "en vigueur"}.
    """
    r = index.query(query_texts=[question], n_results=k, where=filtre)
    return [{"texte": doc, "similarite": round(1 - dist, 3), **meta}
            for doc, meta, dist in zip(r["documents"][0], r["metadatas"][0], r["distances"][0])]


# ---------------------------------------------------------------- 5. Répondre
def repondre(index, question: str, llm=None, k: int = 4, prompt_systeme: str = PROMPT_SYSTEME_DEFAUT,
             filtre: dict | None = None) -> dict:
    """Recherche les extraits pertinents puis demande au modèle de répondre à partir d'eux."""
    if llm is None:
        from common.llm import get_llm
        llm = get_llm()
    debut = time.time()
    extraits = rechercher(index, question, k=k, filtre=filtre)
    contexte = "\n\n".join(f"[{i + 1}] ({e['titre']}, {e['date']})\n{e['texte']}" for i, e in enumerate(extraits))
    messages = [("system", prompt_systeme),
                ("user", f"Extraits :\n{contexte}\n\nQuestion : {question}")]
    reponse = llm.invoke(messages)
    return {"question": question, "reponse": reponse.content,
            "sources": [f"{e['source']} ({e['statut']})" for e in extraits],
            "duree_s": round(time.time() - debut, 1),
            "tokens": (reponse.usage_metadata or {}).get("total_tokens")}


def afficher(resultat: dict) -> None:
    """Affiche joliment le résultat de repondre()."""
    print("❓", resultat["question"])
    print("💬", resultat["reponse"])
    print("📄 Sources :", ", ".join(dict.fromkeys(resultat["sources"])))
    print(f"⏱  {resultat['duree_s']} s", f"— {resultat['tokens']} tokens" if resultat.get("tokens") else "")
    print()
