"""SI simulé de la Ville de Saint-Denis (données et applications fictives).

Ce module joue le rôle des applications métier de la ville. Chaque fonction
correspond à une « API » d'une application du SI. Toutes les actions sont
enregistrées dans un journal, consultable avec journal().

Les données sont chargées en mémoire : reinitialiser() remet le SI dans son
état de départ.
"""
import copy
import json
from datetime import datetime
from pathlib import Path

import pandas as pd

DOSSIER_DONNEES = Path(__file__).resolve().parent / "si_data"

_familles: dict = {}
_residents: dict = {}
_demandes: list = []
_interventions: list = []
_journal: list = []


def reinitialiser() -> None:
    """Remet le SI simulé dans son état de départ et vide le journal."""
    global _familles, _residents, _demandes, _interventions, _journal
    familles = json.loads((DOSSIER_DONNEES / "familles.json").read_text(encoding="utf-8"))
    residents = json.loads((DOSSIER_DONNEES / "stationnement.json").read_text(encoding="utf-8"))
    _familles = {f["id"]: f for f in familles}
    _residents = {r["id"]: r for r in residents}
    _demandes, _interventions, _journal = [], [], []


def _tracer(application: str, action: str, parametres: dict, resultat) -> None:
    _journal.append({
        "horodatage": datetime.now().strftime("%H:%M:%S"),
        "application": application,
        "action": action,
        "parametres": json.dumps(parametres, ensure_ascii=False),
        "resultat": str(resultat)[:120],
    })


def journal() -> pd.DataFrame:
    """Renvoie le journal de toutes les actions effectuées sur le SI."""
    return pd.DataFrame(_journal, columns=["horodatage", "application", "action", "parametres", "resultat"])


# ---------------------------------------------------------------- Inventaire
def inventaire_applications() -> pd.DataFrame:
    """Renvoie l'inventaire des applications du SI (tableau pandas)."""
    return pd.read_csv(DOSSIER_DONNEES / "applications.csv")


# ---------------------------------------------------------------- Portail famille (cantine)
TARIFS_CANTINE_2026 = [(400, 0.50), (700, 1.20), (1000, 2.10), (1400, 3.20), (float("inf"), 4.30)]
TARIF_MAXIMUM = 5.10


def cantine_tarif_repas(quotient_familial: int | None) -> float:
    """Prix d'un repas (en euros) selon le quotient familial, grille 2026-2027."""
    if quotient_familial is None:
        return TARIF_MAXIMUM
    for plafond, prix in TARIFS_CANTINE_2026:
        if quotient_familial <= plafond:
            return prix
    return TARIF_MAXIMUM


def cantine_consulter_famille(id_famille: str) -> dict:
    """Renvoie le dossier d'une famille (portail famille)."""
    famille = _familles.get(id_famille)
    resultat = copy.deepcopy(famille) if famille else {"erreur": f"Famille {id_famille} inconnue."}
    _tracer("Portail famille", "consulter_famille", {"id_famille": id_famille}, resultat)
    return resultat


def cantine_lister_familles() -> list[dict]:
    """Renvoie la liste de toutes les familles (réservé aux agents habilités)."""
    resultat = [copy.deepcopy(f) for f in _familles.values()]
    _tracer("Portail famille", "lister_familles", {}, f"{len(resultat)} familles")
    return resultat


def cantine_inscrire(id_famille: str, prenom_enfant: str, jours: list[str]) -> dict:
    """Inscrit un enfant à la cantine pour les jours indiqués.

    Attention : comme beaucoup d'applications anciennes, cette API ne vérifie
    pas que le dossier de la famille est complet.
    """
    famille = _familles.get(id_famille)
    if not famille:
        resultat = {"erreur": f"Famille {id_famille} inconnue."}
    else:
        enfant = next((e for e in famille["enfants"] if e["prenom"].lower() == prenom_enfant.lower()), None)
        jours_valides = [j.lower() for j in jours if j.lower() in {"lundi", "mardi", "jeudi", "vendredi"}]
        if not enfant:
            resultat = {"erreur": f"Aucun enfant prénommé {prenom_enfant} dans le dossier {id_famille}."}
        elif not jours_valides:
            resultat = {"erreur": "Jours invalides : la cantine fonctionne lundi, mardi, jeudi et vendredi."}
        else:
            enfant["cantine"], enfant["jours"] = True, jours_valides
            prix = cantine_tarif_repas(famille["quotient_familial"])
            resultat = {"statut": "inscription enregistrée", "enfant": enfant["prenom"],
                        "jours": jours_valides, "prix_repas": prix}
    _tracer("Portail famille", "inscrire", {"id_famille": id_famille, "prenom_enfant": prenom_enfant,
                                             "jours": jours}, resultat)
    return resultat


