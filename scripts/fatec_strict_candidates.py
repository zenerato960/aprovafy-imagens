from __future__ import annotations
import ast,re,json,math
from pathlib import Path
import requests, fitz
from PIL import Image,ImageOps,ImageDraw,ImageFont

base=Path('scripts/publicar_fatec_visuais.py').read_text(encoding='utf-8')
mod=ast.parse(base); SOURCES={}; SPECIAL_PAGES={}
for node in mod.body:
    if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
        if node.targets[0].id in {'SOURCES','SPECIAL_PAGES'}:
            globals()[node.targets[0].id]=ast.literal_eval(node.value)

# Recortes manuais já validados ao longo da auditoria.
MANUAL={}
try:
    src=Path('scripts/recortar_fatec_visuais.py').read_text(encoding='utf-8'); mm=ast.parse(src)
    for n in mm.body:
        if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='MANUAL':
            MANUAL.update(ast.literal_eval(n.value))
except Exception: pass
try:
    for r in json.loads(Path('auditorias/fatec_fixes_manuais_finais.json').read_text(encoding='utf-8')):
        MANUAL[(r['edicao'],int(r['questao']))]=(int(r['pagina']),tuple(r['rect']))
except Exception: pass
# Caso explicitamente conferido na prova oficial.
MANUAL[('2019_1',18)]=(9,(42.5192,163.7003,543.6272,247.5953))

def parse_path(p):
    rel=p.relative_to('imagens/fatec'); y=rel.parts[0]; folder=rel.parts[1]
    m=re.match(r'(\d)sem(?:_([AB]))?',folder)
    if not m:return None
    ed=f'{y}_{m.group(1)}'+(f'_{m.group(2)}' if m.group(2) else '')
    q=int(re.search(r'(\d+)',p.stem).group(1)); return ed,q

def heading_rect(page,q):
    for s in (f'Questão {q}',f'Questao {q}',f'Questão 0{q}',f'Questao 0{q}'):
        rr=page.search_for(s)
        if rr:return min(rr,key=lambda r:(r.y0,r.x0))
    for b in page.get_text('dict')['blocks']:
        if b.get('type')!=0:continue
        for ln in b.get('lines',[]):
            txt=''.join(s['text'] for s in ln.get('spans',[])).strip()
            if re.match(rf'^{q}\.\s*',txt): return fitz.Rect(ln['bbox'])
    return None

def build_map(doc,maxq):
    qm={}; hr={}
    for pi,p in enumerate(doc):
        txt=p.get_text('text')
        for q in range(1,maxq+1):
            if q in qm: continue
            if re.search(rf'Quest[aã]o\s*0?{q}(?!\d)',txt,re.I) or re.search(rf'(?m)^\s*{q}\.\s+',txt):
                h=heading_rect(p,q)
                if h: qm[q]=pi;hr[q]=h
    return qm,hr

def group(rs,gap=16):
    gs=[]
    for rr in sorted(rs,key=lambda r:(r.y0,r.x0)):
        r=fitz.Rect(rr); hit=None
        for i,g in enumerate(gs):
            ex=fitz.Rect(g.x0-gap,g.y0-gap,g.x1+gap,g.y1+gap)
            if ex.intersects(r): hit=i;break
        if hit is None:gs.append(r)
        else:gs[hit]|=r
    changed=True
    while changed:
        changed=False
        for i in range(len(gs)):
            for j in range(i+1,len(gs)):
                a,b=gs[i],gs[j]
                ex=fitz.Rect(a.x0-gap,a.y0-gap,a.x1+gap,a.y1+gap)
                if ex.intersects(b):
                    gs[i]|=b;gs.pop(j);changed=True;break
            if changed:break
    return gs

