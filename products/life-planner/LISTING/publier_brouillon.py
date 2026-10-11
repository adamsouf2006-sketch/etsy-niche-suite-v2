#!/usr/bin/env python3
"""Crée l'annonce Life Planner en BROUILLON sur la boutique Etsy Oakfold.

Utilisation (sur ton ordinateur, dans le dossier LISTING) :
    python3 publier_brouillon.py

Le script :
  1. demande ta clé Etsy (keystring:shared_secret), sans l'afficher ;
  2. ouvre la page de connexion Etsy et récupère le code tout seul ;
  3. crée l'annonce en brouillon (jamais active) ;
  4. envoie les 10 images, la vidéo et le fichier zip ;
  5. relit le brouillon et affiche le lien pour le vérifier.

Aucun jeton n'est enregistré sur le disque. Seulement Python 3, rien à installer.
"""
import base64
import getpass
import hashlib
import http.server
import json
import os
import secrets
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
import webbrowser

SHOP_ID = 67905497
CLIENT_ID = "20vtorwavjcwhplpol1mdv44"
REDIRECT_URI = "http://localhost:8888/callback"
SCOPES = "listings_w listings_r shops_r"
TAXONOMY_ID = 12476  # Paper & Party Supplies > ... > Templates > Planner Templates
API = "https://openapi.etsy.com/v3/application"
TOKEN_URL = "https://api.etsy.com/v3/public/oauth/token"

DOSSIER = os.path.dirname(os.path.abspath(__file__))
IMAGES = ["01-main.jpg", "02-p2.jpg", "03-p3.jpg", "04-p4.jpg", "05-p5.jpg",
          "06-p6.jpg", "07-p7.jpg", "08-p8.jpg", "09-p9.jpg", "10-p10.jpg"]
VIDEO = "life-planner.mp4"
ZIP = "Oakfold-Life-Planner.zip"


def stop(msg):
    print("\nERREUR : " + msg)
    sys.exit(1)


def requete(methode, url, api_key, token=None, data=None, content_type=None):
    headers = {"x-api-key": api_key}
    if token:
        headers["Authorization"] = "Bearer " + token
    if content_type:
        headers["Content-Type"] = content_type
    req = urllib.request.Request(url, data=data, headers=headers, method=methode)
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            corps = r.read()
    except urllib.error.HTTPError as e:
        stop("%s %s -> HTTP %s\n%s" % (methode, url, e.code, e.read().decode(errors="replace")))
    return json.loads(corps) if corps else {}


def formulaire(champs):
    return urllib.parse.urlencode(champs).encode(), "application/x-www-form-urlencoded"


def multipart(champs, nom_champ_fichier, chemin, type_mime):
    limite = uuid.uuid4().hex
    morceaux = []
    for cle, valeur in champs.items():
        morceaux.append(("--%s\r\nContent-Disposition: form-data; name=\"%s\"\r\n\r\n%s\r\n"
                         % (limite, cle, valeur)).encode())
    with open(chemin, "rb") as f:
        contenu = f.read()
    morceaux.append(("--%s\r\nContent-Disposition: form-data; name=\"%s\"; filename=\"%s\"\r\n"
                     "Content-Type: %s\r\n\r\n" % (limite, nom_champ_fichier,
                                                    os.path.basename(chemin), type_mime)).encode())
    morceaux.append(contenu)
    morceaux.append(("\r\n--%s--\r\n" % limite).encode())
    return b"".join(morceaux), "multipart/form-data; boundary=" + limite


def verifier_fichiers():
    manquants = [n for n in IMAGES + [VIDEO, ZIP, "listing.json", "description.txt"]
                 if not os.path.isfile(os.path.join(DOSSIER, n))]
    if manquants:
        stop("fichiers introuvables dans %s : %s" % (DOSSIER, ", ".join(manquants)))


