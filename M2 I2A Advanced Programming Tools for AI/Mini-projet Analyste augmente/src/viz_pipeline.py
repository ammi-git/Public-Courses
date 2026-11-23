"""Pipeline de visualisation — À COMPLÉTER. Évalué pour la note Agentic DataViz.

Il doit pouvoir s'appeler SEUL, hors du graphe :
    figures, journal = pipeline(df, "Compare les prix par quartier")
Voir docs/03_architecture.md, section 7.
"""
import pandas as pd
from pydantic import BaseModel, Field


class Graphique(BaseModel):
    type: str = Field(description="bar, line, scatter, histogram, box, pie…")
    x: str
    y: str | None = None
    couleur: str | None = None
    titre: str
    justification: str


class Recommandation(BaseModel):
    raisonnement: str = Field(description="Raisonnement pas à pas AVANT de choisir les graphiques")
    graphiques: list[Graphique]


def resumer(df: pd.DataFrame, max_lignes: int = 10) -> str:
    """Résumé du dataset qui tient dans la fenêtre de contexte (jamais les données brutes complètes)."""
    raise NotImplementedError


def recommander(llm, resume: str, demande: str) -> Recommandation:
    """Recommandation en sortie structurée (voir src/sortie.py, fonction structurer)."""
    raise NotImplementedError


def generer_code(llm, resume: str, reco: Recommandation, erreur: str | None = None, code_precedent: str | None = None) -> str:
    """Demande au LLM le code Plotly ; en cas de réparation, lui renvoie le code précédent et l'erreur."""
    raise NotImplementedError


def extraire_code(texte: str) -> str:
    """Extrait le bloc ```python ... ``` de la réponse du LLM."""
    raise NotImplementedError


def executer_isole(code: str, df: pd.DataFrame):
    """Exécute le code dans un espace de noms restreint ; renvoie (figures, erreur). Voir docs/06_guide_technique.md."""
    raise NotImplementedError


def pipeline(df: pd.DataFrame, demande: str, llm=None, max_essais: int = 3):
    """Résumé → recommandation → code → exécution isolée → réparation (max_essais). Renvoie (figures, journal)."""
    raise NotImplementedError


def exporter_dashboard(figures: list, chemin: str = "dashboard.html", titre: str = "Dashboard") -> str:
    """Écrit toutes les figures dans un seul fichier HTML ; renvoie le chemin."""
    raise NotImplementedError
