// Prova Comentada sem cabeçalhos legíveis ou de outra versão do caderno: localiza cada questão pela busca do seu
// enunciado em QUALQUER posição do texto da comentada, segmenta pelos inícios encontrados e traduz a
// "alternativa correta" da comentada para a letra do nosso caderno comparando o TEXTO das alternativas.
// Uso: node comentada_match.mjs <config.json> <comentada.pdf> [pagIni]
import fs from 'fs';
import { openPdf, pageItems, toLines } from './pdflib.mjs';
const [, , cf, pdf, a, cols] = process.argv;
const cfg = JSON.parse(fs.readFileSync(cf, 'utf8'));
const draft = JSON.parse(fs.readFileSync(cfg.outDir + '/draft.json', 'utf8'));
const doc = await openPdf(pdf);
let text = '';
for (let pn = +a || 1; pn <= doc.numPages; pn++) {
  const { items } = await pageItems(doc, pn);
  const { W } = await pageItems(doc, pn);
  const fs2 = cols === '2' ? [i => i.x < W / 2 - 2, i => i.x >= W / 2 - 2] : [i => true];
  for (const fl of fs2) for (const l of toLines(items.filter(i => i.y > 40 && i.y < 815 && fl(i)))) text += l.text + ' ';
}
const norm = [], pos = [];
for (let i = 0; i < text.length; i++) {
  const ch = text[i].normalize('NFKD').replace(/[̀-ͯ]/g, '').toLowerCase();
  if (/[a-z0-9]/.test(ch)) { norm.push(ch); pos.push(i); }
}
const N = norm.join('');
const key = s => s.normalize('NFKD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]/g, '');
const found = [];
for (const d of draft) {
  const paras = d.enunciado.split('\n').filter(p => key(p).length > 40 && !/^(obs|nasquestoes|semprequenecessario|textocomum|useotexto|useostextos|dados)/.test(key(p)));
  let at = -1;
  for (const p of paras) {
    const k = key(p);
    for (const off of [0, Math.floor(k.length / 3), Math.floor(k.length / 2)]) {
      const probe = k.slice(off, off + 45);
      if (probe.length < 30) continue;
      const i = N.indexOf(probe);
      if (i >= 0 && N.indexOf(probe, i + 1) < 0) { at = i; break; } // ocorrência única
    }
    if (at >= 0) break;
  }
  found.push({ num: d.num, at });
}
const ordered = found.filter(f => f.at >= 0).sort((x, y) => x.at - y.at);
const res = {};
for (let i = 0; i < ordered.length; i++) {
  const f = ordered[i];
  const s = pos[f.at], e = i + 1 < ordered.length ? pos[ordered[i + 1].at] : text.length;
  const body = text.slice(s, e).replace(/\s+/g, ' ');
  const alt = body.match(/Alternativa [Cc]orreta:?\s*\(?([a-dA-D])\)?/) || body.match(/alternativa correta (?:é|e) (?:a )?\(?([a-dA-D])\)?/i)
    || body.match(/alternativa \(?([a-dA-D])\)? (?:está|esta|é a) correta/i) || body.match(/resposta correta[^.]{0,30}?(?:é|e) a \(?([a-dA-D])\)?[ ,.;]/i);
  const letraCom = alt ? alt[1].toUpperCase() : null;
  // texto da alternativa indicada, na comentada: trecho após "x) " na reprodução da questão
  let correta = null, textoCom = null;
  if (letraCom) {
    const lc = letraCom.toLowerCase();
    const m = body.match(new RegExp('(?:^|\\s)' + lc + '\\)\\s+(.{20,220}?)(?=\\s[a-d]\\)\\s|Objetivo|Alternativa|$)'));
    if (m) {
      textoCom = m[1];
      const d = draft.find(x => x.num === f.num);
      // similaridade por sequência: maior prefixo comum (texto sem hifenização de linha) entre a alternativa da
      // comentada e cada alternativa do caderno; exige vencedor único
      const kc = key(textoCom.replace(/(\p{L})- (\p{L})/gu, '$1$2'));
      const lcp = (x, y) => { let i = 0; while (i < x.length && i < y.length && x[i] === y[i]) i++; return i; };
      const sc = d.alternativas.map(x => { const k = key(x); return lcp(k, kc) / Math.max(1, Math.min(k.length, kc.length)); });
      const best = Math.max(...sc), idx = sc.indexOf(best);
      if (best >= 0.9 && sc.filter(v => v === best).length === 1) correta = 'ABCD'[idx];
    }
  }
  res[f.num] = { correta, letra_na_comentada: letraCom, texto_alternativa_comentada: textoCom, anulada_mencionada: /anulad/i.test(body), texto: body };
}
fs.writeFileSync(cfg.outDir + '/comentada.json', JSON.stringify(res, null, 1));
console.log('localizadas', Object.keys(res).length, '/', draft.length, '| sem local:', found.filter(f => f.at < 0).map(f => f.num).join(',') || '-',
  '| letra traduzida pelo texto:', Object.values(res).filter(r => r.correta).length, '| letra sem tradução:', Object.entries(res).filter(([k, r]) => r.letra_na_comentada && !r.correta).map(([k]) => k).join(',') || '-');
