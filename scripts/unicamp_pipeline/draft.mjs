// Monta o rascunho de cada questão a partir do raw.json + revisão manual (overrides).
// Uso: node draft.mjs <config.json> [nums...]   (com nums: imprime esses rascunhos)
// Saída: <outDir>/draft.json
import fs from 'fs';
import path from 'path';
import { pathToFileURL } from 'url';
const cfg = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const raw = JSON.parse(fs.readFileSync(cfg.outDir + '/raw.json', 'utf8'));
const rev = cfg.review ? (await import(pathToFileURL(path.resolve(path.dirname(process.argv[2]), cfg.review)).href)).default : {};

const out = [];
for (const q of raw.questions) {
  const r = rev[q.num] || {};
  const parts = [...q.notes];
  if (q.shared) parts.push(...q.shared.paras.map(p => p.text));
  parts.push(...q.stem.map(p => p.text));
  let enunciado = parts.join('\n');
  let alts = ['a', 'b', 'c', 'd'].map(k => q.alts[k].replace(/\n/g, ' ').trim());
  if (r.enunciado !== undefined) enunciado = r.enunciado.trim();
  if (r.replace) for (const [a, b] of r.replace) { if (!enunciado.includes(a)) throw new Error(`Q${q.num}: trecho não encontrado para substituir: ${a}`); enunciado = enunciado.split(a).join(b); }
  if (r.alternativas) alts = r.alternativas;
  // limpeza tipográfica comum (não altera conteúdo)
  const clean = t => t.replace(/\^o ?C/g, '°C').replace(/\( ?°C\)/g, '(°C)').replace(/(\d\/\d+)\s+([.,;])/g, '$1$2').replace(/ +([.,;:])(?=\s|$)/g, '$1');
  enunciado = clean(enunciado); alts = alts.map(clean);
  if (r.altReplace) for (const [i, a, b] of r.altReplace) { if (!alts[i].includes(a)) throw new Error(`Q${q.num}: alt ${i} sem trecho ${a}`); alts[i] = alts[i].split(a).join(b); }
  out.push({
    num: q.num,
    enunciado,
    alternativas: alts,
    crops: r.crops !== undefined ? r.crops : q.figs.concat(q.shared?.figs || []).map(f => [f.pn, f.x0, f.y0, f.x1, f.y1]),
    cropLayout: r.cropLayout || 'stack',
    cropGap: r.cropGap, cropAlign: r.cropAlign,
    cropLabels: r.cropLabels || null,
    revisado: !!rev[q.num],
    obs: r.obs || '',
    segs: q.segs,
  });
}
fs.writeFileSync(cfg.outDir + '/draft.json', JSON.stringify(out, null, 1));
const show = process.argv.slice(3).map(Number);
for (const d of out.filter(d => show.includes(d.num))) {
  console.log(`\n##### Q${d.num} crops=${JSON.stringify(d.crops.map(c => c.map(v => typeof v === 'number' ? Math.round(v) : v)))}`);
  console.log(d.enunciado);
  d.alternativas.forEach((a, i) => console.log('abcd'[i] + ') ' + a));
}
