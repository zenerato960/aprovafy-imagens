const fs = require('fs');
const f = 'extract.mjs';
let s = fs.readFileSync(f, 'utf8');
const r = (a, b) => { if (!s.includes(a)) throw new Error('nf: ' + a.slice(0, 70)); s = s.replace(a, b); };
// 1) cabeçalho "O texto a seguir será usado para responder às questões N e M."
r('|O texto abaixo será utilizado nas questões|', '|O texto abaixo será utilizado nas questões|Os? textos? a seguir (será|serão) usados? para responder às questões|');
// 2) cabeçalho em 2 linhas só quando ainda não tem número de questão
r("(!/\\d/.test(cur.header) || (!/\\.$/.test(cur.header.trim()) && ln.text.length < 30))",
  "(!/quest(ões|ão)\\s+\\d/i.test(cur.header) || (!/[.:]$/.test(cur.header.trim()) && ln.text.length < 30))");
// 3) lista de questões do cabeçalho: só números ligados por vírgula/"e"/"a" logo após "questões"
r("b.qs = parseList(b.header.replace(/^.*?quest(ões|ão)/i, 'questões'));",
  "b.qs = parseList((b.header.match(/quest(?:ões|ão)\\s+(?:de\\s+)?[\\d\\s,ea]+?(?=[.:]|$)/i) || [''])[0]);");
// 4) hífen: listas explícitas de manter/juntar têm prioridade sobre a decisão automática
r("const joined = (cfg.dehyphen || []).includes(`${w1}-${w2}`) || (cfg.autoDehyphen && decideJoin(w1, w2));",
  "const joined = !(cfg.keepHyphen || []).includes(`${w1}-${w2}`) && ((cfg.dehyphen || []).includes(`${w1}-${w2}`) || (cfg.autoDehyphen && decideJoin(w1, w2)));");
fs.writeFileSync(f, s);
console.log('ok');
