// Caixas (pt, topo-esquerda) de imagens raster e caminhos vetoriais de uma página.
import { pdfjs } from './pdflib.mjs';
const OPS = pdfjs.OPS;
const mul = (m, n) => [m[0] * n[0] + m[2] * n[1], m[1] * n[0] + m[3] * n[1], m[0] * n[2] + m[2] * n[3], m[1] * n[2] + m[3] * n[3], m[0] * n[4] + m[2] * n[5] + m[4], m[1] * n[4] + m[3] * n[5] + m[5]];
const ap = (m, x, y) => [m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5]];

export async function pageGraphics(page) {
  const H = page.getViewport({ scale: 1 }).height;
  const ol = await page.getOperatorList();
  let ctm = [1, 0, 0, 1, 0, 0];
  const stack = [];
  const out = [];
  const imgOps = new Set([OPS.paintImageXObject, OPS.paintInlineImageXObject, OPS.paintImageMaskXObject, OPS.paintJpegXObject, OPS.paintImageXObjectRepeat, OPS.paintInlineImageXObjectGroup, OPS.paintImageMaskXObjectGroup].filter(x => x !== undefined));
  const box = (pts, kind, extra = {}) => {
    const xs = pts.map(p => p[0]), ys = pts.map(p => p[1]);
    out.push({ kind, x0: Math.min(...xs), x1: Math.max(...xs), y0: H - Math.max(...ys), y1: H - Math.min(...ys), ...extra });
  };
  let pending = null; // caminho construído aguardando operador de pintura
  for (let i = 0; i < ol.fnArray.length; i++) {
    const fn = ol.fnArray[i], args = ol.argsArray[i];
    if (fn === OPS.save) stack.push(ctm.slice());
    else if (fn === OPS.restore) { const s = stack.pop(); if (s) ctm = s; }
    else if (fn === OPS.transform) ctm = mul(ctm, args);
    else if (fn === OPS.paintFormXObjectBegin) { stack.push(ctm.slice()); if (args[0]) ctm = mul(ctm, args[0]); }
    else if (fn === OPS.paintFormXObjectEnd) { const s = stack.pop(); if (s) ctm = s; }
    else if (imgOps.has(fn)) box([[0, 0], [1, 0], [0, 1], [1, 1]].map(p => ap(ctm, p[0], p[1])), 'img');
    else if (fn === OPS.constructPath) {
      const mm = args[2];
      if (mm && mm.length === 4 && isFinite(mm[0])) {
        const pts = [[mm[0], mm[1]], [mm[2], mm[1]], [mm[0], mm[3]], [mm[2], mm[3]]].map(p => ap(ctm, p[0], p[1]));
        pending = { pts, nops: args[0].length };
      }
    } else if (pending && [OPS.stroke, OPS.closeStroke, OPS.fill, OPS.eoFill, OPS.fillStroke, OPS.eoFillStroke, OPS.closeFillStroke, OPS.closeEOFillStroke].includes(fn)) {
      const fill = [OPS.fill, OPS.eoFill].includes(fn);
      box(pending.pts, 'path', { n: pending.nops, fill });
      pending = null;
    } else if (fn === OPS.endPath) pending = null;
  }
  return out;
}
