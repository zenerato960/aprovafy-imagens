import { openPdf, pageItems } from './pdflib.mjs';
for (const f of process.argv.slice(2)) {
  const doc = await openPdf(f); let res=0, txt='', meta=await doc.getMetadata().catch(()=>({}));
  for (let pn=1; pn<=doc.numPages; pn++){ const {items}=await pageItems(doc,pn); const t=items.map(i=>i.s).join(' '); if(/Resolu[cç][aã]o|Resposta:/i.test(t)) res++; if(pn<=2) txt+=t+' '; }
  console.log(`\n## ${f.split('/').pop()} pags=${doc.numPages} pagsComResolucao=${res} producer=${meta.info?.Producer} creator=${meta.info?.Creator}`);
  console.log(txt.replace(/\s+/g,' ').slice(0,300));
}
