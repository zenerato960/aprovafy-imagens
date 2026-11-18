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
  const crops = r.crops !== undefined ? r.crops : q.figs.concat(q.shared?.figs || []).map(f => [f.pn, f.x0, f.y0, f.x1, f.y1]);
  // texto cujas linhas estão todas dentro de um recorte (rótulos de gráfico, legendas internas) já aparece na imagem
  const inCrop = p => p.boxes && p.boxes.every(([pn, x0, y0, x1, y1]) => crops.some(([cp, cx0, cy0, cx1, cy1]) => cp === pn && x0 >= cx0 - 2 && x1 <= cx1 + 2 && y0 >= cy0 - 2 && y1 <= cy1 + 2));
  const dropped = [];
  const lineIn = ([pn, x0, y0, x1, y1]) => crops.some(([cp, cx0, cy0, cx1, cy1]) => cp === pn && x0 >= cx0 - 2 && x1 <= cx1 + 2 && y0 >= cy0 - 2 && y1 <= cy1 + 2);
  const keep = p => {
    if (inCrop(p)) { dropped.push(p.text); return false; }
    // linhas iniciais dentro do recorte (ex.: título de mapa colado ao parágrafo seguinte) são retiradas do início
    while (p.boxes && p.boxes.length > 1 && lineIn(p.boxes[0]) && p.text.startsWith(p.boxes[0][5])) {
      dropped.push(p.boxes[0][5]); p = { ...p, text: p.text.slice(p.boxes[0][5].length).trim(), boxes: p.boxes.slice(1) }; keep.last = p;
    }
    return true;
  };
  const txt = p => { keep.last = null; const k = keep(p); return k ? (keep.last || p).text : null; };
  const parts = [...q.notes];
  if (q.shared) parts.push(...q.shared.paras.map(txt).filter(t => t !== null));
  parts.push(...q.stem.map(txt).filter(t => t !== null));
  // com alternativas transcritas à mão, o material pós-alternativas deve vir explicitamente na revisão (posAlt)
  const pos = r.alternativas ? (r.posAlt || []) : (q.posAlternativas || []);
  if (pos.length) parts.push(...pos);
  let enunciado = parts.join('\n');
  let alts = ['a', 'b', 'c', 'd'].map(k => q.alts[k].replace(/\n/g, ' ').trim());
  if (r.enunciado !== undefined) enunciado = r.enunciado.trim();
  if (r.replace) for (const [a, b] of r.replace) { if (!enunciado.includes(a) && b.trim() === '') continue; /* remoção já feita pelo filtro de texto na imagem */ if (!enunciado.includes(a)) throw new Error(`Q${q.num}: trecho não encontrado para substituir: ${a}`); enunciado = enunciado.split(a).join(b); }
  if (r.alternativas) alts = r.alternativas;
  // limpeza tipográfica comum (não altera conteúdo)
  const clean = t => t.replace(/\^o ?C/g, '°C').replace(/\( ?°C\)/g, '(°C)').replace(/(\d\/\d+)\s+([.,;])/g, '$1$2').replace(/ +([.,;:])(?=\s|$)/g, '$1');
  enunciado = clean(enunciado); alts = alts.map(clean);
  if (r.altReplace) for (const [i, a, b] of r.altReplace) { if (!alts[i].includes(a)) throw new Error(`Q${q.num}: alt ${i} sem trecho ${a}`); alts[i] = alts[i].split(a).join(b); }
  out.push({
    num: q.num,
    enunciado,
    alternativas: alts,
    crops,
    textoNaImagem: r.enunciado !== undefined ? [] : dropped,
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