def connexion_etsy(api_key):
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    state = secrets.token_urlsafe(16)
    lien = "https://www.etsy.com/oauth/connect?" + urllib.parse.urlencode({
        "response_type": "code", "redirect_uri": REDIRECT_URI, "scope": SCOPES,
        "client_id": CLIENT_ID, "state": state, "code_challenge": challenge,
        "code_challenge_method": "S256"}, quote_via=urllib.parse.quote)

    resultat = {}

    class Retour(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            url = urllib.parse.urlparse(self.path)
            if url.path != "/callback":
                self.send_response(404)
                self.end_headers()
                return
            resultat.update({k: v[0] for k, v in urllib.parse.parse_qs(url.query).items()})
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("<h2>C'est bon, tu peux revenir au terminal.</h2>".encode())

        def log_message(self, *args):
            pass

    serveur = http.server.HTTPServer(("localhost", 8888), Retour)
    print("\nJ'ouvre la page de connexion Etsy. Clique sur « Allow access ».")
    print("Si le navigateur ne s'ouvre pas, copie ce lien :\n" + lien + "\n")
    webbrowser.open(lien)
    while "code" not in resultat and "error" not in resultat:
        serveur.handle_request()
    serveur.server_close()

    if "error" in resultat:
        stop("Etsy a refusé la connexion : %s" % resultat.get("error_description", resultat["error"]))
    if resultat.get("state") != state:
        stop("le paramètre state ne correspond pas, connexion annulée par sécurité.")

    data, ct = formulaire({"grant_type": "authorization_code", "client_id": CLIENT_ID,
                           "redirect_uri": REDIRECT_URI, "code": resultat["code"],
                           "code_verifier": verifier})
    jetons = requete("POST", TOKEN_URL, api_key, data=data, content_type=ct)
    if "access_token" not in jetons:
        stop("pas de jeton reçu d'Etsy.")
    print("Connexion Etsy OK.")
    return jetons["access_token"]


def main():
    verifier_fichiers()
    with open(os.path.join(DOSSIER, "listing.json"), encoding="utf-8") as f:
        fiche = json.load(f)
    with open(os.path.join(DOSSIER, "description.txt"), encoding="utf-8") as f:
        description = f.read().strip()
    if len(fiche["tags"]) != 13:
        stop("listing.json doit contenir 13 tags.")

    api_key = os.environ.get("ETSY_API_KEY") or getpass.getpass(
        "Colle ta clé Etsy au format keystring:shared_secret (elle ne s'affiche pas) : ").strip()
    if not api_key.startswith(CLIENT_ID + ":"):
        stop("la clé doit commencer par %s: suivi du shared secret." % CLIENT_ID)

    ping = requete("GET", API + "/openapi-ping", api_key)
    print("Clé API OK (application %s)." % ping.get("application_id"))

    token = connexion_etsy(api_key)

    print("\nCréation du brouillon...")
    data, ct = formulaire({
        "title": fiche["title"], "description": description, "price": fiche["price_eur"],
        "quantity": 999, "who_made": "i_did", "when_made": "made_to_order",
        "is_supply": "false", "type": "download", "taxonomy_id": TAXONOMY_ID,
        "tags": ",".join(fiche["tags"]),
    })
    annonce = requete("POST", "%s/shops/%d/listings" % (API, SHOP_ID), api_key, token, data, ct)
    lid = annonce["listing_id"]
    print("Brouillon créé : listing_id %s (state=%s)" % (lid, annonce.get("state")))

    base = "%s/shops/%d/listings/%s" % (API, SHOP_ID, lid)
    for rang, nom in enumerate(IMAGES, start=1):
        data, ct = multipart({"rank": rang}, "image", os.path.join(DOSSIER, nom), "image/jpeg")
        requete("POST", base + "/images", api_key, token, data, ct)
        print("  image %2d/10 envoyée (%s)" % (rang, nom))

    print("  envoi de la vidéo (peut prendre une minute)...")
    data, ct = multipart({"name": VIDEO}, "video", os.path.join(DOSSIER, VIDEO), "video/mp4")
    requete("POST", base + "/videos", api_key, token, data, ct)
    print("  vidéo envoyée")

    data, ct = multipart({"name": ZIP, "rank": 1}, "file", os.path.join(DOSSIER, ZIP), "application/zip")
    requete("POST", base + "/files", api_key, token, data, ct)
    print("  fichier zip envoyé")

    print("\nVérification...")
    l = requete("GET", "%s/listings/%s?includes=Images,Videos" % (API, lid), api_key, token)
    fichiers = requete("GET", base + "/files", api_key, token)
    prix = l["price"]["amount"] / l["price"]["divisor"]
    controles = [
        ("Titre", l["title"] == fiche["title"], l["title"]),
        ("Prix", abs(prix - fiche["price_eur"]) < 0.001, "%.2f %s" % (prix, l["price"]["currency_code"])),
        ("Tags", len(l["tags"]) == 13, "%d tags" % len(l["tags"])),
        ("Images", len(l.get("images", [])) == 10, "%d images" % len(l.get("images", []))),
        ("Vidéo", len(l.get("videos", [])) == 1, "%d vidéo" % len(l.get("videos", []))),
        ("Fichier", fichiers.get("count") == 1, "%s fichier" % fichiers.get("count")),
        ("État", l["state"] == "draft", l["state"]),
    ]
    for nom, ok, valeur in controles:
        print("  [%s] %-8s %s" % ("OK" if ok else "!!", nom, valeur))

    print("\nTerminé. L'annonce est en BROUILLON, rien n'est publié.")
    print("Vérifie-la et publie-la toi-même ici :")
    print("https://www.etsy.com/your/shops/me/listing-editor/edit/%s" % lid)


if __name__ == "__main__":
    main()
