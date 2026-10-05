from pathlib import Path
import ast
import requests
import fitz

# Reusa apenas a relação de fontes oficiais já mantida no projeto.
mod = ast.parse(Path('scripts/publicar_fatec_visuais.py').read_text(encoding='utf-8'))
SOURCES = {}
for node in mod.body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'SOURCES':
        SOURCES = ast.literal_eval(node.value)
        break

# Coordenadas em pontos do PDF, revisadas visualmente a partir das provas oficiais.
# O recorte contém apenas o elemento visual necessário, jamais a folha completa.
CROPS = {
    ('2009_1', 36): (14, (96, 84, 498, 478)),       # mapa de fluxos migratórios
    ('2009_1', 38): (15, (337, 546, 558, 714)),     # teia alimentar
    ('2010_2', 20): (8,  (382, 365, 488, 452)),     # semicircunferência / triângulo
    ('2010_2', 21): (8,  (315, 625, 510, 712)),     # plano cartesiano / losango
    ('2013_1', 22): (11, (40, 220, 538, 482)),      # tabela de poluentes
    ('2013_1', 23): (12, (326, 52, 557, 127)),      # tabela de estruturas de Lewis
    ('2013_1', 33): (14, (342, 336, 557, 503)),     # figura 2, reuso de frequência
    ('2013_2', 31): (11, (342, 481, 552, 632)),     # figura do problema de topografia
    ('2014_1', 39): (15, (30, 48, 250, 493)),       # recorte do material visual da questão
    ('2014_2', 35): (12, (372, 456, 559, 584)),     # descarga elétrica atmosférica
    ('2015_1', 1):  (2,  (62, 72, 402, 346)),       # cartum
    ('2015_1', 2):  (2,  (316, 506, 568, 710)),     # formação militar romana
    ('2015_1', 5):  (4,  (40, 158, 305, 347)),      # gráfico de tecnologia vestível
    ('2015_2', 10): (5,  (302, 77, 545, 148)),      # tabela de disponibilidade
    ('2015_2', 20): (9,  (92, 135, 497, 322)),      # imagem da pilha / Google Doodle
    ('2015_2', 21): (9,  (92, 135, 497, 322)),      # visual compartilhado com q20
    ('2015_2', 30): (11, (292, 182, 559, 363)),     # tabela de usuários
    ('2016_1', 48): (19, (266, 172, 545, 306)),     # tabela do experimento
    ('2016_2', 13): (6,  (355, 105, 558, 203)),     # painel pentagonal
    ('2017_1', 3):  (3,  (122, 60, 470, 228)),      # gráfico de rendimentos
    ('2017_1', 4):  (3,  (122, 60, 470, 228)),      # gráfico compartilhado
    ('2017_1', 20): (10, (60, 250, 292, 354)),      # cartões de isótopos
    ('2018_1', 35): (15, (72, 210, 278, 340)),      # carro e sensores de radar
    ('2018_2', 11): (7,  (424, 321, 550, 447)),     # letra P e centro de reflexão
    ('2019_2', 8):  (5,  (82, 194, 504, 424)),      # gráficos da Pintec
    ('2023_1', 20): (10, (38, 205, 558, 386)),      # geometrias moleculares
    ('2023_2', 32): (14, (295, 74, 562, 250)),      # quadro das variedades de café
    ('2023_2', 37): (16, (54, 235, 286, 390)),      # tabelas nutricionais do milho painço
    ('2023_2', 39): (17, (42, 78, 296, 479)),       # rótulo nutricional
    ('2024_2', 11): (5,  (143, 100, 474, 311)),     # tabela de projeções do PIB
    ('2024_2', 34): (14, (117, 72, 523, 350)),      # Mapa Invertido da América do Sul
    ('2025_2', 32): (12, (54, 295, 527, 431)),      # gráfico de pegada de carbono
    ('2025_2', 40): (15, (48, 143, 532, 262)),      # esboço da Tabela Periódica
    ('2025_2', 44): (16, (101, 435, 498, 532)),      # quadro do campeonato
}

def output_path(ed, q):
    parts = ed.split('_')
    year, semester = parts[0], parts[1]
    variant = parts[2] if len(parts) > 2 else None
    folder = f'{semester}sem' + (f'_{variant}' if variant else '')
    return Path(f'imagens/fatec/{year}/{folder}/questao_{q:03d}.png')

session = requests.Session()
session.headers['User-Agent'] = 'Mozilla/5.0 FATEC reviewed exception crops'
cache = {}
for (ed, q), (page1, coords) in CROPS.items():
    if ed not in cache:
        r = session.get(SOURCES[ed], timeout=120)
        r.raise_for_status()
        if not r.content.startswith(b'%PDF'):
            raise RuntimeError(f'{ed}: fonte não retornou PDF')
        cache[ed] = fitz.open(stream=r.content, filetype='pdf')
    page = cache[ed][page1 - 1]
    rect = fitz.Rect(*coords) & page.rect
    pix = page.get_pixmap(matrix=fitz.Matrix(2.6, 2.6), clip=rect, alpha=False)
    out = output_path(ed, q)
    out.parent.mkdir(parents=True, exist_ok=True)
    pix.save(out)
    if pix.width > 1600 and pix.height > 1900:
        raise RuntimeError(f'{ed} q{q}: recorte excedeu limite {pix.width}x{pix.height}')
    print(f'{ed} q{q}: p{page1} {pix.width}x{pix.height} -> {out}')
