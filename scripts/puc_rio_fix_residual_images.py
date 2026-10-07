import hashlib, subprocess, tempfile, zipfile, unicodedata
from pathlib import Path
import fitz
from PIL import Image

ITEMS = [
{"edition":"2016-inverno","source":"VEST2016-2_PUCRioProva_G1_20160619.pdf","page":3,"q":3,"crop":[153.4,186.05,441.7,467.0]},
{"edition":"2016-inverno","source":"VEST2016-2_PUCRioProva_G2_20160619.pdf","page":7,"q":18,"crop":[162.11,356.86,433.1,529.72]},
{"edition":"2009","source":"VEST2009PUCRio_GRUPO2_24102008.pdf","page":10,"q":3,"crop":[79.5,84.2,504.8,413.5]},
{"edition":"2012-inverno","source":"informatica_tarde.pdf","page":8,"q":1,"crop":[56.7,233.0,242.7,364.3]},
{"edition":"2013","source":"VEST2013PUCRio_GRUPO_3_15102012.pdf","page":9,"q":3,"crop":[151.2,148.5,444.1,356.9]},
{"edition":"2016","source":"Vest2016_prova_G1_3_4_20151011.pdf","page":3,"q":7,"crop":[46.8,382.6,265.0,517.3]},
{"edition":"2016","source":"Vest2016_prova_G2_20151011.pdf","page":3,"q":8,"crop":[170.0,536.8,425.2,680.8]},
{"edition":"2017","source":"Vest2017_prova_G1_20161010.pdf","page":6,"q":15,"crop":[190.0,340.1,405.3,591.3]},
{"edition":"2017","source":"Vest2017_prova_G1_20161010.pdf","page":9,"q":20,"crop":[141.9,88.0,453.8,320.3]},
{"edition":"2018","source":"Vest2018_prova_G1_20171015.pdf","page":3,"q":4,"crop":[311.8,420.9,564.9,522.2]},
{"edition":"2018","source":"Vest2018_prova_G2_20171015.pdf","page":14,"q":4,"crop":[177.7,99.7,417.5,361.7]},
{"edition":"2018-inverno","source":"VEST2018-2_PUCRioProva_G5_20180708.pdf","page":17,"q":3,"crop":[156.5,308.8,445.8,463.0]},
{"edition":"2023","source":"2o DIA - MANH#U00c3 - GRUPO 2.pdf","page":6,"q":13,"crop":[309.0,282.5,569.5,548.9]},
{"edition":"2023","source":"2o DIA - TARDE - GRUPO 4.pdf","page":14,"q":39,"crop":[122.1,91.7,473.1,325.7]},
{"edition":"2024","source":"2oDIA-TARDE-GRUPO-1.pdf","page":3,"q":1,"crop":[107.0,135.4,488.3,302.9]},
{"edition":"2024","source":"2oDIA-TARDE-GRUPO-5.pdf","page":22,"q":5,"crop":[85.0,150.6,510.2,376.3]},
{"edition":"2025","source":"2o DIA - MANH#U00c3 - GRUPO 2.pdf","page":5,"q":11,"crop":[72.4,137.7,522.9,292.7]},
]
URLS={
"2016-inverno":"https://www.puc-rio.br/vestibular/repositorio/provas/2016-2/download/VEST2016-2PUCRio_PROVAS_GABARITOS.zip",
"2009":"https://www.puc-rio.br/vestibular/repositorio/provas/2009/download/VEST2009PUCRio_PROVAS_GABARITOS.zip",
"2012-inverno":"https://www.puc-rio.br/vestibular/repositorio/provas/2012-2/download/VEST2012PUCRio_PROVAS_GABARITOS_v2.zip",
"2013":"https://www.puc-rio.br/vestibular/repositorio/provas/2013/download/VEST2013PUCRio_PROVAS_GABARITOS_v4.zip",
"2016":"https://www.puc-rio.br/vestibular/repositorio/provas/2016/download/VEST2016PUCRio_PROVAS_GABARITOS_V4.zip",
"2017":"https://www.puc-rio.br/vestibular/repositorio/provas/2017/download/VEST2017PUCRio_PROVAS_GABARITOS_v4.zip",
"2018":"https://www.puc-rio.br/vestibular/repositorio/provas/2018/download/VEST2018PUCRio_PROVAS_GABARITOS_V7.zip",
"2018-inverno":"https://www.puc-rio.br/vestibular/repositorio/provas/2018-2/download/VestibularPUC-RioINVERNO2018-2_provas_gabaritos.zip",
"2023":"https://www.puc-rio.br/vestibular/repositorio/provas/2023/download/Vestibular2023_provasegabaritos_completo-19-10-2022.zip",
"2024":"https://www.puc-rio.br/vestibular/repositorio/provas/2023-2/download/Vestibular2024-Provas-e-Gabaritos-v2.zip",
"2025":"https://www.puc-rio.br/vestibular/repositorio/provas/2025/download/Vestibular2025_Download-Completo.zip",
}
def nn(s):
 s=unicodedata.normalize("NFKC",s).casefold()
 return s.replace("#u00c3","ã").replace("#u00e3","ã")
with tempfile.TemporaryDirectory() as td:
 td=Path(td)
 for edition in sorted(set(x["edition"] for x in ITEMS)):
  its=[x for x in ITEMS if x["edition"]==edition]
  zp=td/(edition+".zip"); ed=td/edition; ed.mkdir()
  proc=subprocess.run(["curl","-L","--fail","--retry","3","-o",str(zp),URLS[edition]],check=False)
  if proc.returncode:
   print("SKIP",edition); continue
  with zipfile.ZipFile(zp) as z:z.extractall(ed)
  files=[p for p in ed.rglob("*") if p.is_file()]
  for it in its:
   hits=[p for p in files if nn(p.name)==nn(it["source"])]
   if not hits:
    print("SOURCE_NOT_FOUND",edition,it["source"]); continue
   src=hits[0]; folder=hashlib.sha1(it["source"].encode()).hexdigest()[:8]
   target=Path(f'imagens/puc-rio/{edition}/{folder}/questao_{it["q"]:03d}_pagina_{it["page"]:02d}.png')
   if target.exists():
    print("EXISTS",target); continue
   doc=fitz.open(src); pg=doc[it["page"]-1]; rect=fitz.Rect(*it["crop"]) & pg.rect
   pix=pg.get_pixmap(matrix=fitz.Matrix(2,2),clip=rect,alpha=False)
   target.parent.mkdir(parents=True,exist_ok=True); pix.save(target); doc.close()
   im=Image.open(target)
   if im.width>1400:
    ratio=1400/im.width; im=im.resize((1400,int(im.height*ratio)),Image.Resampling.LANCZOS)
   im.save(target,optimize=True)
   print("WROTE",target)
