#!/usr/bin/env python3
from pathlib import Path
import urllib.request, zipfile, re, hashlib, shutil, sys, json
import fitz

SOURCES = {
'2025':'https://www.puc-rio.br/vestibular/repositorio/provas/2025/download/Vestibular2025_Download-Completo.zip',
'2024':'https://www.puc-rio.br/vestibular/repositorio/provas/2023-2/download/Vestibular2024-Provas-e-Gabaritos-v2.zip',
'2023':'https://www.puc-rio.br/vestibular/repositorio/provas/2023/download/Vestibular2023_provasegabaritos_completo-19-10-2022.zip',
'2022':'https://www.puc-rio.br/vestibular/repositorio/provas/2022/download/2022-Provas-e-Gabaritos-VESTIBULAR-2022-v2.zip',
'2021':'https://www.puc-rio.br/vestibular/repositorio/provas/2021/download/GABARITO-VESTIBULAR2021_completo.zip',
'2020-tecfin':'https://www.puc-rio.br/vestibular/repositorio/provas/2020/download/VestibularTECFIN2020_provasegabaritos_completo.zip',
'2020':'https://www.puc-rio.br/vestibular/repositorio/provas/2020/download/Vestibular2020_provasegabaritos_completo.zip',
'2019-inverno':'https://www.puc-rio.br/vestibular/repositorio/provas/2019-2/download/VestibularInverno2019_provasegabaritos.zip',
'2019':'https://www.puc-rio.br/vestibular/repositorio/provas/2019/download/Vestibular2019_20181014_TodasProvasGabaritos.zip',
'2018-inverno':'https://www.puc-rio.br/vestibular/repositorio/provas/2018-2/download/VestibularPUC-RioINVERNO2018-2_provas_gabaritos.zip',
'2018':'https://www.puc-rio.br/vestibular/repositorio/provas/2018/download/VEST2018PUCRio_PROVAS_GABARITOS_V7.zip',
'2017-inverno':'https://www.puc-rio.br/vestibular/repositorio/provas/2017-2/download/VestibularPUC-RioINVERNO2017-2_provas_gabaritos.zip',
'2017':'https://www.puc-rio.br/vestibular/repositorio/provas/2017/download/VEST2017PUCRio_PROVAS_GABARITOS_v4.zip',
'2016-inverno':'https://www.puc-rio.br/vestibular/repositorio/provas/2016-2/download/VEST2016-2PUCRio_PROVAS_GABARITOS.zip',
'2016':'https://www.puc-rio.br/vestibular/repositorio/provas/2016/download/VEST2016PUCRio_PROVAS_GABARITOS_V4.zip',
'2015-inverno':'https://www.puc-rio.br/vestibular/repositorio/provas/2015-2/download/VestiblularPUC-RioINVERNO2015-2_provas_gabaritos.zip',
'2015':'https://www.puc-rio.br/vestibular/repositorio/provas/2015/download/VEST2015PUCRio_PROVAS_GABARITOS_V3.zip',
'2014-inverno':'https://www.puc-rio.br/vestibular/repositorio/provas/2014-2/download/VEST2014-2PUCRio_PROVAS_GABARITOS.zip',
'2014':'https://www.puc-rio.br/vestibular/repositorio/provas/2014/download/VEST2014PUCRio_PROVAS_GABARITOS_V5.zip',
'2013-inverno':'https://www.puc-rio.br/vestibular/repositorio/provas/2013-2/download/VEST2013-2PUCRio_PROVAS_GABARITOS.zip',
'2013':'https://www.puc-rio.br/vestibular/repositorio/provas/2013/download/VEST2013PUCRio_PROVAS_GABARITOS_v4.zip',
'2012-inverno':'https://www.puc-rio.br/vestibular/repositorio/provas/2012-2/download/VEST2012PUCRio_PROVAS_GABARITOS_v2.zip',
'2012':'https://www.puc-rio.br/vestibular/repositorio/provas/2012/download/VEST2012PUCRio_PROVAS_GABARITOS.zip',
'2011-inverno':'https://www.puc-rio.br/vestibular/repositorio/provas/2011-2/download/VEST2011PUCRio_PROVAS_GABARITOS.zip',
'2011':'https://www.puc-rio.br/vestibular/repositorio/provas/2011/download/VEST2011PUCRio_PROVAS_GABARITOS_v4.zip',
'2010-inverno':'https://www.puc-rio.br/vestibular/repositorio/provas/2010-2/download/VEST2010PUCRIO_PROVAS_GABARITOS.ZIP',
'2010':'https://www.puc-rio.br/vestibular/repositorio/provas/2010/download/VEST2010PUCRio_PROVAS_GABARITOS.zip',
'2009-inverno':'https://www.puc-rio.br/vestibular/repositorio/provas/2009-2/download/VEST2009PUCRIO_PROVAS_GABARITOS.zip',
'2009':'https://www.puc-rio.br/vestibular/repositorio/provas/2009/download/VEST2009PUCRio_PROVAS_GABARITOS.zip',
}
VPAT=re.compile(r'(?i)\b(figura|gr[aá]fico|mapa|imagem|charge|tabela|esquema|diagrama|fotografia|tirinha|quadrinho|circuito|estrutura|representa(?:do|da)|mostra(?:do|da)|ilustra(?:do|da))\b')
QRE=re.compile(r'(?is)^\s*(?:quest(?:ão|ao)\s*)?(\d{1,2})(?:\s*\([^\n]{0,50}\))?\s*(?:\n|(?=[A-ZÁÉÍÓÚÂÊÔÃÕ]))')

def download(url,dst):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req,timeout=180) as r, open(dst,'wb') as f: shutil.copyfileobj(r,f)

