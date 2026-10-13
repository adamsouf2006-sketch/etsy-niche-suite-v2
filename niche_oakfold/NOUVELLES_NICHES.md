# Nouvelles niches validées (API Etsy, 2026-10-12)

Méthode : 30 familles de produits numériques × 200 annonces (5 775 annonces) → 220 annonces récentes (≤ 120 j, hors licences) les plus vues → avis des 30 derniers jours (`suivi24h/large2.py`, `large2.json`). Puis test ciblé de 10 mots-clés quilt (`quilt.json`). Avis ≈ ventes ÷ 10.

## Niche n°1 : patrons de quilt (patchwork) en PDF — VALIDÉE
**26 boutiques différentes** avec annonces récentes qui vendent, **142 avis en 30 jours** (≈ 1 400 ventes/mois sur les seules annonces récentes). Prix 4 à 9 $.

| Sous-niche précise | Boutiques récentes qui vendent | Exemples (âge / avis 30 j / prix) |
|---|---|---|
| Table runner de Noël (chemin de table) | 6 + 4 | Candy Star 63 j / 11 / 8,99 $ ; Table Runner & Placemat 37 j / 9 / 3,99 $ ; Holiday Star 26 j / 3 / 6,50 $ |
| Bloc de quilt (FPP, saisonnier) | 5 | Flower Garden 14 j / 11 / 3,86 $ ; Autumn Maple Leaf 106 j / 6 ; Pumpkin Star 69 j / 4 |
| Quilt triangles (HST, pinwheel) | 3 | Scrappy Pinwheel 32 j / 5 / 5,10 $ ; Diamond Daze 44 j / 5 / 8,50 $ — seulement 1 123 résultats |
| Mini quilt saisonnier (série) | 2 | Pumpkin Patch 32 j / 32 / 6 $ |

