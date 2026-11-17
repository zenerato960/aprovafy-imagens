// Prepara pacotes de entrada para redação de explicações/classificação (por faixa de questões).
// Uso: node pack.mjs <config.json> <ini> <fim> <saida.json>
import fs from 'fs';
import path from 'path';
const [, , cf, a, b, outFile] = process.argv;
const cfg = JSON.parse(fs.readFileSync(cf, 'utf8'));
const d = JSON.parse(fs.readFileSync(cfg.outDir + '/draft.json', 'utf8'));
const g = JSON.parse(fs.readFileSync(cfg.outDir + '/gabarito.json', 'utf8')).respostas;
const c = JSON.parse(fs.readFileSync(cfg.outDir + '/comentada.json', 'utf8'));
const m = JSON.parse(fs.readFileSync(cfg.outDir + '/crops_manifest.json', 'utf8'));
const imgDir = path.resolve(cfg.outDir, 'img').replace(/\\/g, '/');
const pack = d.filter(q => q.num >= +a && q.num <= +b).map(q => {
  const im = m.find(x => x.num === q.num);
  const com = c[q.num] ? c[q.num].texto : (c[q.num - 1] ? '[comentada desta questão ficou junto da anterior]: ' + c[q.num - 1].texto : '');
  return { num: q.num, enunciado: q.enunciado, alternativas: q.alternativas, gabarito_oficial: g[q.num], imagem: im ? `${imgDir}/${im.arquivo}` : '', observacao_revisao: q.obs, comentada_oficial: com };
});
fs.writeFileSync(outFile, JSON.stringify(pack, null, 1));
console.log(outFile, pack.length);
