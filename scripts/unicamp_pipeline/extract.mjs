// Extrator por coordenadas para provas Comvest/UNICAMP (2 colunas, cabeçalho "QUESTÃO N").
// Uso: node extract.mjs <config.json>
// Saída: <outDir>/raw.json  questões com segmentos de página, parágrafos, alternativas e figuras candidatas
//        <outDir>/raw.txt   texto para revisão humana
// Regras: figuras = agrupamentos de objetos gráficos (raster + vetoriais) por coluna; o texto dentro de uma
// figura (rótulos de gráficos/tabelas) NÃO entra no enunciado, pois aparece na imagem recortada.
import fs from 'fs';
import { openPdf, pageItems, toLines } from './pdflib.mjs';
import { pageGraphics } from './graphics.mjs';

const cfg = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const doc = await openPdf(cfg.pdf);
const TOP = cfg.top ?? 78, BOTTOM = cfg.bottom ?? 805;
const MATH = cfg.mathMap || {};
const QHEAD = /^QUESTÃO\s+(\d+)$/;
const SHARED = /^(Textos? comu(m|ns) (às|para|para as) questões|Leia os? textos? a seguir e responda às questões|O texto abaixo será utilizado nas questões|Os textos abaixo serão utilizados nas questões|USE OS? TEXTOS?\b)/i;
const NOTE = { test: t => /^(Obs\.?:|Nas questões de \d+ a \d+)/i.test(t) || /^Sempre que necessário,? (aproxime|use)/.test(t) };

// Letras matemáticas (𝑎, ℎ, 𝜃...) viram letras comuns; símbolos de fonte Symbol via mapa da prova.
const mapChars = s => [...s].map(c => {
  if (MATH[c] !== undefined) return MATH[c];
  const cp = c.codePointAt(0);
  if ((cp >= 0x1D400 && cp <= 0x1D7FF) || cp === 0x210E) return c.normalize('NFKC');
  return c;
}).join('');
// Glifos suspeitos: blocos índicos/etíopes (Cambria Math com ToUnicode quebrado) e área de uso privado.
const isWeird = c => { const cp = c.codePointAt(0); return (cp >= 0x0900 && cp <= 0x0DFF) || (cp >= 0x1200 && cp <= 0x13FF) || (cp >= 0xE000 && cp <= 0xF8FF) || cp === 0xFFFD; };

function cluster(boxes, gap) {
  const cl = boxes.map(b => ({ ...b, n: 1 }));
  let merged = true;
  while (merged) {
    merged = false;
    for (let i = 0; i < cl.length; i++) for (let j = i + 1; j < cl.length; j++) {
      const a = cl[i], b = cl[j];
      if (b.x0 < a.x1 + gap && b.x1 > a.x0 - gap && b.y0 < a.y1 + gap && b.y1 > a.y0 - gap) {
        a.x0 = Math.min(a.x0, b.x0); a.x1 = Math.max(a.x1, b.x1); a.y0 = Math.min(a.y0, b.y0); a.y1 = Math.max(a.y1, b.y1); a.n += b.n;
        cl.splice(j, 1); merged = true; j--;
      }
    }
  }
  return cl;
}

const stream = [];       // linhas na ordem de leitura
const figsByPage = {};   // figuras candidatas por página
for (let pn = cfg.firstPage; pn <= (cfg.lastPage || doc.numPages); pn++) {
  const { W, items } = await pageItems(doc, pn);
  const mid = W / 2;
  const gr = (await pageGraphics(await doc.getPage(pn))).filter(g => {
    const w = g.x1 - g.x0, h = g.y1 - g.y0;
    // só descarta o que está inteiramente no cabeçalho/rodapé; figuras que invadem as margens são mantidas
    if (g.y1 <= TOP || g.y0 >= BOTTOM) return false;
    if (g.kind === 'path' && g.fill && h < 15 && w > 200) return false; // barra cinza "QUESTÃO N"
    if (w < 3 && h > 500) return false;                               // fio separador de colunas
    if (w < 3 && h < 3) return false;
    if (h < 1.6 && w < 60) return false;                              // traço de fração/raiz
    return w * h > 2 || w > 20 || h > 20;
  });
  const figs = [];
  for (const col of [0, 1]) {
    const inCol = gr.filter(g => (col === 0 ? (g.x0 + g.x1) / 2 < mid : (g.x0 + g.x1) / 2 >= mid));
    figs.push(...cluster(inCol, 8).filter(c => (c.x1 - c.x0) > 15 && (c.y1 - c.y0) > 12).map(c => ({ pn, col, x0: c.x0, y0: c.y0, x1: c.x1, y1: c.y1, n: c.n })));
  }
  figsByPage[pn] = figs;
  const body = items.filter(i => i.y > TOP && i.y < BOTTOM).map(i => ({ ...i, s: mapChars(i.s) }));
  for (const [col, f] of [[0, i => i.x < mid - 4], [1, i => i.x >= mid - 4]]) {
    for (const l of toLines(body.filter(f))) {
      const fig = figs.find(F => F.col === col && l.x0 >= F.x0 - 3 && l.x1 <= F.x1 + 3 && l.y - l.h * 0.7 >= F.y0 - 3 && l.y <= F.y1 + 3);
      const rec = { pn, col, y: l.y, x0: l.x0, x1: l.x1, h: l.h, text: l.text, fonts: [...new Set(l.items.map(i => i.font))] };
      if (fig) { (fig.text ||= []).push(l.text); continue; }
      stream.push(rec);
    }
  }
}

