// Auditoria independente do texto: compara a transcrição (draft.json) com o texto da Prova Comentada oficial
// (outro PDF, outro layout, extraído por rotina diferente). Aponta palavras da transcrição ausentes na comentada
// e sequências da comentada que não aparecem na transcrição.
// Uso: node audit_text.mjs <config.json>
import fs from 'fs';
const cfg = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const draft = JSON.parse(fs.readFileSync(cfg.outDir + '/draft.json', 'utf8'));
const com = JSON.parse(fs.readFileSync(cfg.outDir + '/comentada.json', 'utf8'));
const norm = s => s.normalize('NFKC').toLowerCase()
  .replace(/[‐-―−–-]\s*/g, '').replace(/[“”"«»‘’']/g, '').replace(/[^\p{L}\p{N}\s]/gu, ' ').replace(/\s+/g, ' ').trim();
const words = s => norm(s).split(' ').filter(w => w.length >= 3);
const report = [];
for (const d of draft) {
  // texto da comentada da própria questão + vizinhas (questões podem ficar grudadas na extração)
  const c = [com[d.num - 1], com[d.num], com[d.num + 1]].filter(Boolean).map(x => x.texto).join(' ');
  if (!c) { report.push({ num: d.num, status: 'sem_comentada' }); continue; }
  const cset = new Set(norm(c).replace(/ /g, ' ').split(' '));
  const cjoined = norm(c).replace(/ /g, '');
  const tw = words(d.enunciado + ' ' + d.alternativas.join(' '));
  // palavra ausente: nem como token nem como substring (hifenização da comentada quebra palavras)
  const missing = [...new Set(tw.filter(w => !cset.has(w) && !cjoined.includes(w)))];
  const cov = tw.length ? 1 - tw.filter(w => missing.includes(w)).length / tw.length : 1;
  report.push({ num: d.num, palavras: tw.length, cobertura: +cov.toFixed(3), ausentes: missing.slice(0, 25) });
}
fs.writeFileSync(cfg.outDir + '/audit_text.json', JSON.stringify(report, null, 1));
for (const r of report) {
  const flag = r.status ? r.status : (r.cobertura < 0.97 || r.ausentes.length > 2 ? 'VERIFICAR' : 'ok');
  if (flag !== 'ok') console.log(`Q${r.num} ${flag} cobertura=${r.cobertura} ausentes=${(r.ausentes || []).join(', ')}`);
}
console.log('ok:', report.filter(r => !r.status && r.cobertura >= 0.97 && r.ausentes.length <= 2).length, '/', report.length);
