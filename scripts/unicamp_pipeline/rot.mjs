// Lista itens de texto rotacionados (vertical) por página. Uso: node rot.mjs <pdf>
import { openPdf } from './pdflib.mjs';
const doc = await openPdf(process.argv[2]);
for (let pn = 1; pn <= doc.numPages; pn++) {
  const p = await doc.getPage(pn); const vp = p.getViewport({ scale: 1 });
  const tc = await p.getTextContent();
  const rot = tc.items.filter(i => i.str.trim() && Math.abs(i.transform[1]) > 0.01);
  if (rot.length) console.log('p' + pn, rot.length, 'x≈' + Math.round(rot[0].transform[4]), 'y≈' + Math.round(vp.height - rot[0].transform[5]), '|', rot.map(i => i.str).join(' ').slice(0, 160));
}
