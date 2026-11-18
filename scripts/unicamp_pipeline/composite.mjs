// Junta várias regiões (pdf, pág, caixa) numa única imagem para conferência. Uso: node composite.mjs <saida.png> <escala> "pdf|pg|x0|y0|x1|y1" ...
import fs from 'fs';
import { openPdf, crop, createCanvas } from './pdflib.mjs';
const [, , out, sc, ...specs] = process.argv;
const pieces = [];
const docs = {};
for (const s of specs) { const [f, pg, x0, y0, x1, y1] = s.split('|'); docs[f] ||= await openPdf(f); pieces.push(await crop(docs[f], +pg, { x0: +x0, y0: +y0, x1: +x1, y1: +y1 }, +sc)); }
const W = Math.max(...pieces.map(p => p.width)), H = pieces.reduce((a, p) => a + p.height + 10, 0);
const c = createCanvas(W, H); const g = c.getContext('2d'); g.fillStyle = '#888'; g.fillRect(0, 0, W, H);
let y = 0; for (const p of pieces) { g.drawImage(p, 0, y); y += p.height + 10; }
fs.writeFileSync(out, c.toBuffer('image/png')); console.log(W, H);
