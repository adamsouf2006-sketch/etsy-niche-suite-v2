// Boucle : lit la réponse de Scalelist pour UNE entreprise. E-mail trouvé ? vérifié (Valid) ? domaine cohérent ?
// Compte les e-mails valides et signale l'arrêt dès que l'objectif du jour est atteint.
const cfg = $('Config').first().json;
const sd = $getWorkflowStaticData('global');
sd.vus = sd.vus || {};
const c = $('Une entreprise à la fois').first().json;   // entreprise du passage en cours
const brut = ($input.first() && $input.first().json) || {};
// Réponse Prospeo (enrich-person) ramenée au format attendu plus bas : { email, status } ou { error }
// Prospeo ne facture que les e-mails VÉRIFIÉS trouvés (only_verified_email) : « NO_MATCH » est gratuit.
function depuisProspeo(b) {
  if (b && b.error === true) {
    const code = String(b.error_code || b.message || 'ERREUR');
    if (/NO_MATCH|NOT_FOUND|NO_RESULT/i.test(code)) return {};
    if (/CREDIT|QUOTA/i.test(code)) return { error: '402 credits epuises (' + code + ')' };
    if (/API_KEY|UNAUTH|INVALID_KEY/i.test(code)) return { error: '401 api key (' + code + ')' };
    return { error: code };
  }
  const e = (b && b.person && b.person.email) || {};
  if (!e.email || e.revealed === false) return {};
  return { email: e.email, status: /^VERIFIED$/i.test(String(e.status)) ? 'Valid' : String(e.status || ''), company_domain: (b.company && b.company.domain) || '' };
}
const r = depuisProspeo(brut);
const accepterRisky = cfg.ACCEPTER_EMAILS_RISKY === true || String(cfg.ACCEPTER_EMAILS_RISKY).toLowerCase() === 'true';
const RE_MAIL = /^[A-Za-z0-9._%+'-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;

function explorer(obj, visite, chemin) {
  if (obj === null || obj === undefined) return;
  if (typeof obj !== 'object') { visite(chemin, obj); return; }
  for (const k of Object.keys(obj)) {
    if (k === 'custom') continue; // nos propres données renvoyées en écho
    explorer(obj[k], visite, chemin ? chemin + '.' + k : k);
  }
}
function lire(r) {
  let email = '', statutBrut = '';
  explorer(r, (chemin, v) => {
    if (typeof v !== 'string') return;
    const cle = chemin.split('.').pop().toLowerCase();
    if (!email && RE_MAIL.test(v.trim()) && /mail/.test(cle)) email = v.trim();
    if (!statutBrut && /status|statut|result|verif|quality|state/.test(cle) && /valid|risky|catch|not[ _-]?found|unknown/i.test(v)) statutBrut = v.trim();
  });
  if (!email) explorer(r, (chemin, v) => { if (!email && typeof v === 'string' && RE_MAIL.test(v.trim())) email = v.trim(); });
  return { email, statutBrut };
}

// Garde-fou : le domaine de l'adresse trouvée doit correspondre au nom de l'entreprise
// (Scalelist déduit le domaine du nom ; il peut se tromper de société).
const GENERIQUES = new Set(['france', 'francaise', 'francais', 'groupe', 'group', 'holding', 'societe', 'compagnie', 'international', 'internationale', 'europe', 'paris', 'services', 'service', 'national', 'nationale', 'generale', 'general', 'gestion', 'participations', 'financiere', 'industries', 'industrie', 'distribution', 'solutions']);
const plat = s => String(s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
function domaineCoherent(email, c) {
  const dom = plat(String(email).split('@')[1] || '');
  const labels = dom.split('.').filter(Boolean);
  if (labels.length < 2) return false;
  const coeur = labels.slice(0, -1).join('').replace(/[^a-z0-9]/g, '');
  const mots = plat(c.entreprise).split(/[^a-z0-9]+/).filter(Boolean);
  const colle = mots.join('');
  const sigle = plat(c.sigle).replace(/[^a-z0-9]/g, '');
  const acronyme = mots.map(m => m[0]).join('');
  if (mots.some((m, i) => !GENERIQUES.has(m) && (m.length >= 4 || (i === 0 && m.length >= 3)) && coeur.includes(m))) return true;
  if (sigle.length >= 3 && coeur.includes(sigle)) return true;
  if (acronyme.length >= 3 && coeur.includes(acronyme)) return true;
  if (coeur.length >= 4 && colle.includes(coeur)) return true;
  return false;
}

if (r.custom && r.custom.siren && String(r.custom.siren) !== String(c.siren)) {
  throw new Error(`Incohérence : la réponse Scalelist (SIREN ${r.custom.siren}) ne correspond pas à l'entreprise en cours (${c.entreprise}, ${c.siren}). Arrêt par sécurité.`);
}
const moi = $('E-mail trouvé et vérifié ?');
const dejaRetenus = moi.isExecuted ? (Number(moi.last().json.total_retenus) || 0) : (Number(c.en_attente) || 0);
const modeTest = c.mode_test;
const erreur = r.error ? (typeof r.error === 'string' ? r.error : JSON.stringify(r.error)) : '';
const creditsEpuises = !!erreur && /402|credit/i.test(erreur);
if (erreur && !creditsEpuises && /401|unauthor|api key/i.test(erreur)) {
  throw new Error('Scalelist a refusé la requête (clé API invalide) : ' + erreur.slice(0, 300));
}
const { email, statutBrut } = erreur ? { email: '', statutBrut: '' } : lire(r);
let statut = 'non_trouve';
if (creditsEpuises) statut = 'credits_epuises';
else if (erreur) statut = 'erreur';
else if (email && /risky|catch/i.test(statutBrut)) statut = 'risky';
else if (email && /valid/i.test(statutBrut) && !/invalid/i.test(statutBrut)) statut = 'valid';
else if (email) statut = 'inconnu';
if (email && !domaineCoherent(email, c)) statut = 'domaine_douteux';
// Anti-doublon par ADRESSE : un même dirigeant peut diriger plusieurs filiales (SIREN différents, même e-mail)
const emailsDeja = new Set([...Object.values(sd.vus || {}).map(v => v && v.email), ...Object.values(sd.attente || {}).map(a => a && a.email_pdg)].filter(Boolean).map(x => String(x).toLowerCase()));
if (!modeTest && email && emailsDeja.has(email.toLowerCase())) statut = 'deja_contacte';
const ok = statut === 'valid' || (statut === 'risky' && accepterRisky);
if (!modeTest && statut !== 'erreur' && statut !== 'credits_epuises') {
  sd.vus[c.siren] = { statut: ok ? 'email_trouve' : statut, date: new Date().toISOString().slice(0, 10), entreprise: c.entreprise, email };
}
// En réel : seules les adresses trouvées, vérifiées et cohérentes sont retenues. En test : tout est retenu pour contrôle.
const retenu = creditsEpuises ? false : (modeTest ? true : ok);
const total = dejaRetenus + (retenu ? 1 : 0);
// Crédits Scalelist consommés aujourd'hui : 1 par e-mail trouvé (quel que soit son statut)
const creditsAvant = moi.isExecuted ? (Number(moi.last().json.credits_utilises) || 0) : 0;
const creditsUtilises = creditsAvant + (email ? 1 : 0);
const soldeDepart = Number(c.credits_scalelist);
const limiteCredits = Math.min(Number(c.objectif) || 10, Number.isFinite(soldeDepart) && c.credits_scalelist !== null ? soldeDepart : Infinity);
const fiche = {
  ...c,
  email_pdg: email,
  email_statut: statut,
  email_statut_brut: statutBrut,
  prospeo_reponse: JSON.stringify(brut).slice(0, 600),
  destinataire: modeTest ? cfg.EMAIL_TEST : email,
  recherche_faite: !creditsEpuises,
  retenu,
  total_retenus: total,
  credits_epuises: creditsEpuises,
  credits_utilises: creditsUtilises,
  stop: creditsEpuises || (!modeTest && creditsUtilises >= limiteCredits), // arrêt dès que N crédits ont été consommés
};
if (!modeTest && retenu) {
  // File d'attente : l'adresse est payée, elle sera envoyée même si une étape suivante tombe en panne aujourd'hui
  sd.seq = (Number(sd.seq) || 0) + 1;
  fiche.file_seq = sd.seq;                              // ordre d'arrivée dans la file
  sd.attente = { ...(sd.attente || {}), [c.siren]: fiche };
}
sd.maj = Date.now();
return [{ json: fiche }];
