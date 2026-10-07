from pathlib import Path
import ast, json, re, shutil, math
import requests, fitz, cv2, numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFont

# Load official PDF URLs from the existing publisher script.
base = Path("scripts/publicar_fatec_visuais.py").read_text(encoding="utf-8")
mod = ast.parse(base)
SOURCES={}
for node in mod.body:
    if isinstance(node, ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name) and node.targets[0].id=="SOURCES":
        SOURCES=ast.literal_eval(node.value)
        break
manifest=json.loads(Path("auditorias/fatec_recortes_manifest.json").read_text(encoding="utf-8"))
MAN={(x["edicao"],int(x["questao"])):x for x in manifest}

src_root=Path("imagens/fatec")
out_root=Path("auditorias/fatec_v7")
sheet_root=Path("auditorias/fatec_v7_sheets")
for d in (out_root,sheet_root):
    if d.exists(): shutil.rmtree(d)
    d.mkdir(parents=True,exist_ok=True)

def parse_target(p):
    rel=p.relative_to(src_root)
    year=rel.parts[0]; folder=rel.parts[1]
    q=int(re.search(r"(\d+)",p.stem).group(1))
    m=re.match(r"([12])sem(?:_([AB]))?",folder)
    if not m: return None
    ed=f"{year}_{m.group(1)}" + (f"_{m.group(2)}" if m.group(2) else "")
    return ed,q

def expand(rect,page,margin_x=26,margin_y=30):
    return fitz.Rect(max(page.rect.x0,rect.x0-margin_x),max(page.rect.y0,rect.y0-margin_y),
                     min(page.rect.x1,rect.x1+margin_x),min(page.rect.y1,rect.y1+margin_y))

def page_to_px_rect(r,region,scale):
    return [max(0,int((r.x0-region.x0)*scale)),max(0,int((r.y0-region.y0)*scale)),
            max(0,int((r.x1-region.x0)*scale)),max(0,int((r.y1-region.y0)*scale))]

def detect_visual(page, region, scale=3.0):
    pix=page.get_pixmap(matrix=fitz.Matrix(scale,scale),clip=region,alpha=False)
    arr=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,pix.n)[:,:,:3]
    gray=cv2.cvtColor(arr,cv2.COLOR_RGB2GRAY)
    mask=(gray<246).astype(np.uint8)*255

    # Remove PDF text spans from the detection mask only.
    # Final crop is rendered from the original page, so labels/text within figures return.
    tdict=page.get_text("dict")
    for b in tdict.get("blocks",[]):
        if b.get("type")!=0: continue
        for line in b.get("lines",[]):
            for sp in line.get("spans",[]):
                rr=fitz.Rect(sp["bbox"]) & region
                if rr.get_area()<=0: continue
                x0,y0,x1,y1=page_to_px_rect(rr,region,scale)
                pad=4
                mask[max(0,y0-pad):min(mask.shape[0],y1+pad),max(0,x0-pad):min(mask.shape[1],x1+pad)]=0

    # Image blocks are strong visual candidates even when they contain text.
    strong=[]
    for b in tdict.get("blocks",[]):
        if b.get("type")!=1: continue
        rr=fitz.Rect(b["bbox"]) & region
        if rr.get_area()<=0: continue
        x0,y0,x1,y1=page_to_px_rect(rr,region,scale)
        if (x1-x0)>20 and (y1-y0)>20:
            strong.append((x0,y0,x1,y1,10.0))

    # Keep vectors / photos after text masking.
    mm=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8),iterations=1)
    n,labels,stats,_=cv2.connectedComponentsWithStats(mm,8)
    H,W=mask.shape
    comps=[]
    for i in range(1,n):
        x,y,w,h,area=stats[i]
        if area<28 or w<5 or h<5: continue
        # skip page/question separator rules
        if (w>.86*W and h<14) or (h>.86*H and w<9): continue
        bbox_area=w*h
        density=area/max(1,bbox_area)
        # graphical structures can be sparse, so bbox size matters.
        score=(bbox_area**0.72)*(1+min(h/H,0.8)*2.5)*(0.35+min(density,0.6))
        if w>.10*W and h>.06*H:
            comps.append((x,y,x+w,y+h,score))
        elif bbox_area>.006*W*H and (w>25 or h>25):
            comps.append((x,y,x+w,y+h,score*.75))

    allc=strong+comps
    if not allc: return None

    # merge candidates that overlap or are close; this reunites multi-panel graphics.
    groups=[]
    for x0,y0,x1,y1,score in sorted(allc,key=lambda z:z[4],reverse=True):
        placed=False
        for g in groups:
            gx0,gy0,gx1,gy1,gs=g
            gapx=max(0,max(gx0,x0)-min(gx1,x1))
            gapy=max(0,max(gy0,y0)-min(gy1,y1))
            overlapx=max(0,min(gx1,x1)-max(gx0,x0))
            overlapy=max(0,min(gy1,y1)-max(gy0,y0))
            if (gapx<45 and gapy<45) or (overlapx>0 and gapy<70) or (overlapy>0 and gapx<70):
                g[0]=min(gx0,x0);g[1]=min(gy0,y0);g[2]=max(gx1,x1);g[3]=max(gy1,y1);g[4]+=score
                placed=True;break
        if not placed: groups.append([x0,y0,x1,y1,score])

    # Prefer groups with substantial 2D extent, not long text-like strips.
    def gscore(g):
        x0,y0,x1,y1,s=g; w=x1-x0; h=y1-y0
        return s*(1+min(w/W,0.8))*(1+min(h/H,0.8)*2)
    groups.sort(key=gscore,reverse=True)
    g=groups[0]
    x0,y0,x1,y1,_=g

    # Include another large group when it is clearly part of the same visual set.
    best_area=(x1-x0)*(y1-y0)
    for gg in groups[1:]:
        ax0,ay0,ax1,ay1,_=gg
        a=(ax1-ax0)*(ay1-ay0)
        gapx=max(0,max(x0,ax0)-min(x1,ax1)); gapy=max(0,max(y0,ay0)-min(y1,ay1))
        if a>.28*best_area and gapx<80 and gapy<95:
            x0,y0,x1,y1=min(x0,ax0),min(y0,ay0),max(x1,ax1),max(y1,ay1)

    pad=9
    x0=max(0,x0-pad);y0=max(0,y0-pad);x1=min(W,x1+pad);y1=min(H,y1+pad)
    if (x1-x0)*(y1-y0)<.025*W*H: return None
    return fitz.Rect(region.x0+x0/scale,region.y0+y0/scale,region.x0+x1/scale,region.y0+y1/scale)

