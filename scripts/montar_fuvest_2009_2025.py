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
UA = {'User-Agent': 'Mozilla/5.0 Aprovafy-FUVEST-Archive/1.0'}

INCLUDE = (
    'prova', 'gabarito', '1fase', '1_fase', '1-fase', 'primeira_fase',
    'primeira-fase', '2fase', '2_fase', '2-fase', 'segunda_fase',
    'segunda-fase', 'resposta', 'abordagem'
)
EXCLUDE = (
    'manual', 'guia', 'regulamento', 'resolucao', 'resolução', 'isen',
    'nota_de_corte', 'nota-de-corte', 'notas_de_corte', 'notas-de-corte',
    'local', 'lista', 'chamada', 'estat', 'questionario', 'questionário',
    'candidato_vaga', 'candidato-vaga', 'carreira', 'programa', 'convocado'
)

session = requests.Session()
session.headers.update(UA)


def norm(s: str) -> str:
    return unquote(s or '').lower().replace(' ', '_')


def safe_name(name: str) -> str:
    name = unquote(name)
    name = re.sub(r'[^A-Za-z0-9._-]+', '_', name).strip('._')
    return name or 'arquivo.pdf'


def fetch_page(year: int) -> tuple[str, str]:
    urls = [
        f'https://www.fuvest.br/acervo-vestibular-{year}/',
        f'https://www.fuvest.br/acervo-vestibular-{year}',
        f'https://acervo.fuvest.br/fuvest/{year}/',
    ]
    errors = []
    for url in urls:
        try:
            r = session.get(url, timeout=45, allow_redirects=True)
            if r.ok and len(r.text) > 1000:
                return r.url, r.text
            errors.append(f'{url}: HTTP {r.status_code}')
        except Exception as exc:
            errors.append(f'{url}: {exc}')
    raise RuntimeError('; '.join(errors))


def is_pdf(href: str) -> bool:
    p = urlparse(href).path.lower()
    return p.endswith('.pdf') or '.pdf/' in p


def extract_links(page_url: str, html: str) -> list[tuple[str, str]]:
    soup = BeautifulSoup(html, 'html.parser')
    found: list[tuple[str, str]] = []
    seen: set[str] = set()

    for a in soup.find_all('a', href=True):
        href = urljoin(page_url, a['href'].strip())
        if not is_pdf(href):
            continue
        text = ' '.join(a.stripped_strings).strip()
        contexts = [text, href]
        parent = a.parent
        for _ in range(4):
            if parent is None:
                break
            try:
                contexts.append(' '.join(parent.stripped_strings)[:1200])
            except Exception:
                pass
            parent = parent.parent
        blob = norm(' '.join(contexts))

        if any(x in blob for x in EXCLUDE):
            continue
        relevant = any(x in blob for x in INCLUDE) or ('provas_e_gabaritos' in blob)
        if not relevant:
            continue
        if href not in seen:
            seen.add(href)
            found.append((text, href))

    return dedupe_first_phase_variants(found)


def dedupe_first_phase_variants(items: list[tuple[str, str]]) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    kept_variant = False
    variant_re = re.compile(r'(?:^|[_\-\s])(v[1-4]?|k|q|x|z)(?:[_\-\s.]|$)', re.I)

    for text, href in items:
        b = norm(text + ' ' + href)
        if 'gabarito' in b or '2fase' in b or '2_fase' in b or 'segunda_fase' in b or 'segunda-fase' in b:
            result.append((text, href))
            continue
        if variant_re.search(unquote(text + ' ' + urlparse(href).path)) and ('prova' in b or 'fase' in b):
            preferred = bool(re.search(r'(?:^|[_\-\s])v1?(?:[_\-\s.]|$)', unquote(text + ' ' + urlparse(href).path), re.I))
            if not kept_variant and preferred:
                result.append((text, href))
                kept_variant = True
            elif not kept_variant:
                result.append((text, href))
                kept_variant = True
            continue
        result.append((text, href))

    return result


def download_pdf(url: str, dest: Path) -> int:
    last = None
    for attempt in range(4):
        try:
            with session.get(url, timeout=90, allow_redirects=True, stream=True) as r:
                r.raise_for_status()
                dest.parent.mkdir(parents=True, exist_ok=True)
                with dest.open('wb') as f:
                    for chunk in r.iter_content(1024 * 1024):
                        if chunk:
                            f.write(chunk)
            data = dest.read_bytes()[:5]
            if not data.startswith(b'%PDF'):
                raise RuntimeError(f'arquivo não parece PDF: assinatura={data!r}')
            return dest.stat().st_size
        except Exception as exc:
            last = exc
            if dest.exists():
                dest.unlink()
            time.sleep(2 + attempt * 2)
    raise RuntimeError(str(last))


def main() -> None:
    if OUT.exists():
        import shutil
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    manifest = [
        'FUVEST / USP - provas e gabaritos 2009-2025',
        'Fontes: acervo oficial da FUVEST.',
        'Uma única versão equivalente da 1ª fase é mantida quando o mesmo caderno aparece em várias versões de ordem.',
        '',
    ]
    failures = []
    total_files = 0
    total_bytes = 0

    for year in YEARS:
        print(f'\n=== {year} ===', flush=True)
        try:
            page_url, html = fetch_page(year)
            links = extract_links(page_url, html)
        except Exception as exc:
            failures.append(f'{year}: não foi possível ler acervo: {exc}')
            continue

        if not links:
            failures.append(f'{year}: nenhum PDF de prova/gabarito identificado em {page_url}')
            continue

        manifest.append(f'[{year}] {page_url}')
        year_dir = OUT / str(year)
        used_names: set[str] = set()

        for idx, (label, url) in enumerate(links, start=1):
            basename = safe_name(Path(urlparse(url).path).name)
            if not basename.lower().endswith('.pdf'):
                basename += '.pdf'
            name = f'{idx:02d}_{basename}'
            n = 2
            while name in used_names:
                name = f'{idx:02d}_{n}_{basename}'
                n += 1
            used_names.add(name)
            dest = year_dir / name
            try:
                size = download_pdf(url, dest)
                total_files += 1
                total_bytes += size
                manifest.append(f'  OK {name} | {size} bytes | {label or "(sem rótulo)"} | {url}')
                print(f'OK {dest} ({size/1024/1024:.1f} MiB)', flush=True)
            except Exception as exc:
                failures.append(f'{year}: {url}: {exc}')
                manifest.append(f'  FALHA | {label or "(sem rótulo)"} | {url} | {exc}')
                print(f'FALHA {url}: {exc}', file=sys.stderr, flush=True)

        manifest.append('')

    manifest.extend([
        f'Total de PDFs baixados: {total_files}',
        f'Tamanho total: {total_bytes} bytes ({total_bytes/1024/1024:.1f} MiB)',
        '',
        'FALHAS:',
        *(failures or ['Nenhuma.']),
    ])
    (OUT / 'MANIFESTO_FONTES.txt').write_text('\n'.join(manifest), encoding='utf-8')

    missing_years = [y for y in YEARS if not (OUT / str(y)).exists() or not list((OUT / str(y)).glob('*.pdf'))]
    if missing_years:
        raise SystemExit(f'Pacote incompleto. Anos sem PDFs: {missing_years}')

    print(f'\nConcluído: {total_files} PDFs, {total_bytes/1024/1024:.1f} MiB', flush=True)


if __name__ == '__main__':
    main()

# trigger: workflow FUVEST 2009-2025