def region_for(doc,q,qm,hr):
    if q not in qm:return None,None
    pi=qm[q];p=doc[pi];h=hr[q];W=p.rect.width
    side=0 if h.x0<W/2 else 1
    ys=[]
    for nq,npi in qm.items():
        if nq<=q or npi!=pi:continue
        nh=hr[nq];ns=0 if nh.x0<W/2 else 1
        if ns==side and nh.y0>h.y0+5:ys.append(nh.y0)
    y0=h.y1+1;y1=min(ys)-3 if ys else p.rect.height-22
    if y1<y0+20:y1=p.rect.height-22
    x0,x1=(18,W/2+8) if side==0 else (W/2-8,W-18)
    return pi,fitz.Rect(x0,y0,x1,y1)

def spans_in(p,rect,pad=10,maxlen=45):
    rr=fitz.Rect(rect)
    zone=fitz.Rect(rr.x0-pad,rr.y0-pad,rr.x1+pad,rr.y1+pad)&p.rect
    for b in p.get_text('dict')['blocks']:
        if b.get('type')!=0:continue
        for ln in b.get('lines',[]):
            for sp in ln.get('spans',[]):
                txt=sp.get('text','').strip(); sr=fitz.Rect(sp['bbox'])
                if not txt or len(txt)>maxlen:continue
                if re.match(r'^(Quest[aã]o|\(?[A-E]\)?[.)]?)\b',txt,re.I):continue
                cx=(sr.x0+sr.x1)/2;cy=(sr.y0+sr.y1)/2
                if zone.contains(fitz.Point(cx,cy)): rr|=sr
    return rr&p.rect

def candidates(p,reg):
    out=[]
    # 1) Tabelas verdadeiras.
    try:
        for t in p.find_tables().tables:
            r=fitz.Rect(t.bbox); inter=r&reg
            if inter.get_area()>0 and inter.get_area()/max(1,r.get_area())>.55 and r.width>45 and r.height>18:
                out.append(('table',r,200+r.get_area()/5000))
    except Exception:pass
    # 2) imagens raster originais.
    ims=[]
    for b in p.get_text('dict')['blocks']:
        if b.get('type')==1:
            r=fitz.Rect(b['bbox']); inter=r&reg
            if r.get_area()>100 and inter.get_area()/max(1,r.get_area())>.50 and r.get_area()<p.rect.get_area()*.70:
                ims.append(r)
    for r in group(ims,20): out.append(('image',r,180+r.get_area()/5000))
    # 3) desenhos vetoriais.
    dr=[]
    for d in p.get_drawings():
        r=fitz.Rect(d['rect']); inter=r&reg
        if r.get_area()<12 or inter.get_area()/max(1,r.get_area())<.50:continue
        if r.width>reg.width*.88 and r.height<3:continue
        if r.height>reg.height*.88 and r.width<3:continue
        dr.append(r)
    for r in group(dr,13):
        if r.width>=14 and r.height>=14: out.append(('drawing',r,100+r.get_area()/6500))
    return out

def select(doc,ed,q,qm,hr):
    if (ed,q) in MANUAL:
        pg,box=MANUAL[(ed,q)];return pg-1,fitz.Rect(*box),'manual'
    pi,reg=region_for(doc,q,qm,hr)
    if reg is None:
        spi=SPECIAL_PAGES.get((ed,q))
        if spi is None:return None,None,'missing'
        pi=spi;p=doc[pi];reg=fitz.Rect(18,20,p.rect.width-18,p.rect.height-22)
    p=doc[pi]; c=candidates(p,reg)
    # Se houver visual cruzando a coluna, refaz a busca em largura total na mesma faixa vertical.
    if not c:
        full=fitz.Rect(18,reg.y0,p.rect.width-18,reg.y1); c=candidates(p,full); reg=full
    if not c:return None,None,'no_object'
    # prioridade: imagens/tabelas; desenhos depois. Entre iguais, maior score.
    mode,r,_=max(c,key=lambda x:x[2])
    # Se houver mais de um objeto do mesmo tipo muito próximo/alinhado, une.
    for m2,r2,s2 in c:
        if r2==r:continue
        hg=max(0,max(r.x0,r2.x0)-min(r.x1,r2.x1));vg=max(0,max(r.y0,r2.y0)-min(r.y1,r2.y1))
        xov=max(0,min(r.x1,r2.x1)-max(r.x0,r2.x0));yov=max(0,min(r.y1,r2.y1)-max(r.y0,r2.y0))
        if m2==mode and ((yov>.3*min(r.height,r2.height) and hg<28) or (xov>.3*min(r.width,r2.width) and vg<22)):
            u=r|r2
            if u.get_area()<reg.get_area()*.82:r=u
    if mode=='drawing': r=spans_in(p,r,pad=14,maxlen=28)
    # Margem pequena, sem capturar enunciado.
    r=fitz.Rect(r.x0-5,r.y0-5,r.x1+5,r.y1+5)&p.rect
    return pi,r,mode

