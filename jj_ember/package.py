# Prépare les dossiers produit_jj_* lus par commun/publish.py (listing.json + photos + vidéo + PDF).
# Usage : python3 package.py <produit> <variante_principale 1|2|3>
import os, sys, json, shutil
import listings as L, build as B
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(H); OUT = os.path.join(H, "out")

def select(key, main):
    ph = os.path.join(OUT, key, "photos")
    sel = [f"main_v{main}.jpg"] + [f"photo_{i:02d}.jpg" for i in range(2, 11)]
    json.dump(sel, open(os.path.join(ph, "selection.json"), "w"))
    return sel

def package(key, main):
    li = L.LISTINGS[key]; d = os.path.join(ROOT, li["dir"]); src = os.path.join(OUT, key)
    shutil.rmtree(d, ignore_errors=True); os.makedirs(os.path.join(d, "img")); os.makedirs(os.path.join(d, "files"))
    sel = select(key, main); imgs = []
    for i, f in enumerate(sel, 1):
        n = f"img/{i:02d}_{f}"; shutil.copy(os.path.join(src, "photos", f), os.path.join(d, n)); imgs.append(n)
    shutil.copy(os.path.join(src, "video.mp4"), os.path.join(d, "video.mp4"))
    man = json.load(open(os.path.join(src, "manifest.json"))); files = []
    for f in man["files"]: shutil.copy(os.path.join(src, f), os.path.join(d, "files", f)); files.append("files/" + f)
    json.dump(dict(title=li["title"], price=li["price"], tags=li["tags"], description=li["description"], taxonomy_id=L.TAXONOMY,
                   images=imgs, video="video.mp4", files=files), open(os.path.join(d, "listing.json"), "w"), indent=1, ensure_ascii=False)
    print(key, "->", li["dir"], len(imgs), "photos,", len(files), "fichiers")

if __name__ == "__main__":
    package(sys.argv[1], int(sys.argv[2]))
