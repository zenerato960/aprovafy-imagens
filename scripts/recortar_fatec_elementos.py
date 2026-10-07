from pathlib import Path
import ast
import json
import re
import unicodedata
import requests
import fitz
import numpy as np
import cv2

BASE_SCRIPT = Path('scripts/publicar_fatec_visuais.py')
TREE = ast.parse(BASE_SCRIPT.read_text(encoding='utf-8'))
VALUES = {}
for node in TREE.body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        name = node.targets[0].id
        if name in {'SOURCES', 'CANDIDATES', 'SPECIAL_PAGES'}:
            VALUES[name] = ast.literal_eval(node.value)
SOURCES = VALUES['SOURCES']
CANDIDATES = VALUES['CANDIDATES']
SPECIAL_PAGES = VALUES.get('SPECIAL_PAGES', {})

MANUAL_KEEP = {
    ('2010_2', 47), ('2011_1', 23), ('2011_1', 24), ('2011_2', 49),
    ('2013_1', 5), ('2013_1', 37), ('2014_1', 10), ('2014_1', 33),
    ('2015_2', 49), ('2017_2', 3), ('2019_1', 12), ('2022_2', 44),
    ('2025_2', 41),
}

def norm(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower().strip()

def output_path(edicao, questao):
    parts = edicao.split('_')
    year, semester = parts[0], parts[1]
    variant = parts[2] if len(parts) > 2 else None
    folder = f'{semester}sem' + (f'_{variant}' if variant else '')
    return Path(f'imagens/fatec/{year}/{folder}/questao_{questao:03d}.png')

def add_hit(hits, q, page_index, rect, kind, score):
    if 1 <= q <= 100:
        hits.setdefault(q, []).append({'page': page_index, 'rect': fitz.Rect(rect), 'kind': kind, 'score': score})

def page_markers(doc):
    hits = {}
    for pi, page in enumerate(doc):
        words = page.get_text('words')
        for j, w in enumerate(words):
            t = norm(w[4]).strip(' .:-')
            if t.startswith('questao'):
                q = None
                r = fitz.Rect(w[:4])
                m = re.search(r'(\d+)', t)
                if m:
                    q = int(m.group(1))
                else:
                    for k in range(j + 1, min(j + 4, len(words))):
                        m2 = re.fullmatch(r'0*(\d{1,3})[.)]?', words[k][4].strip())
                        if m2:
                            q = int(m2.group(1))
                            r |= fitz.Rect(words[k][:4])
                            break
                if q:
                    add_hit(hits, q, pi, r, 'explicit', 300)
        for block in page.get_text('dict')['blocks']:
            if 'lines' not in block:
                continue
            for line in block['lines']:
                for sp in line['spans']:
                    text = sp['text'].strip()
                    m = re.fullmatch(r'0*([1-9]\d?)', text)
                    if not m or 'bold' not in sp.get('font', '').lower():
                        continue
                    q = int(m.group(1))
                    r = fitz.Rect(sp['bbox'])
                    size = float(sp.get('size', 0))
                    if r.y0 > page.rect.y1 - 45 or r.x0 > page.rect.x1 * 0.72 or not (7 <= size <= 18):
                        continue
                    score = 110 + (40 if pi > 0 else -90) + (30 if r.x0 < 150 else 0)
                    add_hit(hits, q, pi, r, 'number', score)
    return hits

def choose_marker(doc, hits, q):
    options = []
    for h in hits.get(q, []):
        pi, r = h['page'], h['rect']
        page = doc[pi]
        rr = fitz.Rect(max(0, r.x0 - 8), r.y0, min(page.rect.x1, r.x1 + 470), min(page.rect.y1, r.y1 + 120))
        context = page.get_textbox(rr).strip()
        score = h['score'] + min(len(context), 220) * 0.2
        if pi > 0:
            score += 45
        if pi == 0:
            score -= 80
        if r.x0 < 160:
            score += 20
        if h['kind'] == 'explicit':
            score += 80
        options.append((score, pi, r, h['kind']))
    if not options:
        return None
    options.sort(reverse=True, key=lambda x: x[0])
    _, pi, r, kind = options[0]
    return pi, r, kind

def detect_two_columns(page):
    mid = page.rect.x1 / 2
    blocks = [fitz.Rect(b[:4]) for b in page.get_text('blocks') if b[4].strip() and b[1] < page.rect.y1 - 45]
    left = sum(1 for b in blocks if b.x1 < mid + 30)
    right = sum(1 for b in blocks if b.x0 > mid - 30)
    return left >= 2 and right >= 2

def question_region(doc, markers, q):
    cur = markers.get(q)
    if cur is None:
        return None
    pi, lab, _ = cur
    page = doc[pi]
    two = detect_two_columns(page)
    mid = page.rect.x1 / 2
    if two and lab.x0 < mid * 0.95:
        x0, x1, col = 20, mid + 5, 'left'
    elif two and lab.x0 >= mid * 0.95:
        x0, x1, col = mid - 5, page.rect.x1 - 20, 'right'
    else:
        x0, x1, col = 20, page.rect.x1 - 20, 'full'
    y0 = max(0, lab.y0 - 4)
    y1 = page.rect.y1 - 28
    candidates = []
    for qq, mk in markers.items():
        if qq == q or mk is None or mk[0] != pi:
            continue
        r = mk[1]
        if r.y0 <= y0 + 8:
            continue
        same_col = col == 'full' or (col == 'left' and r.x0 < mid) or (col == 'right' and r.x0 >= mid)
        if same_col:
            candidates.append(r.y0)
    if candidates:
        y1 = min(candidates) - 3
    if y1 <= y0 + 12:
        y1 = page.rect.y1 - 28

    # Segunda checagem: algumas questões ocupam visualmente as duas colunas,
    # embora o marcador esteja só na coluna esquerda. Se um objeto gráfico
    # nativo atravessa claramente o meio da página dentro da faixa vertical
    # da questão, a região deve ser de largura total.
    if col != 'full':
        probe = fitz.Rect(x0, y0, x1, y1)
        crosses = False
        for info in page.get_image_info(xrefs=True):
            fr = fitz.Rect(info['bbox'])
            inter = fr & probe
            if (not inter.is_empty and fr.x0 < mid - 18 and fr.x1 > mid + 18
                    and fr.width < page.rect.width * 0.96
                    and inter.get_area() >= fr.get_area() * 0.30):
                crosses = True
                break
        if not crosses:
            for d in page.get_drawings():
                fr = fitz.Rect(d['rect'])
                inter = fr & probe
                if (not inter.is_empty and fr.x0 < mid - 18 and fr.x1 > mid + 18
                        and fr.height >= 8 and fr.width >= page.rect.width * 0.45
                        and inter.get_area() >= fr.get_area() * 0.30):
                    crosses = True
                    break
        if crosses:
            x0, x1, col = 20, page.rect.x1 - 20, 'full'
            # Para região full-width, qualquer próxima questão abaixo limita y1.
            candidates = []
            for qq, mk in markers.items():
                if qq == q or mk is None or mk[0] != pi:
                    continue
                r = mk[1]
                if r.y0 > y0 + 8:
                    candidates.append(r.y0)
            if candidates:
                y1 = min(candidates) - 3

    return pi, fitz.Rect(x0, y0, x1, y1)

def union_rect(rects):
    if not rects:
        return None
    u = fitz.Rect(rects[0])
    for r in rects[1:]:
        u |= fitz.Rect(r)
    return u

def image_crop(page, qrect):
    rects = []
    for info in page.get_image_info(xrefs=True):
        full = fitz.Rect(info['bbox'])
        if full.width > page.rect.width * 0.82 and full.height > page.rect.height * 0.82:
            continue
        inter = full & qrect
        if inter.is_empty or inter.width < 18 or inter.height < 18 or inter.width * inter.height < 650:
            continue
        # Nunca recortar um objeto raster nativo no limite artificial da coluna.
        # Se uma parte relevante do objeto pertence à questão, preserva o bbox
        # COMPLETO do objeto original. Isso corrige visuais de largura total que
        # atravessam as duas colunas (ex.: FATEC 2019/1 Q18).
        if inter.width * inter.height < full.width * full.height * 0.35:
            continue
        rects.append(full)
    if not rects:
        return None
    rects.sort(key=lambda r: r.y0)
    areas = [r.width * r.height for r in rects]
    mx = max(areas)
    keep = [r for r, a in zip(rects, areas) if a >= mx * 0.12]
    return union_rect(keep)

def drawing_crop(page, qrect):
    rects = []
    for d in page.get_drawings():
        full = fitz.Rect(d['rect'])
        inter = full & qrect
        if inter.is_empty or inter.width * inter.height < 100:
            continue
        if full.height < 1.5 and full.width > 220:
            continue
        # Assim como nas imagens raster, não truncar desenhos/tabelas na
        # divisória de coluna. Exige sobreposição material para evitar captar
        # elementos da questão vizinha.
        if inter.width * inter.height < full.width * full.height * 0.30:
            continue
        if full.width > page.rect.width * 0.98 and full.height > page.rect.height * 0.9:
            continue
        rects.append(full)
    if not rects:
        return None
    clusters = []
    for r in sorted(rects, key=lambda z: (z.y0, z.x0)):
        placed = False
        for c in clusters:
            u = union_rect(c)
            if fitz.Rect(u.x0 - 18, u.y0 - 18, u.x1 + 18, u.y1 + 18).intersects(r):
                c.append(r)
                placed = True
                break
        if not placed:
            clusters.append([r])
    scored = []
    for c in clusters:
        u = union_rect(c)
        if u.width >= 35 and u.height >= 18:
            scored.append((u.width * u.height, u))
    if not scored:
        return None
    scored.sort(reverse=True, key=lambda z: z[0])
    top = scored[0][0]
    u = union_rect([r for a, r in scored if a >= top * 0.15])
    # add nearby short labels, axes and legends
    grown = fitz.Rect(u)
    for _ in range(2):
        exp = fitz.Rect(grown.x0 - 24, grown.y0 - 18, grown.x1 + 24, grown.y1 + 18) & qrect
        for b in page.get_text('blocks', clip=qrect):
            br = fitz.Rect(b[:4])
            txt = b[4].strip()
            if not txt or not exp.intersects(br):
                continue
            if len(txt) > 130 and br.width > page.rect.width * 0.55:
                continue
            if len(txt) < 110 or br.width < page.rect.width * 0.42:
                grown |= br
    return grown & qrect

def raster_crop(page, qrect):
    scale = 1.55
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), clip=qrect, alpha=False)
    if pix.width < 10 or pix.height < 10:
        return None
    arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    gray = cv2.cvtColor(arr[:, :, :3], cv2.COLOR_RGB2GRAY)
    ink = (gray < 225).astype(np.uint8) * 255
    for w in page.get_text('words', clip=qrect):
        wr = fitz.Rect(w[:4]) & qrect
        x0 = max(0, int((wr.x0 - qrect.x0) * scale) - 2)
        y0 = max(0, int((wr.y0 - qrect.y0) * scale) - 2)
        x1 = min(pix.width, int((wr.x1 - qrect.x0) * scale) + 3)
        y1 = min(pix.height, int((wr.y1 - qrect.y0) * scale) + 3)
        ink[y0:y1, x0:x1] = 0
    n, labels, stats, _ = cv2.connectedComponentsWithStats((ink > 0).astype(np.uint8), 8)
    boxes = []
    for k in range(1, n):
        x, y, w, h, area = [int(v) for v in stats[k]]
        if area < 30 or w < 3 or h < 3:
            continue
        if h <= 3 and w > 260:
            continue
        boxes.append((x, y, w, h, area))
    if not boxes:
        return None
    mask = np.zeros_like(ink)
    for x, y, w, h, area in boxes:
        mask[y:y+h, x:x+w] = 255
    dil = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25)), iterations=1)
    n2, _, stats2, _ = cv2.connectedComponentsWithStats((dil > 0).astype(np.uint8), 8)
    groups = []
    for k in range(1, n2):
        x, y, w, h, _ = [int(v) for v in stats2[k]]
        orig = int((mask[y:y+h, x:x+w] > 0).sum())
        if orig < 95 or w < 26 or h < 16:
            continue
        groups.append((orig, x, y, w, h))
    if not groups:
        return None
    groups.sort(reverse=True)
    best = groups[0]
    _, x0, y0, w0, h0 = best
    x1, y1 = x0 + w0, y0 + h0
    for orig, x, y, w, h in groups[1:]:
        if orig < best[0] * 0.13:
            continue
        if y <= y1 + 80 and y + h >= y0 - 80:
            x0, y0 = min(x0, x), min(y0, y)
            x1, y1 = max(x1, x + w), max(y1, y + h)
    pad = 11
    x0, y0 = max(0, x0 + pad), max(0, y0 + pad)
    x1, y1 = min(pix.width, x1 - pad), min(pix.height, y1 - pad)
    r = fitz.Rect(qrect.x0 + x0 / scale, qrect.y0 + y0 / scale, qrect.x0 + x1 / scale, qrect.y0 + y1 / scale)
    if r.width < 22 or r.height < 14:
        return None
    return r & qrect

