from __future__ import annotations
from pathlib import Path
import ast,re,json,math,requests
import fitz
from PIL import Image,ImageDraw

base=Path('scripts/publicar_fatec_visuais.py').read_text(encoding='utf-8')
mod=ast.parse(base);SOURCES={}
for node in mod.body:
    if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name) and node.targets[0].id=='SOURCES':
        SOURCES=ast.literal_eval(node.value)

BAD={
'2009_1':[11],'2009_2':[7,29,30,47,48],
'2010_1':[19,23,24,29,30,39,42,43],'2010_2':[25,26],
'2011_1':[24,26,29],'2011_2':[16,19,21,23,37,49],
'2012_1':[9,13,19,30,34,37,46],'2012_2':[1,10,31,34,36],
'2013_1':[10,11,14,19,20,31,34,37,42],
'2013_2':[10,13,14,18,24,32,34,36,37,39,40,43],
'2014_1':[1,2,3,5,10,12,19,22,31,33,39,40,46],
'2014_2':[17,21,24,32,39,40,42,44],
'2015_1':[8,10,12,20,22,33,38,48],
'2015_2':[4,5,6,9,11,14,20,21,23,30,31,41,46,49],
'2016_1':[9,11,44,45],
'2016_2':[2,10,11,14,34,35,49],
'2017_1':[8,9,11,12,20,21,37,41],
'2017_2':[3,11,18,23,24,38],
'2018_1':[10,11,24,30,32,33,34,35,36,38],
'2018_2':[2,5],
'2019_1':[18,19,49],'2019_2':[5,22,33,34,50],
'2020_1':[8,9,11,14,17,34,35,36,37,47],
'2022_2':[6,15,45],
'2023_1':[27,30,31,38],
'2023_2':[14,24,36,37,40],
'2024_1':[2,5,28,30,31,46,54],
'2024_2':[1,17,21,23,48,52],
'2025_1_A':[39,52],'2025_1_B':[39,52],
'2025_2':[33,63],
}

# known exact override requested by user: render the straight rounded source box, not an extracted skewed-looking crop
OVERRIDE={('2019_1',18):(9,(42.5,163.5,543.8,248.0))}

def path_for(ed,q):
    y,s,*v=ed.split('_'); folder=f'{s}sem'+(f'_{v[0]}' if v else '')
    return f'imagens/fatec/{y}/{folder}/questao_{q:03d}.png'

old=[]
mf=Path('auditorias/fatec_recortes_manifest.json')
if mf.exists(): old=json.loads(mf.read_text(encoding='utf-8'))
oldmap={x.get('path'):(x) for x in old if x.get('path')}

session=requests.Session();session.headers['User-Agent']='Mozilla/5.0 FATEC precision repair'
docs={}
for ed in BAD:
    r=session.get(SOURCES[ed],timeout=120);r.raise_for_status();docs[ed]=fitz.open(stream=r.content,filetype='pdf')

def heading_occurrences(doc,q):
    out=[]
    for pi,p in enumerate(doc):
        # standalone headings from text rectangles
        for s in (f'Questão {q}',f'Questao {q}',f'Questão 0{q}',f'Questao 0{q}'):
            for r in p.search_for(s):
                out.append((pi,r))
        # 2025 numbered headings
        for b in p.get_text('dict')['blocks']:
            if b.get('type')!=0:continue
            for ln in b.get('lines',[]):
                txt=''.join(sp['text'] for sp in ln.get('spans',[]))
                if re.match(rf'^\s*{q}\.\s*',txt):out.append((pi,fitz.Rect(ln['bbox'])))
    return out

def question_heading(doc,q,prefer_page=None):
    occ=heading_occurrences(doc,q)
    if not occ:return None,None
    if prefer_page is not None:
        same=[x for x in occ if x[0]==prefer_page]
        if same:return min(same,key=lambda x:(x[1].y0,x[1].x0))
        close=sorted(occ,key=lambda x:abs(x[0]-prefer_page))
        return close[0]
    return min(occ,key=lambda x:(x[0],x[1].y0))

def group_rects(rs,gap=18):
    gs=[]
    for rr in rs:
        r=fitz.Rect(rr);placed=False
        for i,g in enumerate(gs):
            dx=max(0,max(g.x0,r.x0)-min(g.x1,r.x1));dy=max(0,max(g.y0,r.y0)-min(g.y1,r.y1))
            if dx<=gap and dy<=gap:gs[i]|=r;placed=True;break
        if not placed:gs.append(r)
    ch=True
    while ch:
        ch=False
        for i in range(len(gs)):
            for j in range(i+1,len(gs)):
                a,b=gs[i],gs[j];dx=max(0,max(a.x0,b.x0)-min(a.x1,b.x1));dy=max(0,max(a.y0,b.y0)-min(a.y1,b.y1))
                if dx<=gap and dy<=gap:gs[i]|=b;gs.pop(j);ch=True;break
            if ch:break
    return gs

def overlap_ratio(r,search):
    inter=r&search
    return inter.get_area()/max(1,r.get_area())

def graphics_on_page(p,search):
    c=[]
    # raster images
    imgs=[]
    for b in p.get_text('dict')['blocks']:
        if b.get('type')==1:
            r=fitz.Rect(b['bbox'])
            if r.get_area()>120 and overlap_ratio(r,search)>.28:imgs.append(r)
    for g in group_rects(imgs,25):
        c.append(('image',g,120+math.sqrt(g.get_area())))
    # tables
    try: tabs=p.find_tables().tables
    except Exception: tabs=[]
    for t in tabs:
        r=fitz.Rect(t.bbox)
        if r.width>55 and r.height>20 and overlap_ratio(r,search)>.35:
            c.append(('table',r,105+math.sqrt(r.get_area())))
    # drawings, grouped
    ds=[]
    for d in p.get_drawings():
        r=fitz.Rect(d['rect'])
        if r.get_area()<15 or overlap_ratio(r,search)<.35:continue
        if (r.width>search.width*.85 and r.height<3) or (r.height>search.height*.85 and r.width<3):continue
        ds.append(r)
    for g in group_rects(ds,16):
        if g.width<12 or g.height<12:continue
        c.append(('drawing',g,70+math.sqrt(g.get_area())))
    return c

