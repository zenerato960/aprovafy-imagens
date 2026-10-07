from pathlib import Path
src=Path("scripts/propor_recortes_fatec_v7.py").read_text(encoding="utf-8")
old='''    # Image blocks are strong visual candidates even when they contain text.\n    strong=[]\n    for b in tdict.get("blocks",[]):\n        if b.get("type")!=1: continue\n        rr=fitz.Rect(b["bbox"]) & region\n        if rr.get_area()<=0: continue\n        x0,y0,x1,y1=page_to_px_rect(rr,region,scale)\n        if (x1-x0)>20 and (y1-y0)>20:\n            strong.append((x0,y0,x1,y1,10.0))\n'''
new='''    # Do not trust whole raster image blocks as visual bounds: several FATEC PDFs\n    # store an entire question as one raster block. We detect the actual visual\n    # from the rendered page after masking the PDF text layer instead.\n    strong=[]\n'''
if old not in src:
    raise RuntimeError("v7 raster block section not found")
src=src.replace(old,new)
src=src.replace('out_root=Path("auditorias/fatec_v7")','out_root=Path("auditorias/fatec_v9")')
src=src.replace('sheet_root=Path("auditorias/fatec_v7_sheets")','sheet_root=Path("auditorias/fatec_v9_sheets")')
exec(compile(src,"fatec_v9_runtime.py","exec"))
