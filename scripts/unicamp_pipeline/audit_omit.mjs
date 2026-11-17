// Auditoria de omissões: palavras do trecho da comentada que reproduz a questão (até "Alternativa Correta"/"Objetivo")
// que não aparecem na transcrição. Uso: node audit_omit.mjs <config.json>
import fs from 'fs';
const cfg = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const draft = JSON.parse(fs.readFileSync(cfg.outDir + '/draft.json', 'utf8'));
const com = JSON.parse(fs.readFileSync(cfg.outDir + '/comentada.json', 'utf8'));
const norm = s => s.normalize('NFKC').toLowerCase().replace(/[‐-―−–-]\s*/g, '').replace(/[“”"«»‘’']/g, '').replace(/[^\p{L}\p{N}\s]/gu, ' ').replace(/\s+/g, ' ').trim();
const out = {};
for (const d of draft) {
  const c = com[d.num]; if (!c) continue;
  const head = c.texto.split(/Alternativa [Cc]orreta|Objetivo da [Qq]uestão|Desempenho dos [Cc]andidatos|Comentários/)[0];
  const mine = norm(d.enunciado + ' ' + d.alternativas.join(' ')); const mineJ = mine.replace(/ /g, '');
  const miss = [...new Set(norm(head).split(' ').filter(w => w.length >= 4 && !/^\d+$/.test(w) && !mine.split(' ').includes(w) && !mineJ.includes(w)))];
  if (miss.length > 3) out[d.num] = miss.slice(0, 20);
}
for (const [n, m] of Object.entries(out)) console.log('Q' + n, m.join(', '));
console.log('questões com >3 palavras da comentada ausentes:', Object.keys(out).length);
