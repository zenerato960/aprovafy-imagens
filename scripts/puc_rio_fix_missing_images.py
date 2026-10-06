import base64, gzip, json, os, subprocess, tempfile, zipfile, unicodedata
from pathlib import Path
import fitz
from PIL import Image

CONFIG_GZ_B64 = """H4sIAMNyxWoC/82c224bRxKGX8XQ9XDYVd3Vh9w5m8AwsLs27Dg3QUAMh6RDIBYVHXKz2Hffv5oWSVE91AwPwt5ElqjDfKzTX9XV+e0/V/PZ8n65ur764YqNSVfV1d3q4badT6bN3fy6+TbHC7/+/PkXffHjl398Wq4m7z59+fjBTtiRwVdjfTNb4Mdumq/4Xltd/XX98O3qh1hd3Te3X+f3k5vm/g/8kuU3fMP13fjmoR3dLldj/YVj9tPgA/nxXw/zu/tmNcHvww98XV43E2Prm+uv+M3t7erm6offoq3FVxylJq6YpPaVjamm+Pt/q3NjyCMG2SM5yG445ClHsjVzRWJqJxXbVIdUOQ61oVNA+AV7uF4cjeNoZtNde7gue7CpTeXZ1wwMQHmpIqU6XYAiPVLwsRS8oUhPKfDX6hAr72oXK5dcHVwVgqvjSdagMgf5jV/1AplRu5jFKe2A0CMI+T1zOJgDzx9DJYHwb86fPKMgc4CCzJ41bKZITyl4gDnIjGeNTW1oZiVzED+lCLHmUHlfm1iJpZpttgb7UzhcBwc9ctheHNZFmQvLDscmyIkK1iAAyKM5LCNXpVMwqIxhh1HMvLGzRTMvUeyHuLWmDha5imqfKnG+lsq6hDx8AY6tOehYEOo0R6wDspRwzVSRt0i2FZ6hjpcwCMmApFsG2SRdkoJffQ+P7FYaHel5CSQ6REFPKSgoBd6O46Ocxm7uo0ynsU+UM2oHu4rwdYqVDZxLYZLahVNIbJnEDgMJLqXUuFSsHnsBIogHmJu9qYTNBZ7dDdBT5Wff6in3/NmNyc/u0iWefZCIKj58t4haiw9IQXrUHpw/OwXDnQfDovSzY/d/hkFuSFYqYexkJbeflVwtqSIUCFRvm0JtHUiQmQr5lUbL67/nt9erIlG7nF+3y+ZuMl2u/lx9Xbb4J552Nu8QhKYPzONfHJsWOn1hd1Itmy5luC7hjusoOddCtEe111Ci5fVidfutuQdKgWRQ9d6CtM4ZWRjpU8VJUs2xouhqWzmxqBeVoEKSPy/KRtz6U1H8BmVf5KJiRF9RMnVC94e6gSbQwyh8XpRt8XOnsrjOIojOI7rMIg5Bw9qBWDiaPS/LsDp+CGVbBvdQJNQIezR/3qOWxNqjlQqhJvechE+xihkSLNwrWDRLPgkWG2qv8wWbfQvGsTG357YAYw8lZbublCeMpJmzMh89LyE7nko7CzFSn3nJ9xZE6hAe85dlW5OcxAG1KAWOrXj3phdJm4TncWq3JN4cbKYc6mOIjyQhaE67CIkMaUNKIDttiOw7l9F4R3AYda2LPH4ckrmKj7/NWLE0gSM0Uy5VTstJQJWPtQkXIRmk24sk2wbk2exKoE2q/Oxbl0LiolODvETihgV5w0xtM+M+Ih5SKzCKukc9pOSUQxzaW3sJjm3+5WNBuDPvIlaSoCX0tRACJNUWLbrXvr2AMqyITPRHOsRwryDfVpKmgdxYmGKw75lGvaoin3RcbYEVUd1jqBMP5Vk93N+u7ibtw+3d6q6LaBMsMghIItPM0G5plIMFhaPPs6AYNSfnT57zuEOu5p64mnusi3bSrr7d/Dm/X3Wk4z41341NTL5paFGs9fvpGNEDXeyoNuiFoVvgFmzL0XNOJD8kRReRXOcU2GoMobqE3NmfxCEvcQwa2LnxzDcsXkyfgR2KJAn6LqBwSbHIIQzZx8hTOnIdGDzEw2Ts58F6a2ZFD9sTxqQJjGCRpL6VGxZoS0jjkovJwSzwyDbiyRrv4+3q72byjjQXiPEcO4zTJ1dv/vQ4yUyaOJ8Wc3ZxyC1o83MNtchz+slJ1qKXrDUoeGCtMA1oqkKf4CE9aQjZWkEg+vPxg4WC9qcxuZeY7JBAknGw0izclIuBtJ+0YTRBkoN9EmCS6GfOprIHnpFpoJ0KTAfsRHpMp8crDloBTQ2UgxUqHaEOYPoM57MKxofA7DCuqeWpDWL7nKjqKBkNWyXrsfK5MoTryBCDuumdDOHibOq979NNu5z+dNwPQ1nDqk9dgMSLl05/Zsgw6mD68y/B+SxVAYfmyHsuztV8HzhfhPPG0wknfpu/PPY0b6dt4/vNDG2NCIO+gzRyUEihcj6Uhp/HkXGZLGwSYRyERsG0EnezPG1bprBfk1nn7RY9U/RIhbamShgpvyDMQxkKf0NfnNysYWyGoc6zm9SDJYyJWuNa2XW91NX2QeJpHhcdsVeMVxFeHlpDjmagMsMwGRHGLbm0sFPuIx9I+z1GFwEX4yjHPjl/f/K9U1geUlPx7i9CJJ7OSjV1f9xptVeNFUvMo3QIBNFdpIgW7/i3XyvPYRDXzwLzFFszK6/w7I+gfQ3tIdHkSQ6CHV6U0HnLBTDssGgoYKTOZIUvQKk56AGLD4khbiqPMnO8U7mOcAjDjNFIm8zCladr+3kJ77+qGif5bCPpHESna1KYroU+STcUk24wwXQl3T5MO+UktS3Niu3cs5yLvgBBbiDYUE2Mru4hdUV/LjIqk7khhXJLFprGzdGtFgvlfib2ooXSWzA5VJGIhiEhHV+YLB1nswIZdW7GwUJ6Lo0CKeqQTg8SLHrXkkPGQ1EVnxSZgKiSp1E1ZL+P4ti0DvLcFzc06Nl+n2hSIN2zRG5AWFlUTEiZ6M5MMaiJK0JQ5+RNd5fWqxpSSs79nlvKz82D+oA4hmxrUpwVo4P3p7ouz3F1uKvvvipmCEmUoeMpXIcPbc49qJ8Teb8IQrtTNeKugw9VWCmgiTZ5cUz0IJ3xXxPOTZGG2eI5xE4vtr/PYCBQko7V8iQA1ebkSHAveZQ7lsJ1eRR/P9b0+TwzsC5YWmOKY/V+EPxCOPdzp6ZBZzVtQp+tMYsv6IDJ5RovusEnFZqhYtmIfcpGLJb6iLIRy1qyl3ttykaU4K2fu2JBfK4pESMCxKjb+qaGZvKuXOzPyrY9t3UnwpHr2tfKG72VC6KrWlro0bpI0vnTheG2i+PhVLjQtVyT96yR5LIBdY1Dd7jgooXhZ+qMrOX04c/mVr/lX831H02mIX1Hf1ouGw0JxXzHHadxfYY1aZyaOVs3dcUhjXt25K69Aa93yR3UmtEWQYqxlg6a7OOnD7++/Tx5/+9fKU1+efvpp5+hBTrW0vqML9J26tTOg21pp03g2LmWplM0HXeG7INodnwlHIp7Hafy7GzI2xOBbOeqvM5jXF4rRxZ0FhldkyEXm7eTgbYJ0J0K1LnYRcK1bhXAJMjxrB8YXfV5eKSjH6VBOAG9csttWzxBCAUN59fL2j5veRlaJwa6JBCfCsRdQGiwoUmd83ldDUoi+VyhzsPDHXk7DeMhHxax2RHZlDqXIpGw1TAx28dmjeqNXqR5xsPlyw2oQPraiFc/vX/7CJI3u49eVmMzblu/iPLk6KN7WS1qkxlyk8bRPh68FW5hDUVwHf5lezF4jgs7W5QPe8N+Zg7a3ujKnSboiExm1/tRfBzFmx0M6dA6pheGCFRKmu2EB5kujaO3fFIukZLWA6gEjQNxenaKQX1CkeJAnwBjoL8h6AEX8uJNDNmzku+Lse4PJqpqvhO9yfLswxdVbmnyTQVOx0FuP+9q7Ywa4bboXcV1znxPtBK/vnUJdZ0KEVLe9OLVG5jjzWhtD3zMFnlzQkFhO/YN7DGfp16FBF9Am54XngNENAIDfuYC2tGzMjAP2IUqM2x2oHi/tiOvJs5upUGiTbRfi5aCHVwHAxBGGWCUH390wjyGHUoFRS/EveYxTLqORjbqzrmD4nd6o8+XblGzvJYbyTA3EpP1iApGuI/ki7uuuLt5CsLWDHIsgnSaAZLXIBJQBdH76BEkwwpS2sng8sWfd29/fPvp/S8fRtpHvv/xyz/ffkK6He151ucRj+zIjf7mcvXo0W4xjRehJaF5LF7Q2G+QkZl0pS7U66NVg0Yllja1L8G1EVvhWK7O3jjmZU6nU35BZYHR8B2vhLWdbNKRXLSdLMf9Qyfd4ySDJhlIenyhJ//mVbhoyBFt2V7U2YOhL455kwvJwegtO9XHZ+Ya0dGbQcDxKZiYZr3+XwtkSHsWPaLV1XvAJb2PXdb4Z0TartHQsUzUufENiiC5lOqOicl3s3VR2haYuJzI8cKovw+6UceIt0++4DHZ1tqFo2K+sM/2cPN4JqZcYSXpFMCTLa2zXwZuyKWDMlznpQNGSXYW6dBlxhDybrsWs/hKcH7IrLdItzPj3d8ujCoseL2564zLW0Kk51ivBLdzzeJYOnZdURdF52va3DEqWVJGq6db/Fpw2+uI6Vi41Jn1dSO0yuoK5cxbvZUIYP9qltsuHPCRcJY7J9nO5omitoD4gMJN60EpvZrtNmFn5Vg8ObTUq/066TBLd3qNXiI1cNDXotvoLHtsPbCh6wRZT1Vcvt2knolXURWc7o/5V6Lb6SqPjTubOvsZEV0kW2cV3e+Bp4iX0jriOehobo8XXjw20c0WPO23ku00XRIKt57UepNv2yHL6LLo7/8Dj8BK4T5NAAA="""

