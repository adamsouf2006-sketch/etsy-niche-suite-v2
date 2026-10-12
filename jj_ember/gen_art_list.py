# Liste des illustrations attendues (lue dans gen_art.py sans lancer la génération).
import re, os
KEYS = re.findall(r'^ "([a-z0-9_]+)":\(', open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen_art.py")).read(), re.M)
