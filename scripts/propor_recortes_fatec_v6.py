from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import cv2, numpy as np, math, shutil

src_root = Path("imagens/fatec")
prop_root = Path("auditorias/fatec_proposed")
sheet_root = Path("auditorias/fatec_proposed_sheets")
if prop_root.exists(): shutil.rmtree(prop_root)
if sheet_root.exists(): shutil.rmtree(sheet_root)
prop_root.mkdir(parents=True, exist_ok=True)
sheet_root.mkdir(parents=True, exist_ok=True)

def smart_bbox(im):
    arr=np.array(im.convert("RGB"))
    gray=cv2.cvtColor(arr,cv2.COLOR_RGB2GRAY)
    # foreground
    mask=(gray<244).astype(np.uint8)*255
    # suppress isolated speckle
    mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,np.ones((2,2),np.uint8))
    # connect graphical structures but avoid merging body text too aggressively
    m1=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,np.ones((5,5),np.uint8),iterations=1)
    n,lab,stats,_=cv2.connectedComponentsWithStats(m1,8)
    H,W=mask.shape
    comps=[]
    for i in range(1,n):
        x,y,w,h,area=stats[i]
        if area<120 or w<18 or h<14: continue
        # horizontal/vertical separators, page borders
        if (w>.90*W and h<18) or (h>.90*H and w<12): continue
        density=area/max(1,w*h)
        # text lines tend to be shallow; visual regions tend to have more vertical extent
        score=area*(1+min(h,220)/55)*(1+min(w,500)/300)
        if h<28 and density<0.55:
            score*=0.18
        comps.append([score,x,y,w,h,area,density])
    if not comps:
        return (0,0,W,H)
    comps.sort(reverse=True)
    seed=comps[0]
    _,x,y,w,h,_,_=seed
    ux0,uy0,ux1,uy1=x,y,x+w,y+h

    # grow around the dominant visual object. Nearby components often belong to
    # labels, legends, panels or separate pieces of the same diagram.
    changed=True
    while changed:
        changed=False
        for c in comps[1:]:
            _,x,y,w,h,area,dens=c
            cx0,cy0,cx1,cy1=x,y,x+w,y+h
            gapx=max(0,max(ux0,cx0)-min(ux1,cx1))
            gapy=max(0,max(uy0,cy0)-min(uy1,cy1))
            overlapx=max(0,min(ux1,cx1)-max(ux0,cx0))
            overlapy=max(0,min(uy1,cy1)-max(uy0,cy0))
            close=(gapx<=max(28,int(.055*W)) and gapy<=max(24,int(.055*H)))
            aligned=((overlapx>0.25*min(ux1-ux0,cx1-cx0)) and gapy<70) or ((overlapy>0.25*min(uy1-uy0,cy1-cy0)) and gapx<70)
            if close or aligned:
                nx0,ny0,nx1,ny1=min(ux0,cx0),min(uy0,cy0),max(ux1,cx1),max(uy1,cy1)
                # avoid swallowing almost the entire screenshot just because body text is nearby
                if (nx1-nx0)*(ny1-ny0) <= .90*W*H:
                    if (nx0,ny0,nx1,ny1)!=(ux0,uy0,ux1,uy1):
                        ux0,uy0,ux1,uy1=nx0,ny0,nx1,ny1; changed=True

    # If a strong rectangular border/table encloses the seed, use its bounds.
    contours,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        bx,by,bw,bh=cv2.boundingRect(cnt)
        if bw<40 or bh<25: continue
        if bx<=ux0+10 and by<=uy0+10 and bx+bw>=ux1-10 and by+bh>=uy1-10:
            if bw*bh < .88*W*H:
                ux0,uy0,ux1,uy1=bx,by,bx+bw,by+bh

    pad=max(5,int(min(W,H)*.012))
    x0=max(0,ux0-pad); y0=max(0,uy0-pad)
    x1=min(W,ux1+pad); y1=min(H,uy1+pad)
    area=(x1-x0)*(y1-y0)
    # don't overcrop tiny ambiguous components
    if area < .035*W*H:
        return (0,0,W,H)
    # if change is negligible, retain exact original
    if x0<8 and y0<8 and x1>W-8 and y1>H-8:
        return (0,0,W,H)
    return (x0,y0,x1,y1)

files=sorted(src_root.rglob("questao_*.png"))
records=[]
for p in files:
    im=Image.open(p).convert("RGB")
    box=smart_bbox(im)
    out=prop_root / p.relative_to(src_root)
    out.parent.mkdir(parents=True,exist_ok=True)
    cropped=im.crop(box)
    cropped.save(out,optimize=True)
    records.append((p,out,box,im.size,cropped.size))

# comparison sheets: original above / proposal below
cell_w,cell_h=420,360
cols,rows=4,5
per=cols*rows
font=ImageFont.load_default()
for si in range(math.ceil(len(records)/per)):
    batch=records[si*per:(si+1)*per]
    canvas=Image.new("RGB",(cols*cell_w,rows*cell_h),"white")
    d=ImageDraw.Draw(canvas)
    for j,(p,out,box,orig_sz,new_sz) in enumerate(batch):
        rr,cc=divmod(j,cols)
        x0=cc*cell_w; y0=rr*cell_h
        orig=Image.open(p).convert("RGB")
        new=Image.open(out).convert("RGB")
        a=ImageOps.contain(orig,(cell_w-10,145))
        b=ImageOps.contain(new,(cell_w-10,145))
        canvas.paste(a,(x0+(cell_w-a.width)//2,y0+5))
        canvas.paste(b,(x0+(cell_w-b.width)//2,y0+165))
        d.line((x0,y0+158,x0+cell_w,y0+158),fill="gray")
        label=str(p).replace("imagens/fatec/","")
        d.text((x0+5,y0+315),label,fill="black",font=font)
        d.text((x0+5,y0+330),f"{orig_sz}->{new_sz} box={box}",fill="black",font=font)
        d.rectangle((x0,y0,x0+cell_w-1,y0+cell_h-1),outline="gray")
    canvas.save(sheet_root/f"sheet_{si+1:02d}.jpg",quality=88)

print("FILES",len(records),"SHEETS",math.ceil(len(records)/per))