URLS = {
"2009":"https://www.puc-rio.br/vestibular/repositorio/provas/2009/download/VEST2009PUCRio_PROVAS_GABARITOS.zip",
"2010":"https://www.puc-rio.br/vestibular/repositorio/provas/2010/download/VEST2010PUCRio_PROVAS_GABARITOS.zip",
"2011":"https://www.puc-rio.br/vestibular/repositorio/provas/2011/download/VEST2011PUCRio_PROVAS_GABARITOS_v4.zip",
"2011-inverno":"https://www.puc-rio.br/vestibular/repositorio/provas/2011-2/download/VEST2011PUCRio_PROVAS_GABARITOS.zip",
"2012-inverno":"https://www.puc-rio.br/vestibular/repositorio/provas/2012-2/download/VEST2012PUCRio_PROVAS_GABARITOS_v2.zip",
"2013":"https://www.puc-rio.br/vestibular/repositorio/provas/2013/download/VEST2013PUCRio_PROVAS_GABARITOS_v4.zip",
"2013-inverno":"https://www.puc-rio.br/vestibular/repositorio/provas/2013-2/download/VEST2013-2PUCRio_PROVAS_GABARITOS.zip",
"2014":"https://www.puc-rio.br/vestibular/repositorio/provas/2014/download/VEST2014PUCRio_PROVAS_GABARITOS_V5.zip",
"2015":"https://www.puc-rio.br/vestibular/repositorio/provas/2015/download/VEST2015PUCRio_PROVAS_GABARITOS_V3.zip",
"2015-inverno":"https://www.puc-rio.br/vestibular/repositorio/provas/2015-2/download/VestiblularPUC-RioINVERNO2015-2_provas_gabaritos.zip",
"2016-inverno":"https://www.puc-rio.br/vestibular/repositorio/provas/2016-2/download/VEST2016-2PUCRio_PROVAS_GABARITOS.zip",
"2017":"https://www.puc-rio.br/vestibular/repositorio/provas/2017/download/VEST2017PUCRio_PROVAS_GABARITOS_v4.zip",
"2017-inverno":"https://www.puc-rio.br/vestibular/repositorio/provas/2017-2/download/VestibularPUC-RioINVERNO2017-2_provas_gabaritos.zip",
"2018":"https://www.puc-rio.br/vestibular/repositorio/provas/2018/download/VEST2018PUCRio_PROVAS_GABARITOS_V7.zip",
"2018-inverno":"https://www.puc-rio.br/vestibular/repositorio/provas/2018-2/download/VestibularPUC-RioINVERNO2018-2_provas_gabaritos.zip",
"2019":"https://www.puc-rio.br/vestibular/repositorio/provas/2019/download/Vestibular2019_20181014_TodasProvasGabaritos.zip",
"2019-inverno":"https://www.puc-rio.br/vestibular/repositorio/provas/2019-2/download/VestibularInverno2019_provasegabaritos.zip",
"2020":"https://www.puc-rio.br/vestibular/repositorio/provas/2020/download/Vestibular2020_provasegabaritos_completo.zip",
"2021":"https://www.puc-rio.br/vestibular/repositorio/provas/2021/download/GABARITO-VESTIBULAR2021_completo.zip",
"2022":"https://www.puc-rio.br/vestibular/repositorio/provas/2022/download/2022-Provas-e-Gabaritos-VESTIBULAR-2022-v2.zip",
"2023":"https://www.puc-rio.br/vestibular/repositorio/provas/2023/download/Vestibular2023_provasegabaritos_completo-19-10-2022.zip",
"2024":"https://www.puc-rio.br/vestibular/repositorio/provas/2023-2/download/Vestibular2024-Provas-e-Gabaritos-v2.zip",
"2025":"https://www.puc-rio.br/vestibular/repositorio/provas/2025/download/Vestibular2025_Download-Completo.zip",
}

