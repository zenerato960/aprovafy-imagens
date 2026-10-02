from pathlib import Path
from io import BytesIO
import requests
import fitz
from PIL import Image

SOURCES = {
    '2010_2': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2021/09/prova-vestibular-2s-2010.pdf',
    '2011_1': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2021/09/prova-vestibular-1s-2011.pdf',
    '2013_1': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2021/09/prova-vestibular-1s-2013.pdf',
    '2014_1': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2021/09/prova-vestibular-1s-2014.pdf',
    '2019_1': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2018/12/prova-vestibular-1sem-2019.pdf',
    '2022_2': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2022/07/caderno_lar_2_sem_2022.pdf',
    '2025_2': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2025/07/prova-vestibular-2-sem-2025.pdf',
}

# Coordenadas em pixels depois de renderizar a página em 2x.
# Os recortes foram conferidos visualmente contra os cadernos oficiais.
CROPS = [
    ('2010_2', 18, (90, 35, 1110, 1385), 'imagens/fatec/2010/2sem/questao_047.png'),
    ('2011_1', 7,  (40, 20, 1150, 900),  'imagens/fatec/2011/1sem/questao_023.png'),
    ('2011_1', 7,  (40, 900, 1150, 1360), 'imagens/fatec/2011/1sem/questao_024.png'),
    ('2013_1', 2,  (25, 760, 1145, 1425), 'imagens/fatec/2013/1sem/questao_005.png'),
    ('2014_1', 5,  (30, 25, 1160, 820),   'imagens/fatec/2014/1sem/questao_010.png'),
    ('2019_1', 5,  (575, 20, 1180, 1450), 'imagens/fatec/2019/1sem/questao_012.png'),
    ('2022_2', 17, (25, 15, 1160, 700),   'imagens/fatec/2022/2sem/questao_044.png'),
    ('2025_2', 14, (20, 780, 1140, 1415), 'imagens/fatec/2025/2sem/questao_041.png'),
]

session = requests.Session()
session.headers['User-Agent'] = 'Mozilla/5.0 FATEC archive publisher'
cache = {}

for edicao, page_index, crop_box, output_path in CROPS:
    if edicao not in cache:
        response = session.get(SOURCES[edicao], timeout=120)
        response.raise_for_status()
        if not response.content.startswith(b'%PDF'):
            raise RuntimeError(f'{edicao}: fonte não retornou PDF')
        cache[edicao] = fitz.open(stream=response.content, filetype='pdf')

    doc = cache[edicao]
    page = doc[page_index]
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
    img = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    img = img.crop(crop_box)

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, format='PNG', optimize=True)
    if out.stat().st_size < 5000:
        raise RuntimeError(f'{output_path}: arquivo gerado parece inválido')
    print(output_path, img.size, out.stat().st_size)
