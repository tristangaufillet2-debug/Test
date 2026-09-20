# Reflex Services — Site web

Site vitrine **statique** (HTML / CSS / JS, sans dépendance ni build) pour **Reflex Services**,
entreprise de nettoyage professionnelle en Île-de-France : canapés, intérieurs de voiture,
dégâts des eaux, tapis & matelas.

Conçu selon le PRD fourni : **mobile-first**, **orienté conversion** (appel téléphonique en
priorité), **SEO local** et **accessibilité** (WCAG).

## 🚀 Mise en ligne

C'est un site 100 % statique : il suffit de servir le dossier tel quel.

```bash
# Prévisualisation locale
python3 -m http.server 8000
# puis ouvrir http://localhost:8000
```

Hébergement compatible : Netlify, Vercel, GitHub Pages, Cloudflare Pages, o2switch, OVH, etc.
(glisser-déposer du dossier, aucun compilateur requis).

## 📁 Structure

```
index.html                         Accueil (hero, services, preuves, avis, CTA)
services.html                      Hub des services
services/
  ├─ nettoyage-canape.html
  ├─ nettoyage-voiture-interieur.html
  ├─ degat-des-eaux.html           (page urgence)
  └─ nettoyage-tapis-matelas.html
zones-intervention.html            SEO local (Val-d'Oise 95 + IDF)
avis.html                          Avis clients (5★ / 48 avis)
about.html                         À propos
faq.html                           FAQ (+ schema FAQPage)
contact.html                       Formulaire + carte + coordonnées
mentions-legales.html              Légal (modèle à compléter)
politique-confidentialite.html     RGPD (modèle à compléter)
robots.txt · sitemap.xml           SEO
assets/
  ├─ css/style.css                 Design system complet
  ├─ js/main.js                    Menu, FAQ, slider avant/après, reveal, form
  └─ img/                          (déposer ici les vraies photos)
```

## ✅ À personnaliser avant la mise en ligne

Les valeurs ci-dessous sont des **espaces réservés** — remplacez-les partout :

| Élément | Valeur actuelle (placeholder) | Où |
|---|---|---|
| Téléphone | `+33612345678` / `06 12 34 56 78` | tous les liens `tel:` + affichage |
| E-mail | `contact@reflex-services.fr` | liens `mailto:` |
| Domaine | `https://www.reflex-services.fr` | balises `canonical`, `og:url`, `sitemap.xml`, `robots.txt` |
| Adresse | Saint-Ouen-l'Aumône (95310) | pied de page, schema, contact |
| Mentions légales | champs entre `[crochets]` | `mentions-legales.html` |

> 💡 Astuce : un chercher-remplacer global sur `+33612345678` et `contact@reflex-services.fr`
> suffit à brancher les vraies coordonnées.

### Photos avant / après (essentiel)
Les zones grisées « Photo réelle client » sont des placeholders. Déposez vos vraies photos
dans `assets/img/` et remplacez les blocs `.placeholder` par des `<img>` (les comparateurs
avant/après fonctionnent avec deux images superposées). **Le PRD insiste : pas de photos
de stock, uniquement des transformations réelles.**

### Carte Google Maps
La carte utilise OpenStreetMap (sans clé API). Pour le SEO local, remplacez l'`<iframe>`
dans `contact.html` et `zones-intervention.html` par l'embed de votre **fiche Google Business**.

### Formulaire de contact
Le formulaire est fonctionnel côté client (validation + message de succès) mais **n'envoie rien
pour l'instant**. Branchez-le à un service (Formspree, Netlify Forms, un endpoint CRM…) en
modifiant le `<form id="contact-form">` et le handler dans `assets/js/main.js`.

### Analytics & tracking (GA4)
Le code est prêt : les clics `tel:` et l'envoi du formulaire déclenchent des événements
`gtag` (`click_to_call`, `generate_lead`). Ajoutez votre snippet GA4 dans le `<head>` des pages
pour activer le suivi des conversions.

## 🎨 Design

- Palette : bleu profond (confiance), blanc (propreté), gris clair (structure),
  orange (CTA / urgence), vert (validation / confiance).
- Typographies : **Poppins** (titres) + **Inter** (texte) via Google Fonts.
- Composants : hero CTA, cartes services, **comparateur avant/après** interactif,
  carrousel d'avis, **accordéon FAQ**, **bouton d'appel collant** (mobile) + flottant (desktop).

## ♿ Accessibilité & performance

- HTML sémantique, `lang="fr"`, liens d'évitement, focus visibles, `aria-*` sur les composants.
- `prefers-reduced-motion` respecté, contrastes soignés.
- Zéro dépendance JS externe, images à charger en lazy → chargement rapide (< 2,5 s visé).
- Données structurées Schema.org : `LocalBusiness/CleaningService`, `Service`, `FAQPage`,
  `AggregateRating`, `Review`, `BreadcrumbList`.
