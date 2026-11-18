// Biblioteca comum: carregar PDF, extrair linhas com coordenadas, renderizar regiões.
import { createCanvas, DOMMatrix, Path2D, ImageData } from '@napi-rs/canvas';
globalThis.DOMMatrix = DOMMatrix; globalThis.Path2D = Path2D; globalThis.ImageData = ImageData;
import * as pdfjs from 'pdfjs-dist/legacy/build/pdf.mjs';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const FONTS = path.join(HERE, 'node_modules/pdfjs-dist/standard_fonts/').replace(/\\/g, '/');
const CMAPS = path.join(HERE, 'node_modules/pdfjs-dist/cmaps/').replace(/\\/g, '/');

class CF {
  create(w, h) { const c = createCanvas(w, h); return { canvas: c, context: c.getContext('2d') }; }
  reset(cc, w, h) { cc.canvas.width = w; cc.canvas.height = h; }
  destroy(cc) { cc.canvas.width = 0; cc.canvas.height = 0; }
}

export async function openPdf(file) {
  return pdfjs.getDocument({
    data: new Uint8Array(fs.readFileSync(file)), useSystemFonts: false,
    canvasFactory: new CF(), standardFontDataUrl: FONTS, cMapUrl: CMAPS, cMapPacked: true,
  }).promise;
}

// Itens de texto em coordenadas de topo (y cresce para baixo), unidade = pt.
export async function pageItems(doc, pn) {
  const p = await doc.getPage(pn);
  const vp = p.getViewport({ scale: 1 });
  const tc = await p.getTextContent();
  // texto rotacionado (legendas verticais, rótulos de eixo) é ignorado: fica dentro das figuras recortadas
  const items = tc.items.filter(i => i.str && i.str.trim() !== '' && Math.abs(i.transform[1]) <= 0.01).map(i => {
    const fs_ = Math.hypot(i.transform[2], i.transform[3]);
    return { s: i.str, x: i.transform[4], y: vp.height - i.transform[5], w: i.width, h: fs_ || i.height, font: i.fontName };
  });
  return { W: vp.width, H: vp.height, items };
}

const SUP = { 'x': 'ˣ', 'T': 'ᵀ', '°': '°', '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹', '+': '⁺', '-': '⁻', '−': '⁻', '(': '⁽', ')': '⁾', 'n': 'ⁿ', '=': '⁼', 'i': 'ⁱ' };
const SUB = { '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄', '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉', '+': '₊', '-': '₋', '−': '₋', '(': '₍', ')': '₎', '=': '₌' };
// Converte para sobrescrito/subscrito Unicode quando todos os caracteres têm equivalente; senão marca com ^( ) / _( ).
export function toScript(s, kind) {
  const m = kind === 'sup' ? SUP : SUB;
  if ([...s].every(c => m[c])) return [...s].map(c => m[c]).join('');
  return (kind === 'sup' ? '^' : '_') + (s.length > 1 ? '(' + s + ')' : s);
}

// Agrupa itens em linhas (por coluna opcional).
export function toLines(items, tol = 2.5) {
  const s = [...items].sort((a, b) => a.y - b.y || a.x - b.x);
  const lines = [];
  for (const it of s) {
    const L = lines.find(l => Math.abs(l.y - it.y) <= tol && !(it.x > l.x1 + 60) && !(it.x + it.w < l.x0 - 60));
    if (L) { L.items.push(it); L.x0 = Math.min(L.x0, it.x); L.x1 = Math.max(L.x1, it.x + it.w); }
    else lines.push({ y: it.y, x0: it.x, x1: it.x + it.w, items: [it] });
  }
  // Índices: itens pequenos logo acima (sobrescrito) ou abaixo (subscrito) de uma linha de corpo maior.
  for (const l of lines) l.h = Math.max(...l.items.map(i => i.h));
  for (let i = lines.length - 1; i >= 0; i--) {
    const s = lines[i];
    if (s.items.length > 6) continue;
    const host = lines.find(L => L !== s && L.h - s.h >= 2 && s.x0 >= L.x0 - 2 && s.x1 <= L.x1 + 8 && L.items.length >= 1 &&
      ((s.y < L.y && L.y - s.y <= 5.5) || (s.y > L.y && s.y - L.y <= 4.5)) &&
      s.items.every(it => L.items.some(o => it.x >= o.x - 15 && it.x <= o.x + o.w + 15)));
    if (!host) continue;
    const kind = s.y < host.y ? 'sup' : 'sub';
    for (const it of s.items) host.items.push({ ...it, script: kind });
    lines.splice(i, 1);
  }
  // Índices na mesma linha (agrupados pela tolerância): item menor e deslocado em relação à linha de base.
  for (const l of lines) {
    const body = l.items.filter(i => !i.script);
    const H = Math.max(...body.map(i => i.h));
    const base = body.filter(i => i.h >= H - 0.3).map(i => i.y).sort((a, b) => a - b)[0];
    for (const it of body) {
      if (it.h > H * 0.8 || base === undefined || it.s.trim().length > 4) continue;
      if (it.y - base > 1) it.script = 'sub';
      else if (base - it.y > 1) it.script = 'sup';
    }
  }
  for (const l of lines) {
    l.items.sort((a, b) => a.x - b.x);
    let t = '';
    let prev = null;
    for (const it of l.items) {
      const s = it.script ? toScript(it.s.trim(), it.script) : it.s;
      if (prev && !(it.script && prev.script) && !(it.script === 'sup' && it.x - (prev.x + prev.w) < 1.2) && it.x - (prev.x + prev.w) > 1.2 && !t.endsWith(' ') && !s.startsWith(' ')) t += ' ';
      t += s; prev = it;
    }
    l.text = t.replace(/\s+/g, ' ').trim();
    l.h = Math.max(...l.items.map(i => i.h));
  }
  return lines.sort((a, b) => a.y - b.y || a.x0 - b.x0);
}

const pageCache = new Map();
export async function renderPage(doc, pn, scale) {
  const key = doc.fingerprints?.[0] + ':' + pn + ':' + scale;
  if (pageCache.has(key)) return pageCache.get(key);
  const p = await doc.getPage(pn);
  const vp = p.getViewport({ scale });
  const cc = new CF().create(Math.ceil(vp.width), Math.ceil(vp.height));
  cc.context.fillStyle = '#fff'; cc.context.fillRect(0, 0, cc.canvas.width, cc.canvas.height);
  // 1ª renderização carrega as fontes (evita glifos ausentes por condição de corrida do pdfjs); a 2ª é a definitiva
  await p.render({ canvasContext: cc.context, viewport: vp }).promise;
  cc.context.fillStyle = '#fff'; cc.context.fillRect(0, 0, cc.canvas.width, cc.canvas.height);
  await p.render({ canvasContext: cc.context, viewport: vp }).promise;
  if (pageCache.size > 6) pageCache.delete(pageCache.keys().next().value);
  pageCache.set(key, cc.canvas);
  return cc.canvas;
}

// rect em pt (topo-esquerda). Retorna canvas recortado.
export async function crop(doc, pn, r, scale) {
  const cv = await renderPage(doc, pn, scale);
  const x = Math.max(0, Math.floor(r.x0 * scale)), y = Math.max(0, Math.floor(r.y0 * scale));
  const w = Math.min(cv.width - x, Math.ceil((r.x1 - r.x0) * scale)), h = Math.min(cv.height - y, Math.ceil((r.y1 - r.y0) * scale));
  const c = createCanvas(w, h); c.getContext('2d').drawImage(cv, x, y, w, h, 0, 0, w, h);
  return c;
}

export { createCanvas, pdfjs };
