# Accès à l'API Etsy (boutique Oakfold)

Aucun secret n'est stocké dans ce dépôt. Une session a besoin de 3 choses :

1. **Réseau** : `openapi.etsy.com` et `api.etsy.com` dans les domaines autorisés de l'environnement cloud
   (menu environnement > Edit > Network access). Ne PAS créer de « secret » qui injecte un en-tête
   `Authorization` : il écrase le jeton OAuth.
2. **Variables d'environnement** (menu environnement > Edit > Environment variables) :
   - `ETSY_KEY` = `keystring:shared_secret` (lecture : recherche, boutiques, prix)
   - `ETSY_REFRESH_TOKEN` = refresh token OAuth (écriture : créer / modifier / publier ; valable 90 jours)
   - `ETSY_SHOP_ID` = `67905497`
3. **Quota** : 5 000 requêtes / jour, 5 / seconde. En cas de 429, l'en-tête `retry-after` donne le délai en secondes.

## Utilisation
- Lecture : en-tête `x-api-key: $ETSY_KEY`.
- Écriture : `commun/publish.py` renouvelle le jeton à partir de `ETSY_REFRESH_TOKEN`.
  - Brouillon : `python3 commun/publish.py produit_xxx --draft`
  - Publication (0,20 $ par fiche) : `python3 commun/publish.py produit_xxx`
- Chaque produit a un `listing.json` (titre, tags, prix, catégorie, photos, vidéo, fichiers).
- Non faisable via l'API : la case « Avec un générateur d'IA » (à cocher dans l'éditeur Etsy).

## Obtenir un refresh token (ou s'il a expiré)
Autorisation OAuth PKCE, callback `http://localhost:8888/callback`, scopes `listings_w listings_r shops_r` :
ouvrir le lien `https://www.etsy.com/oauth/connect?...`, cliquer « Allow access », recopier l'adresse
`localhost:8888/callback?code=...` (la page d'erreur est normale), puis échanger le code sur
`https://api.etsy.com/v3/public/oauth/token`. La réponse contient `refresh_token`.
