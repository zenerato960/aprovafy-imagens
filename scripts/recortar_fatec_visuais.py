from __future__ import annotations

import ast
import re
from pathlib import Path
from io import BytesIO

import cv2
import fitz
import numpy as np
import requests
from PIL import Image

# Reaproveita as fontes oficiais e a lista de questões visuais já cadastradas.
base_script = Path('scripts/publicar_fatec_visuais.py').read_text(encoding='utf-8')
mod = ast.parse(base_script)
SOURCES = {}
CANDIDATES = {}
SPECIAL_PAGES = {}
for node in mod.body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        name = node.targets[0].id
        if name in {'SOURCES', 'CANDIDATES', 'SPECIAL_PAGES'}:
            globals()[name] = ast.literal_eval(node.value)

# Questões que receberam URL por heurística textual, mas não possuem visual necessário.
UNNEEDED = {
    ('2009_1', 6), ('2009_2', 27),
    ('2011_2', 50), ('2011_2', 51), ('2011_2', 52), ('2011_2', 53), ('2011_2', 54),
    ('2012_2', 50), ('2016_2', 2), ('2018_1', 52), ('2019_2', 23), ('2024_1', 46),
}

# Casos compartilhados / fora da região normal da questão. Coordenadas em pontos PDF.
# page é 1-based.
MANUAL = {
    ('2013_2', 32): (12, (410, 45, 560, 165)),
    ('2014_2', 23): (9, (38, 98, 292, 215)),
    ('2014_2', 25): (9, (50, 420, 548, 590)),
    ('2014_2', 26): (9, (50, 420, 548, 590)),
    ('2014_2', 27): (9, (50, 420, 548, 590)),
    ('2014_2', 28): (9, (50, 420, 548, 590)),
    ('2014_2', 48): (19, (355, 55, 558, 170)),
    ('2015_1', 31): (12, (60, 255, 548, 505)),
    ('2015_2', 5): (3, (35, 440, 292, 705)),
    ('2015_2', 6): (3, (35, 440, 292, 705)),
    ('2016_1', 4): (3, (320, 50, 550, 315)),
    ('2016_1', 30): (12, (40, 105, 352, 475)),
    ('2016_1', 31): (12, (40, 105, 352, 475)),
    ('2016_1', 32): (12, (40, 105, 352, 475)),
    ('2016_2', 25): (10, (55, 410, 545, 570)),
    ('2016_2', 26): (10, (55, 410, 545, 570)),
    ('2016_2', 27): (10, (55, 410, 545, 570)),
    ('2016_2', 28): (10, (55, 410, 545, 570)),
    ('2016_2', 29): (10, (55, 410, 545, 570)),
    ('2017_2', 30): (12, (40, 105, 565, 405)),
    ('2017_2', 31): (12, (40, 105, 565, 405)),
    ('2017_2', 32): (12, (40, 105, 565, 405)),
    ('2018_1', 32): (14, (55, 335, 285, 570)),
    ('2018_1', 33): (14, (55, 335, 285, 570)),
    ('2018_1', 34): (14, (55, 335, 285, 570)),
    ('2022_2', 17): (8, (28, 445, 568, 570)),
    ('2023_2', 15): (9, (292, 228, 570, 382)),
    ('2023_2', 16): (9, (292, 228, 570, 382)),
    ('2023_2', 17): (9, (292, 228, 570, 382)),
    ('2023_2', 27): (12, (25, 245, 570, 518)),
    ('2024_1', 18): (8, (32, 312, 308, 700)),
    ('2024_1', 19): (8, (32, 312, 308, 700)),
    ('2024_2', 17): (8, (20, 410, 550, 575)),
    ('2025_2', 63): (22, (148, 64, 433, 406)),
}

session = requests.Session()
session.headers['User-Agent'] = 'Mozilla/5.0 FATEC crop publisher'


