from pathlib import Path
import re
import requests
import fitz
from PIL import Image

SOURCES = {
    '2009_1': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2021/09/Prova_2009_1_SEM.pdf',
    '2009_2': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2021/09/prova-vestibular-2s-2009.pdf',
    '2010_1': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2021/09/prova-vestibular-1s-2010.pdf',
    '2010_2': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2021/09/prova-vestibular-2s-2010.pdf',
    '2011_1': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2021/09/prova-vestibular-1s-2011.pdf',
    '2011_2': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2021/09/prova-vestibular-2s-2011.pdf',
    '2012_1': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2021/09/prova-vestibular-1s-2012.pdf',
    '2012_2': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2021/09/prova-vestibular-2s-2012.pdf',
    '2013_1': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2021/09/prova-vestibular-1s-2013.pdf',
    '2013_2': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2021/09/prova-vestibular-2s-2013.pdf',
    '2014_1': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2021/09/prova-vestibular-1s-2014.pdf',
    '2014_2': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2021/09/prova-vestibular-2s-2014.pdf',
    '2015_1': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2021/09/prova-vestibular-1s-2015.pdf',
    '2015_2': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2021/09/prova-vestibular-2s-2015.pdf',
    '2016_1': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2021/09/prova-vestibular-1s-2016.pdf',
    '2016_2': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2021/09/prova-vestibular-2s-2016.pdf',
    '2017_1': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2017/10/prova_1_semestre.pdf',
    '2017_2': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2017/10/Prova.pdf',
    '2018_1': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2018/01/prova-vestibular-1sem-2018.pdf',
    '2018_2': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2018/07/ProvaVestibular.pdf',
    '2019_1': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2018/12/prova-vestibular-1sem-2019.pdf',
    '2019_2': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2019/06/prova-vestibular-2sem-2019.pdf',
    '2020_1': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2019/12/prova-vestibular-1sem-2020.pdf',
    '2022_2': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2022/07/caderno_lar_2_sem_2022.pdf',
    '2023_1': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2023/01/Caderno-Vestibular-1sem-2023.pdf',
    '2023_2': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2023/06/Caderno-Vestibular-2SEM2023.pdf',
    '2024_1': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2024/01/CADERNO-FATEC-1SEM-2024.pdf',
    '2024_2': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2024/07/CADERNO-FATEC-2-SEM2024.pdf',
    '2025_1_A': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2025/01/2025-vestibular-1-semestre-prova-a.pdf',
    '2025_1_B': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2025/01/2025-vestibular-1-semestre-prova-b.pdf',
    '2025_2': 'https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/1/2025/07/prova-vestibular-2-sem-2025.pdf',
}

CANDIDATES = {
    '2009_1': [2, 3, 6, 11, 21, 27, 28, 29, 36, 38, 39, 40],
    '2009_2': [3, 5, 7, 27, 29, 30, 35, 37, 41, 47, 48],
    '2010_1': [2, 4, 5, 19, 23, 24, 29, 30, 39, 42, 43, 45],
    '2010_2': [4, 20, 21, 25, 26, 30, 33, 39, 47, 54],
    '2011_1': [1, 6, 23, 25, 26, 29, 36, 37, 38],
    '2011_2': [9, 16, 18, 19, 21, 23, 25, 27, 30, 37, 39, 50, 51, 52, 53, 54],
    '2012_1': [4, 8, 9, 13, 19, 30, 34, 37, 40, 41, 44, 46],
    '2012_2': [1, 2, 10, 31, 34, 36, 39, 40, 43, 49, 50],
    '2013_1': [2, 5, 9, 10, 11, 14, 19, 20, 22, 23, 31, 33, 34, 41, 42],
    '2013_2': [9, 10, 13, 18, 20, 21, 24, 30, 31, 32, 34, 39, 40, 43, 45, 47, 53],
    '2014_1': [1, 2, 3, 5, 8, 10, 12, 19, 22, 26, 31, 39, 40, 46],
    '2014_2': [2, 10, 11, 15, 17, 21, 23, 24, 25, 26, 27, 28, 31, 32, 34, 35, 36, 39, 40, 41, 42, 44, 46, 48, 50],
    '2015_1': [1, 2, 5, 8, 10, 12, 20, 22, 31, 33, 36, 38, 47, 48, 49],
    '2015_2': [4, 5, 8, 9, 10, 11, 14, 20, 21, 23, 30, 31, 34, 35, 39, 41, 46],
    '2016_1': [4, 9, 11, 16, 30, 32, 44, 45, 48],
    '2016_2': [2, 10, 11, 13, 25, 26, 27, 28, 30, 32, 34, 35, 39, 45, 49],
    '2017_1': [3, 4, 5, 6, 7, 8, 9, 11, 12, 20, 21, 22, 35, 37, 39, 41],
    '2017_2': [11, 17, 18, 23, 24, 30, 31, 32, 34, 35, 36, 37, 38, 39, 40],
    '2018_1': [2, 5, 10, 11, 12, 18, 24, 30, 32, 33, 34, 35, 36, 38, 42, 49, 52],
    '2018_2': [2, 5, 8, 11, 22, 23, 24, 43, 48, 51, 52],
    '2019_1': [2, 6, 7, 12, 13, 18, 19, 38, 41, 49],
    '2019_2': [4, 5, 6, 8, 12, 14, 17, 18, 22, 23, 33, 34, 38, 50],
    '2020_1': [1, 3, 8, 9, 11, 14, 15, 17, 34, 35, 36, 37, 42, 47, 48, 50, 54],
    '2022_2': [2, 3, 6, 9, 11, 14, 15, 16, 17, 28, 40, 44, 45, 46],
    '2023_1': [1, 4, 11, 20, 22, 27, 30, 31, 35, 38, 39, 40, 42, 43, 47, 50],
    '2023_2': [4, 12, 13, 14, 15, 16, 24, 27, 32, 36, 37, 39, 40, 44, 54],
    '2024_1': [2, 5, 7, 18, 23, 26, 28, 29, 30, 31, 32, 42, 44, 46, 47, 54],
    '2024_2': [1, 11, 15, 17, 21, 23, 34, 48, 52],
    '2025_1_A': [25, 39, 52],
    '2025_1_B': [25, 39, 52],
    '2025_2': [10, 17, 20, 27, 32, 33, 40, 41, 44, 63],
}

