// Uso: node render_pages.mjs <pdf> <dirSaida> [escala] [pagIni] [pagFim]
import fs from 'fs';
import { openPdf, renderPage } from './pdflib.mjs';
const [, , file, outDir, sc, a, b] = process.argv;
const scale = +sc || 1.5;
const doc = await openPdf(file);
fs.mkdirSync(outDir, { recursive: true });
for (let pn = +a || 1; pn <= Math.min(+b || doc.numPages, doc.numPages); pn++) {
  const cv = await renderPage(doc, pn, scale);
  fs.writeFileSync(`${outDir}/p${String(pn).padStart(2, '0')}.png`, cv.toBuffer('image/png'));
}
console.log('ok', doc.numPages);