session=requests.Session(); session.headers["User-Agent"]="Mozilla/5.0 FATEC v7 audit"
cache={}
records=[]
for p in sorted(src_root.rglob("questao_*.png")):
    pq=parse_target(p)
    if not pq: continue
    ed,q=pq
    meta=MAN.get((ed,q))
    if not meta or ed not in SOURCES or not meta.get("pagina"):
        continue
    if ed not in cache:
        r=session.get(SOURCES[ed],timeout=120); r.raise_for_status()
        cache[ed]=fitz.open(stream=r.content,filetype="pdf")
    doc=cache[ed]
    pi=int(meta["pagina"])-1
    if pi<0 or pi>=len(doc): continue
    page=doc[pi]
    if meta.get("rect") and len(meta["rect"])==4:
        base_rect=fitz.Rect(*meta["rect"])
    else:
        # fall back to broad central page region
        base_rect=fitz.Rect(20,30,page.rect.width-20,page.rect.height-30)
    region=expand(base_rect,page,32,38)
    vr=detect_visual(page,region)
    if vr is None:
        # keep original when detection is uncertain.
        out=out_root/p.relative_to(src_root);out.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(p,out)
        records.append((p,out,"keep",None))
        continue
    pix=page.get_pixmap(matrix=fitz.Matrix(2.5,2.5),clip=vr,alpha=False)
    out=out_root/p.relative_to(src_root);out.parent.mkdir(parents=True,exist_ok=True)
    pix.save(out)
    records.append((p,out,"pdf",list(vr)))

# Comparison sheets
cell_w,cell_h=420,360; cols,rows=4,5; per=cols*rows
font=ImageFont.load_default()
for si in range(math.ceil(len(records)/per)):
    batch=records[si*per:(si+1)*per]
    can=Image.new("RGB",(cols*cell_w,rows*cell_h),"white");d=ImageDraw.Draw(can)
    for j,(p,out,mode,rect) in enumerate(batch):
        rr,cc=divmod(j,cols); X=cc*cell_w;Y=rr*cell_h
        a=ImageOps.contain(Image.open(p).convert("RGB"),(cell_w-10,145))
        b=ImageOps.contain(Image.open(out).convert("RGB"),(cell_w-10,145))
        can.paste(a,(X+(cell_w-a.width)//2,Y+5))
        can.paste(b,(X+(cell_w-b.width)//2,Y+165))
        d.line((X,Y+158,X+cell_w,Y+158),fill="gray")
        d.text((X+5,Y+315),str(p).replace("imagens/fatec/",""),fill="black",font=font)
        d.text((X+5,Y+330),f"{mode} {rect}",fill="black",font=font)
        d.rectangle((X,Y,X+cell_w-1,Y+cell_h-1),outline="gray")
    can.save(sheet_root/f"sheet_{si+1:02d}.jpg",quality=88)
print("DONE",len(records))