SPECIAL_PAGES = {
    ('2010_2', 4): 3, ('2010_2', 20): 7, ('2010_2', 21): 7, ('2010_2', 25): 8,
    ('2010_2', 26): 9, ('2010_2', 30): 11, ('2010_2', 33): 12, ('2010_2', 39): 14,
    ('2010_2', 47): 18, ('2010_2', 54): 21,
    ('2025_1_A', 25): 6, ('2025_1_A', 39): 11, ('2025_1_A', 52): 16,
    ('2025_1_B', 25): 6, ('2025_1_B', 39): 11, ('2025_1_B', 52): 16,
}

session = requests.Session()
session.headers['User-Agent'] = 'Mozilla/5.0 FATEC visual publisher'


def question_pages(doc, max_question):
    occurrences = {n: [] for n in range(1, max_question + 1)}
    for page_index, page in enumerate(doc):
        text = page.get_text('text')
        for n in range(1, max_question + 1):
            if re.search(rf'Quest[aã]o\s*0?{n}(?!\d)', text, re.I):
                occurrences[n].append(page_index)

    chosen = {}
    last = -1
    for n in range(1, max_question + 1):
        options = occurrences[n]
        if not options:
            chosen[n] = None
            continue
        forward = [p for p in options if p >= last]
        chosen[n] = forward[0] if forward else options[0]
        last = chosen[n]
    return chosen


def output_path(edicao, questao):
    parts = edicao.split('_')
    year, semester = parts[0], parts[1]
    variant = parts[2] if len(parts) > 2 else None
    folder = f'{semester}sem' + (f'_{variant}' if variant else '')
    return Path(f'imagens/fatec/{year}/{folder}/questao_{questao:03d}.png')


for edicao, questions in CANDIDATES.items():
    print('Baixando', edicao)
    response = session.get(SOURCES[edicao], timeout=120)
    response.raise_for_status()
    if not response.content.startswith(b'%PDF'):
        raise RuntimeError(f'{edicao}: resposta não é PDF')

    doc = fitz.open(stream=response.content, filetype='pdf')
    qmap = question_pages(doc, max(questions))
    rendered = {}

    for q in questions:
        out = output_path(edicao, q)
        # Preserva os recortes manuais de maior qualidade publicados anteriormente.
        if out.exists():
            print('preservado', out)
            continue

        page_index = SPECIAL_PAGES.get((edicao, q), qmap.get(q))
        if page_index is None:
            raise RuntimeError(f'{edicao} questão {q}: página não localizada')

        if page_index not in rendered:
            page = doc[page_index]
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
            image = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
            # Remove somente a borda externa; mantém a página original integral para não perder contexto visual.
            rendered[page_index] = image.crop((12, 12, image.width - 12, image.height - 18))

        out.parent.mkdir(parents=True, exist_ok=True)
        rendered[page_index].save(out, format='PNG', optimize=True)
        if out.stat().st_size < 5000:
            raise RuntimeError(f'{out}: arquivo gerado parece inválido')
        print('gerado', out, out.stat().st_size)
