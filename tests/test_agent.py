import json
from types import SimpleNamespace as NS

from agent_devis.agent import AgentDevis


class FakeClient:
    """Simule l'API : 1er appel -> demande l'outil, 2e appel -> réponse texte."""

    def __init__(self):
        self.appels = []
        self.beta = NS(messages=NS(create=self.create))

    def create(self, **kwargs):
        self.appels.append(kwargs)
        if len(self.appels) == 1:
            outil = NS(type="tool_use", id="t1", name="calculer_devis",
                       input={"lignes": [{"prestation": "facade", "surface_m2": 120}], "urgence": False})
            return NS(stop_reason="tool_use", content=[outil])
        return NS(stop_reason="end_turn", content=[NS(type="text", text="Votre devis : 4 370 €")])


def test_boucle_outil_puis_reponse():
    client = FakeClient()
    reponse = AgentDevis(client).repondre("120 m² de façade au 3 rue des Lilas, le 15 novembre")

    assert reponse == "Votre devis : 4 370 €"
    resultat = client.appels[1]["messages"][-2]["content"][0]
    assert resultat["type"] == "tool_result" and not resultat["is_error"]
    assert json.loads(resultat["content"])["total_ttc"] == "4370.00"
