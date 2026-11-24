// Aplica a limpeza tipográfica também ANTES das substituições da revisão (as substituições passam a casar com o
// texto já limpo); a limpeza é idempotente, então o resultado final para revisões antigas não muda.
const fs = require('fs');
let s = fs.readFileSync('draft.mjs', 'utf8');
const L = s.split('\n');
const iEn = L.findIndex(l => l.startsWith('  if (r.enunciado !== undefined) enunciado = r.enunciado.trim();'));
const iCl = L.findIndex(l => l.startsWith('  const clean = t =>'));
if (iEn < 0 || iCl < 0 || iCl < iEn) throw new Error('nf');
const cleanLine = L[iCl];
L.splice(iCl, 1);
L.splice(iEn, 0, cleanLine, '  const preCleaned = r.enunciado === undefined;', '  if (preCleaned && !r.rawReplace) { enunciado = clean(enunciado); alts = alts.map(clean); }');
fs.writeFileSync('draft.mjs', L.join('\n'));
console.log('ok');