paths=sorted(Path('imagens/fatec').glob('*/*/questao_*.png'))
byed={}
for p in paths:
    z=parse_path(p)
    if z:byed.setdefault(z[0],[]).append((z[1],p))
s=requests.Session();s.headers['User-Agent']='Mozilla/5.0 FATEC strict crop audit'
outroot=Path('auditorias/fatec_strict_candidates'); outroot.mkdir(parents=True,exist_ok=True)
report=[]
for ed,items in sorted(byed.items()):
    if ed not in SOURCES:continue
    rr=s.get(SOURCES[ed],timeout=120);rr.raise_for_status()
    if not rr.content.startswith(b'%PDF'):raise RuntimeError(ed)
    doc=fitz.open(stream=rr.content,filetype='pdf');qm,hr=build_map(doc,max(q for q,_ in items))
    for q,oldp in items:
        pi,r,mode=select(doc,ed,q,qm,hr)
        rec={'edicao':ed,'questao':q,'path':str(oldp),'modo':mode}
        if r is None: rec['status']='preserve';report.append(rec);continue
        p=doc[pi];r&=p.rect
        pix=p.get_pixmap(matrix=fitz.Matrix(3,3),clip=r,alpha=False)
        out=outroot/Path(oldp).relative_to('imagens/fatec');out.parent.mkdir(parents=True,exist_ok=True);pix.save(out)
        rec.update({'status':'candidate','pagina':pi+1,'rect':[round(v,2) for v in r],'candidate':str(out),'width':pix.width,'height':pix.height});report.append(rec)
    print(ed,len(items))
Path('auditorias/fatec_strict_candidates_manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
# contact sheets of candidates
cand=[x for x in report if x['status']=='candidate']; cols=4;rows=4;W,H=360,270;LH=34;font=ImageFont.load_default()
sheetdir=Path('auditorias/fatec_strict_candidates_sheets');sheetdir.mkdir(parents=True,exist_ok=True)
for si in range(math.ceil(len(cand)/16)):
    sh=Image.new('RGB',(W*cols,(H+LH)*rows),'white');d=ImageDraw.Draw(sh)
    for j,x in enumerate(cand[si*16:(si+1)*16]):
        r0,c0=divmod(j,cols); im=Image.open(x['candidate']).convert('RGB'); im.thumbnail((W-12,H-12))
        xx=c0*W+(W-im.width)//2; yy=r0*(H+LH)+(H-im.height)//2; sh.paste(im,(xx,yy))
        d.text((c0*W+5,r0*(H+LH)+H+7),f"{x['edicao']} q{x['questao']:03d} {x['modo']}",fill='black',font=font)
        d.rectangle((c0*W,r0*(H+LH),(c0+1)*W-1,(r0+1)*(H+LH)-1),outline='black')
    sh.save(sheetdir/f'sheet_{si+1:02d}.jpg',quality=90)
print('TOTAL',len(report),'CAND',len(cand),'PRESERVE',len(report)-len(cand))

# run strict audit
