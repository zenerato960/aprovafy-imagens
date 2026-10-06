from __future__ import annotations
import ast, json, re, shutil
from pathlib import Path
from io import BytesIO
import requests, fitz
from PIL import Image, ImageOps, ImageDraw, ImageFont

# fontes oficiais
src_text=Path("scripts/publicar_fatec_visuais.py").read_text(encoding="utf-8")
mod=ast.parse(src_text)
SOURCES={}
for node in mod.body:
    if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name) and node.targets[0].id=="SOURCES":
        SOURCES=ast.literal_eval(node.value)

manifest=json.loads(Path("auditorias/fatec_recortes_manifest.json").read_text(encoding="utf-8"))
session=requests.Session()
session.headers["User-Agent"]="Mozilla/5.0 FATEC clipped crop repair"

def image_blocks(page):
    out=[]
    for b in page.get_text("dict")["blocks"]:
        if b.get("type")==1:
            r=fitz.Rect(b["bbox"])
            if r.get_area()<page.rect.get_area()*.75:
                out.append(r)
    return out

def rect_expansion(a,b):
    return max(0,a.x0-b.x0)+max(0,b.x1-a.x1)+max(0,a.y0-b.y0)+max(0,b.y1-a.y1)

def overlaps(a,b):
    inter=a&b
    if inter.get_area()<=0: return 0
    return inter.get_area()/max(1,min(a.get_area(),b.get_area()))

# preserva manual overrides já validados
manual_text=Path("scripts/recortar_fatec_visuais.py").read_text(encoding="utf-8")
mm=ast.parse(manual_text); MANUAL={}
for node in mm.body:
    if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name) and node.targets[0].id=="MANUAL":
        MANUAL=ast.literal_eval(node.value)

# Q18/2019-1 foi reportada pelo usuário e conferida diretamente na página oficial.
MANUAL[("2019_1",18)]=(9,(36.49,159.36,551.29,256.81))

byed={}
for rec in manifest:
    if rec.get("status")!="recortado": continue
    ed=rec["edicao"]; q=int(rec["questao"])
    if Path(rec["path"]).exists():
        byed.setdefault(ed,[]).append(rec)

