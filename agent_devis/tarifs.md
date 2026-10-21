# Couleurs Express - Grille tarifaire (cas fictif)

Entreprise de peinture en bâtiment. Document à réutiliser dans le prompt système de l'agent de devis.

## Tarifs

| Prestation | Prix |
|---|---|
| Peinture murs intérieurs | 25 € / m² |
| Peinture plafond (murs + plafond) | 30 € / m² |
| Façade extérieure | 40 € / m² |
| Forfait déplacement | 50 € (une seule fois par chantier) |

## Règles

- **Remise volume** : -10 % sur le total des prestations au-delà de 100 m².
- **Urgence** : +15 % si l'intervention doit avoir lieu sous 48 heures.
- **Validité du devis** : 30 jours.
- **Acompte** : 30 % à la signature.

## Ordre de calcul

1. Total des prestations (surface x prix au m²).
2. Application de la remise de 10 % si la surface dépasse 100 m².
3. Application du supplément urgence de 15 % si besoin.
4. Ajout du forfait déplacement de 50 € (non soumis à remise ni supplément).
5. Calcul de l'acompte de 30 % sur le total final.

## Exemples

**Exemple 1 : 60 m² de murs intérieurs, délai normal**
- Prestations : 60 x 25 = 1 500 €
- Déplacement : 50 €
- **Total : 1 550 €**, acompte 465 €

**Exemple 2 : 120 m² de façade, délai normal**
- Prestations : 120 x 40 = 4 800 €
- Remise 10 % : -480 € = 4 320 €
- Déplacement : 50 €
- **Total : 4 370 €**, acompte 1 311 €

**Exemple 3 : 40 m² de murs + plafond, urgence**
- Prestations : 40 x 30 = 1 200 €
- Urgence +15 % : +180 € = 1 380 €
- Déplacement : 50 €
- **Total : 1 430 €**, acompte 429 €

## Informations à demander si elles manquent

- Surface en m²
- Type de travaux (intérieur, plafond, façade)
- Date souhaitée d'intervention
- Adresse du chantier
