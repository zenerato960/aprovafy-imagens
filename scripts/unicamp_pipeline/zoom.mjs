// Uso: node zoom.mjs <pdf> <pag> x0 y0 x1 y1 <saida.png> [escala]
import fs from 'fs';
import { openPdf, crop } from './pdflib.mjs';
const [, , f, pn, x0, y0, x1, y1, out, sc] = process.argv;
const doc = await openPdf(f);
const c = await crop(doc, +pn, { x0: +x0, y0: +y0, x1: +x1, y1: +y1 }, +sc || 4);
fs.writeFileSync(out, c.toBuffer('image/png'));
