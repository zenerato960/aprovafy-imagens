import { openPdf } from './pdflib.mjs';
import { pageGraphics } from './graphics.mjs';
const [, , file, ...pgs] = process.argv;
const doc = await openPdf(file);
for (const pg of pgs) { const p = await doc.getPage(+pg); const g = await pageGraphics(p);
  console.log('== p'+pg, g.length);
  for (const b of g.filter(b=>(b.x1-b.x0)*(b.y1-b.y0)>4)) console.log(b.kind, b.fill?'F':'', [b.x0,b.y0,b.x1,b.y1].map(v=>v.toFixed(0)).join(','), 'n'+(b.n||''));
}