changes=[]
comparisons=[]
for ed,recs in sorted(byed.items()):
    if ed not in SOURCES: continue
    resp=session.get(SOURCES[ed],timeout=120)
    resp.raise_for_status()
    if not resp.content.startswith(b"%PDF"): raise RuntimeError(f"{ed}: fonte não PDF")
    doc=fitz.open(stream=resp.content,filetype="pdf")
    for rec in recs:
        q=int(rec["questao"])
        pth=Path(rec["path"])
        before=Image.open(pth).convert("RGB").copy()
        manual=MANUAL.get((ed,q))
        changed=False; reason=None
        if manual:
            pno,box=manual
            pi=pno-1; new=fitz.Rect(*box)
            old=fitz.Rect(*rec["rect"])
            # só regrava manual se difere materialmente
            if rect_expansion(old,new)>2 or rect_expansion(new,old)>2:
                changed=True; reason="manual_validado"
        else:
            pi=int(rec["pagina"])-1
            page=doc[pi]
            old=fitz.Rect(*rec["rect"])
            new=fitz.Rect(old)
            mode=rec.get("modo","")
            imgs=image_blocks(page)
            # Objetos raster reais parcialmente cortados: expande para o bbox original do PDF.
            relevant=[]
            for ir in imgs:
                inter=ir&old
                if inter.get_area()<=0: continue
                center=fitz.Point((ir.x0+ir.x1)/2,(ir.y0+ir.y1)/2)
                center_inside=old.contains(center)
                overlap=inter.get_area()/max(ir.get_area(),1)
                if center_inside or overlap>=.22:
                    relevant.append(ir)
            if relevant:
                u=fitz.Rect(relevant[0])
                for rr in relevant[1:]: u|=rr
                # Se o objeto real extrapola o recorte atual, isso é evidência objetiva de clipping.
                outside=(max(0,old.x0-u.x0)+max(0,u.x1-old.x1)+max(0,old.y0-u.y0)+max(0,u.y1-old.y1))
                if outside>8 and u.get_area()<page.rect.get_area()*.65:
                    new=fitz.Rect(max(0,u.x0-5),max(0,u.y0-5),min(page.rect.width,u.x1+5),min(page.rect.height,u.y1+5))
                    changed=True; reason=f"objeto_pdf_cortado:{mode}"

            # Para vetores, só expande quando o recorte termina exatamente na divisória de colunas
            # e há desenhos atravessando essa divisória.
            if not changed:
                half=page.rect.width/2
                hits_half=abs(old.x1-half)<18 or abs(old.x0-half)<18
                if hits_half:
                    ds=[]
                    for d in page.get_drawings():
                        r=d["rect"]
                        if r.get_area()<18: continue
                        if r.width>page.rect.width*.7 and r.height<3: continue
                        if (r&old).get_area()>0 and (r.x0<old.x0-4 or r.x1>old.x1+4):
                            ds.append(r)
                    if ds:
                        u=fitz.Rect(old)
                        for rr in ds: u|=rr
                        if u.get_area()<page.rect.get_area()*.55:
                            new=fitz.Rect(max(0,u.x0-6),max(0,u.y0-6),min(page.rect.width,u.x1+6),min(page.rect.height,u.y1+6))
                            changed=True; reason=f"vetor_cruza_coluna:{mode}"

        if not changed: continue
        page=doc[pi]
        new &= page.rect
        pix=page.get_pixmap(matrix=fitz.Matrix(3,3),clip=new,alpha=False)
        after=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
        pth.parent.mkdir(parents=True,exist_ok=True)
        after.save(pth,"PNG",optimize=True)
        changes.append({
            "edicao":ed,"questao":q,"path":str(pth),"pagina":pi+1,
            "reason":reason,
            "old_rect":[round(v,2) for v in (old.x0,old.y0,old.x1,old.y1)],
            "new_rect":[round(v,2) for v in (new.x0,new.y0,new.x1,new.y1)],
            "before_size":before.size,"after_size":after.size
        })
        comparisons.append((ed,q,pth,before,after))

# gera pranchas antes/depois APENAS das alterações
outdir=Path("auditorias/fatec_clip_review"); outdir.mkdir(parents=True,exist_ok=True)
for old in outdir.glob("*.jpg"): old.unlink()
font=ImageFont.load_default()
tw,th=360,260
per=6
for si in range((len(comparisons)+per-1)//per):
    batch=comparisons[si*per:(si+1)*per]
    sheet=Image.new("RGB",(tw*2,(th+34)*len(batch)),"white")
    dr=ImageDraw.Draw(sheet)
    for j,(ed,q,p,bef,aft) in enumerate(batch):
        for k,img in enumerate((bef,aft)):
            fit=ImageOps.contain(img,(tw-10,th-10))
            x=k*tw+(tw-fit.width)//2
            y=j*(th+34)+(th-fit.height)//2
            sheet.paste(fit,(x,y))
        dr.text((6,j*(th+34)+th+8),f"{ed} q{q:03d} ANTES",fill="black",font=font)
        dr.text((tw+6,j*(th+34)+th+8),f"{ed} q{q:03d} DEPOIS",fill="black",font=font)
        dr.line((tw,j*(th+34),tw,(j+1)*(th+34)),fill="black",width=1)
        dr.line((0,(j+1)*(th+34)-1,tw*2,(j+1)*(th+34)-1),fill="black",width=1)
    sheet.save(outdir/f"sheet_{si+1:02d}.jpg",quality=90,optimize=True)

Path("auditorias/fatec_clip_fixes.json").write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding="utf-8")
print("ALTERADAS",len(changes))
for c in changes: print(c["edicao"],c["questao"],c["reason"],c["old_rect"],"=>",c["new_rect"])
