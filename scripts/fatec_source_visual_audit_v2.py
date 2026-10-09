from pathlib import Path
import ast, json, re, math, unicodedata
import requests, fitz
from PIL import Image, ImageOps, ImageDraw, ImageFont

# Fontes oficiais
base=Path("scripts/publicar_fatec_visuais.py").read_text(encoding="utf-8")
mod=ast.parse(base); SOURCES={}
for n in mod.body:
    if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id=="SOURCES":
        SOURCES=ast.literal_eval(n.value)

# Manifesto anterior serve SOMENTE como dica de página/região.
try:
    old=json.loads(Path("auditorias/fatec_recortes_manifest.json").read_text(encoding="utf-8"))
except Exception:
    old=[]
oldmap={x.get("path"):x for x in old if x.get("path")}

BLACKLIST=("gabarito oficial","divulgacao dos resultados","divulgação dos resultados",
           "matriculas","matrículas","boa prova","aguarde a ordem do fiscal",
           "vestibular 1","vestibular 2","idecan")

# Exceção exata conferida na página oficial.
EXACT={("2019_1",18):(9,(42.5192,163.7003,543.6272,247.5953))}

def parse_path(p):
    rel=p.relative_to("imagens/fatec"); y=rel.parts[0]; folder=rel.parts[1]
    m=re.match(r"(\d)sem(?:_([AB]))?",folder)
    if not m:return None
    ed=f"{y}_{m.group(1)}"+(f"_{m.group(2)}" if m.group(2) else "")
    q=int(re.search(r"(\d+)",p.stem).group(1))
    return ed,q

