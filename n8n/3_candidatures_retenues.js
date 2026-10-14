// Fin de boucle : candidatures à envoyer aujourd'hui = adresses valides en attente (anciennes d'abord) + nouvelles
const sd = $getWorkflowStaticData('global');
const tous = $input.all().map(i => i.json);
const reels = tous.filter(j => j.factice !== true);
const faits = reels.filter(j => j.recherche_faite === true);
const premier = tous[0] || {};
const modeTest = premier.mode_test !== false;
const objectif = Number(premier.objectif) || 10;
if (!modeTest && reels.length > 0) {
  // Reprise demain : à la première page qui contient une entreprise pas encore recherchée
  const nonFaites = reels.filter(j => j.recherche_faite !== true && j.page_src);
  sd.page = nonFaites.length ? Math.min(...nonFaites.map(j => j.page_src)) : (premier.page_suivante || premier.page_debut + premier.nb_pages);
  sd.maj = Date.now();
}
const credits = tous.some(j => j.credits_epuises === true);
const creditsUtilises = Math.max(0, ...reels.map(j => Number(j.credits_utilises) || 0));
const aEnvoyer = modeTest ? faits.filter(j => j.retenu === true) : Object.values(sd.attente || {}).sort((a, b) => (a.file_seq || 0) - (b.file_seq || 0));
return aEnvoyer.map(j => ({ json: { ...j, mode_test: modeTest, objectif, nb_recherches: faits.length, credits_utilises: creditsUtilises, nb_retenus: aEnvoyer.length, alerte_credits: credits, credits_scalelist: premier.credits_scalelist } }));
