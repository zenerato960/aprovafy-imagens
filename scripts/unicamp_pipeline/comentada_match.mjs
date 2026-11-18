// Prova Comentada sem cabeçalhos "Questão N" legíveis: segmenta o texto localizando, em ordem, o início do
// enunciado de cada questão (do draft.json) no texto da comentada.
// Uso: node comentada_match.mjs <config.json> <comentada.pdf> [pagIni]
import fs from 'fs';
import { openPdf, pageItems, toLines } from './pdflib.mjs';
const [, , cf, pdf, a] = process.argv;
const cfg = JSON.parse(fs.readFileSync(cf, 'utf8'));
const draft = JSON.parse(fs.readFileSync(cfg.outDir + '/draft.json', 'utf8'));
const doc = await openPdf(pdf);
let text = '';
for (let pn = +a || 1; pn <= doc.numPages; pn++) {
  const { items } = await pageItems(doc, pn);
  for (const l of toLines(items.filter(i => i.y > 60 && i.y < 815))) text += l.text + ' ';
}
// normalização com mapa de posições para recuperar o texto original
const norm = []; const pos = [];
for (let i = 0; i < text.length; i++) {
  const ch = text[i].normalize('NFKD').replace(/[̀-ͯ]/g, '').toLowerCase();
  if (/[a-z0-9]/.test(ch)) { norm.push(ch); pos.push(i); }
}
const N = norm.join('');
const key = s => s.normalize('NFKD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]/g, '');
const found = [];
let from = 0;
for (const d of draft) {
  // tenta vários trechos do enunciado (comentada pode reescrever o início)
  const paras = d.enunciado.split('\n').filter(p => key(p).length > 40 && !/^(obs|nas questoes|sempre que|texto comum|use o texto)/i.test(key(p)));
  let at = -1;
  for (const p of paras) {
    const k = key(p);
    for (const off of [0, Math.floor(k.length / 3)]) {
      const probe = k.slice(off, off + 45);
      const i = N.indexOf(probe, from);
      if (i >= 0 && (at < 0 || i < at)) { at = i - (off > 0 ? 0 : 0); break; }
    }
    if (at >= 0) break;
  }
  found.push({ num: d.num, at });
  if (at >= 0) from = at + 10;
}
const res = {};
for (let i = 0; i < found.length; i++) {
  const f = found[i]; if (f.at < 0) continue;
  const nx = found.slice(i + 1).find(x => x.at > f.at);
  const s = pos[f.at], e = nx ? pos[nx.at] : text.length;
  const body = text.slice(s, e).replace(/\s+/g, ' ');
  const alt = body.match(/alternativa correta (?:é|e) (?:a )?\(?([a-dA-D])\)?/i)
    || body.match(/alternativa \(?([a-dA-D])\)? (?:está|esta|é a) correta/i)
    || body.match(/alternativa que (?:contém|apresenta|indica)[^.]{0,60}?(?:é|e) a \(?([a-dA-D])\)?[ ,.;]/i)
    || body.match(/correta (?:é|e) a alternativa \(?([a-dA-D])\)?/i)
    || body.match(/resposta correta[^.]{0,30}?(?:é|e) a \(?([a-dA-D])\)?[ ,.;]/i) || body.match(/Alternativa [Cc]orreta:?\s*\(?([a-dA-D])\)?/) || body.match(/resposta correta (?:é|e) (?:a alternativa )?\(?([a-dA-D])\)?/i);
  const anul = /anulad/i.test(body);
  res[f.num] = { correta: alt ? alt[1].toUpperCase() : null, anulada_mencionada: anul, texto: body };
}
fs.writeFileSync(cfg.outDir + '/comentada.json', JSON.stringify(res, null, 1));
console.log('localizadas', Object.keys(res).length, '/', draft.length, '| sem local:', found.filter(f => f.at < 0).map(f => f.num).join(',') || '-', '| com letra:', Object.values(res).filter(r => r.correta).length);
