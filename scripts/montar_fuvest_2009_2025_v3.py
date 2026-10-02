from __future__ import annotations

import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote

import requests
from bs4 import BeautifulSoup, Tag

OUT = Path('fuvest_pacote')
YEARS = range(2009, 2026)
S = requests.Session()
S.headers.update({'User-Agent': 'Mozilla/5.0 Aprovafy-FUVEST-Archive/3.0'})

EXCLUDE = (
    'manual', 'guia', 'regulamento', 'resolucao', 'resolução', 'isenc',
    'nota_de_corte', 'nota-de-corte', 'notas_de_corte', 'notas-de-corte',
    'local_de_prova', 'locais_de_prova', 'lista_de', 'chamada', 'estat',
    'analise', 'análise', 'inscritos', 'relacao_candidato', 'relação_candidato',
    'questionario', 'questionário', 'socioeconom', 'matriculad', 'treineir',
    'classificacao', 'classificação', 'convocado', 'carreira', 'programa_do_vestibular'
)


def norm(s: str) -> str:
    return unquote(s or '').lower().replace(' ', '_')


def safe(s: str) -> str:
    s = unquote(s)
    return re.sub(r'[^A-Za-z0-9._-]+', '_', s).strip('._') or 'arquivo.pdf'


def get_page(year: int):
    # O acervo antigo tem HTML simples e uma seção explícita Provas e Gabaritos.
    urls = [
        f'https://acervo.fuvest.br/fuvest/{year}/',
        f'https://acervo.fuvest.br/fuvest/{year}/index.html',
        f'https://www.fuvest.br/acervo-vestibular-{year}/',
        f'https://www.fuvest.br/acervo-vestibular-{year}',
    ]
    errs=[]
    for u in urls:
        try:
            r=S.get(u,timeout=(15,30),allow_redirects=True)
            if r.ok and len(r.text)>1000:
                return r.url,r.text
            errs.append(f'{u}: HTTP {r.status_code}')
        except Exception as e:
            errs.append(f'{u}: {e}')
    raise RuntimeError('; '.join(errs))


def pdf_url(base: str, href: str) -> str | None:
    u=urljoin(base,href.strip())
    return u if '.pdf' in urlparse(u).path.lower() else None


def direct_excluded(label: str, u: str) -> bool:
    d=norm(label+' '+u)
    return any(x in d for x in EXCLUDE)


def section_links(base: str, html: str):
    soup=BeautifulSoup(html,'html.parser')
    selected=[]; seen=set()

    # 1) Estrutura clássica do acervo: <li>Provas e Gabaritos<ul>...</ul></li>
    marker=soup.find(string=re.compile(r'Provas\s+e\s+Gabaritos',re.I))
    if marker:
        parent=marker.parent if isinstance(marker.parent,Tag) else None
        li=parent if parent and parent.name=='li' else (parent.find_parent('li') if parent else None)
        if li:
            for a in li.find_all('a',href=True):
                u=pdf_url(base,a['href'])
                if not u: continue
                label=' '.join(a.stripped_strings).strip()
                if direct_excluded(label,u): continue
                if u not in seen:
                    seen.add(u); selected.append((label,u))

    # 2) WordPress atual: varre a partir do marcador até Listas/Estatísticas.
    if not selected and marker:
        start=marker.parent if isinstance(marker.parent,Tag) else None
        if start:
            for el in start.find_all_next():
                if not isinstance(el,Tag): continue
                txt=' '.join(el.stripped_strings).strip()
                if el is not start and re.fullmatch(r'(Listas|Estatísticas|Estatisticas)',txt,re.I):
                    break
                if el.name=='a' and el.has_attr('href'):
                    u=pdf_url(base,el['href'])
                    if not u: continue
                    label=' '.join(el.stripped_strings).strip()
                    if direct_excluded(label,u): continue
                    if u not in seen:
                        seen.add(u); selected.append((label,u))

    # 3) Fallback: apenas PDFs cujo próprio texto/URL indique prova, fase, gabarito ou resposta.
    if not selected:
        for a in soup.find_all('a',href=True):
            u=pdf_url(base,a['href'])
            if not u: continue
            label=' '.join(a.stripped_strings).strip()
            d=norm(label+' '+u)
            if direct_excluded(label,u): continue
            if not any(k in d for k in ('prova','gabarito','1fase','1_fase','primeira','2fase','2_fase','segunda','resposta','abordagem')):
                continue
            if u not in seen:
                seen.add(u); selected.append((label,u))

    return dedupe_first_phase(selected)


