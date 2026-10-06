from __future__ import annotations
import ast, re
from pathlib import Path
import fitz, requests
from PIL import Image, ImageChops

# Reaproveita as fontes oficiais e metadados já mantidos no repositório.
base = Path("scripts/publicar_fatec_visuais.py").read_text(encoding="utf-8")
mod = ast.parse(base)
SOURCES = {}
CANDIDATES = {}
SPECIAL_PAGES = {}
for node in mod.body:
    if isinstance(node, ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0], ast.Name):
        if node.targets[0].id in {"SOURCES","CANDIDATES","SPECIAL_PAGES"}:
            globals()[node.targets[0].id] = ast.literal_eval(node.value)

# Overrides confiáveis já levantados anteriormente.
manual_src = Path("scripts/recortar_fatec_visuais.py").read_text(encoding="utf-8")
mmod = ast.parse(manual_src)
MANUAL = {}
for node in mmod.body:
    if isinstance(node, ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id=="MANUAL":
        MANUAL = ast.literal_eval(node.value)

# Correção explícita do caso reportado: a caixa ocupa praticamente a largura inteira.
MANUAL.update({
    ("2019_1",18):(9,(36.49,159.36,551.29,256.81)),
})

session=requests.Session()
session.headers["User-Agent"]="Mozilla/5.0 FATEC faithful crop auditor"

def parse_path(p:Path):
    rel=p.relative_to(Path("imagens/fatec"))
    year=rel.parts[0]
    folder=rel.parts[1]
    m=re.match(r"(\d)sem(?:_([AB]))?",folder)
    if not m: return None
    sem=m.group(1); var=m.group(2)
    ed=f"{year}_{sem}"+(f"_{var}" if var else "")
    q=int(re.search(r"(\d+)",p.stem).group(1))
    return ed,q

def heading_rect(page,q):
    for s in (f"Questão {q}",f"Questao {q}",f"Questão 0{q}",f"Questao 0{q}"):
        rr=page.search_for(s)
        if rr:
            # prefere o cabeçalho visual, normalmente o mais à esquerda/alto
            return min(rr,key=lambda r:(r.y0,r.x0))
    # formato 2025
    for b in page.get_text("dict")["blocks"]:
        if b.get("type")!=0: continue
        for line in b.get("lines",[]):
            txt="".join(sp["text"] for sp in line.get("spans",[])).strip()
            if re.match(rf"^{q}\.\s*",txt):
                return fitz.Rect(line["bbox"])
    return None

def build_map(doc,maxq):
    qmap={}; hrect={}
    for pi,page in enumerate(doc):
        txt=page.get_text("text")
        for q in range(1,maxq+1):
            if q in qmap: continue
            if re.search(rf"Quest[aã]o\s*0?{q}(?!\d)",txt,re.I) or re.search(rf"(?m)^\s*{q}\.\s+",txt):
                r=heading_rect(page,q)
                if r:
                    qmap[q]=pi; hrect[q]=r
    return qmap,hrect

def next_y_same_side(q,pi,h,qmap,hrect,W):
    ys=[]
    side=0 if h.x0 < W/2 else 1
    for nq, npi in qmap.items():
        if nq<=q or npi!=pi: continue
        nh=hrect[nq]
        nside=0 if nh.x0 < W/2 else 1
        if nside==side and nh.y0>h.y0+5:
            ys.append(nh.y0)
    return min(ys) if ys else None

def nontrivial_drawings(page,y0,y1):
    out=[]
    W=page.rect.width
    for d in page.get_drawings():
        r=d["rect"]
        if r.y1<y0 or r.y0>y1: continue
        # descarta separadores finos que atravessam a página
        if r.width>W*.65 and r.height<3: continue
        if r.height>page.rect.height*.65 and r.width<3: continue
        if r.get_area()<18: continue
        out.append(r)
    return out

def visual_blocks(page,y0,y1):
    out=[]
    for b in page.get_text("dict")["blocks"]:
        if b.get("type")!=1: continue
        r=fitz.Rect(b["bbox"])
        if r.y1<y0 or r.y0>y1: continue
        if r.get_area()>page.rect.get_area()*.75: continue
        out.append(r)
    return out

def question_region(doc,q,qmap,hrect):
    if q not in qmap: return None,None
    pi=qmap[q]; page=doc[pi]; h=hrect[q]; W=page.rect.width
    ny=next_y_same_side(q,pi,h,qmap,hrect,W)
    y0=max(h.y1+1,0)
    y1=(ny-3 if ny else page.rect.height-22)
    if y1<=y0+15: y1=page.rect.height-22

    # Primeiro assume coluna pelo cabeçalho.
    left = h.x0 < W/2
    x0,x1=(18,W/2-4) if left else (W/2+4,W-18)

    # Se um objeto gráfico/imagem real atravessa o centro, a questão é de largura inteira.
    objs=visual_blocks(page,y0,y1)+nontrivial_drawings(page,y0,y1)
    cross=[r for r in objs if r.x0 < W*.46 and r.x1 > W*.54]
    wide=[r for r in objs if r.width > W*.48]
    if cross or wide:
        x0,x1=18,W-18

    return pi,fitz.Rect(x0,y0,x1,y1)

def group_rects(rects,gap=22):
    groups=[]
    for r in sorted(rects,key=lambda z:(z.y0,z.x0)):
        hit=None
        for i,g in enumerate(groups):
            ex=fitz.Rect(g.x0-gap,g.y0-gap,g.x1+gap,g.y1+gap)
            if ex.intersects(r):
                hit=i; break
        if hit is None:
            groups.append(fitz.Rect(r))
        else:
            groups[hit] |= r
            # consolida grupos que passaram a se tocar
            changed=True
            while changed:
                changed=False
                for j in range(len(groups)-1,-1,-1):
                    if j==hit: continue
                    ex=fitz.Rect(groups[hit].x0-gap,groups[hit].y0-gap,groups[hit].x1+gap,groups[hit].y1+gap)
                    if ex.intersects(groups[j]):
                        groups[hit] |= groups[j]; groups.pop(j)
                        if j<hit: hit-=1
                        changed=True
    return groups

def choose_bbox(doc,ed,q,qmap,hrect):
    if (ed,q) in MANUAL:
        pno,box=MANUAL[(ed,q)]
        return pno-1,fitz.Rect(*box),"manual"

    pi,reg=question_region(doc,q,qmap,hrect)
    if reg is None:
        spi=SPECIAL_PAGES.get((ed,q))
        if spi is None: return None,None,"missing"
        pi=spi; page=doc[pi]; reg=fitz.Rect(18,20,page.rect.width-18,page.rect.height-22)
    page=doc[pi]
    reg &= page.rect

    imgs=[]
    for r in visual_blocks(page,reg.y0,reg.y1):
        inter=r & reg
        if inter.get_area()/max(r.get_area(),1)>.35:
            imgs.append(inter)

    draws=[]
    for r in nontrivial_drawings(page,reg.y0,reg.y1):
        inter=r & reg
        if inter.get_area()>0:
            draws.append(inter)

    candidates=[]
    # Imagens embutidas são em geral o objeto original mais fiel.
    for g in group_rects(imgs,28):
        if g.get_area() < 80: continue
        candidates.append(("imagem_pdf",g, 5 + min(g.get_area()/9000,8)))

    # Grupos vetoriais: úteis para gráficos/tabelas/diagramas.
    for g in group_rects(draws,18):
        if g.width<18 or g.height<18: continue
        candidates.append(("vetor_pdf",g, 3 + min(g.get_area()/8000,8)))

    if not candidates:
        return None,None,"sem_objeto"

    # Evita selecionar selo/cabeçalho muito pequeno no topo; favorece área visual substantiva.
    filtered=[]
    for mode,g,score in candidates:
        if g.y1 < reg.y0+24 and g.height<28: continue
        if g.get_area()>reg.get_area()*.92: score-=5
        # penaliza faixas muito finas
        if g.width/g.height>14 or g.height/g.width>14: score-=3
        filtered.append((mode,g,score))
    if not filtered: filtered=candidates
    mode,g,_=max(filtered,key=lambda t:t[2])

    # Une objetos vizinhos alinhados que claramente formam um mesmo visual (ex.: Figuras 1 e 2).
    for mode2,g2,score2 in filtered:
        if g2==g: continue
        horiz_gap=max(0,max(g.x0,g2.x0)-min(g.x1,g2.x1))
        vert_gap=max(0,max(g.y0,g2.y0)-min(g.y1,g2.y1))
        y_overlap=max(0,min(g.y1,g2.y1)-max(g.y0,g2.y0))
        x_overlap=max(0,min(g.x1,g2.x1)-max(g.x0,g2.x0))
        if (y_overlap>min(g.height,g2.height)*.35 and horiz_gap<45) or (x_overlap>min(g.width,g2.width)*.35 and vert_gap<35):
            union=g|g2
            if union.get_area()<reg.get_area()*.85:
                g=union

    # Inclui rótulos/captions curtos próximos sem engolir o enunciado inteiro.
    expanded=fitz.Rect(max(reg.x0,g.x0-7),max(reg.y0,g.y0-7),min(reg.x1,g.x1+7),min(reg.y1,g.y1+7))
    for b in page.get_text("dict")["blocks"]:
        if b.get("type")!=0: continue
        br=fitz.Rect(b["bbox"])
        txt=b.get("lines",[])
        raw=""
        for ln in txt:
            raw += " ".join(sp["text"] for sp in ln.get("spans",[]))+" "
        raw=raw.strip()
        if not raw or len(raw)>180: continue
        # texto dentro ou imediatamente colado ao visual
        near=fitz.Rect(expanded.x0-10,expanded.y0-12,expanded.x1+10,expanded.y1+18)
        if near.intersects(br) and (br & reg).get_area()>0:
            # não inclui cabeçalho/alternativas
            if re.match(r"^\(?[A-E]\)?[\s.)]",raw): continue
            if "Questão" in raw or "Questao" in raw: continue
            nr=expanded|br
            if nr.get_area()<reg.get_area()*.78:
                expanded=nr

    return pi,expanded,mode

def save_crop(page,rect,out):
    rect &= page.rect
    pix=page.get_pixmap(matrix=fitz.Matrix(3,3),clip=rect,alpha=False)
    img=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
    # remove apenas borda branca externa; não altera nem redesenha o conteúdo.
    bg=Image.new("RGB",img.size,"white")
    diff=ImageChops.difference(img,bg).convert("L")
    bb=diff.point(lambda x: 255 if x>12 else 0).getbbox()
    if bb:
        pad=10
        bb=(max(0,bb[0]-pad),max(0,bb[1]-pad),min(img.width,bb[2]+pad),min(img.height,bb[3]+pad))
        img=img.crop(bb)
    out.parent.mkdir(parents=True,exist_ok=True)
    img.save(out,"PNG",optimize=True)
    return img.size

paths=sorted(Path("imagens/fatec").glob("*/*/questao_*.png"))
byed={}
for p in paths:
    parsed=parse_path(p)
    if parsed: byed.setdefault(parsed[0],[]).append((parsed[1],p))

report=[]
for ed,items in sorted(byed.items()):
    if ed not in SOURCES:
        report += [{"edicao":ed,"questao":q,"status":"fonte_ausente","path":str(p)} for q,p in items]
        continue
    resp=session.get(SOURCES[ed],timeout=120)
    resp.raise_for_status()
    if not resp.content.startswith(b"%PDF"): raise RuntimeError(f"{ed}: fonte inválida")
    doc=fitz.open(stream=resp.content,filetype="pdf")
    maxq=max(q for q,_ in items)
    qmap,hrect=build_map(doc,maxq)
    for q,p in items:
        pi,box,mode=choose_bbox(doc,ed,q,qmap,hrect)
        if box is None:
            report.append({"edicao":ed,"questao":q,"status":"nao_recortado","modo":mode,"path":str(p)})
            continue
        size=save_crop(doc[pi],box,p)
        report.append({"edicao":ed,"questao":q,"status":"recortado","modo":mode,"path":str(p),"pagina":pi+1,"rect":[round(v,2) for v in (box.x0,box.y0,box.x1,box.y1)],"width":size[0],"height":size[1]})
    print(ed,"ok",len(items))

import json
Path("auditorias").mkdir(exist_ok=True)
Path("auditorias/fatec_recortes_v5.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print("TOTAL",len(report),"nao_recortado",sum(x["status"]!="recortado" for x in report))
