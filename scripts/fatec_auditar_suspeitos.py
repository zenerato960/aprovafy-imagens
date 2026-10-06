from pathlib import Path
import ast,re,requests,fitz
from PIL import Image,ImageDraw,ImageFont,ImageOps

BASE='7b863d6a38b764675a702995f548812ad532d0c6'
# suspicious known bad after corrections will be restored by workflow git command, not here.
targets=[
('2012_1',40),('2015_2',39),('2020_1',15),('2020_1',42),('2022_2',28),
('2023_1',38),('2023_1',43),('2023_2',4),('2024_1',7),('2024_2',15),
('2025_1_A',25),('2025_1_B',25)
]
src=Path('scripts/publicar_fatec_visuais.py').read_text(encoding='utf-8')
mod=ast.parse(src); SOURCES={}
for n in mod.body:
    if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='SOURCES':
        SOURCES=ast.literal_eval(n.value)

def findpage(doc,q):
    for i,p in enumerate(doc):
        txt=p.get_text('text')
        if re.search(rf'Quest[aã]o\s*0?{q}(?!\d)',txt,re.I):
            return i
        if re.search(rf'(?m)^\s*{q}\.\s+',txt):
            return i
    return None

sess=requests.Session(); sess.headers['User-Agent']='Mozilla/5.0'
out=Path('auditorias/fatec_suspeitos_paginas'); out.mkdir(parents=True,exist_ok=True)
for x in out.glob('*.png'): x.unlink()
for ed,q in targets:
    rr=sess.get(SOURCES[ed],timeout=120); rr.raise_for_status()
    doc=fitz.open(stream=rr.content,filetype='pdf')
    pi=findpage(doc,q)
    if pi is None:
        print('NAO LOCALIZADA',ed,q); continue
    page=doc[pi]
    pix=page.get_pixmap(matrix=fitz.Matrix(1.55,1.55),alpha=False)
    fn=out/f'{ed}_q{q:03d}_p{pi+1:02d}.png'; pix.save(fn)
    print(ed,q,pi+1,fn)

# trigger audit suspects