def dedupe_first_phase(items):
    # Cadernos V/K/Q/X/Z (ou V1-V4) têm as mesmas questões em ordem diferente.
    variant_re=re.compile(r'(?:^|[_\-\s])(v[1-4]?|k|q|x|z)(?:[_\-\s.]|$)',re.I)
    variants=[]; result=[]
    for label,u in items:
        d=norm(label+' '+u)
        second=any(k in d for k in ('2fase','2_fase','2-fase','segunda'))
        answer=any(k in d for k in ('gabarito','resposta','abordagem'))
        variant=bool(variant_re.search(unquote(label+' '+urlparse(u).path)))
        if variant and not second and not answer:
            variants.append((label,u))
        else:
            result.append((label,u))
    if variants:
        preferred=None
        for item in variants:
            raw=unquote(item[0]+' '+urlparse(item[1]).path)
            if re.search(r'(?:^|[_\-\s])v1?(?:[_\-\s.]|$)',raw,re.I):
                preferred=item; break
        result.insert(0,preferred or variants[0])
    return result


def download(u: str,dest: Path):
    last=None
    for attempt in range(2):
        try:
            with S.get(u,timeout=(15,45),allow_redirects=True,stream=True) as r:
                r.raise_for_status()
                dest.parent.mkdir(parents=True,exist_ok=True)
                with dest.open('wb') as f:
                    for chunk in r.iter_content(1024*1024):
                        if chunk: f.write(chunk)
            sig=dest.read_bytes()[:5]
            if not sig.startswith(b'%PDF'):
                raise RuntimeError(f'não é PDF ({sig!r})')
            return dest.stat().st_size
        except Exception as e:
            last=e
            if dest.exists(): dest.unlink()
            time.sleep(2)
    raise RuntimeError(last)


def main():
    if OUT.exists():
        import shutil; shutil.rmtree(OUT)
    OUT.mkdir()
    manifest=[
        'FUVEST/USP - provas, gabaritos e respostas 2009-2025',
        'Fonte exclusiva: acervo oficial da FUVEST.',
        'Para reduzir tamanho, quando a primeira fase tem versões equivalentes (V/K/Q/X/Z ou V1-V4), somente uma é mantida.',
        '',
    ]
    failures=[]; total=0; total_bytes=0

    for y in YEARS:
        print(f'=== {y} ===',flush=True)
        try:
            base,html=get_page(y)
            items=section_links(base,html)
        except Exception as e:
            failures.append(f'{y}: acervo: {e}')
            continue
        print(f'{len(items)} PDFs selecionados em {base}',flush=True)
        if not items:
            failures.append(f'{y}: nenhum PDF na seção Provas e Gabaritos')
            continue
        manifest.append(f'[{y}] {base}')
        yd=OUT/str(y)
        for i,(label,u) in enumerate(items,1):
            bn=safe(Path(urlparse(u).path).name)
            if not bn.lower().endswith('.pdf'): bn+='.pdf'
            dest=yd/f'{i:02d}_{bn}'
            print(f'  -> {label!r} | {u}',flush=True)
            try:
                n=download(u,dest)
                total+=1; total_bytes+=n
                manifest.append(f'  OK {dest.name} | {n} bytes | {label or "(sem rótulo)"} | {u}')
                print(f'     OK {n/1024/1024:.1f} MiB',flush=True)
            except Exception as e:
                failures.append(f'{y}: {label}: {u}: {e}')
                manifest.append(f'  FALHA | {label} | {u} | {e}')
                print(f'     FALHA {e}',file=sys.stderr,flush=True)
        manifest.append('')

    missing=[y for y in YEARS if not list((OUT/str(y)).glob('*.pdf'))]
    manifest += [f'Total PDFs: {total}',f'Tamanho total: {total_bytes} bytes ({total_bytes/1024/1024:.1f} MiB)','','Falhas:',*(failures or ['Nenhuma.'])]
    (OUT/'MANIFESTO_FONTES.txt').write_text('\n'.join(manifest),encoding='utf-8')
    if missing:
        raise SystemExit(f'Pacote incompleto: anos sem PDF: {missing}')
    print(f'CONCLUIDO: {total} PDFs, {total_bytes/1024/1024:.1f} MiB',flush=True)

if __name__=='__main__': main()
