// Folhas de contato dos recortes para validação visual. Uso: node contact.mjs <dirImg> <dirSaida> [porFolha]
import fs from 'fs';
import { createCanvas, loadImage } from '@napi-rs/canvas';
const [, , dir, out, n] = process.argv;
const per = +n || 6, CW = 560, CH = 560;
fs.mkdirSync(out, { recursive: true });
const files = fs.readdirSync(dir).filter(f => f.endsWith('.png')).sort();
for (let s = 0; s * per < files.length; s++) {
  const batch = files.slice(s * per, s * per + per);
  const cols = 3, rows = Math.ceil(batch.length / cols);
  const c = createCanvas(cols * CW, rows * (CH + 24)); const g = c.getContext('2d');
  g.fillStyle = '#9aa'; g.fillRect(0, 0, c.width, c.height);
  for (let i = 0; i < batch.length; i++) {
    const img = await loadImage(fs.readFileSync(dir + '/' + batch[i]));
    const k = Math.min((CW - 16) / img.width, (CH - 16) / img.height);
    const w = img.width * k, h = img.height * k, x = (i % cols) * CW + 8, y = Math.floor(i / cols) * (CH + 24) + 24;
    g.fillStyle = '#000'; g.font = 'bold 16px sans-serif'; g.fillText(batch[i].replace(/^.*questao_/, 'Q') + `  ${img.width}x${img.height}`, x, y - 6);
    g.drawImage(img, x, y, w, h); g.strokeStyle = '#f0f'; g.lineWidth = 1; g.strokeRect(x - 0.5, y - 0.5, w + 1, h + 1);
  }
  fs.writeFileSync(`${out}/sheet_${s + 1}.png`, c.toBuffer('image/png'));
}
console.log('folhas', Math.ceil(files.length / per));
