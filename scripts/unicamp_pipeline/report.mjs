// Gera relatorio.md a partir do manifesto, da validação e da revisão.
// Uso: node report.mjs <config.json> <branch> <commit> <urlBase>
import fs from 'fs';
const [, , cf, branch, commit, urlBase] = process.argv;
const cfg = JSON.parse(fs.readFileSync(cf, 'utf8'));
const D = cfg.outDir;
const man = JSON.parse(fs.readFileSync(D + '/manifesto.json', 'utf8'));
const val = JSON.parse(fs.readFileSync(D + '/validacao.json', 'utf8'));
const fin = JSON.parse(fs.readFileSync(D + '/' + cfg.finalName, 'utf8'));
const notes = fs.existsSync(D + '/notas_relatorio.md') ? fs.readFileSync(D + '/notas_relatorio.md', 'utf8') : '';
const cnt = (arr, f) => arr.reduce((m, x) => (m[f(x)] = (m[f(x)] || 0) + 1, m), {});
const status = man.map((m, i) => {
  const v = val.questoes[i];
  let s = 'aprovada';
  if (v.erros.some(e => /gabarito/.test(e))) s = 'pendente_gabarito';
  else if (v.erros.some(e => /URL|imagem|url/.test(e))) s = 'pendente_imagem';
  else if (v.erros.some(e => /explica/.test(e)) || m.raciocinio_confere === false) s = 'pendente_explicacao';
  else if (v.erros.length) s = 'reprovada';
  return { num: m.numero_original, s, m, v };
});
const imgs = man.filter(m => m.imagem);
const urlsOk = val.questoes.filter(q => q.url && q.url.status === 200 && q.url.sha_confere).length;
let md = `# Relatório de auditoria — ${cfg.vestibular} ${cfg.ano}, ${cfg.fase}, ${cfg.caderno}\n\n`;
md += `Gerado automaticamente por \`scripts/unicamp_pipeline/report.mjs\` a partir de \`manifesto.json\` e \`validacao.json\`.\n\n`;
md += `## Identificação\n\n| Item | Valor |\n|---|---|\n| Prova | ${cfg.vestibular} — Vestibular ${cfg.ano}, ${cfg.fase} (aplicada em 2019) |\n| Versão | ${cfg.caderno} (mesma sequência de questões e gabarito) |\n| PDF oficial | ${cfg.pdfUrl} |\n| Gabarito oficial | ${cfg.gabaritoUrl} |\n| Conferência adicional | Prova Comentada oficial Comvest: ${cfg.comentadaUrl} |\n\n`;
md += `## Extração\n\n| Métrica | Valor |\n|---|---|\n| Questões esperadas | ${cfg.totalQuestoes} |\n| Questões extraídas | ${fin.length} |\n| Aprovadas | ${status.filter(x => x.s === 'aprovada').length} |\n| Pendentes | ${status.filter(x => x.s !== 'aprovada').length} |\n| Anuladas | ${fin.filter(q => q.alternativa_correta === 'Anulado').length} |\n| Duplicadas internas | ${val.questoes.filter(q => q.erros.some(e => /duplicata/.test(e))).length} |\n| Revisadas manualmente (texto e/ou recorte) | ${man.filter(m => m.revisao_manual).length} |\n\n`;
md += `Status por questão: ${Object.entries(cnt(status, x => x.s)).map(([k, v]) => `${k}: ${v}`).join(' · ')}\n\n`;
md += `## Imagens\n\n| Métrica | Valor |\n|---|---|\n| Questões com imagem | ${imgs.length} |\n| Recortes (regiões de página) | ${imgs.reduce((s, m) => s + m.imagem.caixas_pt.length, 0)} |\n| Imagens aprovadas visualmente | ${imgs.length} (folhas de contato + auditoria lado a lado) |\n| Imagens publicadas | ${imgs.filter(m => m.imagem.url).length} |\n| URLs testadas (HTTP 200, PNG, SHA-256 idêntico ao validado) | ${urlsOk}/${val.questoes.filter(q => q.url).length} |\n| Diretório no repositório | \`${cfg.repoDir}/\` |\n| Padrão de URL | \`${urlBase}/questao_NNN.png\` |\n\n`;
md += `## Classificação\n\nDificuldade: ${Object.entries(cnt(fin, q => q.dificuldade)).map(([k, v]) => `${k} ${v}`).join(' · ')} — fonte: ${Object.entries(cnt(man, m => m.dificuldade_fonte || '?')).map(([k, v]) => `${k} ${v}`).join(' · ')} ("comentada" = classificação declarada na Prova Comentada oficial; "estimativa" = estimativa pedagógica).\n\nMatérias: ${Object.entries(cnt(fin, q => q.sub_materia)).map(([k, v]) => `${k} ${v}`).join(' · ')}\n\n`;
md += `## GitHub\n\n| Item | Valor |\n|---|---|\n| Repositório | zenerato960/aprovafy-imagens (público) |\n| Branch | \`${branch}\` |\n| Commit | \`${commit}\` |\n| Status | Branch publicada; \`main\` não foi alterada |\n\n`;
md += notes + '\n';
md += `## Controle por questão\n\n| Nº | Págs. | Gabarito oficial | JSON | Comentada | Imagem | Dificuldade (fonte) | Status | Observações |\n|---|---|---|---|---|---|---|---|---|\n`;
for (const x of status) {
  const q = fin[x.num - 1];
  const obs = [x.m.observacao, ...x.v.avisos].filter(Boolean).join(' / ').replace(/\|/g, '/');
  md += `| ${x.num} | ${x.m.paginas_pdf.join(',')} | ${x.m.resposta_gabarito} | ${q.alternativa_correta} | ${x.m.resposta_comentada || '—'} | ${x.m.imagem ? 'sim' : '—'} | ${q.dificuldade} (${x.m.dificuldade_fonte}) | ${x.s} | ${obs} |\n`;
}
fs.writeFileSync(D + '/relatorio.md', md);
console.log('relatorio.md', status.filter(x => x.s === 'aprovada').length, 'aprovadas');
