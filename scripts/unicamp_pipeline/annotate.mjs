// Páginas anotadas para definir recortes: grade em pt (a cada 25, rótulo a cada 50) e caixas candidatas.
// Uso: node annotate.mjs <config.json> [pagIni] [pagFim]
import fs from 'fs';
import { openPdf, renderPage, createCanvas } from './pdflib.mjs';
const cfg = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const raw = JSON.parse(fs.readFileSync(cfg.outDir + '/raw.json', 'utf8'));
const doc = await openPdf(cfg.pdf);
const S = 1.6;
const out = cfg.outDir + '/annot';
fs.mkdirSync(out, { recursive: true });
const a = +process.argv[3] || cfg.firstPage, b = +process.argv[4] || doc.numPages;
for (let pn = a; pn <= b; pn++) {
  const cv = await renderPage(doc, pn, S);
  const c = createCanvas(cv.width, cv.height); const g = c.getContext('2d');
  g.drawImage(cv, 0, 0);
  g.lineWidth = 1; g.font = '11px sans-serif';
  for (let v = 0; v <= 842; v += 25) {
    g.strokeStyle = v % 50 ? 'rgba(0,150,255,0.18)' : 'rgba(0,150,255,0.45)';
    g.beginPath(); g.moveTo(0, v * S); g.lineTo(c.width, v * S); g.stroke();
    g.beginPath(); g.moveTo(v * S, 0); g.lineTo(v * S, c.height); g.stroke();
    if (v % 50 === 0) { g.fillStyle = 'rgba(0,90,200,0.9)'; g.fillText(String(v), 2, v * S - 2); g.fillText(String(v), v * S + 2, 10); }
  }
  g.strokeStyle = 'red'; g.lineWidth = 2; g.fillStyle = 'red'; g.font = 'bold 13px sans-serif';
  for (const q of raw.questions) for (const f of [...q.figs, ...(q.shared?.figs || [])]) if (f.pn === pn) {
    g.strokeRect(f.x0 * S, f.y0 * S, (f.x1 - f.x0) * S, (f.y1 - f.y0) * S);
    g.fillText('Q' + q.num, f.x0 * S + 3, f.y0 * S + 14);
  }
  fs.writeFileSync(`${out}/p${String(pn).padStart(2, '0')}.png`, c.toBuffer('image/png'));
}
console.log('ok');