def output_path(edicao: str, q: int) -> Path:
    parts = edicao.split('_')
    year, sem = parts[0], parts[1]
    variant = parts[2] if len(parts) > 2 else None
    folder = f'{sem}sem' + (f'_{variant}' if variant else '')
    return Path(f'imagens/fatec/{year}/{folder}/questao_{q:03d}.png')


def heading_rect(page: fitz.Page, q: int):
    for s in (f'Questão {q}', f'Questao {q}', f'Questão 0{q}', f'Questao 0{q}'):
        rr = page.search_for(s)
        if rr:
            return min(rr, key=lambda r: (r.y0, r.x0))
    # 2025/1 usa "6.", "7." etc.
    for b in page.get_text('dict')['blocks']:
        if b.get('type') != 0:
            continue
        for line in b.get('lines', []):
            txt = ''.join(sp['text'] for sp in line.get('spans', []))
            if re.match(rf'^\s*{q}\.\s*', txt):
                return fitz.Rect(line['bbox'])
    return None


def build_qmap(doc: fitz.Document, maxq: int):
    qmap = {}
    hrects = {}
    for pi, page in enumerate(doc):
        txt = page.get_text('text')
        for m in re.finditer(r'Quest[aã]o\s*0?(\d{1,2})(?!\d)', txt, re.I):
            q = int(m.group(1))
            if 1 <= q <= maxq and q not in qmap:
                r = heading_rect(page, q)
                if r:
                    qmap[q] = pi
                    hrects[q] = r
        # 2025/1
        for m in re.finditer(r'(?m)^\s*(\d{1,2})\.\s+', txt):
            q = int(m.group(1))
            if 1 <= q <= maxq and q not in qmap:
                r = heading_rect(page, q)
                if r:
                    qmap[q] = pi
                    hrects[q] = r
    return qmap, hrects


def question_region(doc, q, qmap, hrects):
    pi = qmap[q]
    page = doc[pi]
    h = hrects[q]
    W = page.rect.width
    nearby = []
    for b in page.get_text('blocks'):
        r = fitz.Rect(b[:4])
        if r.y0 >= h.y0 - 3 and r.y0 < h.y0 + 170 and len(b[4].strip()) > 20:
            nearby.append(r)
    full = any(r.x0 < 80 and r.x1 > W - 80 for r in nearby)
    if full:
        x0, x1 = 18, W - 18
    elif h.x0 < W * 0.42:
        x0, x1 = 18, W / 2 - 4
    else:
        x0, x1 = W / 2 + 4, W - 18
    ys = []
    for nq in range(q + 1, min(max(qmap) + 1, q + 8)):
        if qmap.get(nq) == pi:
            nh = hrects[nq]
            if nh.y0 > h.y0 + 5 and (full or abs(nh.x0 - h.x0) < 150):
                ys.append(nh.y0)
    y0 = h.y1 + 1
    y1 = min(ys) - 3 if ys else page.rect.height - 24
    if y1 <= y0 + 8:
        y1 = page.rect.height - 24
    return pi, fitz.Rect(x0, y0, x1, y1)


