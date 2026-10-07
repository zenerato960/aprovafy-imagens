from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import cv2, numpy as np, math, shutil

src=Path("auditorias/fatec_v7")
out=Path("auditorias/fatec_v8")
sheets=Path("auditorias/fatec_v8_sheets")
for d in (out,sheets):
    if d.exists(): shutil.rmtree(d)
    d.mkdir(parents=True,exist_ok=True)

def inner_bbox(im):
    arr=np.array(im.convert("RGB"))
    gray=cv2.cvtColor(arr,cv2.COLOR_RGB2GRAY)
    mask=(gray<244).astype(np.uint8)*255
    H,W=mask.shape

    # close small gaps so table borders, axes, boxes and multi-panel drawings become coherent
    m=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8),iterations=1)
    n,lab,stats,_=cv2.connectedComponentsWithStats(m,8)
    comps=[]
    for i in range(1,n):
        x,y,w,h,area=stats[i]
        if area<80 or w<10 or h<8: continue
        # discard separators and isolated body-text lines
        if (w>.88*W and h<16) or (h>.88*H and w<9): continue
        dens=area/max(1,w*h)
        score=area*(1+min(h/H,.8)*4)*(1+min(w/W,.8)*1.2)
        if h<24 and dens<.48: score*=.18
        comps.append([score,x,y,x+w,y+h,area,dens])
    if not comps: return (0,0,W,H)
    comps.sort(reverse=True)
    _,x0,y0,x1,y1,_,_=comps[0]

    # grow into components that are clearly part of the same visual.
    changed=True
    while changed:
        changed=False
        for c in comps[1:]:
            _,a0,b0,a1,b1,area,dens=c
            gapx=max(0,max(x0,a0)-min(x1,a1))
            gapy=max(0,max(y0,b0)-min(y1,b1))
            ovx=max(0,min(x1,a1)-max(x0,a0))
            ovy=max(0,min(y1,b1)-max(y0,b0))
            # labels/panels near a graph are included; distant prompt text is not
            if (gapx<32 and gapy<32) or (ovx>.3*min(x1-x0,a1-a0) and gapy<44) or (ovy>.3*min(y1-y0,b1-b0) and gapx<44):
                nx0,ny0,nx1,ny1=min(x0,a0),min(y0,b0),max(x1,a1),max(y1,b1)
                if (nx1-nx0)*(ny1-ny0)<.90*W*H and (nx0,ny0,nx1,ny1)!=(x0,y0,x1,y1):
                    x0,y0,x1,y1=nx0,ny0,nx1,ny1;changed=True

    # Prefer an enclosing graphical contour (box/table/photo) when present.
    contours,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    best=None
    for cnt in contours:
        bx,by,bw,bh=cv2.boundingRect(cnt)
        if bw<40 or bh<25: continue
        if bx<=x0+12 and by<=y0+12 and bx+bw>=x1-12 and by+bh>=y1-12:
            if bw*bh<.90*W*H:
                if best is None or bw*bh>best[2]*best[3]:
                    best=(bx,by,bw,bh)
    if best:
        bx,by,bw,bh=best;x0,y0,x1,y1=bx,by,bx+bw,by+bh

    pad=max(5,int(min(W,H)*.012))
    x0=max(0,x0-pad);y0=max(0,y0-pad);x1=min(W,x1+pad);y1=min(H,y1+pad)
    if (x1-x0)*(y1-y0)<.025*W*H:
        return (0,0,W,H)
    return (x0,y0,x1,y1)

records=[]
for p in sorted(src.rglob("questao_*.png")):
    im=Image.open(p).convert("RGB")
    box=inner_bbox(im)
    cropped=im.crop(box)
    o=out/p.relative_to(src);o.parent.mkdir(parents=True,exist_ok=True);cropped.save(o,optimize=True)
    records.append((p,o,box,im.size,cropped.size))

cell_w,cell_h=420,360;cols,rows=4,5;per=cols*rows
font=ImageFont.load_default()
for si in range(math.ceil(len(records)/per)):
    batch=records[si*per:(si+1)*per]
    can=Image.new("RGB",(cols*cell_w,rows*cell_h),"white");d=ImageDraw.Draw(can)
    for j,(p,o,box,osz,nsz) in enumerate(batch):
        rr,cc=divmod(j,cols);X=cc*cell_w;Y=rr*cell_h
        a=ImageOps.contain(Image.open(p).convert("RGB"),(cell_w-10,145))
        b=ImageOps.contain(Image.open(o).convert("RGB"),(cell_w-10,145))
        can.paste(a,(X+(cell_w-a.width)//2,Y+5));can.paste(b,(X+(cell_w-b.width)//2,Y+165))
        d.line((X,Y+158,X+cell_w,Y+158),fill="gray")
        d.text((X+5,Y+315),str(p).replace("auditorias/fatec_v7/",""),fill="black",font=font)
        d.text((X+5,Y+330),f"{osz}->{nsz} box={box}",fill="black",font=font)
        d.rectangle((X,Y,X+cell_w-1,Y+cell_h-1),outline="gray")
    can.save(sheets/f"sheet_{si+1:02d}.jpg",quality=88)
print("DONE",len(records))
