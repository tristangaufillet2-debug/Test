"""Moteur de calcul des devis Couleurs Express.

Le calcul est fait en Python (et non par le modèle) pour que les montants
soient toujours exacts et conformes à la grille tarifaire.
"""

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

PRIX_M2 = {
    "murs_interieurs": Decimal("25"),
    "murs_et_plafond": Decimal("30"),
    "facade": Decimal("40"),
}
LIBELLES = {
    "murs_interieurs": "Peinture murs intérieurs",
    "murs_et_plafond": "Peinture murs + plafond",
    "facade": "Façade extérieure",
}
FORFAIT_DEPLACEMENT = Decimal("50")
SEUIL_REMISE_M2 = Decimal("100")
TAUX_REMISE = Decimal("0.10")
TAUX_URGENCE = Decimal("0.15")
TAUX_ACOMPTE = Decimal("0.30")
VALIDITE_JOURS = 30


def _euros(montant: Decimal) -> Decimal:
    return montant.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


@dataclass
class Ligne:
    prestation: str
    surface_m2: Decimal


def calculer_devis(lignes: list[Ligne], urgence: bool) -> dict:
    """Applique l'ordre de calcul officiel et renvoie le détail du devis."""
    if not lignes:
        raise ValueError("Le devis doit contenir au moins une prestation.")

    detail = []
    total_prestations = Decimal("0")
    surface_totale = Decimal("0")
    for ligne in lignes:
        if ligne.prestation not in PRIX_M2:
            raise ValueError(f"Prestation inconnue : {ligne.prestation}")
        if ligne.surface_m2 <= 0:
            raise ValueError("La surface doit être strictement positive.")
        montant = _euros(ligne.surface_m2 * PRIX_M2[ligne.prestation])
        detail.append({
            "prestation": LIBELLES[ligne.prestation],
            "surface_m2": str(ligne.surface_m2),
            "prix_m2": str(PRIX_M2[ligne.prestation]),
            "montant": str(montant),
        })
        total_prestations += montant
        surface_totale += ligne.surface_m2

    # 1. Total des prestations, 2. remise volume au-delà de 100 m²
    remise = _euros(total_prestations * TAUX_REMISE) if surface_totale > SEUIL_REMISE_M2 else _euros(Decimal("0"))
    apres_remise = total_prestations - remise

    # 3. Supplément urgence (intervention sous 48 h)
    supplement = _euros(apres_remise * TAUX_URGENCE) if urgence else _euros(Decimal("0"))
    apres_urgence = apres_remise + supplement

    # 4. Forfait déplacement, non soumis à remise ni supplément
    total = apres_urgence + FORFAIT_DEPLACEMENT

    # 5. Acompte sur le total final
    acompte = _euros(total * TAUX_ACOMPTE)

    return {
        "lignes": detail,
        "surface_totale_m2": str(surface_totale),
        "total_prestations": str(total_prestations),
        "remise_volume": str(remise),
        "supplement_urgence": str(supplement),
        "forfait_deplacement": str(FORFAIT_DEPLACEMENT),
        "total_ttc": str(total),
        "acompte_30_pourcent": str(acompte),
        "solde_restant": str(total - acompte),
        "validite_jours": VALIDITE_JOURS,
    }
