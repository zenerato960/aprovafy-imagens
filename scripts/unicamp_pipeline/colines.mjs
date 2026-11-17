// Uso: node colines.mjs <pdf> <pag> : linhas por coluna com coordenadas e fontes
import { openPdf, pageItems, toLines } from './pdflib.mjs';
const [, , file, pg] = process.argv;
const doc = await openPdf(file);
const { W, items } = await pageItems(doc, +pg);
for (const [nm, f] of [['L', i => i.x < W / 2], ['R', i => i.x >= W / 2]]) {
  console.log('--- col', nm);
  for (const l of toLines(items.filter(f))) console.log(`${l.y.toFixed(1).padStart(6)} ${l.x0.toFixed(0).padStart(4)} h${l.h.toFixed(1)} ${[...new Set(l.items.map(i=>i.font))].join(',')} | ${l.text}`);
}