def render_crop(page, rect, out):
    margin = 5
    rect = fitz.Rect(max(0, rect.x0 - margin), max(0, rect.y0 - margin), min(page.rect.x1, rect.x1 + margin), min(page.rect.y1, rect.y1 + margin))
    pix = page.get_pixmap(matrix=fitz.Matrix(2.4, 2.4), clip=rect, alpha=False)
    out.parent.mkdir(parents=True, exist_ok=True)
    pix.save(out)
    return pix.width, pix.height, rect

session = requests.Session()
session.headers['User-Agent'] = 'Mozilla/5.0 FATEC precise crop publisher'
manifest = []

for edicao, questions in CANDIDATES.items():
    print('PROCESSANDO', edicao)
    response = session.get(SOURCES[edicao], timeout=120)
    response.raise_for_status()
    if not response.content.startswith(b'%PDF'):
        raise RuntimeError(f'{edicao}: fonte não retornou PDF')
    doc = fitz.open(stream=response.content, filetype='pdf')
    hits = page_markers(doc)
    markers = {q: choose_marker(doc, hits, q) for q in range(1, max(questions) + 2)}

    for q in questions:
        out = output_path(edicao, q)
        if (edicao, q) in MANUAL_KEEP and out.exists():
            manifest.append({'edicao': edicao, 'questao': q, 'status': 'manual_preservado', 'path': str(out)})
            continue
        region = question_region(doc, markers, q)
        if region is None and (edicao, q) in SPECIAL_PAGES:
            pi = SPECIAL_PAGES[(edicao, q)]
            page = doc[pi]
            region = (pi, fitz.Rect(20, 20, page.rect.x1 - 20, page.rect.y1 - 28))
        if region is None:
            if out.exists():
                out.unlink()
            manifest.append({'edicao': edicao, 'questao': q, 'status': 'sem_marcador', 'path': str(out)})
            continue
        pi, qrect = region
        page = doc[pi]
        crop = image_crop(page, qrect)
        mode = 'imagem_pdf'
        if crop is None:
            crop = drawing_crop(page, qrect)
            mode = 'vetor_pdf'
        if crop is None:
            crop = raster_crop(page, qrect)
            mode = 'raster_residual'
        if crop is None:
            if out.exists():
                out.unlink()
            manifest.append({'edicao': edicao, 'questao': q, 'status': 'sem_visual_real', 'path': str(out), 'pagina': pi + 1})
            continue
        width, height, final_rect = render_crop(page, crop, out)
        # strong guard against accidentally saving a near-full page again
        if width > 1300 and height > 1550:
            out.unlink(missing_ok=True)
            manifest.append({'edicao': edicao, 'questao': q, 'status': 'recorte_rejeitado_por_tamanho', 'path': str(out), 'pagina': pi + 1, 'modo': mode, 'width': width, 'height': height})
            continue
        manifest.append({'edicao': edicao, 'questao': q, 'status': 'recortado', 'path': str(out), 'pagina': pi + 1, 'modo': mode, 'width': width, 'height': height, 'rect': [round(final_rect.x0, 2), round(final_rect.y0, 2), round(final_rect.x1, 2), round(final_rect.y1, 2)]})
    doc.close()

report = Path('auditorias/fatec_recortes_manifest.json')
report.parent.mkdir(parents=True, exist_ok=True)
report.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
from collections import Counter
print('RESUMO', Counter(item['status'] for item in manifest))
print('MODOS', Counter(item.get('modo') for item in manifest if item.get('modo')))
