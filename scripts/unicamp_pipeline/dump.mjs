// Uso: node dump.mjs <pdf> [pagIni] [pagFim] [--lines]
// Imprime resumo por página (ou linhas com coordenadas).
import { openPdf, pageItems, toLines } from './pdflib.mjs';
const [, , file, a, b, flag] = process.argv;
const doc = await openPdf(file);
const p0 = +a || 1, p1 = +b || doc.numPages;
console.log('paginas', doc.numPages);
for (let pn = p0; pn <= Math.min(p1, doc.numPages); pn++) {
  const { W, H, items } = await pageItems(doc, pn);
  const lines = toLines(items);
  if (flag === '--lines') {
    console.log(`\n=== p${pn} ${W.toFixed(0)}x${H.toFixed(0)}`);
    for (const l of lines) console.log(`${l.y.toFixed(0).padStart(4)} ${l.x0.toFixed(0).padStart(4)}-${l.x1.toFixed(0).padEnd(4)} h${l.h.toFixed(1)} | ${l.text}`);
  } else {
    console.log(`p${pn} ${W.toFixed(0)}x${H.toFixed(0)} itens=${items.length} | ${lines.slice(0, 3).map(l => l.text).join(' / ').slice(0, 150)}`);
  }
}
