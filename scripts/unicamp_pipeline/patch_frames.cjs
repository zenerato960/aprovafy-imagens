const fs = require('fs');
let s = fs.readFileSync('extract.mjs', 'utf8');
const a = '  figsByPage[pn] = figs;';
if (!s.includes(a)) throw new Error('nf');
// molduras de texto (caixas que só emolduram texto transcrito, ex.: citações destacadas) não são figuras:
// cfg.textFrames = [[pn, x, y], ...] remove a figura candidata que contém o ponto (x, y).
s = s.replace(a, `  for (const [fp, fx, fy] of cfg.textFrames || []) if (fp === pn) for (let k = figs.length - 1; k >= 0; k--) { const F = figs[k]; if (fx >= F.x0 && fx <= F.x1 && fy >= F.y0 && fy <= F.y1) figs.splice(k, 1); }
` + a);
fs.writeFileSync('extract.mjs', s);
console.log('ok');