def expand_labels(p,r,search):
    rr=fitz.Rect(r); zone=(fitz.Rect(r.x0-16,r.y0-16,r.x1+16,r.y1+16)&search)
    for b in p.get_text('dict')['blocks']:
        if b.get('type')!=0:continue
        for ln in b.get('lines',[]):
            for sp in ln.get('spans',[]):
                txt=sp.get('text','').strip();sr=fitz.Rect(sp['bbox'])
                if txt and len(txt)<70 and sr.intersects(zone):rr|=sr
    return (fitz.Rect(rr.x0-4,rr.y0-4,rr.x1+4,rr.y1+4)&p.rect)

def choose(ed,q):
    doc=docs[ed]
    if (ed,q) in OVERRIDE:
        pg,bb=OVERRIDE[(ed,q)];return pg-1,fitz.Rect(*bb),'override'
    path=path_for(ed,q); om=oldmap.get(path,{})
    pref=None
    if om.get('pagina'):pref=int(om['pagina'])-1
    elif om.get('page'):pref=int(om['page'])-1
    pi,h=question_heading(doc,q,pref)
    # old manifest rect is the strongest search region when available
    oldr=None
    if om.get('rect') and len(om['rect'])==4:oldr=fitz.Rect(*om['rect'])
    if pref is not None and 0<=pref<len(doc):pi=pref
    if pi is None:pi=0
    p=doc[pi]
    # broad search around old crop / question, allowing shared visuals above heading
    if oldr:
        search=(fitz.Rect(oldr.x0-25,oldr.y0-25,oldr.x1+25,oldr.y1+25)&p.rect)
    elif h:
        W=p.rect.width
        if h.x0<W*.45:x0,x1=18,W/2+5
        elif h.x0>W*.52:x0,x1=W/2-5,W-18
        else:x0,x1=18,W-18
        search=fitz.Rect(x0,max(20,h.y0-260),x1,min(p.rect.height-20,h.y0+420))
    else:search=fitz.Rect(18,20,p.rect.width-18,p.rect.height-20)
    candidates=graphics_on_page(p,search)
    # remove page/header artifacts; prefer candidates overlapping old crop strongly
    if oldr:
        for i,(kind,r,s) in enumerate(candidates):
            ov=(r&oldr).get_area()/max(1,r.get_area())
            candidates[i]=(kind,r,s+80*ov)
    if candidates:
        kind,r,s=max(candidates,key=lambda x:x[2])
        if kind in ('drawing','table'):r=expand_labels(p,r,search)
        return pi,r,kind
    # search immediately before current page (shared image at page break)
    if pi>0:
        pp=doc[pi-1];sr=fitz.Rect(18,pp.rect.height*.45,pp.rect.width-18,pp.rect.height-20)
        cc=graphics_on_page(pp,sr)
        if cc:
            kind,r,s=max(cc,key=lambda x:x[2]);return pi-1,expand_labels(pp,r,sr) if kind!='image' else r,'prev_'+kind
    return None,None,'unresolved'

outdir=Path('auditorias/fatec_reparos_direcionados');outdir.mkdir(parents=True,exist_ok=True)
report=[]
for ed,qs in BAD.items():
    for q in qs:
        pi,r,mode=choose(ed,q);path=path_for(ed,q)
        rec={'edicao':ed,'questao':q,'path':path,'modo':mode}
        if r is not None:
            p=docs[ed][pi];r&=p.rect
            pix=p.get_pixmap(matrix=fitz.Matrix(2.5,2.5),clip=r,alpha=False)
            out=outdir/Path(path).relative_to('imagens/fatec');out.parent.mkdir(parents=True,exist_ok=True);pix.save(out)
            rec.update({'status':'proposto','pagina':pi+1,'rect':[round(v,2) for v in r],'width':pix.width,'height':pix.height,'proposta':str(out)})
        else:rec['status']='unresolved'
        report.append(rec)
Path('auditorias/fatec_reparos_direcionados_manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')

# review sheets
cols=4;rows=4;CW,CH=390,310;thumb=(360,260)
sdir=Path('auditorias/fatec_reparos_direcionados_sheets');sdir.mkdir(parents=True,exist_ok=True)
for si in range(math.ceil(len(report)/16)):
    sh=Image.new('RGB',(CW*cols,CH*rows),'white');dr=ImageDraw.Draw(sh)
    for k,rec in enumerate(report[si*16:(si+1)*16]):
        x=(k%cols)*CW;y=(k//cols)*CH
        dr.text((x+5,y+5),f"{rec['edicao']} q{rec['questao']:02d} [{rec['modo']}]",fill='black')
        if rec.get('proposta'):
            im=Image.open(rec['proposta']).convert('RGB');im.thumbnail(thumb)
            sh.paste(im,(x+(CW-im.width)//2,y+34+(thumb[1]-im.height)//2))
        dr.rectangle((x,y,x+CW-1,y+CH-1),outline='gray')
    sh.save(sdir/f'sheet_{si+1:02d}.jpg',quality=91)
print('total',len(report),'propostos',sum(x['status']=='proposto' for x in report),'unresolved',sum(x['status']=='unresolved' for x in report))
