from __future__ import annotations

import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote

import requests
from bs4 import BeautifulSoup

OUT = Path('fuvest_pacote')
YEARS = range(2009, 2026)
HEADERS = {'User-Agent': 'Mozilla/5.0 Aprovafy-FUVEST-Archive/2.0'}
S = requests.Session()
S.headers.update(HEADERS)

INC = ('prova', 'gabarito', '1fase', '1_fase', '1-fase', 'primeira', '2fase', '2_fase', '2-fase', 'segunda', 'resposta', 'abordagem')
EXC = ('manual', 'guia', 'regulamento', 'resolucao', 'resolução', 'isenc', 'nota_de_corte', 'nota-de-corte', 'notas_de_corte', 'notas-de-corte', 'local_de_prova', 'locais_de_prova', 'lista_de', 'chamada', 'estat', 'questionario', 'questionário', 'candidato_vaga', 'candidato-vaga', 'carreira', 'programa_do_vestibular', 'convocado')


def norm(s: str) -> str:
    return unquote(s or '').lower().replace(' ', '_')


def safe(s: str) -> str:
    s = unquote(s)
    return re.sub(r'[^A-Za-z0-9._-]+', '_', s).strip('._') or 'arquivo.pdf'


def page(year: int):
    candidates = [
        f'https://www.fuvest.br/acervo-vestibular-{year}/',
        f'https://www.fuvest.br/acervo-vestibular-{year}',
        f'https://acervo.fuvest.br/fuvest/{year}/',
    ]
    errs=[]
    for u in candidates:
        try:
            r=S.get(u, timeout=45, allow_redirects=True)
            if r.ok and len(r.text)>1000:
                return r.url, r.text
            errs.append(f'{u} HTTP {r.status_code}')
        except Exception as e:
            errs.append(f'{u} {e}')
    raise RuntimeError('; '.join(errs))


def pdfish(u: str) -> bool:
    return '.pdf' in urlparse(u).path.lower()


def links(base: str, html: str):
    soup=BeautifulSoup(html, 'html.parser')
    out=[]; seen=set()
    all_pdf=[]
    for a in soup.find_all('a', href=True):
        u=urljoin(base, a['href'].strip())
        if not pdfish(u):
            continue
        label=' '.join(a.stripped_strings).strip()
        direct=norm(label+' '+u)
        if any(x in direct for x in EXC):
            continue
        all_pdf.append((label,u))

        near=[]
        p=a.parent
        for _ in range(2):
            if p is None: break
            try: near.append(' '.join(p.stripped_strings)[:800])
            except Exception: pass
            p=p.parent
        context=norm(' '.join(near))
        relevant=any(x in direct for x in INC) or 'provas_e_gabaritos' in context or 'primeira_fase' in context or 'segunda_fase' in context
        if relevant and u not in seen:
            seen.add(u); out.append((label,u))

    # Fallback conservador: se a página não expuser contexto semântico suficiente,
    # usa todos os PDFs não administrativos encontrados no acervo do ano.
    if not out:
        for item in all_pdf:
            if item[1] not in seen:
                seen.add(item[1]); out.append(item)

    return dedupe_variants(out)


def dedupe_variants(items):
    result=[]
    first_phase_variants=[]
    variant_re=re.compile(r'(?:^|[_\-\s])(v[1-4]?|k|q|x|z)(?:[_\-\s.]|$)',re.I)
    for item in items:
        label,u=item
        d=norm(label+' '+u)
        second=('2fase' in d or '2_fase' in d or '2-fase' in d or 'segunda' in d)
        key=('gabarito' in d or 'resposta' in d or 'abordagem' in d)
        explicit_variant=bool(variant_re.search(unquote(label+' '+urlparse(u).path)))
        if explicit_variant and not second and not key:
            first_phase_variants.append(item)
        else:
            result.append(item)
    if first_phase_variants:
        preferred=None
        for item in first_phase_variants:
            raw=unquote(item[0]+' '+urlparse(item[1]).path)
            if re.search(r'(?:^|[_\-\s])v1?(?:[_\-\s.]|$)',raw,re.I):
                preferred=item; break
        result.insert(0, preferred or first_phase_variants[0])
    return result


def download(u: str, dest: Path):
    err=None
    for attempt in range(4):
        try:
            with S.get(u,timeout=120,allow_redirects=True,stream=True) as r:
                r.raise_for_status()
                dest.parent.mkdir(parents=True,exist_ok=True)
                with dest.open('wb') as f:
                    for chunk in r.iter_content(1024*1024):
                        if chunk: f.write(chunk)
            sig=dest.read_bytes()[:5]
            if not sig.startswith(b'%PDF'):
                raise RuntimeError(f'assinatura inválida {sig!r}')
            return dest.stat().st_size
        except Exception as e:
            err=e
            if dest.exists(): dest.unlink()
            time.sleep(2+2*attempt)
    raise RuntimeError(err)


def main():
    if OUT.exists():
        import shutil; shutil.rmtree(OUT)
    OUT.mkdir()
    manifest=['FUVEST/USP - pacote de provas e gabaritos 2009-2025','Fonte: acervo oficial da FUVEST.','Quando a 1ª fase possui cadernos equivalentes V/K/Q/X/Z ou V1-V4, apenas uma versão é mantida para reduzir o tamanho.','']
    failures=[]; total=0; bytes_total=0

    for y in YEARS:
        print(f'=== {y} ===',flush=True)
        try:
            base,html=page(y)
            ls=links(base,html)
            print(f'{len(ls)} PDFs selecionados em {base}',flush=True)
            for label,u in ls:
                print(f'  candidato: {label!r} -> {u}',flush=True)
        except Exception as e:
            failures.append(f'{y}: página: {e}')
            continue
        if not ls:
            failures.append(f'{y}: nenhum PDF selecionado')
            continue
        manifest.append(f'[{y}] {base}')
        yd=OUT/str(y)
        for i,(label,u) in enumerate(ls,1):
            bn=safe(Path(urlparse(u).path).name)
            if not bn.lower().endswith('.pdf'): bn+='.pdf'
            dest=yd/f'{i:02d}_{bn}'
            try:
                n=download(u,dest)
                total+=1; bytes_total+=n
                manifest.append(f'  OK {dest.name} | {n} bytes | {label or "(sem rótulo)"} | {u}')
                print(f'  OK {dest.name} {n/1024/1024:.1f} MiB',flush=True)
            except Exception as e:
                failures.append(f'{y}: {u}: {e}')
                manifest.append(f'  FALHA | {label} | {u} | {e}')
                print(f'  FALHA {u}: {e}',file=sys.stderr,flush=True)
        manifest.append('')

    missing=[y for y in YEARS if not list((OUT/str(y)).glob('*.pdf'))]
    manifest += [f'Total PDFs: {total}',f'Tamanho: {bytes_total} bytes ({bytes_total/1024/1024:.1f} MiB)','','Falhas:',*(failures or ['Nenhuma.'])]
    (OUT/'MANIFESTO_FONTES.txt').write_text('\n'.join(manifest),encoding='utf-8')
    if missing:
        raise SystemExit(f'Pacote incompleto: anos sem PDF: {missing}')
    print(f'CONCLUIDO: {total} PDFs, {bytes_total/1024/1024:.1f} MiB',flush=True)

if __name__=='__main__': main()