# ---------------------------------------------------------------- Stationnement
def stationnement_consulter(id_resident: str) -> dict:
    """Renvoie la situation d'un résident (carte de stationnement)."""
    resident = _residents.get(id_resident)
    resultat = copy.deepcopy(resident) if resident else {"erreur": f"Résident {id_resident} inconnu."}
    _tracer("Gestion stationnement", "consulter", {"id_resident": id_resident}, resultat)
    return resultat


def stationnement_demander_carte(nom: str, adresse: str, immatriculation: str, duree: str = "annuelle") -> dict:
    """Enregistre une demande de carte résident (duree : 'mensuelle' ou 'annuelle')."""
    prix = {"mensuelle": 15, "annuelle": 120}.get(duree)
    if prix is None:
        resultat = {"erreur": "Durée invalide : 'mensuelle' ou 'annuelle'."}
    else:
        numero = f"STA-{len(_demandes) + 1:04d}"
        _demandes.append({"numero": numero, "type": "carte résident", "nom": nom, "adresse": adresse,
                          "immatriculation": immatriculation, "duree": duree})
        resultat = {"numero": numero, "statut": "demande enregistrée", "prix": prix,
                    "pieces_a_fournir": ["carte grise", "justificatif de domicile"]}
    _tracer("Gestion stationnement", "demander_carte", {"nom": nom, "adresse": adresse,
                                                         "immatriculation": immatriculation, "duree": duree}, resultat)
    return resultat


# ---------------------------------------------------------------- État civil
def etat_civil_demander_acte(type_acte: str, nom: str, prenoms: str, date_evenement: str) -> dict:
    """Enregistre une demande d'acte (type_acte : 'naissance', 'mariage' ou 'décès')."""
    if type_acte not in {"naissance", "mariage", "décès"}:
        resultat = {"erreur": "Type d'acte invalide : 'naissance', 'mariage' ou 'décès'."}
    else:
        numero = f"EC-{len(_demandes) + 1:04d}"
        _demandes.append({"numero": numero, "type": f"acte de {type_acte}", "nom": nom,
                          "prenoms": prenoms, "date": date_evenement})
        resultat = {"numero": numero, "statut": "demande enregistrée", "delai": "5 jours ouvrés"}
    _tracer("État civil", "demander_acte", {"type_acte": type_acte, "nom": nom, "prenoms": prenoms,
                                            "date_evenement": date_evenement}, resultat)
    return resultat


# ---------------------------------------------------------------- Plaine Commune (autre SI)
def plaine_commune_creer_intervention(payload: dict) -> dict:
    """API du SI de Plaine Commune (voirie, propreté, éclairage).

    Ce SI n'utilise pas les mêmes formats que la ville. Il attend un dictionnaire :
        {"localisation": {"adresse": str, "commune": str},
         "nature": "voirie" | "proprete" | "eclairage",
         "priorite": 1 | 2 | 3,            # 1 = danger
         "description": str}
    """
    erreurs = []
    loc = payload.get("localisation") if isinstance(payload, dict) else None
    if not isinstance(loc, dict) or not loc.get("adresse") or not loc.get("commune"):
        erreurs.append("localisation.adresse et localisation.commune sont obligatoires")
    if payload.get("nature") not in {"voirie", "proprete", "eclairage"}:
        erreurs.append("nature doit valoir 'voirie', 'proprete' ou 'eclairage'")
    if payload.get("priorite") not in {1, 2, 3}:
        erreurs.append("priorite doit valoir 1, 2 ou 3")
    if erreurs:
        resultat = {"code": 422, "erreurs": erreurs}
    else:
        ticket = f"PC-{2026}-{len(_interventions) + 1:05d}"
        _interventions.append({"ticket": ticket, **payload})
        delai = "48 heures" if payload["priorite"] == 1 else "15 jours"
        resultat = {"code": 201, "ticket": ticket, "statut": "RECU", "delai_indicatif": delai}
    _tracer("Plaine Commune", "creer_intervention", payload if isinstance(payload, dict) else {}, resultat)
    return resultat


reinitialiser()
