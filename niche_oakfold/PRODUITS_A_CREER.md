# Produits précis à créer pour Oakfold (API Etsy, 2026-10-12)

Déjà faits (exclus) : budget, compta, nettoyage, garde/nanny, artisan/handyman.
Méthode : 30 mots-clés précis, 50 annonces chacun (~150 requêtes). Vues/mois = somme des 20 annonces numériques les plus vues.
Ratio = vues/mois ÷ résultats (plus haut = plus de demande par concurrent). Avis = avis des 3 annonces les plus vues.

| # | Produit précis | Résultats | Vues/mois top 20 | Ratio | Avis top 3 |
|---|---|---|---|---|---|
| 1 | DJ Contract Template (contrat + booking form + invoice) | 158 | 1 316 | **8,3** | 1/1/2 |
| 2 | Body Sculpting Consent & Intake Forms | 401 | 1 601 | **4,0** | 4/2/0 |
| 3 | Tutoring Contract + Parent Intake Form | 148 | 582 | **3,9** | 2/0/1 |
| 4 | Microblading Consent Form + Aftercare | 352 | 1 320 | **3,7** | 12/0/1 |
| 5 | Brow Lamination & Lash Lift Consent Form | 318 | 1 111 | **3,5** | 5/2/1 |
| 6 | Massage Therapy Intake Form + SOAP notes | 684 | 1 785 | 2,6 | **22**/6/7 |
| 7 | Landscaping / Lawn Care Invoice + Estimate | 706 | 1 831 | 2,6 | 0/0/0 |
| 8 | Lash Extension Consent Form | 910 | 2 195 | 2,4 | 0/0/3 |
| 9 | Event Planner Contract + Client Questionnaire | 1 012 | 2 210 | 2,2 | 0/0/3 |
| 10 | Dog Walking Contract + Pet Info Sheet | 605 | 1 286 | 2,1 | 9/5/0 |
| 11 | Airbnb Welcome Book (Canva) | 8 206 | 16 591 | 2,0 | **60/57/21** |
| 12 | Notary Forms (journal + invoice) | 1 133 | 2 135 | 1,9 | 4/15/1 |

Écartés (demande faible ou trop de concurrence) : pressure washing estimate, mobile detailing, personal trainer forms, hair salon consultation, therapist intake, reiki forms, airbnb cleaning checklist.

## Vérification ancienneté (2026-10-12, 96 annonces suivies, `suivi24h/age.py`)
Ventes/mois estimées = avis × 10 ÷ âge. **Correction : les niches 1–10 sont de vieilles niches lentes.**
Sur 96 annonces, seulement 2 ont ≤ 120 jours, et 0 avis. Le meilleur de chaque niche fait 1 à 7 ventes/mois, avec des annonces de 2 à 4 ans.

| Mot-clé | Âge mini | Meilleure annonce |
|---|---|---|
| airbnb welcome book | 153 j | **~41 ventes/mois à 153 j (60 vues/j)** → seule niche avec un gagnant récent |
| notary forms | 467 j | ~7/mois |
| massage intake form | 87 j | ~6,6/mois (annonce de 1 002 j) |
| event planner / dog walking contract | 340 / 483 j | ~4/mois |
| dj, body sculpting, microblading, tutoring, brow, lash, landscaping | — | ≤ 3/mois |

Gagnants récents liés à Oakfold (BOUTIQUES_NUMERIQUES_2MOIS.md) : BudgetwithRozCanada (25 j, 2 fiches, ~137 ventes/mois, *Annual Finance Planner Spreadsheet*),
Smarbudget (3 j, 4 fiches, ~75/mois), XclusivetemplatesArt (29 j, ~121/mois, budget paycheck Google Sheets).

## Validation multi-annonces (2026-10-12, `suivi24h/multi.py`, 30 mots-clés)
Critère : plusieurs annonces de ≤ 180 j avec ≥ 3 vues/j **et** des avis (ventes).

- **Validé : Airbnb Welcome Book (Canva)**. 5 annonces récentes vendent : 153 j/60 vues/j/21 avis, 88 j/2 avis, 109 j/4 avis (version espagnole), 114 j/2 avis, 1 j/4 avis. Prix 2–7 $.
- **Partiel : Paycheck Budget Spreadsheet**. 2 annonces récentes vendent (175 j/13 avis/22 €, 30 j/2 avis/8 $). Oakfold a déjà un budget annuel.
- Signaux isolés (1 seule annonce, non validés) : annual finance planner, rental property spreadsheet, landlord forms, inventory spreadsheet, savings challenge.
- Aucune vente récente : DJ, esthéticienne, massage, photographie, event planner, daycare, cleaning bundle, P&L, net worth, sinking funds.

## Airbnb : analyse approfondie (2026-10-12, `suivi24h/airbnb.py`, ~70 requêtes en cache)
**Verdict : NON validé, niche saturée.**
- 859 annonces numériques sur 7 recherches Airbnb ; **423 créées dans les 180 derniers jours**. Seulement 13 font ≥ 5 vues/j.
- Avis des 30 meilleures annonces récentes sur les 30 derniers jours : **~11 au total** (≈ 110 ventes/mois pour tout le marché récent). Un seul vrai gagnant (21 avis) ; tous les autres ont 0 à 4 avis.
- Les ventes vont à de grosses boutiques déjà établies : Templates4branding (43 720 ventes), DesignByMinsiPrincy (36 066), LuvionStudio (11 511), ByPantherStudio (8 528).
- Guerre des prix : 3,99 $, 1,80 $, 0,87 $.
- Langues : demande quasi nulle en français (37 annonces, ≤ 1 vue/j), en espagnol et en allemand.