Pourquoi elle convient : patrons géométriques (calculs de coupe, métrage, schémas d'assemblage) entièrement fabriqués et vérifiés par le code, pas besoin d'objet physique ni de licence. Saison : Noël maintenant.

## Autres signaux (plusieurs boutiques)
- Fichiers de découpe laser (SVG/DXF) : 11 boutiques, ~70 avis 30 j — surtout des méga-bundles ; non testable physiquement.
- Patrons crochet / tricot : ~15 boutiques, ~100 avis 30 j — exige des modèles réellement réalisés et photographiés → écarté.
- Patrons de couture : ~10 boutiques, ~30 avis 30 j — gradation complexe.
- Presets Lightroom : ~8 boutiques, ~22 avis 30 j.
- Clipart PNG : ~8 boutiques, ~17 avis 30 j (réutilise la chaîne d'illustrations Agnès).

## Mise à jour 2026-10-12 : hors religion et fêtes, ventes fortes ET récentes
Source 1 : BOUTIQUES_NUMERIQUES_2MOIS.md (326 boutiques ≤ 2 mois, ≥ 50 ventes/mois), 137 exclues (religion, fêtes, licences).
Source 2 : validation API (`suivi24h/couture.py`, `couture.json`) : ≥ 3 boutiques distinctes, annonces ≤ 120 j vendues dans les 30 j.

| Produit précis | Résultats | Boutiques récentes qui vendent | Avis 30 j (top 10 récentes) |
|---|---|---|---|
| **Memory bear (ours souvenir) — patron de couture PDF, 10 tailles** | **1 696** | **9** | **92** (31, 20, 12, 7, 5, 5, 5, 4, 2) |
| Patchwork quilt pattern | 46 714 | 8 | 22 |
| Crossbody bag sewing pattern | 13 344 | 7 | 18 |
| Tote bag sewing pattern | 44 434 | 7 | 20 |
| Coffee cup sleeve pattern | 2 153 | 5 | 9 |
| Zipper pouch sewing pattern | 6 720 | 4 | 8 |
| Teddy bear sewing pattern | 30 619 | 3 | 8 |
| Felt food sewing pattern | 2 150 | 2 | 9 (non validé) |
Jeunes boutiques memory bear : SewinggiftCrafts 52 j / 347 ventes/mois, MahaPatterns 11 j / 235 ventes/mois.

## Nouvelles boutiques ≤ 60 j, ≥ 50 ventes/mois (2026-10-12, `suivi24h/young.py`, 544 requêtes, hors religion/fêtes/licences, absentes de BOUTIQUES_NUMERIQUES_2MOIS.md)

| Ventes/mois | Ventes | Âge | Fiches | Boutique | Produit phare |
|---|---|---|---|---|---|
| 956 | 1667 | 52 j | 273 | [OneQuietEvening](https://www.etsy.com/shop/OneQuietEvening) | Bag Sewing Pattern PDF, 3 Sizes, Flap Shoulder Bag Pattern, Crossbody Purse, Beg |
| 498 | 700 | 42 j | 429 | [CERISAPATTERN](https://www.etsy.com/shop/CERISAPATTERN) | Baby Kimono Romper Sewing Pattern PDF | Long Sleeve Wrap Jumpsuit | Quilted Gauz |
| 288 | 386 | 40 j | 31 | [CrafelloDesigns](https://www.etsy.com/shop/CrafelloDesigns) | 1400+ Functional STL Files, Home & Decor STL Bundle ,Organizer ,Gadgets, Stands  |
| 205 | 41 | 6 j | 16 | [AurelleDesignsCo](https://www.etsy.com/shop/AurelleDesignsCo) | Bowl Cozy Sewing Pattern PDF, 3 Sizes, Quilted Fabric Bowl Holder, A4 Letter A0 |
| 200 | 337 | 51 j | 14 | [FayeNorthStudio](https://www.etsy.com/shop/FayeNorthStudio) | Sage Green Ivory Floral Wedding Website Canva Template: RSVP, Countdown Timer, M |
| 191 | 277 | 44 j | 48 | [WaheedstudioDesign](https://www.etsy.com/shop/WaheedstudioDesign) | Quilted Star Quilt Pattern PDF, Sawtooth Star Bedspread Pattern, Red Green Farmh |
| 158 | 220 | 42 j | 59 | [LittleBirdsWants](https://www.etsy.com/shop/LittleBirdsWants) | Jungle Baby Quilt Pattern PDF, Safari Animal Applique Quilt, Nursery Crib Quilt  |
| 153 | 227 | 45 j | 28 | [CozySewPattern](https://www.etsy.com/shop/CozySewPattern) | Goose Lovey Sewing Pattern PDF, Baby Comforter Pattern, Digital Download, Full V |
| 149 | 260 | 52 j | 68 | [MssAbbasiDesign](https://www.etsy.com/shop/MssAbbasiDesign) | Tablecloth Crochet Pattern Pdf Bundle 100+ | Vintage Filet Crochet Patterns, Lac |
| 146 | 109 | 22 j | 128 | [YarnBloomPatternsCo](https://www.etsy.com/shop/YarnBloomPatternsCo) | Flower Pan Protector Crochet Pattern PDF, 4 Graduated Sizes, Cotton Cookware Sep |
| 108 | 171 | 48 j | 41 | [DigitalcraftarStudio](https://www.etsy.com/shop/DigitalcraftarStudio) | 100+ Editable Flyer PSD Bundle | Business, Event, Social Media Templates (Digita |
| 89 | 173 | 58 j | 49 | [FIXFLYSTUDIO](https://www.etsy.com/shop/FIXFLYSTUDIO) | 41 Glitter Sparkle Procreate Brushes, Shimmer Glow Texture Set (Digital Download |
| 88 | 95 | 32 j | 61 | [YarnMallowDesign](https://www.etsy.com/shop/YarnMallowDesign) | Ponytail Beanie Crochet Pattern PDF, Ribbed Messy Bun Hat, 3 Adult Sizes, Winter |
| 85 | 112 | 40 j | 33 | [BrightSewPattern](https://www.etsy.com/shop/BrightSewPattern) | Standing Pencil Pouch Sewing Pattern PDF, Pencil Case Pattern, Step by Step Phot |
| 85 | 100 | 35 j | 40 | [LoopArtSociety](https://www.etsy.com/shop/LoopArtSociety) | Yoshi Amigurumi Crochet Pattern PDF, Green Dinosaur Plush Toy (Digital Download) |
| 83 | 149 | 54 j | 39 | [DigitalValleyHub](https://www.etsy.com/shop/DigitalValleyHub) | 21,000+ Kids Worksheets Bundle | Homeschool & Classroom Printable Mega Library | |
| 80 | 146 | 54 j | 49 | [EraSewingCo](https://www.etsy.com/shop/EraSewingCo) | Culotte Pants Sewing Pattern PDF | Wide Leg Pants Pattern | Women Trousers DIY | |
| 75 | 48 | 19 j | 1137 | [CreatorForgeTr](https://www.etsy.com/shop/CreatorForgeTr) | Cozy Book Lover Printable Stickers, 24 Watercolor PNG Designs and PDF Sheets |
| 72 | 106 | 44 j | 9 | [SewingGiftsCo](https://www.etsy.com/shop/SewingGiftsCo) | Fabric Baby and Child Crown Sewing Pattern PDF, Kids Birthday Crown Pattern, Tod |
| 68 | 16 | 7 j | 33 | [YarnThreadCo](https://www.etsy.com/shop/YarnThreadCo) | Girls Dress Sewing Pattern PDF, Puff Sleeve Dress Pattern, Sizes 2Y-12Y, Beginne |
| 66 | 102 | 46 j | 60 | [BrushesCorner](https://www.etsy.com/shop/BrushesCorner) | 1167+ Procreate Brushes Mega Bundle | Ultimate Brush Pack for Digital Art, Natur |
| 60 | 13 | 7 j | 4 | [LucySewingStudio](https://www.etsy.com/shop/LucySewingStudio) | Chicken Pot Holder Sewing Pattern PDF | Crochet-Free Chicken Kitchen Holder | Fa |
| 58 | 33 | 17 j | 16 | [RolyPattern](https://www.etsy.com/shop/RolyPattern) | Star Bag Sewing Pattern PDF, Reversible Star Tote with Hearts, 3 Sizes, Beginner |
| 53 | 31 | 18 j | 33 | [BhaowMixStudio](https://www.etsy.com/shop/BhaowMixStudio) | Woodland Satchel Bag Knitting Pattern PDF, Lace Shoulder Tote, Cotton Market Sho |
| 51 | 55 | 32 j | 4 | [DesignByAbdal](https://www.etsy.com/shop/DesignByAbdal) | Bowl Cozy Sewing Pattern PDF, Microwave Bowl Cozy, Soup Bowl Cozy, Quilted Bowl  |
| 51 | 9 | 5 j | 100 | [ProCrochetPatternPdf](https://www.etsy.com/shop/ProCrochetPatternPdf) | Cocker Spaniel Crochet Pattern PDF, Amigurumi Dog Pattern, Curly Ear Puppy Tutor |

## Analyse des produits des jeunes boutiques (2026-10-13, `suivi24h/young_products.py`, ~690 requêtes)
194 boutiques ≤ 2 mois à fort volume (hors religion, fêtes, licences) → 7 707 annonces → 300 annonces ≥ 5 € les plus vues → avis 30 j.

| Type (annonces ≥ 5 €) | Annonces | Boutiques | Avis 30 j | Prix médian |
|---|---|---|---|---|
| Fichiers STL (impression 3D) | 47 | 9 | 43 | 7,74 € |
| **Patrons couture : sacs, trousses, rangement** | 31 | **13** | 33 | **9,99 €** |
| Patrons crochet : amigurumi | 34 | 14 | 29 | 7,14 € |
| **Patrons couture : bébé** (gigoteuse, barboteuse, doudou, tapis à langer) | 19 | 7 | 22 | **8,59 €** |
| Laser / SVG / broderie | 11 | 5 | 19 | 11,76 € |
| Patrons crochet : plaids | 12 | 6 | 18 | 6,87 € |
| Patrons couture : vêtements | 31 | 9 | 14 | 12,03 € |
| **Patrons couture : ours / peluches** (+ memory bear : 26 boutiques, 92 avis 30 j) | 6 | 5 | 9 | 6,88 € |
| Tableurs / planners (niche Oakfold) | 1 | 1 | 4 | 5,27 € |
Scan niche Oakfold (formulaires, contrats, tableurs) : 1 668 boutiques candidates → 1 seule jeune boutique ≥ 50 ventes/mois (TrueVanta, reçus).
