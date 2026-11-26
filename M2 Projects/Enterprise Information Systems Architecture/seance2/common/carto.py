"""Cartographie du SI de Saint-Denis, enrichie séance après séance.

    from common.carto import Cartographie
    carte = Cartographie.charger()                     # SI existant
    carte = Cartographie.reprendre("S3")               # ou : cartographie de la séance 3
    carte.ajouter_brique("Assistant RAG", couche="applicative", seance="S4")
    carte.afficher()
    carte.sauvegarder("livrables/cartographie_S4.json")
"""
import json
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

FICHIER_EXISTANT = Path(__file__).resolve().parent / "si_data" / "cartographie_existant.json"

COUCHES = {
    "metier": "Métier\n(processus)",
    "fonctionnelle": "Fonctionnelle\n(services)",
    "applicative": "Applicative\n(logiciels)",
    "donnees": "Données et\ntechnique",
}
STYLES = {  # type d'élément : (fond, bordure, style de bordure)
    "existant": ("#eceff3", "#9aa3b2", "-"),
    "doublon": ("#eceff3", "#d9822b", "--"),
    "partage": ("#e3f1ec", "#3d8f6f", "-"),
    "ia": ("#ece8fc", "#5b3fd1", "-"),
    "gouvernance": ("#fbede4", "#b4541f", "-"),
}
PAR_LIGNE = 5


