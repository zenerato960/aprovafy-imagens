from pathlib import Path
import ast, requests, fitz, json

base=Path('scripts/publicar_fatec_visuais.py').read_text(encoding='utf-8')
mod=ast.parse(base); SOURCES={}
for n in mod.body:
    if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='SOURCES':
        SOURCES=ast.literal_eval(n.value)

# Coordenadas conferidas visualmente nas páginas oficiais.
# page é 1-based; box em pontos PDF.
FIXES={
 ('2015_2',8):(4,(40,250,565,498)),
 ('2015_2',39):(14,(392,290,565,425)),
 ('2016_2',32):(13,(96,158,490,247)),
 ('2017_1',22):(10,(96,535,255,582)),
 ('2020_1',3):(3,(34,482,300,720)),
 ('2020_1',15):(7,(296,70,565,288)),
 ('2022_2',16):(7,(27,394,342,711)),
 ('2022_2',17):(7,(27,394,342,711)),
 ('2023_1',38):(16,(383,373,564,507)),
 ('2023_1',43):(18,(355,580,556,710)),
 ('2024_1',7):(4,(34,215,547,398)),
 ('2024_2',15):(7,(174,267,421,483)),
 ('2019_1',18):(9,(36.49,159.36,551.29,256.81)),
}
FALSE_POSITIVES=[
 'imagens/fatec/2012/1sem/questao_040.png',
 'imagens/fatec/2019/1sem/questao_041.png',
 'imagens/fatec/2020/1sem/questao_042.png',
 'imagens/fatec/2022/2sem/questao_028.png',
 'imagens/fatec/2023/2sem/questao_004.png',
 'imagens/fatec/2025/1sem_A/questao_025.png',
 'imagens/fatec/2025/1sem_B/questao_025.png',
]

def opath(ed,q):
    a=ed.split('_'); year=a[0]; sem=a[1]; var=a[2] if len(a)>2 else None
    folder=f'{sem}sem'+(f'_{var}' if var else '')
    return Path(f'imagens/fatec/{year}/{folder}/questao_{q:03d}.png')

sess=requests.Session(); sess.headers['User-Agent']='Mozilla/5.0 FATEC final manual crop'
cache={}
report=[]
for (ed,q),(pno,box) in FIXES.items():
    if ed not in cache:
        rr=sess.get(SOURCES[ed],timeout=120); rr.raise_for_status()
        if not rr.content.startswith(b'%PDF'): raise RuntimeError(ed)
        cache[ed]=fitz.open(stream=rr.content,filetype='pdf')
    doc=cache[ed]; page=doc[pno-1]
    rect=fitz.Rect(*box)&page.rect
    pix=page.get_pixmap(matrix=fitz.Matrix(3,3),clip=rect,alpha=False)
    out=opath(ed,q); out.parent.mkdir(parents=True,exist_ok=True); pix.save(out)
    report.append({'edicao':ed,'questao':q,'path':str(out),'pagina':pno,'rect':list(box),'width':pix.width,'height':pix.height})
    print('FIX',ed,q,out,pix.width,pix.height)

for s in FALSE_POSITIVES:
    p=Path(s)
    if p.exists():
        p.unlink()
        print('REMOVE',s)

Path('auditorias/fatec_fixes_manuais_finais.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')

# trigger final manual fixes
