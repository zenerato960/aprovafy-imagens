# auditoria final pos-recortes 2026-10-07
from pathlib import Path
import json, math
import cv2
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFont

ROOT=Path("imagens/fatec")
OUT=Path("auditoria_visual_fatec")
OUT.mkdir(exist_ok=True)
records=[]

def weighted_median(vals):
    if not vals: return 0.0
    vals=sorted(vals,key=lambda x:x[0])
    total=sum(w for _,w in vals); acc=0
    for v,w in vals:
        acc+=w
        if acc>=total/2: return float(v)
    return float(vals[-1][0])

for p in sorted(ROOT.rglob("*.png")):
    try:
        im=Image.open(p).convert("RGB")
    except Exception:
        continue
    a=np.array(im)
    h,w=a.shape[:2]
    gray=cv2.cvtColor(a,cv2.COLOR_RGB2GRAY)
    ink=gray<245
    if ink.any():
        ys,xs=np.where(ink)
        x0,x1=int(xs.min()),int(xs.max())
        y0,y1=int(ys.min()),int(ys.max())
    else:
        x0=y0=0; x1=w-1; y1=h-1
    margins={"left":x0,"right":w-1-x1,"top":y0,"bottom":h-1-y1}
    edges=cv2.Canny(gray,60,160)
    lines=cv2.HoughLinesP(edges,1,np.pi/180,threshold=max(35,w//8),minLineLength=max(60,int(w*0.35)),maxLineGap=20)
    angles=[]
    if lines is not None:
        arr_lines = lines.reshape(-1, 4)
        for ln in arr_lines:
            xA,yA,xB,yB=map(int,ln)
            dx=xB-xA; dy=yB-yA
            length=(dx*dx+dy*dy)**0.5
            if length<max(60,w*0.35): continue
            ang=math.degrees(math.atan2(dy,dx))
            while ang>90: ang-=180
            while ang<-90: ang+=180
            if abs(ang)<=6:
                angles.append((ang,length))
    skew=weighted_median(angles)
    horiz_weight=sum(l for _,l in angles)
    touches=[k for k,v in margins.items() if v<=2]
    clip_flag=(len(touches)>=1 and (margins["left"]<=2 or margins["right"]<=2) and w>120 and h>60)
    skew_flag=(abs(skew)>=0.65 and horiz_weight>=w*0.9)
    extreme=(w/h>7.5 or h/w>7.5)
    flagged=bool(clip_flag or skew_flag or extreme)
    records.append({
        "path":str(p),"width":w,"height":h,"margins":margins,
        "skew_deg":round(skew,3),"horiz_weight":round(horiz_weight,1),
        "clip_flag":bool(clip_flag),"skew_flag":bool(skew_flag),
        "extreme_aspect":bool(extreme),"flagged":flagged
    })

(OUT/"report.json").write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding="utf-8")
flagged=[r for r in records if r["flagged"]]
(OUT/"flagged.txt").write_text("\n".join(r["path"] for r in flagged),encoding="utf-8")
print("total",len(records),"flagged",len(flagged))

font=ImageFont.load_default()
cell_w,cell_h=760,480
cols,rows=3,4
for s in range(0,len(flagged),cols*rows):
    subset=flagged[s:s+cols*rows]
    sheet=Image.new("RGB",(cols*cell_w,rows*cell_h),"white")
    d=ImageDraw.Draw(sheet)
    for j,r in enumerate(subset):
        p=Path(r["path"])
        im=Image.open(p).convert("RGB")
        thumb=ImageOps.contain(im,(cell_w-30,cell_h-80))
        x=(j%cols)*cell_w+(cell_w-thumb.width)//2
        y=(j//cols)*cell_h+50+(cell_h-80-thumb.height)//2
        sheet.paste(thumb,(x,y))
        label=f'{p} | {r["width"]}x{r["height"]} | skew={r["skew_deg"]} | margins={r["margins"]}'
        d.text(((j%cols)*cell_w+8,(j//cols)*cell_h+8),label,fill="black",font=font)
    sheet.save(OUT/f"flagged_{s//(cols*rows)+1:02d}.jpg",quality=88)


# Folhas de contato de TODAS as imagens, para revisão visual integral e não apenas
# dos casos que a heurística marcou como suspeitos.
for s0 in range(0,len(records),cols*rows):
    subset=records[s0:s0+cols*rows]
    sheet=Image.new("RGB",(cols*cell_w,rows*cell_h),"white")
    d=ImageDraw.Draw(sheet)
    for j,r in enumerate(subset):
        p=Path(r["path"])
        im=Image.open(p).convert("RGB")
        thumb=ImageOps.contain(im,(cell_w-30,cell_h-80))
        x=(j%cols)*cell_w+(cell_w-thumb.width)//2
        y=(j//cols)*cell_h+50+(cell_h-80-thumb.height)//2
        sheet.paste(thumb,(x,y))
        label=f'{p} | {r["width"]}x{r["height"]} | skew={r["skew_deg"]}'
        d.text(((j%cols)*cell_w+8,(j//cols)*cell_h+8),label,fill="black",font=font)
    sheet.save(OUT/f"all_{s0//(cols*rows)+1:02d}.jpg",quality=88)

# reaudit 2026-10-09
