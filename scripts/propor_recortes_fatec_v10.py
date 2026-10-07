from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import cv2, numpy as np, math, shutil

src=Path("auditorias/fatec_v9")
out=Path("auditorias/fatec_v10")
sheets=Path("auditorias/fatec_v10_sheets")
for d in (out,sheets):
    if d.exists(): shutil.rmtree(d)
    d.mkdir(parents=True,exist_ok=True)

def choose_panel(im):
    arr=np.array(im.convert("RGB")); H,W=arr.shape[:2]
    gray=cv2.cvtColor(arr,cv2.COLOR_RGB2GRAY)
    candidates=[]

    # 1. Large filled/toned panels (photos, gray source boxes, scans).
    fg=(gray<247).astype(np.uint8)*255
    # merge content inside the same block.
    filled=cv2.morphologyEx(fg,cv2.MORPH_CLOSE,np.ones((17,17),np.uint8),iterations=2)
    n,lab,stats,_=cv2.connectedComponentsWithStats(filled,8)
    for i in range(1,n):
        x,y,w,h,area=stats[i]; A=w*h
        if w<80 or h<55 or A<.08*W*H or A>.93*W*H: continue
        # Require either toned background/photo or reasonably dense drawing.
        roi=gray[y:y+h,x:x+w]
        nonwhite=np.mean(roi<242)
        edges=np.mean(cv2.Canny(roi,70,160)>0)
        if nonwhite>.055 or edges>.035:
            score=A*(0.7+min(nonwhite,0.5)*2+min(edges,0.2)*2)
            candidates.append((score,x,y,x+w,y+h,"filled"))

    # 2. Rectangular frame / table candidates from long lines.
    bw=(gray<180).astype(np.uint8)*255
    hor=cv2.morphologyEx(bw,cv2.MORPH_OPEN,np.ones((max(25,W//12),1),np.uint8))
    ver=cv2.morphologyEx(bw,cv2.MORPH_OPEN,np.ones((1,max(20,H//12)),np.uint8))
    lines=cv2.bitwise_or(hor,ver)
    if np.any(lines):
        ys,xs=np.where(lines>0)
        if len(xs):
            x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
            ww,hh=x1-x0+1,y1-y0+1; A=ww*hh
            if ww>100 and hh>50 and .04*W*H<A<.90*W*H:
                # line cluster may cover alternatives; connected subclusters are also considered
                candidates.append((A*1.05,x0,y0,x1+1,y1+1,"lines-all"))
        n2,lab2,stats2,_=cv2.connectedComponentsWithStats(cv2.dilate(lines,np.ones((15,15),np.uint8)),8)
        for i in range(1,n2):
            x,y,w,h,area=stats2[i];A=w*h
            if w>100 and h>50 and .04*W*H<A<.88*W*H:
                candidates.append((A*1.15,x,y,x+w,y+h,"lines"))

    # 3. External contours that enclose a meaningful panel.
    contours,_=cv2.findContours(bw,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        x,y,w,h=cv2.boundingRect(c); A=w*h
        if w>100 and h>50 and .06*W*H<A<.88*W*H:
            peri=cv2.arcLength(c,True)
            approx=cv2.approxPolyDP(c,.02*peri,True) if peri else []
            if 3<=len(approx)<=12:
                candidates.append((A*1.1,x,y,x+w,y+h,"contour"))

    if not candidates: return (0,0,W,H,"full")
    candidates.sort(reverse=True,key=lambda z:z[0])
    _,x0,y0,x1,y1,mode=candidates[0]

    # Padding. If candidate is mostly a prompt block touching edge, be conservative.
    px=max(5,int(W*.012)); py=max(5,int(H*.012))
    x0=max(0,x0-px);y0=max(0,y0-py);x1=min(W,x1+px);y1=min(H,y1+py)
    if (x1-x0)*(y1-y0)>.90*W*H:
        return (0,0,W,H,"full")
    return (x0,y0,x1,y1,mode)

records=[]
for p in sorted(src.rglob("questao_*.png")):
    im=Image.open(p).convert("RGB")
    x0,y0,x1,y1,mode=choose_panel(im)
    cropped=im.crop((x0,y0,x1,y1))
    o=out/p.relative_to(src);o.parent.mkdir(parents=True,exist_ok=True);cropped.save(o,optimize=True)
    records.append((p,o,(x0,y0,x1,y1),mode,im.size,cropped.size))

cell_w,cell_h=420,360; cols,rows=4,5;per=cols*rows;font=ImageFont.load_default()
for si in range(math.ceil(len(records)/per)):
    can=Image.new("RGB",(cols*cell_w,rows*cell_h),"white");d=ImageDraw.Draw(can)
    for j,(p,o,box,mode,osz,nsz) in enumerate(records[si*per:(si+1)*per]):
        rr,cc=divmod(j,cols);X=cc*cell_w;Y=rr*cell_h
        a=ImageOps.contain(Image.open(p).convert("RGB"),(cell_w-10,145)); b=ImageOps.contain(Image.open(o).convert("RGB"),(cell_w-10,145))
        can.paste(a,(X+(cell_w-a.width)//2,Y+5));can.paste(b,(X+(cell_w-b.width)//2,Y+165))
        d.line((X,Y+158,X+cell_w,Y+158),fill="gray")
        d.text((X+5,Y+315),str(p).replace("auditorias/fatec_v9/",""),fill="black",font=font)
        d.text((X+5,Y+330),f"{mode} {osz}->{nsz}",fill="black",font=font)
        d.rectangle((X,Y,X+cell_w-1,Y+cell_h-1),outline="gray")
    can.save(sheets/f"sheet_{si+1:02d}.jpg",quality=88)
print("DONE",len(records))