class Cartographie:
    def __init__(self, donnees: dict):
        self.donnees = donnees

    # ------------------------------------------------------------ chargement
    @classmethod
    def charger(cls, chemin: str | Path | None = None) -> "Cartographie":
        """Charge une cartographie (par défaut : le SI existant fourni)."""
        chemin = Path(chemin) if chemin else FICHIER_EXISTANT
        return cls(json.loads(chemin.read_text(encoding="utf-8")))

    @classmethod
    def reprendre(cls, seance: str) -> "Cartographie":
        """Reprend la cartographie produite à une séance précédente, par exemple reprendre("S2").

        Cherche d'abord votre livrable (livrables/ de cette séance, puis du dossier de
        la séance concernée). S'il n'existe pas, charge le point de reprise fourni.
        """
        n = seance.upper().lstrip("S")
        candidats = [Path("livrables") / f"cartographie_S{n}.json",
                     Path("..") / f"seance{n}" / "livrables" / f"cartographie_S{n}.json"]
        for chemin in candidats:
            if chemin.exists():
                print(f"Reprise de votre cartographie : {chemin}")
                return cls.charger(chemin)
        reprise = FICHIER_EXISTANT.parent / "reprise" / f"cartographie_S{n}.json"
        print(f"Livrable S{n} introuvable : reprise du point de référence fourni ({reprise.name}).")
        return cls.charger(reprise)

    def sauvegarder(self, chemin: str | Path) -> None:
        chemin = Path(chemin)
        chemin.parent.mkdir(parents=True, exist_ok=True)
        chemin.write_text(json.dumps(self.donnees, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Cartographie enregistrée dans {chemin}")

    # ------------------------------------------------------------ modification
    def ajouter_brique(self, nom: str, couche: str, seance: str = "", type: str = "ia") -> None:
        """Ajoute une brique. couche : metier, fonctionnelle, applicative, donnees ou gouvernance."""
        if couche not in self.donnees["couches"]:
            raise ValueError(f"Couche inconnue : {couche}. Choix : {list(self.donnees['couches'])}")
        self.retirer(nom, silencieux=True)
        self.donnees["couches"][couche].append({"nom": nom, "type": type, "seance": seance})

    def retirer(self, nom: str, silencieux: bool = False) -> None:
        """Retire un élément (par exemple une application décommissionnée)."""
        for elements in self.donnees["couches"].values():
            for e in list(elements):
                if e["nom"] == nom:
                    elements.remove(e)
                    return
        if not silencieux:
            print(f"Aucun élément nommé « {nom} ».")

    def briques_ia(self) -> list[dict]:
        return [dict(e, couche=c) for c, el in self.donnees["couches"].items() for e in el if e["type"] == "ia"]

    # ------------------------------------------------------------ affichage
    def afficher(self, titre: str | None = None) -> None:
        couches = self.donnees["couches"]
        gouv = couches.get("gouvernance", [])
        lignes = {c: max(1, -(-len(couches.get(c, [])) // PAR_LIGNE)) for c in COUCHES}
        h_case, gap = 0.9, 0.35
        hauteur_totale = sum(lignes[c] * h_case + 0.4 for c in COUCHES) + gap * (len(COUCHES) - 1)
        largeur = 16 if gouv else 13.5
        fig, ax = plt.subplots(figsize=(largeur, hauteur_totale * 0.62 + 1.2))
        ax.set_xlim(0, largeur)
        ax.set_ylim(0, hauteur_totale)
        ax.axis("off")

        y = hauteur_totale
        largeur_case = (13.5 - 2.4 - 0.2 * (PAR_LIGNE + 1)) / PAR_LIGNE
        for c, libelle in COUCHES.items():
            h = lignes[c] * h_case + 0.4
            y -= h
            ax.add_patch(FancyBboxPatch((0, y), 13.5, h, boxstyle="round,pad=0,rounding_size=0.12",
                                        fc="white", ec="#c9cfd9", lw=1))
            ax.text(1.15, y + h / 2, libelle, ha="center", va="center", fontsize=10, fontweight="bold")
            for i, e in enumerate(couches.get(c, [])):
                ligne, col = divmod(i, PAR_LIGNE)
                x0 = 2.4 + 0.2 + col * (largeur_case + 0.2)
                y0 = y + h - 0.2 - (ligne + 1) * h_case + 0.12
                self._case(ax, x0, y0, largeur_case, h_case - 0.24, e)
            y -= gap

        if gouv:
            ax.add_patch(FancyBboxPatch((13.8, 0), 2.1, hauteur_totale, boxstyle="round,pad=0,rounding_size=0.12",
                                        fc=STYLES["gouvernance"][0], ec=STYLES["gouvernance"][1], lw=1.5))
            ax.text(14.85, hauteur_totale - 0.35, "Gouvernance IA", ha="center", va="top", fontsize=10,
                    fontweight="bold", color=STYLES["gouvernance"][1])
            for i, e in enumerate(gouv):
                txt = "\n".join(textwrap.wrap(e["nom"], 18))
                ax.text(14.85, hauteur_totale - 1.1 - i * 0.75, "• " + txt, ha="center", va="top", fontsize=8)

        ax.set_title(titre or self.donnees.get("titre", "Cartographie du SI"), fontsize=13, loc="left")
        legende = [("SI existant", "existant"), ("Doublon (fusion)", "doublon"),
                   ("Partagé Plaine Commune", "partage"), ("Brique IA", "ia")]
        for i, (txt, t) in enumerate(legende):
            fc, ec, ls = STYLES[t]
            ax.add_patch(FancyBboxPatch((2.4 + i * 2.8, -0.55), 0.35, 0.3, boxstyle="round,pad=0.02",
                                        fc=fc, ec=ec, ls=ls, lw=1.5, clip_on=False))
            ax.text(2.4 + i * 2.8 + 0.5, -0.4, txt, va="center", fontsize=8.5)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def _case(ax, x, y, w, h, e):
        fc, ec, ls = STYLES.get(e["type"], STYLES["existant"])
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                    fc=fc, ec=ec, ls=ls, lw=1.6 if e["type"] == "ia" else 1))
        texte = "\n".join(textwrap.wrap(e["nom"], 22)[:3])
        ax.text(x + w / 2, y + h / 2, texte, ha="center", va="center", fontsize=8,
                fontweight="bold" if e["type"] == "ia" else "normal",
                color="#3b259e" if e["type"] == "ia" else "#1b2230")
        if e.get("seance"):
            ax.text(x + w - 0.05, y + h - 0.05, e["seance"], ha="right", va="top", fontsize=7,
                    color="white", bbox=dict(boxstyle="round,pad=0.15", fc=ec, ec="none"))