def normalize(s):
    s=unicodedata.normalize("NFKD",s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()

def text_in(page,r):
    try:return normalize(page.get_textbox(r))
    except:return ""

def blacklisted(page,r):
    t=text_in(page,r)
    return any(x in t for x in BLACKLIST)

def find_heading(doc,q,prefer=None):
    opts=[]
    for pi,p in enumerate(doc):
        for s in (f"Questão {q}",f"Questao {q}",f"Questão 0{q}",f"Questao 0{q}"):
            for r in p.search_for(s):
                opts.append((pi,fitz.Rect(r),300))
        for b in p.get_text("dict")["blocks"]:
            if b.get("type")!=0:continue
            for ln in b.get("lines",[]):
                txt="".join(sp["text"] for sp in ln.get("spans",[])).strip()
                if re.match(rf"^{q}\.\s*",txt):
                    opts.append((pi,fitz.Rect(ln["bbox"]),180))
    if not opts:return None
    if prefer is not None:
        same=[x for x in opts if x[0]==prefer]
        if same:return max(same,key=lambda x:x[2])
        return min(opts,key=lambda x:abs(x[0]-prefer))
    return max(opts,key=lambda x:x[2])

def qregion(doc,q,page_hint=None):
    h=find_heading(doc,q,page_hint)
    if h is None:return None
    pi,hr,_=h; p=doc[pi]; W=p.rect.width
    # Column determined by heading; allow full width later if native object crosses middle.
    if hr.x0 < W*.46: x0,x1=18,W/2+7
    elif hr.x0 > W*.52: x0,x1=W/2-7,W-18
    else: x0,x1=18,W-18
    # next heading on same page/column
    y0=max(20,hr.y1)
    nexty=[]
    for nq in range(q+1,q+8):
        hh=find_heading(doc,nq,pi)
        if hh and hh[0]==pi:
            r=hh[1]
            same=(x0< W/4 and r.x0<W/2) or (x0>W/4 and r.x0>=W/2) or (x0==18 and x1>W*.8)
            if same and r.y0>y0+5: nexty.append(r.y0)
    y1=min(nexty)-3 if nexty else p.rect.height-28
    if y1<y0+20:y1=p.rect.height-28
    return pi,fitz.Rect(x0,y0,x1,y1)

def union(rs):
    if not rs:return None
    u=fitz.Rect(rs[0])
    for r in rs[1:]:u|=r
    return u

def group_rects(rs,gap=18):
    groups=[]
    for rr in sorted(rs,key=lambda z:(z.y0,z.x0)):
        r=fitz.Rect(rr); placed=False
        for i,g in enumerate(groups):
            ex=fitz.Rect(g.x0-gap,g.y0-gap,g.x1+gap,g.y1+gap)
            if ex.intersects(r):
                groups[i]|=r;placed=True;break
        if not placed:groups.append(r)
    changed=True
    while changed:
        changed=False
        for i in range(len(groups)):
            for j in range(i+1,len(groups)):
                a,b=groups[i],groups[j]
                if fitz.Rect(a.x0-gap,a.y0-gap,a.x1+gap,a.y1+gap).intersects(b):
                    groups[i]|=b;groups.pop(j);changed=True;break
            if changed:break
    return groups

def frame_candidates(page,search):
    out=[]
    for d in page.get_drawings():
        r=fitz.Rect(d["rect"])
        inter=r&search
        if inter.get_area()<=0 or inter.get_area()/max(1,r.get_area())<.55:continue
        if r.width<70 or r.height<35:continue
        if r.get_area()>page.rect.get_area()*.70:continue
        if blacklisted(page,r):continue
        # strong preference for panels that contain meaningful text/objects.
        txt=page.get_textbox(r).strip()
        score=r.get_area()*(1.0 + min(len(txt),800)/2400)
        out.append(("frame",r,score))
    return out

def table_candidates(page,search):
    out=[]
    try:tabs=page.find_tables().tables
    except Exception:tabs=[]
    for t in tabs:
        r=fitz.Rect(t.bbox); inter=r&search
        if inter.get_area()<=0 or inter.get_area()/max(1,r.get_area())<.55:continue
        if r.width<60 or r.height<25 or blacklisted(page,r):continue
        out.append(("table",r,r.get_area()*1.35))
    return out

def image_candidates(page,search):
    rs=[]
    for b in page.get_text("dict")["blocks"]:
        if b.get("type")!=1:continue
        r=fitz.Rect(b["bbox"]); inter=r&search
        if r.get_area()<500 or inter.get_area()/max(1,r.get_area())<.42:continue
        if r.get_area()>page.rect.get_area()*.72:continue
        if r.y0>page.rect.height-85:continue
        rs.append(r)
    out=[]
    for g in group_rects(rs,22):
        if blacklisted(page,g):continue
        out.append(("image",g,g.get_area()*1.5))
    return out

def drawing_candidates(page,search):
    rs=[]
    for d in page.get_drawings():
        r=fitz.Rect(d["rect"]); inter=r&search
        if r.get_area()<15 or inter.get_area()/max(1,r.get_area())<.55:continue
        if r.width>search.width*.9 and r.height<3:continue
        if r.height>search.height*.9 and r.width<3:continue
        if r.y0>page.rect.height-80:continue
        rs.append(r)
    out=[]
    for g in group_rects(rs,14):
        if g.width<25 or g.height<20 or blacklisted(page,g):continue
        out.append(("drawing",g,g.get_area()))
    return out

def expand_short_labels(page,r,limit=32,pad=10):
    rr=fitz.Rect(r); zone=fitz.Rect(rr.x0-pad,rr.y0-pad,rr.x1+pad,rr.y1+pad)&page.rect
    for b in page.get_text("dict")["blocks"]:
        if b.get("type")!=0:continue
        for ln in b.get("lines",[]):
            for sp in ln.get("spans",[]):
                txt=sp.get("text","").strip(); sr=fitz.Rect(sp["bbox"])
                if not txt or len(txt)>limit:continue
                if re.match(r"^(Quest[aã]o|\(?[A-E]\)?[.)]?)\b",txt,re.I):continue
                c=fitz.Point((sr.x0+sr.x1)/2,(sr.y0+sr.y1)/2)
                if zone.contains(c):rr|=sr
    return fitz.Rect(rr.x0-4,rr.y0-4,rr.x1+4,rr.y1+4)&page.rect

def select_visual(doc,ed,q,path):
    if (ed,q) in EXACT:
        pg,box=EXACT[(ed,q)];return pg-1,fitz.Rect(*box),"exact"
    hint=oldmap.get(path,{})
    page_hint=int(hint.get("pagina",0))-1 if hint.get("pagina") else None
    hint_rect=fitz.Rect(*hint["rect"]) if hint.get("rect") and len(hint["rect"])==4 else None
    qr=qregion(doc,q,page_hint)
    if qr is None and page_hint is not None and 0<=page_hint<len(doc):
        p=doc[page_hint]; qr=(page_hint,fitz.Rect(18,20,p.rect.width-18,p.rect.height-28))
    if qr is None:return None,None,"no_question"
    pi,reg=qr;p=doc[pi]
    # If previous crop gives a reliable neighborhood, use it, but never narrower than q region intersection.
    searches=[reg]
    if hint_rect is not None and page_hint==pi:
        ex=fitz.Rect(hint_rect.x0-30,hint_rect.y0-30,hint_rect.x1+30,hint_rect.y1+30)&p.rect
        searches.insert(0,ex)
    # Also try full width at same vertical interval for cross-column visuals.
    searches.append(fitz.Rect(18,reg.y0,p.rect.width-18,reg.y1))
    best=None
    for search in searches:
        cand=image_candidates(p,search)+table_candidates(p,search)+frame_candidates(p,search)+drawing_candidates(p,search)
        # reject candidates that are mostly header/footer/question-label material
        filtered=[]
        for mode,r,score in cand:
            if blacklisted(p,r):continue
            if hint_rect is not None:
                inter=(r&hint_rect).get_area()
                score += 2.0*inter
            filtered.append((mode,r,score))
        if not filtered:continue
        filtered.sort(key=lambda z:z[2],reverse=True)
        mode,r,score=filtered[0]
        # Merge same-type companions aligned closely (multiple panels/graphs/alternatives).
        for m2,r2,s2 in filtered[1:]:
            if m2!=mode or s2<score*.08:continue
            dx=max(0,max(r.x0,r2.x0)-min(r.x1,r2.x1))
            dy=max(0,max(r.y0,r2.y0)-min(r.y1,r2.y1))
            xov=max(0,min(r.x1,r2.x1)-max(r.x0,r2.x0))
            yov=max(0,min(r.y1,r2.y1)-max(r.y0,r2.y0))
            if (dx<35 and yov>.15*min(r.height,r2.height)) or (dy<35 and xov>.15*min(r.width,r2.width)):
                u=r|r2
                if u.get_area()<search.get_area()*.88:r=u
        if mode in ("drawing","table"):r=expand_short_labels(p,r)
        score2=score
        # prefer compact object over giant question-region captures
        if r.get_area()>p.rect.get_area()*.52:score2*=.25
        if best is None or score2>best[3]:best=(mode,r,search,score2)
    if best is None:return None,None,"no_visual"
    mode,r,_,_=best
    r=fitz.Rect(r.x0-5,r.y0-5,r.x1+5,r.y1+5)&p.rect
    if blacklisted(p,r):return None,None,"blacklisted"
    return pi,r,mode

targets=[]
for p in sorted(Path("imagens/fatec").glob("*/*/questao_*.png")):
    z=parse_path(p)
    if z:targets.append((z[0],z[1],p))

session=requests.Session();session.headers["User-Agent"]="Mozilla/5.0 FATEC source visual audit v2"
byed={}
for ed,q,p in targets:byed.setdefault(ed,[]).append((q,p))

OUT=Path("auditorias/fatec_source_v2");SHEETS=Path("auditorias/fatec_source_v2_sheets")
OUT.mkdir(parents=True,exist_ok=True);SHEETS.mkdir(parents=True,exist_ok=True)
for d in (OUT,SHEETS):
    for x in d.rglob("*"):
        if x.is_file():x.unlink()

report=[]
for ed,items in sorted(byed.items()):
    if ed not in SOURCES:continue
    rr=session.get(SOURCES[ed],timeout=120);rr.raise_for_status()
    if not rr.content.startswith(b"%PDF"):raise RuntimeError(ed)
    doc=fitz.open(stream=rr.content,filetype="pdf")
    for q,p in items:
        pi,r,mode=select_visual(doc,ed,q,str(p))
        rec={"edicao":ed,"questao":q,"path":str(p),"modo":mode}
        if r is None:
            rec["status"]="no_visual";report.append(rec);continue
        page=doc[pi];r&=page.rect
        pix=page.get_pixmap(matrix=fitz.Matrix(3,3),clip=r,alpha=False)
        op=OUT/Path(p).relative_to("imagens/fatec");op.parent.mkdir(parents=True,exist_ok=True);pix.save(op)
        rec.update({"status":"candidate","pagina":pi+1,"rect":[round(v,2) for v in (r.x0,r.y0,r.x1,r.y1)],
                    "candidate":str(op),"width":pix.width,"height":pix.height})
        report.append(rec)
    doc.close();print(ed,len(items))
Path("auditorias/fatec_source_v2_manifest.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")

# contact sheets
cand=[x for x in report if x["status"]=="candidate"]
cols,rows,CW,CH=4,4,460,340; per=cols*rows
try:font=ImageFont.truetype("DejaVuSans.ttf",15)
except:font=ImageFont.load_default()
for si in range(math.ceil(len(cand)/per)):
    sh=Image.new("RGB",(CW*cols,CH*rows),"white");dr=ImageDraw.Draw(sh)
    for j,x in enumerate(cand[si*per:(si+1)*per]):
        rr,cc=divmod(j,cols); X=cc*CW;Y=rr*CH
        im=Image.open(x["candidate"]).convert("RGB"); im.thumbnail((CW-16,CH-58))
        sh.paste(im,(X+(CW-im.width)//2,Y+28+(CH-58-im.height)//2))
        dr.text((X+5,Y+5),f"{x['edicao']} q{x['questao']:03d} {x['modo']}",fill="black",font=font)
        dr.text((X+5,Y+CH-24),f"{x['width']}x{x['height']}",fill="black",font=font)
        dr.rectangle((X,Y,X+CW-1,Y+CH-1),outline="gray")
    sh.save(SHEETS/f"sheet_{si+1:02d}.jpg",quality=91,optimize=True)
print("TOTAL",len(report),"CAND",len(cand),"NO_VISUAL",len(report)-len(cand))

# trigger audit v2 2026-10-09
