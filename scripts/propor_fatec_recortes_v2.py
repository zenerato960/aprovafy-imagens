from __future__ import annotations
from pathlib import Path
import ast,re,json,math,requests
import fitz
from PIL import Image,ImageDraw

base=Path('scripts/publicar_fatec_visuais.py').read_text(encoding='utf-8')
mod=ast.parse(base); SOURCES={}
for node in mod.body:
    if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name) and node.targets[0].id=='SOURCES':
        SOURCES=ast.literal_eval(node.value)

MANUAL={
('2013_2',32):(12,(410,45,560,165)),('2014_2',23):(9,(38,98,292,215)),
('2014_2',25):(9,(50,420,548,590)),('2014_2',26):(9,(50,420,548,590)),('2014_2',27):(9,(50,420,548,590)),('2014_2',28):(9,(50,420,548,590)),
('2014_2',48):(19,(355,55,558,170)),('2015_1',31):(12,(60,255,548,505)),('2015_2',5):(3,(35,440,292,705)),('2015_2',6):(3,(35,440,292,705)),
('2016_1',4):(3,(320,50,550,315)),('2016_1',30):(12,(40,105,352,475)),('2016_1',31):(12,(40,105,352,475)),('2016_1',32):(12,(40,105,352,475)),
('2016_2',25):(10,(55,410,545,570)),('2016_2',26):(10,(55,410,545,570)),('2016_2',27):(10,(55,410,545,570)),('2016_2',28):(10,(55,410,545,570)),('2016_2',29):(10,(55,410,545,570)),
('2017_2',30):(12,(40,105,565,405)),('2017_2',31):(12,(40,105,565,405)),('2017_2',32):(12,(40,105,565,405)),
('2018_1',32):(14,(55,335,285,570)),('2018_1',33):(14,(55,335,285,570)),('2018_1',34):(14,(55,335,285,570)),
('2022_2',17):(8,(28,445,568,570)),('2023_2',15):(9,(292,228,570,382)),('2023_2',16):(9,(292,228,570,382)),('2023_2',17):(9,(292,228,570,382)),
('2023_2',27):(12,(25,245,570,518)),('2024_1',18):(8,(32,312,308,700)),('2024_1',19):(8,(32,312,308,700)),('2024_2',17):(8,(20,410,550,575)),
('2025_2',63):(22,(148,64,433,406)),
}

def parse_path(p):
    m=re.search(r'imagens/fatec/(\d{4})/(1sem|2sem)(?:_([AB]))?/questao_(\d+)\.png$',str(p))
    if not m:return None
    y,sem,var,q=m.groups(); return f"{y}_{sem[0]}"+(f"_{var}" if var else ""),int(q)

def heading(page,q):
    for s in (f'Questão {q}',f'Questao {q}',f'Questão 0{q}',f'Questao 0{q}'):
        rr=page.search_for(s)
        if rr:return min(rr,key=lambda r:(r.y0,r.x0))
    for b in page.get_text('dict')['blocks']:
        if b.get('type')!=0:continue
        for line in b.get('lines',[]):
            txt=''.join(sp['text'] for sp in line.get('spans',[]))
            if re.match(rf'^\s*{q}\.\s*',txt):return fitz.Rect(line['bbox'])
    return None

def build_qmap(doc,maxq=70):
    qm={};hr={}
    for pi,p in enumerate(doc):
        txt=p.get_text('text')
        nums=set(int(x) for x in re.findall(r'Quest[aã]o\s*0?(\d{1,2})(?!\d)',txt,re.I))
        nums|=set(int(x) for x in re.findall(r'(?m)^\s*(\d{1,2})\.\s+',txt))
        for q in sorted(nums):
            if 1<=q<=maxq and q not in qm:
                r=heading(p,q)
                if r:qm[q]=pi;hr[q]=r
    return qm,hr

