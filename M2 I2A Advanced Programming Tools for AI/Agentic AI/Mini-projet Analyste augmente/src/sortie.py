"""Sortie structurée robuste (fourni).

Les petits modèles locaux (ex. llama3.2:3b) respectent mal le format demandé : JSON emballé
dans un champ ({"object": "{...}"}), schéma recopié au lieu des valeurs, texte libre...
structurer() essaie d'abord le tool calling, puis redemande une réponse JSON simple,
et valide toujours le résultat avec Pydantic.
"""
import json
import re

from pydantic import BaseModel


def _forme(modele: type[BaseModel]) -> str:
    """Exemple de JSON attendu, construit à partir des champs du modèle."""
    champs = []
    for nom, champ in modele.model_fields.items():
        aide = champ.description or getattr(champ.annotation, "__name__", "valeur")
        champs.append(f'"{nom}": <{aide}>')
    return "{" + ", ".join(champs) + "}"


def _deballer(args: dict, texte: str) -> dict:
    """Récupère le dictionnaire de valeurs, quelle que soit la façon dont le modèle l'a emballé."""
    if len(args) == 1:                                   # tout le JSON dans un seul champ
        (v,) = args.values()
        if isinstance(v, dict):
            args = v
        elif isinstance(v, str) and v.strip().startswith("{"):
            args = json.loads(v)
    if not args:                                         # réponse en texte contenant du JSON
        m = re.search(r"\{.*\}", texte or "", re.S)
        args = json.loads(m.group(0)) if m else {}
    # un champ qui contient le schéma ({"type": ..., "description": ...}) n'est pas une valeur
    return {k: v for k, v in args.items() if not (isinstance(v, dict) and "type" in v and "description" in v)}


def structurer(llm, modele: type[BaseModel], consigne: str, essais: int = 3) -> BaseModel:
    """Renvoie une instance valide de `modele`, ou lève une erreur claire après `essais` tentatives."""
    derniere_erreur = None
    for i in range(essais):
        try:
            if i == 0:
                r = llm.with_structured_output(modele, method="function_calling", include_raw=True).invoke(consigne)
                if r["parsed"] is not None:
                    return r["parsed"]
                brut = r["raw"]
                args, texte = (brut.tool_calls[0]["args"] if brut.tool_calls else {}), brut.content
            else:
                texte = llm.invoke(f"{consigne}\n\nRéponds UNIQUEMENT par un objet JSON de cette forme, "
                                   f"avec de vraies valeurs : {_forme(modele)}").content
                args = {}
            return modele.model_validate(_deballer(args, texte))
        except Exception as e:  # noqa: BLE001
            derniere_erreur = e
    raise ValueError(f"Pas de {modele.__name__} valide après {essais} essais "
                     f"(modèle trop petit ?) : {derniere_erreur}")
