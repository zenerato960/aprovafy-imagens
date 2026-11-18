const fs = require('fs');
const f = 'extract.mjs';
let s = fs.readFileSync(f, 'utf8');
const r = (a, b) => { if (!s.includes(a)) throw new Error('nf: ' + a.slice(0, 60)); s = s.replace(a, b); };
// cabeçalho de texto comum em 2 linhas: continua enquanto não terminar em "." e a linha seguinte for curta
r("if (cur && cur.type === 'S' && !/\\d/.test(cur.header) && !cur.lines.length) {",
  "if (cur && cur.type === 'S' && !cur.lines.length && (!/\\d/.test(cur.header) || (!/\\.$/.test(cur.header.trim()) && ln.text.length < 30))) {");
// números do cabeçalho: só os que vêm depois de "questões"
r("for (const b of blocks) if (b.type === 'S') b.qs = parseList(b.header);",
  "for (const b of blocks) if (b.type === 'S') b.qs = parseList(b.header.replace(/^.*?quest(ões|ão)/i, 'questões'));");
fs.writeFileSync(f, s);
console.log('ok');
