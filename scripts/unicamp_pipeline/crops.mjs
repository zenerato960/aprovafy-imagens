// Gera as imagens finais das questões a partir das caixas revisadas (draft.json) + imagens de auditoria.
// Uso: node crops.mjs <config.json>
// Saída: <outDir>/img/<prefixo>_questao_NNN.png    (imagem publicada)
//        <outDir>/audit/q_NNN.png                  (auditoria: página com a caixa marcada | recorte)
//        <outDir>/crops_manifest.json              (questão, página, caixas, tamanho, hash)
import fs from 'fs';
import crypto from 'crypto';
import { openPdf, crop, renderPage, createCanvas } from './pdflib.mjs';
const cfg = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const draft = JSON.parse(fs.readFileSync(cfg.outDir + '/draft.json', 'utf8'));
const doc = await openPdf(cfg.pdf);
const S = cfg.cropScale || 3; // 3 × 72 = 216 dpi
const GAP = Math.round(6 * S);
fs.mkdirSync(cfg.outDir + '/img', { recursive: true });
fs.mkdirSync(cfg.outDir + '/audit', { recursive: true });
for (const f of fs.readdirSync(cfg.outDir + '/img')) fs.unlinkSync(cfg.outDir + '/img/' + f);

const manifest = [];
for (const d of draft) {
  if (!d.crops.length) continue;
  const pieces = [];
  for (const [pn, x0, y0, x1, y1] of d.crops) pieces.push(await crop(doc, pn, { x0, y0, x1, y1 }, S));
  let W, H, place;
  if (d.cropLayout === 'grid' && pieces.length === 4) {
    const cw = [Math.max(pieces[0].width, pieces[2].width), Math.max(pieces[1].width, pieces[3].width)];
    const rh = [Math.max(pieces[0].height, pieces[1].height), Math.max(pieces[2].height, pieces[3].height)];
    W = cw[0] + cw[1] + GAP; H = rh[0] + rh[1] + GAP;
    place = [[0, 0], [cw[0] + GAP, 0], [0, rh[0] + GAP], [cw[0] + GAP, rh[0] + GAP]];
  } else if (d.cropLayout === 'row') {
    W = pieces.reduce((s, c) => s + c.width, 0) + GAP * (pieces.length - 1); H = Math.max(...pieces.map(c => c.height));
    let x = 0; place = pieces.map(c => { const p = [x, 0]; x += c.width + GAP; return p; });
  } else {
    W = Math.max(...pieces.map(c => c.width)); H = pieces.reduce((s, c) => s + c.height, 0) + GAP * (pieces.length - 1);
    let y = 0; place = pieces.map(c => { const p = [Math.round((W - c.width) / 2), y]; y += c.height + GAP; return p; });
  }
  const out = createCanvas(W, H); const g = out.getContext('2d');
  g.fillStyle = '#fff'; g.fillRect(0, 0, W, H);
  pieces.forEach((c, i) => g.drawImage(c, place[i][0], place[i][1]));
  const name = `${cfg.imgPrefix}_questao_${String(d.num).padStart(3, '0')}.png`;
  const buf = out.toBuffer('image/png');
  fs.writeFileSync(`${cfg.outDir}/img/${name}`, buf);
  manifest.push({ num: d.num, arquivo: name, largura: W, altura: H, bytes: buf.length, sha256: crypto.createHash('sha256').update(buf).digest('hex'), caixas: d.crops, layout: d.cropLayout });

  // auditoria: miniatura da(s) página(s) com caixas em vermelho ao lado do recorte
  const pages = [...new Set(d.crops.map(c => c[0]))];
  const thumbs = [];
  for (const pn of pages) {
    const pg = await renderPage(doc, pn, 1);
    const t = createCanvas(pg.width, pg.height); const tg = t.getContext('2d');
    tg.drawImage(pg, 0, 0); tg.strokeStyle = 'red'; tg.lineWidth = 2;
    for (const [p, x0, y0, x1, y1] of d.crops) if (p === pn) tg.strokeRect(x0, y0, x1 - x0, y1 - y0);
    tg.fillStyle = 'red'; tg.font = 'bold 14px sans-serif'; tg.fillText(`Q${d.num} p${pn}`, 8, 18);
    thumbs.push(t);
  }
  const sc = Math.min(1, 842 / H);
  const AW = thumbs.reduce((s, t) => s + t.width, 0) + Math.round(W * sc) + 20, AH = Math.max(842, Math.round(H * sc));
  const a = createCanvas(AW, AH); const ag = a.getContext('2d'); ag.fillStyle = '#ddd'; ag.fillRect(0, 0, AW, AH);
  let x = 0; for (const t of thumbs) { ag.drawImage(t, x, 0); x += t.width; }
  ag.drawImage(out, x + 20, 0, Math.round(W * sc), Math.round(H * sc));
  fs.writeFileSync(`${cfg.outDir}/audit/q_${String(d.num).padStart(3, '0')}.png`, a.toBuffer('image/png'));
}
fs.writeFileSync(cfg.outDir + '/crops_manifest.json', JSON.stringify(manifest, null, 1));
console.log('imagens', manifest.length, 'total KB', Math.round(manifest.reduce((s, m) => s + m.bytes, 0) / 1024));
