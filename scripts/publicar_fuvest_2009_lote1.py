from pathlib import Path
from io import BytesIO
import requests
import fitz

URL='https://www.fuvest.br/wp-content/uploads/fuvest_2009_1fase_prova_V.pdf'
OUT=Path('imagens/fuvest/2009')
OUT.mkdir(parents=True, exist_ok=True)

r=requests.get(URL, timeout=120, headers={'User-Agent':'Mozilla/5.0 Aprovafy/1.0'})
r.raise_for_status()
doc=fitz.open(stream=r.content, filetype='pdf')

# page is zero-based; coordinates are PDF points, validated against the official caderno.
CROPS={
    1:(1,(64.92,149.40,298.72,306.90)),
    8:(3,(80.94,66.36,282.99,433.98)),
    10:(4,(120.18,59.46,243.79,192.66)),
}

for q,(page_no,box) in CROPS.items():
    page=doc[page_no]
    pix=page.get_pixmap(matrix=fitz.Matrix(2.5,2.5), clip=fitz.Rect(*box), alpha=False)
    dest=OUT/f'questao_{q:03d}.png'
    pix.save(dest)
    print(dest, dest.stat().st_size)