const parseList = t => {
  const m = t.match(/quest(?:ões|ão)\s+(?:de\s+)?(\d+)\s*(?:a|até)\s*(\d+)/i);
  if (m) { const a = []; for (let k = +m[1]; k <= +m[2]; k++) a.push(k); return a; }
  return [...t.matchAll(/(\d+)/g)].map(x => +x[1]);
};

// Segmentação em blocos: questão, texto comum, observação.
const blocks = [];
let cur = null;
for (const ln of stream) {
  let m;
  if ((m = ln.text.match(QHEAD))) { cur = { type: 'Q', num: +m[1], head: ln, lines: [] }; blocks.push(cur); continue; }
  if (cur && cur.type === 'S' && !/\d/.test(cur.header) && !cur.lines.length) { cur.header += ' ' + ln.text; continue; } // cabeçalho em 2 linhas
  if (SHARED.test(ln.text)) { cur = { type: 'S', header: ln.text, head: ln, lines: [] }; blocks.push(cur); continue; }
  if (NOTE.test(ln.text)) { cur = { type: 'N', header: ln.text, head: ln, lines: [] }; blocks.push(cur); continue; }
  if (cur && cur.type === 'N' && (ln.pn !== cur.head.pn || ln.col !== cur.head.col || ln.y - (cur.lines.at(-1)?.y ?? cur.head.y) > 13)) {
    // observação terminou; linha órfã pertence ao bloco anterior não-observação
    cur = blocks.filter(b => b.type !== 'N').at(-1);
  }
  if (cur) cur.lines.push(ln);
}
for (const b of blocks) if (b.type === 'N') { b.text = [b.header, ...b.lines.map(l => l.text)].join(' ').replace(/\s+/g, ' '); b.qs = /quest/i.test(b.text) ? parseList(b.text) : []; for (const [re, qs] of cfg.noteQs || []) if (new RegExp(re).test(b.text)) b.qs = qs; }
for (const b of blocks) if (b.type === 'S') b.qs = parseList(b.header);

