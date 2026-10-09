from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import re, math

ROOT = Path("imagens/fatec")
OUT = Path("auditorias/fatec_contact_sheets")
OUT.mkdir(parents=True, exist_ok=True)

for old in OUT.glob("*.jpg"):
    old.unlink()

files = sorted(ROOT.glob("**/questao_*.png"))
by_year = {}
for p in files:
    m = re.search(r"imagens/fatec/(\d{4})/", str(p))
    if m:
        by_year.setdefault(m.group(1), []).append(p)

CELL_W, CELL_H = 700, 520
COLS, ROWS = 4, 4
PER = COLS * ROWS

try:
    font = ImageFont.truetype("DejaVuSans.ttf", 23)
    small = ImageFont.truetype("DejaVuSans.ttf", 18)
except Exception:
    font = ImageFont.load_default()
    small = font

for year, paths in sorted(by_year.items()):
    for page_idx in range(math.ceil(len(paths)/PER)):
        subset = paths[page_idx*PER:(page_idx+1)*PER]
        sheet = Image.new("RGB", (CELL_W*COLS, CELL_H*ROWS), "white")
        draw = ImageDraw.Draw(sheet)
        for i,p in enumerate(subset):
            r,c = divmod(i,COLS)
            x0,y0 = c*CELL_W, r*CELL_H
            draw.rectangle((x0+2,y0+2,x0+CELL_W-3,y0+CELL_H-3),outline="gray",width=2)
            try:
                im = Image.open(p).convert("RGB")
                ow,oh = im.size
                box_h = CELL_H-80
                ratio = min((CELL_W-30)/ow, (box_h-20)/oh, 1.0)
                nw,nh = max(1,int(ow*ratio)),max(1,int(oh*ratio))
                thumb = im.resize((nw,nh), Image.Resampling.LANCZOS)
                tx = x0+(CELL_W-nw)//2
                ty = y0+48+(box_h-nh)//2
                sheet.paste(thumb,(tx,ty))
                label = str(p).replace("imagens/fatec/","")
                draw.text((x0+10,y0+8),label,fill="black",font=font)
                draw.text((x0+10,y0+CELL_H-28),f"{ow}x{oh}",fill="black",font=small)
            except Exception as e:
                draw.text((x0+10,y0+70),f"ERRO {e}",fill="black",font=font)
        out=OUT/f"{year}_{page_idx+1:02d}.jpg"
        sheet.save(out,quality=90,optimize=True)
        print(out)
