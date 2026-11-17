// Lê gabarito oficial Comvest (grade "01 D 19 C ...") de uma página. Uso: node gabarito.mjs <pdf> <pag> <saida.json>
import fs from 'fs';
import { openPdf, pageItems, toLines } from './pdflib.mjs';
const [, , file, pg, out] = process.argv;
const doc = await openPdf(file);
const { items } = await pageItems(doc, +pg);
const lines = toLines(items, 2.5);
const head = lines.slice(0, 3).map(l => l.text).join(' | ');
const ans = {};
for (const l of lines) for (const m of l.text.matchAll(/\b(\d{2})\s+([A-D]|\*|ANULADA|Anulada)/g)) ans[+m[1]] = m[2].length === 1 ? m[2] : 'Anulado';
fs.writeFileSync(out, JSON.stringify({ fonte: file.split('/').pop(), pagina: +pg, cabecalho: head, respostas: ans }, null, 1));
console.log(head, '| total', Object.keys(ans).length);