def region(doc,q,qm,hr):
    pi=qm[q];p=doc[pi];h=hr[q];W=p.rect.width
    if h.x0<W*.44:x0,x1=18,W/2-3
    elif h.x0>W*.54:x0,x1=W/2+3,W-18
    else:x0,x1=18,W-18
    for b in p.get_text('blocks'):
        r=fitz.Rect(b[:4])
        if h.y1<=r.y0<=h.y1+65 and r.x0<70 and r.x1>W-70:
            x0,x1=18,W-18;break
    y1=p.rect.height-24
    for nq in range(q+1,q+8):
        if qm.get(nq)==pi:
            nh=hr[nq]
            if nh.y0>h.y0+6 and (x0<=nh.x0<=x1):
                y1=min(y1,nh.y0-3)
    return pi,fitz.Rect(x0,h.y1+1,x1,y1)

def union_rects(rs):
    r=fitz.Rect(rs[0])
    for x in rs[1:]:r|=x
    return r

def group(rs,gap=18):
    gs=[]
    for r in rs:
        put=None
        for i,g in enumerate(gs):
            u=g
            dx=max(0,max(u.x0,r.x0)-min(u.x1,r.x1));dy=max(0,max(u.y0,r.y0)-min(u.y1,r.y1))
            if dx<=gap and dy<=gap:put=i;break
        if put is None:gs.append(fitz.Rect(r))
        else:gs[put]|=r
    changed=True
    while changed:
        changed=False
        for i in range(len(gs)):
            for j in range(i+1,len(gs)):
                a,b=gs[i],gs[j]
                dx=max(0,max(a.x0,b.x0)-min(a.x1,b.x1));dy=max(0,max(a.y0,b.y0)-min(a.y1,b.y1))
                if dx<=gap and dy<=gap:
                    gs[i]|=b;gs.pop(j);changed=True;break
            if changed:break
    return gs

def add_near_text(page,r,reg,pad=15):
    search=(fitz.Rect(r.x0-pad,r.y0-pad,r.x1+pad,r.y1+pad)&reg)
    rr=fitz.Rect(r)
    for b in page.get_text('dict')['blocks']:
        if b.get('type')!=0:continue
        for ln in b.get('lines',[]):
            for sp in ln.get('spans',[]):
                t=sp.get('text','').strip()
                if not t:continue
                sr=fitz.Rect(sp['bbox'])
                # include labels that overlap expanded visual; avoid long prose lines far outside
                if sr.intersects(search):
                    if len(t)<80 or sr.intersects(rr):
                        rr|=sr
    return rr&reg

def detect(doc,ed,q,qm,hr):
    if (ed,q) in MANUAL:
        pg,bb=MANUAL[(ed,q)];return pg-1,fitz.Rect(*bb),'manual'
    if q not in qm:return None,None,'not_found'
    pi,reg=region(doc,q,qm,hr);p=doc[pi]
    # 1 embedded raster objects: exact source object(s)
    imgs=[]
    for b in p.get_text('dict')['blocks']:
        if b.get('type')!=1:continue
        r=fitz.Rect(b['bbox']);inter=r&reg
        if r.get_area()>100 and inter.get_area()/max(1,r.get_area())>.60:
            imgs.append(r)
    if imgs:
        gs=group(imgs,22);areas=[g.get_area() for g in gs];mx=max(areas)
        chosen=[g for g,a in zip(gs,areas) if a>=mx*.16]
        r=union_rects(chosen)
        # if crop is absurdly page-like, keep exact largest object instead
        if r.get_area()>p.rect.get_area()*.60:r=max(gs,key=lambda x:x.get_area())
        return pi,r,'imagem_pdf'
    # 2 tables: preserve cell text by rendering bbox
    try:tabs=p.find_tables().tables
    except Exception:tabs=[]
    valid=[]
    for t in tabs:
        r=fitz.Rect(t.bbox);inter=r&reg
        if r.height>=24 and r.width>=60 and inter.get_area()/max(1,r.get_area())>.75:
            valid.append(r)
    if valid:
        r=max(valid,key=lambda x:x.get_area())
        return pi,fitz.Rect(r.x0-3,r.y0-3,r.x1+3,r.y1+3)&reg,'tabela'
    # 3 vector drawings. Prefer coherent graphic group, then include short labels.
    ds=[]
    for d in p.get_drawings():
        r=fitz.Rect(d['rect']);inter=r&reg
        if r.get_area()<12 or inter.get_area()/max(1,r.get_area())<.7:continue
        if (r.width>reg.width*.78 and r.height<3) or (r.height>reg.height*.78 and r.width<3):continue
        if r.y0<reg.y0+10 and r.height<20:continue
        ds.append(r)
    if ds:
        gs=group(ds,16)
        def score(r):
            shape=min(r.width,r.height)
            return math.sqrt(max(1,r.get_area())) + min(80,shape) - (40 if r.height<15 or r.width<15 else 0)
        r=max(gs,key=score)
        r=add_near_text(p,r,reg,18)
        r=fitz.Rect(r.x0-4,r.y0-4,r.x1+4,r.y1+4)&reg
        return pi,r,'vetor_pdf'
    return None,None,'sem_deteccao'

