from decimal import Decimal

from agent_devis.agent import executer_outil
from agent_devis.calcul import Ligne, calculer_devis


def devis(prestation, surface, urgence=False):
    return calculer_devis([Ligne(prestation, Decimal(surface))], urgence)


def test_exemple_1_murs_interieurs_delai_normal():
    d = devis("murs_interieurs", "60")
    assert d["total_prestations"] == "1500.00"
    assert d["total_ttc"] == "1550.00"
    assert d["acompte_30_pourcent"] == "465.00"


def test_exemple_2_facade_avec_remise():
    d = devis("facade", "120")
    assert d["remise_volume"] == "480.00"
    assert d["total_ttc"] == "4370.00"
    assert d["acompte_30_pourcent"] == "1311.00"


def test_exemple_3_murs_plafond_urgence():
    d = devis("murs_et_plafond", "40", urgence=True)
    assert d["supplement_urgence"] == "180.00"
    assert d["total_ttc"] == "1430.00"
    assert d["acompte_30_pourcent"] == "429.00"


def test_pas_de_remise_a_100_m2_pile():
    assert devis("murs_interieurs", "100")["remise_volume"] == "0.00"


def test_remise_puis_urgence_et_deplacement_non_majore():
    # 150 x 25 = 3750 ; -10 % = 3375 ; +15 % = 3881.25 ; +50 = 3931.25
    d = devis("murs_interieurs", "150", urgence=True)
    assert d["total_ttc"] == "3931.25"


def test_plusieurs_prestations_surface_cumulee_pour_la_remise():
    d = calculer_devis(
        [Ligne("murs_interieurs", Decimal("60")), Ligne("facade", Decimal("50"))],
        urgence=False,
    )
    # (1500 + 2000) - 350 + 50
    assert d["total_ttc"] == "3200.00"


def test_outil_renvoie_une_erreur_sur_prestation_inconnue():
    contenu, erreur = executer_outil({"lignes": [{"prestation": "papier_peint", "surface_m2": 10}], "urgence": False})
    assert erreur and "inconnue" in contenu