def markers(pg):
    out=[]
    for b in pg.get_text('blocks',sort=False):
        x0,y0,x1,y1,t,*_=b
        if y0<55 or y1>pg.rect.height-35: continue
        m=QRE.match(t.strip())
        if m and 1<=int(m.group(1))<=99:
            if any(z in t.lower() for z in ['candidato recebeu','será eliminado','sera eliminado']): continue
            out.append((int(m.group(1)),fitz.Rect(x0,y0,x1,y1)))
    return out

def qregion(pg,num):
    ms=markers(pg); mid=pg.rect.width/2
    cand=[b for n,b in ms if n==num]
    if not cand: return None
    b=min(cand,key=lambda r:r.get_area()); col='L' if b.x0<mid else 'R'
    same=[bb for n,bb in ms if ('L' if bb.x0<mid else 'R')==col and bb.y0>b.y0+1]
    y1=min((bb.y0 for bb in same),default=pg.rect.height-40)
    if any(bb.x0<mid for _,bb in ms) and any(bb.x0>mid for _,bb in ms):
        x0,x1=(20,mid-4) if col=='L' else (mid+4,pg.rect.width-20)
    else: x0,x1=25,pg.rect.width-25
    return fitz.Rect(x0,b.y0,x1,y1)

def crop_for(pg,reg):
    rs=[]
    for b in pg.get_text('dict')['blocks']:
        if b.get('type')==1:
            r=fitz.Rect(b['bbox']); inter=r & reg
            if inter.is_empty or inter.get_area()<250: continue
            if r.get_area()>pg.rect.get_area()*0.55: continue
            rs.append(inter)
    if rs:
        u=rs[0]
        for r in rs[1:]: u|=r
        return fitz.Rect(max(reg.x0,u.x0-10),max(reg.y0,u.y0-10),min(reg.x1,u.x1+10),min(reg.y1,u.y1+10)), 'raster'
    ds=[]
    for d in pg.get_drawings():
        r=fitz.Rect(d['rect']); inter=r & reg
        if inter.is_empty or inter.width<4 or inter.height<4 or inter.get_area()<30: continue
        if inter.get_area()>reg.get_area()*0.85: continue
        ds.append(inter)
    if ds:
        ds=sorted(ds,key=lambda r:r.y0); clusters=[]
        for r in ds:
            if not clusters or r.y0-clusters[-1][-1].y1>30: clusters.append([r])
            else: clusters[-1].append(r)
        unions=[]
        for cl in clusters:
            u=cl[0]
            for r in cl[1:]: u|=r
            if u.width>25 and u.height>25: unions.append(u)
        if unions:
            u=max(unions,key=lambda r:r.get_area())
            return fitz.Rect(max(reg.x0,u.x0-14),max(reg.y0,u.y0-14),min(reg.x1,u.x1+14),min(reg.y1,u.y1+14)), 'vector'
    # Fallback conservador: recorte apenas da região da questão, nunca da página inteira.
    # Garante imagem funcional quando o PDF codifica o desenho como glifos/texto ou máscara.
    return fitz.Rect(reg.x0,reg.y0,reg.x1,reg.y1), 'question-region'

def question_texts(pg):
    ms=markers(pg); out=[]
    blocks=[(fitz.Rect(b[:4]),b[4]) for b in pg.get_text('blocks',sort=False) if b[4].strip()]
    for num,b in ms:
        reg=qregion(pg,num)
        if not reg: continue
        txt='\n'.join(t for r,t in blocks if not (r & reg).is_empty)
        out.append((num,txt,reg))
    return out

def main():
    tmp=Path('/tmp/puc-rio-src'); tmp.mkdir(parents=True,exist_ok=True)
    outroot=Path('imagens/puc-rio'); outroot.mkdir(parents=True,exist_ok=True)
    manifest=[]
    total=0
    for edition,url in SOURCES.items():
        z=tmp/f'{edition}.zip'; dest=tmp/edition
        try:
            print('download',edition); download(url,z); dest.mkdir(exist_ok=True)
            with zipfile.ZipFile(z) as zz: zz.extractall(dest)
        except Exception as e:
            print('FAILED',edition,e,file=sys.stderr); continue
        for p in dest.rglob('*'):
            if p.suffix.lower()!='.pdf': continue
            try: d=fitz.open(p)
            except: continue
            rel=p.relative_to(dest).as_posix(); sh=hashlib.sha1(rel.encode()).hexdigest()[:8]
            for pi,pg in enumerate(d):
                for num,txt,reg in question_texts(pg):
                    if not VPAT.search(txt): continue
                    cr,kind=crop_for(pg,reg)
                    if not cr or cr.width<25 or cr.height<25: continue
                    folder=outroot/edition/sh; folder.mkdir(parents=True,exist_ok=True)
                    fn=folder/f'questao_{num:03d}_pagina_{pi+1:02d}.png'
                    pg.get_pixmap(matrix=fitz.Matrix(2,2),clip=cr,alpha=False).save(fn)
                    manifest.append({
                        'edition':edition,'source':rel,'hashdir':sh,'question':num,'page':pi+1,
                        'path':fn.as_posix(),'crop_kind':kind,'text':txt.strip()[:6000]
                    })
                    total+=1
            d.close()
        shutil.rmtree(dest,ignore_errors=True)
        try:z.unlink()
        except:pass
    mdir=outroot/'_manifests'; mdir.mkdir(parents=True,exist_ok=True)
    with open(mdir/'visual_manifest.json','w',encoding='utf-8') as f:
        json.dump(manifest,f,ensure_ascii=False,indent=2)
    print('TOTAL_IMAGES',total,'MANIFEST',len(manifest))

if __name__=='__main__': main()