def raster_graphic_bbox(page: fitz.Page, region: fitz.Rect, scale=2.2):
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), clip=region, alpha=False)
    if pix.width < 10 or pix.height < 10:
        return None
    arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3]
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    mask = (gray < 245).astype(np.uint8) * 255
    for b in page.get_text('dict')['blocks']:
        if b.get('type') != 0:
            continue
        for line in b.get('lines', []):
            for span in line.get('spans', []):
                r = fitz.Rect(span['bbox']) & region
                if r.get_area() <= 0:
                    continue
                x0 = max(0, int((r.x0 - region.x0) * scale) - 3)
                y0 = max(0, int((r.y0 - region.y0) * scale) - 3)
                x1 = min(mask.shape[1], int((r.x1 - region.x0) * scale) + 3)
                y1 = min(mask.shape[0], int((r.y1 - region.y0) * scale) + 3)
                mask[y0:y1, x0:x1] = 0
    mask[:8, :] = 0; mask[-8:, :] = 0; mask[:, :8] = 0; mask[:, -8:] = 0
    mm = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8), iterations=1)
    n, labels, stats, cent = cv2.connectedComponentsWithStats(mm, 8)
    comps = []
    for lab in range(1, n):
        x, y, w, h, area = stats[lab]
        if area < 120 or w < 12 or h < 12:
            continue
        if w > .92 * mask.shape[1] and h < 28:
            continue
        comps.append((area, x, y, w, h))
    if not comps:
        return None
    area, x, y, w, h = max(comps)
    pad = 10
    x0 = max(0, x - pad); y0 = max(0, y - pad)
    x1 = min(mask.shape[1], x + w + pad); y1 = min(mask.shape[0], y + h + pad)
    return fitz.Rect(region.x0 + x0 / scale, region.y0 + y0 / scale,
                     region.x0 + x1 / scale, region.y0 + y1 / scale)


def crop_bbox(doc, edicao, q, qmap, hrects):
    if (edicao, q) in MANUAL:
        page_no, rect = MANUAL[(edicao, q)]
        return page_no - 1, fitz.Rect(*rect)
    if q not in qmap:
        page_index = SPECIAL_PAGES.get((edicao, q))
        if page_index is None:
            return None, None
        # SPECIAL_PAGES já é zero-based no script original
        page = doc[page_index]
        region = fitz.Rect(18, 20, page.rect.width - 18, page.rect.height - 24)
        r = raster_graphic_bbox(page, region)
        return page_index, r
    pi, region = question_region(doc, q, qmap, hrects)
    page = doc[pi]
    # 1) imagens raster embutidas na região
    rects = []
    for b in page.get_text('dict')['blocks']:
        if b.get('type') != 1:
            continue
        r = fitz.Rect(b['bbox'])
        inter = r & region
        if r.get_area() and inter.get_area() / r.get_area() > .45:
            rects.append(r)
    if rects:
        r = rects[0]
        for rr in rects[1:]:
            if abs(rr.y0 - r.y1) < 80 or rr.intersects(r):
                r |= rr
        if r.get_area() < page.rect.get_area() * .45:
            return pi, r
    # 2) componentes gráficos vetoriais/rasterizados após mascarar texto
    r = raster_graphic_bbox(page, region)
    if r and r.get_area() < page.rect.get_area() * .45:
        return pi, r
    return None, None


cache = {}
failed = []
removed = []
written = []
for edicao, questions in CANDIDATES.items():
    if edicao not in cache:
        resp = session.get(SOURCES[edicao], timeout=120)
        resp.raise_for_status()
        if not resp.content.startswith(b'%PDF'):
            raise RuntimeError(f'{edicao}: fonte não é PDF')
        doc = fitz.open(stream=resp.content, filetype='pdf')
        cache[edicao] = (doc, *build_qmap(doc, max(questions)))
    doc, qmap, hrects = cache[edicao]
    for q in questions:
        out = output_path(edicao, q)
        if (edicao, q) in UNNEEDED:
            if out.exists():
                out.unlink()
                removed.append(str(out))
            continue
        pi, rect = crop_bbox(doc, edicao, q, qmap, hrects)
        if rect is None or rect.width < 10 or rect.height < 10:
            failed.append((edicao, q))
            continue
        page = doc[pi]
        rect &= page.rect
        pix = page.get_pixmap(matrix=fitz.Matrix(2.5, 2.5), clip=rect, alpha=False)
        if pix.width < 25 or pix.height < 25:
            failed.append((edicao, q))
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        pix.save(out)
        written.append(str(out))

print('gravadas', len(written), 'removidas', len(removed), 'falhas', len(failed))
if failed:
    print('FALHAS:', failed)
    raise SystemExit(2)
