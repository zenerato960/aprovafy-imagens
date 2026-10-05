from pathlib import Path
import ast
import requests
import fitz

base = Path('scripts/publicar_fatec_visuais.py').read_text(encoding='utf-8')
mod = ast.parse(base)
SOURCES = {}
for node in mod.body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'SOURCES':
        SOURCES = ast.literal_eval(node.value)
        break

# Recortes revisados manualmente no projeto. Em grupos de questões, o mesmo visual
# é deliberadamente reutilizado, pois a figura/tabela é comum ao conjunto.
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

# Recortes adicionais que já haviam sido validados separadamente.
EXTRA = {
    ('2011_2', 49): (18, (48, 225, 555, 705)),
    ('2013_1', 37): (16, (45, 45, 555, 345)),
    ('2014_1', 33): (13, (42, 35, 560, 258)),
    ('2015_2', 49): (18, (42, 35, 555, 705)),
    ('2017_2', 3): (2, (300, 45, 555, 715)),
}
MANUAL.update(EXTRA)

def outpath(ed, q):
    p = ed.split('_')
    year, sem = p[0], p[1]
    variant = p[2] if len(p) > 2 else None
    folder = f'{sem}sem' + (f'_{variant}' if variant else '')
    return Path(f'imagens/fatec/{year}/{folder}/questao_{q:03d}.png')

s = requests.Session()
s.headers['User-Agent'] = 'Mozilla/5.0 FATEC manual crop restorer'
cache = {}
for (ed, q), (page1, coords) in MANUAL.items():
    if ed not in cache:
        r = s.get(SOURCES[ed], timeout=120)
        r.raise_for_status()
        if not r.content.startswith(b'%PDF'):
            raise RuntimeError(f'{ed}: fonte não retornou PDF')
        cache[ed] = fitz.open(stream=r.content, filetype='pdf')
    doc = cache[ed]
    page = doc[page1 - 1]
    rect = fitz.Rect(*coords) & page.rect
    pix = page.get_pixmap(matrix=fitz.Matrix(2.6, 2.6), clip=rect, alpha=False)
    out = outpath(ed, q)
    out.parent.mkdir(parents=True, exist_ok=True)
    pix.save(out)
    if pix.width > 1550 and pix.height > 1900:
        raise RuntimeError(f'{ed} q{q}: recorte grande demais {pix.width}x{pix.height}')
    print(ed, q, page1, pix.width, pix.height, out)
