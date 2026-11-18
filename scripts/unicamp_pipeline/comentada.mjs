// Estrutura a "Prova Comentada" oficial da Comvest: texto por questão, alternativa correta, % de acerto.
// Uso: node comentada.mjs <pdf> <saida.json> [pagIni]
import fs from 'fs';
import { openPdf, pageItems, toLines } from './pdflib.mjs';
const [, , file, out, a, cols] = process.argv;
const doc = await openPdf(file);
let text = '';
for (let pn = +a || 4; pn <= doc.numPages; pn++) {
  const { W, items } = await pageItems(doc, pn);
  const body = items.filter(i => i.y > 60 && i.y < 815);
  for (const f of (cols === "1" ? [i => true] : [i => i.x < W / 2 - 2, i => i.x >= W / 2 - 2])) {
    for (const l of toLines(body.filter(f))) text += l.text + '\n';
  }
}
const parts = ('\n' + text).split(/\n(?=(?:QUESTÃO|Questão) \d+\n)/);
const res = {};
for (const p of parts) {
  const m = p.match(/^(?:QUESTÃO|Questão) (\d+)\n/);
  if (!m) continue;
  const n = +m[1];
  const body = p.slice(m[0].length);
  const alt = body.match(/Alternativa [Cc]orreta:?\s*\(?([a-dA-D])\)?/);
  // percentuais de acerto mencionados (ex.: "acerto de 45,3%" ou "45,30% dos candidatos")
  const pct = [...body.matchAll(/(\d{1,2}(?:,\d+)?)\s?%/g)].map(x => +x[1].replace(',', '.'));
  const nivel = body.match(/(muito fácil|fácil|média|médio|difícil|muito difícil)/gi);
  res[n] = { correta: alt ? alt[1].toUpperCase() : null, pcts: pct, niveis: nivel ? [...new Set(nivel.map(s => s.toLowerCase()))] : [], texto: body.replace(/\n/g, ' ').replace(/\s+/g, ' ') };
}
fs.writeFileSync(out, JSON.stringify(res, null, 1));
console.log('questoes', Object.keys(res).length, 'com alternativa', Object.values(res).filter(r => r.correta).length);