config = json.loads(gzip.decompress(base64.b64decode(CONFIG_GZ_B64)).decode("utf-8"))
pending = [x for x in config if not Path(x["target_path"]).exists()]
print("configured", len(config), "pending", len(pending))
if not pending:
    raise SystemExit(0)

def norm_name(s):
    return unicodedata.normalize("NFKC", s).casefold().replace("\\","/")

with tempfile.TemporaryDirectory() as td:
    td = Path(td)
    by_edition = {}
    for item in pending:
        by_edition.setdefault(item["edition"], []).append(item)
    for edition, items in by_edition.items():
        url = URLS[edition]
        zpath = td / (edition + ".zip")
        edir = td / edition
        edir.mkdir()
        print("download", edition, url)
        proc = subprocess.run(["curl","-L","--fail","--retry","3","--connect-timeout","30","--max-time","300","-o",str(zpath),url],check=False)
        if proc.returncode != 0:
            print("SKIP_DOWNLOAD_FAILED", edition, url)
            continue
        with zipfile.ZipFile(zpath) as z:
            z.extractall(edir)
        all_files = [p for p in edir.rglob("*") if p.is_file()]
        lookup = {}
        for p in all_files:
            lookup.setdefault(norm_name(p.name), []).append(p)
        for item in items:
            wanted = norm_name(item["source_basename"])
            hits = lookup.get(wanted, [])
            if not hits:
                # tolerate minor archive naming differences
                hits = [p for p in all_files if norm_name(p.name).endswith(wanted)]
            if not hits:
                raise FileNotFoundError(f'{edition}: {item["source_basename"]}')
            src = hits[0]
            doc = fitz.open(src)
            page = doc[item["page"]-1]
            rect = fitz.Rect(*item["crop"]) & page.rect
            pix = page.get_pixmap(matrix=fitz.Matrix(1.8,1.8), clip=rect, alpha=False)
            target = Path(item["target_path"])
            target.parent.mkdir(parents=True, exist_ok=True)
            pix.save(target)
            doc.close()
            try:
                im = Image.open(target)
                if im.width > 1400:
                    ratio = 1400 / im.width
                    im = im.resize((1400, max(1,int(im.height*ratio))), Image.Resampling.LANCZOS)
                im.save(target, optimize=True)
            except Exception as e:
                print("optimize warning", target, e)
            print("wrote", target)
        zpath.unlink(missing_ok=True)