paths=sorted(Path('imagens/fatec').glob('**/*.png'))
targets=[(p,*parse_path(p)) for p in paths if parse_path(p)]
session=requests.Session();session.headers['User-Agent']='Mozilla/5.0 FATEC precise crop audit'
docs={};maps={}
outroot=Path('auditorias/fatec_propostas_v2');outroot.mkdir(parents=True,exist_ok=True)
report=[]
for ed in sorted(set(ed for _,ed,_ in targets)):
    url=SOURCES.get(ed)
    if not url:continue
    resp=session.get(url,timeout=120);resp.raise_for_status()
    doc=fitz.open(stream=resp.content,filetype='pdf');docs[ed]=doc;maps[ed]=build_qmap(doc)
for n,(path,ed,q) in enumerate(targets,1):
    doc=docs[ed];qm,hr=maps[ed]
    pi,r,mode=detect(doc,ed,q,qm,hr)
    rec={'path':str(path),'edicao':ed,'questao':q,'status':'ok' if r else 'preservar','modo':mode}
    if r:
        r &= doc[pi].rect
        pix=doc[pi].get_pixmap(matrix=fitz.Matrix(2.5,2.5),clip=r,alpha=False)
        out=outroot/path.relative_to('imagens/fatec')
        out.parent.mkdir(parents=True,exist_ok=True);pix.save(out)
        rec.update({'proposta':str(out),'pagina':pi+1,'rect':[round(v,2) for v in r],'width':pix.width,'height':pix.height})
    report.append(rec)
print('total',len(report),'geradas',sum(x['status']=='ok' for x in report),'preservar',sum(x['status']!='ok' for x in report))
Path('auditorias/fatec_propostas_v2_manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')

# contact sheets of proposals (fallback to current if proposal absent)
thumb=(360,260);cols=4;rows=4;CW,CH=390,310
sheetdir=Path('auditorias/fatec_propostas_v2_sheets');sheetdir.mkdir(parents=True,exist_ok=True)
for si in range(math.ceil(len(report)/16)):
    sheet=Image.new('RGB',(CW*cols,CH*rows),'white');d=ImageDraw.Draw(sheet)
    for k,rec in enumerate(report[si*16:(si+1)*16]):
        x=(k%cols)*CW;y=(k//cols)*CH
        src=Path(rec.get('proposta',rec['path']))
        im=Image.open(src).convert('RGB');im.thumbnail(thumb)
        sheet.paste(im,(x+(CW-im.width)//2,y+34+(thumb[1]-im.height)//2))
        label=rec['path'].replace('imagens/fatec/','')+' ['+rec['modo']+']'
        d.text((x+5,y+5),label,fill='black')
        d.rectangle((x,y,x+CW-1,y+CH-1),outline='gray')
    sheet.save(sheetdir/f'sheet_{si+1:03d}.jpg',quality=90)

# trigger v2
