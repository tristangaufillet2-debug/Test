# Agent IA de devis – Couleurs Express

Agent IA (Claude) qui répond automatiquement aux demandes de devis de Couleurs Express, entreprise de peinture en bâtiment.

## Ce que fait l'agent

1. Lit la demande du client.
2. Demande les informations manquantes (surface, type de travaux, date, adresse), toutes en une fois.
3. Calcule le devis avec l'outil `calculer_devis` : un calcul en Python, exact, qui suit la grille tarifaire dans l'ordre officiel (prestations → remise de 10 % au-delà de 100 m² → +15 % si urgence sous 48 h → +50 € de déplacement → acompte de 30 %).
4. Présente le devis complet : détail, total, acompte, validité de 30 jours.

Le modèle ne calcule jamais les prix lui-même, donc il ne peut pas se tromper sur les montants.

## Installation

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Utilisation

Mode discussion dans le terminal :

```bash
python -m agent_devis.agent
```

Depuis votre code (formulaire web, email, WhatsApp, n8n/Make via un petit serveur…) :

```python
from agent_devis.agent import AgentDevis

agent = AgentDevis()          # une instance par client / conversation
print(agent.repondre("Bonjour, je voudrais repeindre 120 m² de façade au 12 rue des Lilas à Lyon, début décembre."))
```

## Structure

| Fichier | Rôle |
|---|---|
| `agent_devis/tarifs.md` | Grille tarifaire (à modifier pour un autre client) |
| `agent_devis/calcul.py` | Calcul exact des devis |
| `agent_devis/agent.py` | Agent Claude : prompt, outil, boucle de conversation |
| `tests/` | Tests (les 3 exemples officiels de la grille, entre autres) |

Lancer les tests : `pip install pytest && python -m pytest`

## Adapter à un autre client

Remplacez `tarifs.md`, puis modifiez les constantes en haut de `calcul.py` (prix au m², forfait, seuils, taux). Le reste de l'agent reste identique.
