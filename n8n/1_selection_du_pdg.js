// Garde les grandes entreprises dont le siège est en Île-de-France et choisit leur dirigeant (PDG)
const cfg = $('Config').first().json;
const prep = $('Préparer la recherche').first().json;
const sd = $getWorkflowStaticData('global');
sd.vus = sd.vus || {};
const modeTest = prep.mode_test;
const attente = sd.attente || {};                      // adresses valides déjà trouvées mais pas encore envoyées
const nbAttente = modeTest ? 0 : Object.keys(attente).length;

// Solde de crédits Scalelist (appel gratuit) : on ne lance jamais plus de recherches qu'il ne reste de crédits
function lireCredits(o) {
  const vals = [];
  (function voir(x, chemin) {
    if (x === null || x === undefined) return;
    if (typeof x === 'object') { for (const k of Object.keys(x)) voir(x[k], chemin ? chemin + '.' + k : k); return; }
    if (typeof x === 'number' && /credit/i.test(chemin)) vals.push({ chemin, v: x });
  })(o, '');
  if (vals.length === 1) return vals[0].v;
  const pref = vals.filter(e => /remain|balance|available|left|restant/i.test(e.chemin));
  if (pref.length === 1) return pref[0].v;
  return null; // format non reconnu : pas de limite appliquée
}
let credits = null;
try { const cr = $('Prospeo – Solde de crédits').first().json; if (cr && !cr.error) credits = lireCredits(cr); } catch (e) { credits = null; }
const IDF = ['75', '77', '78', '91', '92', '93', '94', '95'];
// Secteurs visés (sections NAF). Vide = tous les secteurs.
const SECTEURS = String(cfg.SECTEURS_NAF || '').toUpperCase().split(/[^A-Z]+/).filter(Boolean);
// Activités exclues : débuts de code NAF (ex. 65 = assurance, 64.1 = banques, 96.03 = services funéraires)
const NAF_EXCLUS = String(cfg.EXCLURE_NAF || '').split(/[,;\s]+/).map(x => x.trim()).filter(Boolean);
// Entreprises exclues : mots contenus dans le nom (ex. VEOLIA)
const sansAccent = x => String(x || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toUpperCase();
const NOMS_EXCLUS = String(cfg.EXCLURE_NOMS || '').split(/[,;]+/).map(x => sansAccent(x).trim()).filter(Boolean);

const norm = s => String(s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[’`]/g, "'").toLowerCase().replace(/\s+/g, ' ').trim();
function rang(qualite) {
  const q = norm(qualite);
  if (!q) return null;
  if (/administrateur|commissaire|membre|vice|delegue|suppleant|autre|controleur|liquidateur|adjoint|representant|censeur|secretaire/.test(q)) {
    if (!/president.*directeur general/.test(q)) return null;
  }
  if (/president.*directeur general|president-directeur general|^pdg$/.test(q)) return 1;
  if (/^president du conseil d'administration/.test(q)) return 2;
  if (/^president/.test(q) && !/surveillance/.test(q) && !/directoire/.test(q)) return 3;
  if (/^president du directoire/.test(q)) return 4;
  if (/^directeur general/.test(q)) return 5;
  if (/^gerant/.test(q)) return 6;
  return null;
}
const PARTICULES = ['de', 'du', 'des', 'la', 'le', 'les', 'dit', 'd', 'l', 'von', 'van', 'der', 'den', 'da', 'di', 'del', 'el', 'al', 'ben'];
function casse(s, particules) {
  return String(s || '').toLowerCase().split(/(\s+|-|')/).map((m, i) => {
    if (!m || /^(\s+|-|')$/.test(m)) return m;
    if (particules && i > 0 && PARTICULES.includes(m)) return m;
    return m.charAt(0).toUpperCase() + m.slice(1);
  }).join('').replace(/\s+/g, ' ').trim();
}
function adresseSiege(s) {
  const voie = [s.numero_voie, s.indice_repetition, s.type_voie, s.libelle_voie].filter(Boolean).join(' ');
  return casse(voie, true);
}

// Noms courts pour Prospeo : il reconnaît le nom d'usage (« Elior »), pas la raison sociale (« ELIOR RESTAURATION FRANCE »)
const MOTS_VIDES = new Set(['SA', 'SAS', 'SASU', 'SARL', 'SNC', 'SCA', 'SE', 'EURL', 'GIE', 'DE', 'DU', 'DES', 'LA', 'LE', 'LES', 'L', 'D', 'ET', 'EN', 'FRANCE', 'FRANCAISE', 'FRANCAIS', 'SOCIETE', 'STE', 'SOC', 'NATIONALE', 'NATIONAL', 'COMPAGNIE', 'CIE', 'GROUPE', 'GROUP', 'HOLDING', 'ETABLISSEMENTS', 'ETS', 'SERVICES', 'SERVICE', 'SOLUTIONS', 'OPERATIONS', 'INTERNATIONAL', 'INTERNATIONALE', 'INDUSTRIE', 'INDUSTRIES', 'DISTRIBUTION', 'PARTICIPATIONS', 'GESTION', 'EXPLOITATION', 'ANONYME', 'SIMPLIFIEE', 'ACTIONS', 'PAR']);
function nomsCourts(r) {
  const mots = sansAccent(r.nom_raison_sociale || r.nom_complet || '').replace(/[^A-Z0-9&]+/g, ' ').split(' ').filter(m => m && !MOTS_VIDES.has(m));
  const sigle = String(r.sigle || '').trim();
  const un = sigle.length >= 2 ? sigle : (mots[0] && mots[0].length >= 4 ? mots[0] : mots.slice(0, 2).join(' '));
  const brut = String(r.nom_raison_sociale || r.nom_complet || '').replace(/\s+/g, ' ').trim();
  let deux = mots.slice(0, 2).join(' ');
  if (sigle.length >= 2 || !deux || deux === un) deux = brut;           // 2e essai : raison sociale complète
  return { prospeo_nom1: casse(un, false) || '', prospeo_nom2: casse(deux, false) || '' };
}
const vus = new Set();
const candidats = [];
let totalResultats = 0;
function traiterPage(res) {
  totalResultats += res.length;
  for (const r of res) {
    if (!r || !r.siren || vus.has(r.siren)) continue;
    vus.add(r.siren);
    const siege = r.siege || {};
    if (r.etat_administratif && r.etat_administratif !== 'A') continue;
    if (!IDF.includes(String(siege.departement || ''))) continue;          // siège social en Île-de-France
    if (String(r.categorie_entreprise || '') !== String(cfg.CATEGORIE || 'GE')) continue; // grande entreprise
    if (!String(r.nature_juridique || '').startsWith('5')) continue;       // sociétés commerciales uniquement
    if (SECTEURS.length && !SECTEURS.includes(String(r.section_activite_principale || '').toUpperCase())) continue; // secteur non visé
    const codeNaf = String(r.activite_principale || '');
    if (NAF_EXCLUS.some(p => codeNaf.startsWith(p))) continue;             // activité exclue (banque, assurance...)
    const nomTest = sansAccent((r.nom_raison_sociale || '') + ' ' + (r.nom_complet || ''));
    if (NOMS_EXCLUS.some(m => nomTest.includes(m))) continue;              // entreprise exclue par son nom
    if (!modeTest && (sd.vus[r.siren] || attente[r.siren])) continue;     // déjà traitée lors d'une exécution précédente
    let best = null;
    for (const d of (r.dirigeants || [])) {
      if (d.type_dirigeant !== 'personne physique' || !d.nom || !d.prenoms) continue;
      const k = rang(d.qualite);
      if (k === null) continue;
      if (!best || k < best.k) best = { k, d };
    }
    if (!best) continue;
    const brut = String(best.d.nom);
    const m = brut.match(/^(.*?)\s*\((.*?)\)\s*$/);
    const nom = casse(m ? m[1] : brut, true);
    const nomAlt = m ? casse(m[2], true) : '';
    const prenom = casse(String(best.d.prenoms).split(/[\s,]+/)[0], false);
    const entreprise = String(r.nom_raison_sociale || r.nom_complet || '').replace(/\s+/g, ' ').trim();
    if (!entreprise || !nom || !prenom) continue;
    candidats.push({
      siren: r.siren,
      entreprise,
      ...nomsCourts(r),
      sigle: r.sigle || '',
      section: r.section_activite_principale || '',
      naf: r.activite_principale || '',
      adresse_ligne: adresseSiege(siege),
      code_postal: siege.code_postal || '',
      ville: siege.libelle_commune || '',
      departement: siege.departement || '',
      dirigeant_prenom: prenom,
      dirigeant_nom: nom,
      dirigeant_nom_alt: nomAlt,
      dirigeant_qualite: String(best.d.qualite || '').replace(/’/g, "'"),
    });
  }
}
// Scalelist ne facture QUE les e-mails trouvés (une recherche « Not found » est gratuite).
// On prépare donc jusqu'à MAX_RECHERCHES_PAR_JOUR entreprises ; la boucle s'arrête dès que CANDIDATURES_PAR_JOUR crédits
// ont été consommés (= e-mails trouvés). Si les pages reçues ne suffisent pas, on lit les pages suivantes de data.gouv.
const helpers = this.helpers;
const sleep = ms => new Promise(ok => setTimeout(ok, ms));
async function lirePage(p) {
  for (let essai = 0; essai < 3; essai++) {
    try {
      return await helpers.httpRequest({ method: 'GET', url: 'https://recherche-entreprises.api.gouv.fr/search', qs: { categorie_entreprise: cfg.CATEGORIE || 'GE', region: '11', etat_administratif: 'A', per_page: 25, page: p }, json: true, timeout: 30000 });
    } catch (e) { await sleep(2000 * (essai + 1)); }
  }
  return null;
}
const objectif = modeTest ? (Number(cfg.MAX_TEST) || 2) : (Number(cfg.CANDIDATURES_PAR_JOUR) || 10);
const plafond = modeTest ? objectif : Math.max(objectif, Number(cfg.MAX_RECHERCHES_PAR_JOUR) || 40);
const recues = $input.all().map(it => (it.json && it.json.results) || []);
let prochaine = prep.page_debut;
let lues = 0;
for (let p = prep.page_debut; candidats.length < plafond && p <= 400 && lues < 80; p++, lues++) {
  let res = recues[p - prep.page_debut];
  if (!res) { const rep = await lirePage(p); if (!rep) break; res = rep.results || []; await sleep(300); }
  if (!res.length) { prochaine = 1; break; }            // fin de la liste : on repartira du début (les déjà-vues sont ignorées)
  const avant = candidats.length;
  traiterPage(res);
  for (let i = avant; i < candidats.length; i++) candidats[i].page_src = p;
  prochaine = candidats.length > plafond ? p : p + 1;   // page pas entièrement utilisée : on y revient demain
}
const lot = candidats.slice(0, plafond);
const commun = { mode_test: modeTest, objectif, en_attente: nbAttente, credits_scalelist: credits, page_suivante: prochaine, page_debut: prep.page_debut, nb_pages: prep.nb_pages };
if (lot.length === 0) {
  if (!modeTest) { sd.page = prochaine; sd.maj = Date.now(); }
  return nbAttente > 0 ? [{ json: { factice: true, ...commun } }] : [];
}
return lot.map(c => ({ json: { ...c, ...commun } }));
