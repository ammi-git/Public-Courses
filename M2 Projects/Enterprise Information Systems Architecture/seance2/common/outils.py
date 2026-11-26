"""Outils donnés aux agents (séances 5 à 7) : chaque outil appelle une API du SI simulé.

Ce module reprend les outils construits en séance 5. Le modèle ne voit jamais
le code : il ne voit que le nom, la description (docstring) et les paramètres.
"""
from langchain_core.tools import tool

from common import si


@tool
def consulter_famille(id_famille: str) -> dict:
    """Consulte le dossier d'une famille dans le portail famille.

    Args:
        id_famille: identifiant du dossier, par exemple "FAM001".

    Returns:
        Le dossier : responsable, quotient familial, justificatif de domicile, enfants.
    """
    return si.cantine_consulter_famille(id_famille)


@tool
def tarif_repas(quotient_familial: int | None) -> float:
    """Calcule le prix d'un repas de cantine (en euros) pour l'année 2026-2027.

    Args:
        quotient_familial: quotient familial de la famille, ou null s'il n'est pas calculé.
    """
    return si.cantine_tarif_repas(quotient_familial)


@tool
def inscrire_cantine(id_famille: str, prenom_enfant: str, jours: list[str]) -> dict:
    """Inscrit un enfant à la cantine.

    Args:
        id_famille: identifiant du dossier, par exemple "FAM001".
        prenom_enfant: prénom de l'enfant tel qu'il figure dans le dossier.
        jours: jours choisis parmi "lundi", "mardi", "jeudi", "vendredi".
    """
    return si.cantine_inscrire(id_famille, prenom_enfant, jours)


@tool
def consulter_stationnement(id_resident: str) -> dict:
    """Consulte la situation d'un résident (carte de stationnement).

    Args:
        id_resident: identifiant du résident, par exemple "RES001".
    """
    return si.stationnement_consulter(id_resident)


@tool
def demander_carte_resident(nom: str, adresse: str, immatriculation: str, duree: str = "annuelle") -> dict:
    """Enregistre une demande de carte de stationnement résident.

    Args:
        nom: nom et prénom du demandeur.
        adresse: adresse du domicile à Saint-Denis.
        immatriculation: plaque du véhicule, par exemple "AB-123-CD".
        duree: "mensuelle" (15 €) ou "annuelle" (120 €).
    """
    return si.stationnement_demander_carte(nom, adresse, immatriculation, duree)


@tool
def demander_acte_etat_civil(type_acte: str, nom: str, prenoms: str, date_evenement: str) -> dict:
    """Enregistre une demande d'acte d'état civil (gratuit, envoyé sous 5 jours ouvrés).

    Args:
        type_acte: "naissance", "mariage" ou "décès".
        nom: nom de famille de la personne concernée.
        prenoms: prénoms de la personne concernée.
        date_evenement: date de l'événement, au format AAAA-MM-JJ.
    """
    return si.etat_civil_demander_acte(type_acte, nom, prenoms, date_evenement)


OUTILS_VILLE = [consulter_famille, tarif_repas, inscrire_cantine, consulter_stationnement,
                demander_carte_resident, demander_acte_etat_civil]
