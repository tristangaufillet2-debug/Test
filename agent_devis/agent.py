"""Agent IA de devis pour Couleurs Express (peinture en bâtiment).

Lancement :  python -m agent_devis.agent
"""

import json
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

import anthropic

from .calcul import PRIX_M2, Ligne, calculer_devis

MODEL = "claude-opus-5-5"
TARIFS = (Path(__file__).parent / "tarifs.md").read_text(encoding="utf-8")

SYSTEM_PROMPT = f"""Tu es l'assistant devis de Couleurs Express, une entreprise de peinture en bâtiment.
Tu réponds aux demandes de devis des clients, en français, de façon chaleureuse, claire et professionnelle.

Ta mission :
1. Comprendre la demande du client.
2. Vérifier que tu as les 4 informations nécessaires : surface en m², type de travaux
   (murs intérieurs, murs + plafond, façade), date souhaitée d'intervention, adresse du chantier.
   S'il en manque, demande-les poliment, toutes en une seule fois.
3. Quand tu as tout, appelle l'outil `calculer_devis`. Ne calcule JAMAIS les prix toi-même :
   utilise uniquement les montants renvoyés par l'outil.
   Mets `urgence` à true seulement si l'intervention doit avoir lieu dans les 48 heures
   (compare la date souhaitée à la date du jour indiquée plus bas ; en cas de doute, demande).
4. Présente le devis : détail des prestations, remise éventuelle, supplément urgence éventuel,
   forfait déplacement, total, acompte de 30 % à la signature, validité de 30 jours, adresse et date.
   Termine en proposant au client de valider le devis ou de poser ses questions.

Si une demande sort de la grille (papier peint, enduit, boiserie, etc.), explique que cette
prestation nécessite une visite et qu'un conseiller recontactera le client. N'invente aucun tarif.

Grille tarifaire officielle de l'entreprise :

{TARIFS}
"""

OUTIL_DEVIS = {
    "name": "calculer_devis",
    "description": (
        "Calcule le montant exact d'un devis Couleurs Express selon la grille tarifaire "
        "(remise volume, urgence, déplacement, acompte). À appeler dès que la surface, "
        "le type de travaux et la date sont connus."
    ),
    "strict": True,
    "input_schema": {
        "type": "object",
        "properties": {
            "lignes": {
                "type": "array",
                "description": "Une ligne par type de prestation demandée.",
                "items": {
                    "type": "object",
                    "properties": {
                        "prestation": {
                            "type": "string",
                            "enum": list(PRIX_M2),
                            "description": "murs_interieurs (25 €/m²), murs_et_plafond (30 €/m²) ou facade (40 €/m²).",
                        },
                        "surface_m2": {"type": "number", "description": "Surface en m²."},
                    },
                    "required": ["prestation", "surface_m2"],
                    "additionalProperties": False,
                },
            },
            "urgence": {
                "type": "boolean",
                "description": "true si l'intervention doit avoir lieu sous 48 heures.",
            },
        },
        "required": ["lignes", "urgence"],
        "additionalProperties": False,
    },
}


def executer_outil(entree: dict) -> tuple[str, bool]:
    """Exécute calculer_devis. Renvoie (contenu, est_une_erreur)."""
    try:
        lignes = [
            Ligne(l["prestation"], Decimal(str(l["surface_m2"])))
            for l in entree["lignes"]
        ]
        resultat = calculer_devis(lignes, bool(entree["urgence"]))
        return json.dumps(resultat, ensure_ascii=False), False
    except (KeyError, TypeError, ValueError, InvalidOperation) as e:
        return f"Erreur : {e}", True


class AgentDevis:
    """Conversation avec un client. Une instance par client / fil de discussion."""

    def __init__(self, client: anthropic.Anthropic | None = None, aujourd_hui: date | None = None):
        self.client = client or anthropic.Anthropic()
        self.messages: list[dict] = []
        jour = aujourd_hui or date.today()
        self.contexte_date = f"Date du jour : {jour.strftime('%d/%m/%Y')}."

    def repondre(self, message_client: str) -> str:
        self.messages.append({"role": "user", "content": message_client})

        while True:
            response = self.client.beta.messages.create(
                model=MODEL,
                max_tokens=16000,
                system=[
                    {"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}},
                    {"type": "text", "text": self.contexte_date},
                ],
                tools=[OUTIL_DEVIS],
                messages=self.messages,
                thinking={"type": "adaptive"},
                output_config={"effort": "medium"},
                betas=["server-side-fallback-2026-07-01"],
                fallbacks="default",
            )
            # On renvoie le contenu complet (y compris les blocs de réflexion) pour garder l'historique intact.
            self.messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason == "refusal":
                return ("Je ne peux pas traiter cette demande automatiquement. "
                        "Un conseiller Couleurs Express va vous recontacter.")

            if response.stop_reason != "tool_use":
                return "".join(b.text for b in response.content if b.type == "text")

            resultats = []
            for bloc in response.content:
                if bloc.type == "tool_use":
                    contenu, erreur = executer_outil(bloc.input)
                    resultats.append({
                        "type": "tool_result",
                        "tool_use_id": bloc.id,
                        "content": contenu,
                        "is_error": erreur,
                    })
            self.messages.append({"role": "user", "content": resultats})


def main() -> None:
    agent = AgentDevis()
    print("Assistant devis Couleurs Express (Ctrl+C pour quitter)\n")
    try:
        while True:
            message = input("Client : ").strip()
            if message:
                print(f"\nAgent : {agent.repondre(message)}\n")
    except (KeyboardInterrupt, EOFError):
        print("\nAu revoir !")


if __name__ == "__main__":
    main()
