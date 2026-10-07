from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import math

root = Path("imagens/fatec")
files = sorted(root.rglob("questao_*.png"))
outdir = Path("auditorias/fatec_contact_sheets")
outdir.mkdir(parents=True, exist_ok=True)
for p in outdir.glob("sheet_*.jpg"):
    p.unlink()

thumb_w, thumb_h = 420, 280
label_h = 48
cols, rows = 4, 5
per = cols * rows
font = ImageFont.load_default()

for si in range(math.ceil(len(files)/per)):
    batch = files[si*per:(si+1)*per]
    canvas = Image.new("RGB", (cols*thumb_w, rows*(thumb_h+label_h)), "white")
    draw = ImageDraw.Draw(canvas)
    for j,p in enumerate(batch):
        r,c = divmod(j, cols)
        im = Image.open(p).convert("RGB")
        fitted = ImageOps.contain(im, (thumb_w-12, thumb_h-12))
        x = c*thumb_w + (thumb_w-fitted.width)//2
        y = r*(thumb_h+label_h) + (thumb_h-fitted.height)//2
        canvas.paste(fitted, (x,y))
        draw.rectangle([c*thumb_w, r*(thumb_h+label_h), (c+1)*thumb_w-1, (r+1)*(thumb_h+label_h)-1], outline="gray")
        label = str(p).replace("imagens/fatec/","")
        draw.text((c*thumb_w+6, r*(thumb_h+label_h)+thumb_h+4), label, fill="black", font=font)
    out = outdir / f"sheet_{si+1:02d}.jpg"
    canvas.save(out, quality=90)
print("FILES", len(files), "SHEETS", math.ceil(len(files)/per))