function paragraphs(lines) {
  const paras = [];
  let p = null, prev = null;
  for (const ln of lines) {
    const gap = prev && prev.pn === ln.pn && prev.col === ln.col ? ln.y - prev.y : null;
    const small = ln.h < 7.5;
    const colRight = cfg.colRight[ln.col];
    const shortPrev = prev && !small && prev.x1 < cfg.colRight[prev.col] - 45;          // linha anterior curta = fim de parágrafo/verso
    const colJump = prev && gap === null && /[.:?!”"]$/.test(prev.text);               // mudança de coluna após fim de frase
    // travessão inicia parágrafo (fala de diálogo) só se a linha anterior terminou a frase
    const dashStart = /^[–—-]\s/.test(ln.text) && (!prev || /[.:?!”"…]$/.test(prev.text));
    const starts = dashStart || /^(\[\d+\]|Texto [IVX]+\b)/.test(ln.text) || /^Texto [IVX]+$/.test(prev?.text || '');
    const newPara = !p || (gap !== null && gap > Math.max(prev.h, ln.h) * 1.55) || (prev && (prev.h < 7.5) !== small) || shortPrev || colJump || starts;
    if (newPara) { p = { lines: [ln], small }; paras.push(p); } else p.lines.push(ln);
    prev = ln;
  }
  return paras.map(p => {
    let t = '';
    const hy = [];
    for (const ln of p.lines) {
      if (!t) t = ln.text;
      else if (/[A-Za-zÀ-ÿ]-$/.test(t) && /^[a-zà-ÿ]/.test(ln.text)) {
        // hífen em fim de linha: mantido (compostos reais), salvo se a junção constar da lista de quebras silábicas da prova
        const w1 = t.match(/([A-Za-zÀ-ÿ]+)-$/)[1]; const w2 = ln.text.match(/^([a-zà-ÿ]+)/)[1];
        const joined = (cfg.dehyphen || []).includes(`${w1}-${w2}`);
        hy.push(`${w1}-${w2}${joined ? '→' + w1 + w2 : ''}`);
        t = joined ? t.slice(0, -1) + ln.text : t + ln.text;
      }
      else if (/(https?:\/\/|www\.)\S*$/.test(t) && !/[.)]$/.test(t) && !/^(Acess|Adaptad|Dispon)/.test(ln.text)) t += ln.text; // URL quebrada
      else if (/\d\/$/.test(t)) t += ln.text; // data quebrada
      else t += ' ' + ln.text;
    }
    t = t.replace(/(\d+) (\d+)⁄/g, '$1/$2'); // frações do Word: "2 3⁄" = 2/3
    return { text: t.replace(/\s+/g, ' ').trim(), small: p.small, hyphen: hy, pn: p.lines[0].pn, col: p.lines[0].col, y0: p.lines[0].y, y1: p.lines.at(-1).y,
      // caixa de cada linha (para descartar texto que fica dentro de um recorte de figura)
      boxes: p.lines.map(l => [l.pn, l.x0, l.y - l.h, l.x1, l.y, l.text]) };
  });
}

const segsOf = lines => {
  const segs = {};
  for (const ln of lines) {
    const k = ln.pn + ':' + ln.col;
    const s = (segs[k] ||= { pn: ln.pn, col: ln.col, y0: ln.y - ln.h, y1: ln.y + 2 });
    s.y0 = Math.min(s.y0, ln.y - ln.h); s.y1 = Math.max(s.y1, ln.y + 2);
  }
  return Object.values(segs);
};

// Região de um bloco em cada coluna/página que ocupa: do seu cabeçalho (ou topo) até o próximo cabeçalho.
const heads = blocks.map(b => b.head);
function regionsOf(b) {
  const regs = [];
  const pcs = new Map();
  pcs.set(b.head.pn + ':' + b.head.col, { pn: b.head.pn, col: b.head.col, y0: b.head.y });
  for (const ln of b.lines) { const k = ln.pn + ':' + ln.col; if (!pcs.has(k)) pcs.set(k, { pn: ln.pn, col: ln.col, y0: TOP }); }
  // continuação de coluna sem texto (só figura): incluir coluna seguinte se ela começa sem cabeçalho
  for (const r of pcs.values()) {
    const nh = heads.filter(h => h.pn === r.pn && h.col === r.col && h.y > r.y0 + 1).sort((a, c) => a.y - c.y)[0];
    regs.push({ ...r, y1: nh ? nh.y - 12 : BOTTOM });
  }
  return regs;
}
const figsIn = regs => regs.flatMap(r => figsByPage[r.pn].filter(F => F.col === r.col && (F.y0 + F.y1) / 2 > r.y0 && (F.y0 + F.y1) / 2 < r.y1));

const ALT = /^([a-d])\)\s*(.*)$/;
const result = [];
for (const b of blocks.filter(b => b.type === 'Q')) {
  const colX = c => cfg.colX[c];
  const stem = [], alts = { a: [], b: [], c: [], d: [] };
  let curAlt = null;
  const used = new Set(), markers = [];
  // alternativas em grade (a c / b d): divide linhas como "a) 1,25. c) 3,20." em duas
  const lines = b.lines.flatMap(ln => {
    if (!ALT.test(ln.text)) return [ln];
    const parts = ln.text.split(/\s+(?=[b-d]\)\s)/);
    if (parts.length === 1) return [ln];
    const w = (ln.x1 - ln.x0) / ln.text.length;
    let off = 0;
    return parts.map(t => { const x0 = ln.x0 + off * w; off += t.length + 1; return { ...ln, text: t, x0 }; });
  });
  for (const ln of lines) {
    const m = ln.text.match(ALT);
    const atMargin = Math.abs(ln.x0 - colX(ln.col)) < 6;
    const ok = m && !used.has(m[1]) && (m[1] === 'a' ? atMargin : used.size > 0);
    if (ok) {
      curAlt = m[1]; used.add(curAlt); markers.push({ k: curAlt, x0: ln.x0, pn: ln.pn, col: ln.col });
      alts[curAlt].push({ ...ln, text: m[2] }); continue;
    }
    if (curAlt) {
      // continuação: alternativa cujo marcador está mais próximo à esquerda na mesma coluna
      // Grade (a c / b d) só quando há marcadores lado a lado (x distantes > 80 pt) na mesma coluna;
      // nesse caso a continuação vai para o marcador mais próximo à esquerda. Caso contrário, alternativas
      // empilhadas: vale a mais recente (mesmo que o rótulo esteja recuado, como "  a)").
      const same = markers.filter(mk => mk.pn === ln.pn && mk.col === ln.col);
      const grid = same.some(p => same.some(q => Math.abs(p.x0 - q.x0) > 80));
      let cand = null;
      if (grid) for (const mk of same) if (mk.x0 <= ln.x0 + 25 && (!cand || mk.x0 >= cand.x0 - 2)) cand = mk;
      alts[cand ? cand.k : curAlt].push(ln);
    } else stem.push(ln);
  }
  const sh = blocks.find(s => s.type === 'S' && s.qs.includes(b.num));
  const regs = regionsOf(b);
  // Material impresso depois da última alternativa (dados, glossário, fontes) não pertence a ela:
  // vai para "posAlternativas" (exibido ao fim do enunciado). Critério: parágrafos seguintes ao 1º da alternativa d,
  // e, dentro do 1º, o trecho a partir de "Dados:"/"Dado:".
  const lastK = ['d', 'c', 'b', 'a'].find(k => alts[k].length);
  const altParas = Object.fromEntries(Object.entries(alts).map(([k, v]) => [k, paragraphs(v)]));
  const posAlt = [];
  if (lastK && altParas[lastK].length) {
    const [first, ...rest] = altParas[lastK];
    posAlt.push(...rest.map(p => p.text));
    const m = first.text.match(/^(.*?[.)”"])\s+(Dados?:.*)$/);
    if (m) { first.text = m[1]; posAlt.unshift(m[2]); }
    altParas[lastK] = [first];
  }
  result.push({
    num: b.num,
    notes: blocks.filter(n => n.type === 'N' && n.qs.includes(b.num)).map(n => n.text),
    shared: sh ? { header: sh.header, paras: paragraphs(sh.lines), figs: figsIn(regionsOf(sh)) } : null,
    stem: paragraphs(stem),
    posAlternativas: posAlt,
    alts: Object.fromEntries(Object.entries(altParas).map(([k, ps]) => [k, ps.map(p => p.text).join('\n')])),
    altPos: Object.fromEntries(Object.entries(alts).map(([k, v]) => [k, v.length ? { pn: v[0].pn, col: v[0].col, y: v[0].y } : null])),
    segs: segsOf([b.head, ...b.lines]),
    regions: regs,
    figs: figsIn(regs),
    weird: [...new Set(b.lines.flatMap(l => [...l.text].filter(isWeird)))],
  });
}

fs.mkdirSync(cfg.outDir, { recursive: true });
fs.writeFileSync(cfg.outDir + '/raw.json', JSON.stringify({ source: cfg.pdf, questions: result }, null, 1));
const fb = f => `p${f.pn}[${[f.x0, f.y0, f.x1, f.y1].map(v => v.toFixed(0))}]`;
let txt = '';
for (const r of result) {
  txt += `\n##### Q${r.num}  segs=${r.segs.map(s => `p${s.pn}c${s.col}`).join(',')} figs=${r.figs.map(fb).join(' ')}${r.weird.length ? ' WEIRD=' + r.weird.join('') : ''}\n`;
  for (const n of r.notes) txt += `[NOTA] ${n}\n`;
  if (r.shared) txt += `[COMUM] ${r.shared.header} figs=${r.shared.figs.map(fb).join(' ')}\n`;
  for (const p of r.stem) txt += (p.small ? '  (fonte) ' : '') + p.text + (p.hyphen.length ? `   {hif: ${p.hyphen.join(', ')}}` : '') + '\n';
  for (const f of r.figs) if (f.text) txt += `  [texto na figura ${fb(f)}] ${f.text.join(' / ').slice(0, 160)}\n`;
  for (const k of 'abcd') txt += `${k}) ${r.alts[k]}\n`;
}
fs.writeFileSync(cfg.outDir + '/raw.txt', txt);
console.log('questoes', result.length, 'nums ok:', result.map(r => r.num).every((n, i) => n === i + 1));
console.log('comuns', blocks.filter(b => b.type === 'S').map(b => b.header + ' -> ' + b.qs).join(' | '));
console.log('notas', blocks.filter(b => b.type === 'N').map(n => n.qs.join('-') + ': ' + n.text).join(' | '));
console.log('sem figura & sem texto em alguma alternativa:', result.filter(r => 'abcd'.split('').some(k => !r.alts[k].trim())).map(r => r.num).join(','));
