from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import math, json, re

files=sorted(Path("imagens/fatec").glob("**/*.png"))
thumb_w, thumb_h = 360, 260
cols, rows = 4, 4
cell_w, cell_h = 390, 310
sheet_w, sheet_h = cols*cell_w, rows*cell_h
outdir=Path("auditorias/fatec_contact_sheets")
outdir.mkdir(parents=True, exist_ok=True)

manifest=[]
for idx,p in enumerate(files):
    try:
        im=Image.open(p).convert("RGB")
    except Exception:
        continue
    manifest.append({"index":idx,"path":str(p),"width":im.width,"height":im.height})
    sheet_no=idx//(cols*rows)
    pos=idx%(cols*rows)
    sheet_path=outdir/f"sheet_{sheet_no+1:03d}.jpg"
    if sheet_path.exists():
        sheet=Image.open(sheet_path).convert("RGB")
    else:
        sheet=Image.new("RGB",(sheet_w,sheet_h),"white")
    im.thumbnail((thumb_w,thumb_h))
    x=(pos%cols)*cell_w+(cell_w-im.width)//2
    y=(pos//cols)*cell_h+35+(thumb_h-im.height)//2
    sheet.paste(im,(x,y))
    d=ImageDraw.Draw(sheet)
    label=str(p).replace("imagens/fatec/","")
    d.text(((pos%cols)*cell_w+6,(pos//cols)*cell_h+6),label,fill="black")
    d.rectangle(((pos%cols)*cell_w,(pos//cols)*cell_h,(pos%cols+1)*cell_w-1,(pos//cols+1)*cell_h-1),outline="gray")
    sheet.save(sheet_path,quality=88)

Path("auditorias/fatec_contact_sheets_manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
print("imagens",len(manifest),"pranchas",math.ceil(len(manifest)/(cols*rows)))

# trigger audit
