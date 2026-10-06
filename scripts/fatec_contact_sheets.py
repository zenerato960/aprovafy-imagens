from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import math

ROOT = Path("imagens/fatec")
OUT = Path("auditorias/fatec_contact_sheets")
OUT.mkdir(parents=True, exist_ok=True)

paths = sorted(ROOT.glob("*/*/questao_*.png"))
thumb_w, thumb_h = 360, 270
label_h = 34
cols, rows = 4, 4
per = cols * rows

font = ImageFont.load_default()

for si in range(math.ceil(len(paths)/per)):
    batch = paths[si*per:(si+1)*per]
    sheet = Image.new("RGB", (cols*thumb_w, rows*(thumb_h+label_h)), "white")
    d = ImageDraw.Draw(sheet)
    for j,p in enumerate(batch):
        r, c = divmod(j, cols)
        img = Image.open(p).convert("RGB")
        fitted = ImageOps.contain(img, (thumb_w-12, thumb_h-12))
        x = c*thumb_w + (thumb_w-fitted.width)//2
        y = r*(thumb_h+label_h) + (thumb_h-fitted.height)//2
        sheet.paste(fitted, (x,y))
        label = str(p.relative_to(ROOT))
        d.rectangle((c*thumb_w, r*(thumb_h+label_h)+thumb_h, (c+1)*thumb_w-1, r*(thumb_h+label_h)+thumb_h+label_h-1), fill="white")
        d.text((c*thumb_w+6, r*(thumb_h+label_h)+thumb_h+8), label, fill="black", font=font)
        d.rectangle((c*thumb_w, r*(thumb_h+label_h), (c+1)*thumb_w-1, (r+1)*(thumb_h+label_h)-1), outline="black", width=1)
    out = OUT / f"sheet_{si+1:02d}.jpg"
    sheet.save(out, quality=88, optimize=True)
print("imagens", len(paths), "sheets", math.ceil(len(paths)/per))

# trigger audit
