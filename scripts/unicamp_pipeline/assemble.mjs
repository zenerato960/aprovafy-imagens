// Monta o JSON final (12 campos, mesmo modelo do ENEM 2023) + manifesto de rastreabilidade.
// Uso: node assemble.mjs <config.json> <urlBase|->
//   urlBase: prefixo público das imagens, ex. https://raw.githubusercontent.com/<dono>/<repo>/<sha>/imagens/unicamp/2020/qx
//   "-" = ainda sem URL publicada (url_imagem fica vazia e a questão fica pendente_imagem)
import fs from 'fs';
const [, , cf, urlBase] = process.argv;
const cfg = JSON.parse(fs.readFileSync(cf, 'utf8'));
const D = cfg.outDir;
const draft = JSON.parse(fs.readFileSync(D + '/draft.json', 'utf8'));
const gab = JSON.parse(fs.readFileSync(D + '/gabarito.json', 'utf8'));
const com = JSON.parse(fs.readFileSync(D + '/comentada.json', 'utf8'));
const crops = JSON.parse(fs.readFileSync(D + '/crops_manifest.json', 'utf8'));
const exp = Object.assign({}, ...cfg.explicFiles.map(f => JSON.parse(fs.readFileSync(D + '/' + f, 'utf8'))));
const audit = fs.existsSync(D + '/audit_text.json') ? JSON.parse(fs.readFileSync(D + '/audit_text.json', 'utf8')) : [];
const extra = cfg.explicOverrides ? JSON.parse(fs.readFileSync(D + '/' + cfg.explicOverrides, 'utf8')) : {};

const final = [], manifest = [];
for (const d of draft) {
  const e = { ...(exp[d.num] || {}), ...(extra[d.num] || {}) };
  const img = crops.find(c => c.num === d.num);
  const resp = gab.respostas[d.num];
  const url = img && urlBase && urlBase !== '-' ? `${urlBase}/${cfg.repoFilePrefix}${String(d.num).padStart(3, '0')}.png` : '';
  final.push({
    vestibular: cfg.vestibular,
    materia: e.materia || '',
    sub_materia: e.sub_materia || '',
    ano: cfg.ano,
    dificuldade: e.dificuldade || '',
    tipo: 'Fechada',
    topico: e.topico || '',
    enunciado: d.enunciado,
    url_imagem: url,
    alternativas: d.alternativas.join('|'),
    alternativa_correta: resp === 'Anulado' ? 'Anulado' : resp,
    explicacao: e.explicacao || '',
  });
  const a = audit.find(x => x.num === d.num);
  manifest.push({
    prova: cfg.vestibular, ano: cfg.ano, fase: cfg.fase, caderno: cfg.caderno, numero_original: d.num,
    paginas_pdf: [...new Set(d.segs.map(s => s.pn))], pdf_fonte: cfg.pdfUrl,
    gabarito_fonte: cfg.gabaritoUrl, resposta_gabarito: resp, resposta_comentada: (com[d.num] || {}).correta || null,
    resposta_json: final.at(-1).alternativa_correta,
    imagem: img ? { arquivo_local: 'img/' + img.arquivo, arquivo_repo: `${cfg.repoDir}/${cfg.repoFilePrefix}${String(d.num).padStart(3, '0')}.png`, caixas_pt: img.caixas, layout: img.layout, largura: img.largura, altura: img.altura, sha256: img.sha256, url } : null,
    revisao_manual: d.revisado, observacao: d.obs,
    auditoria_texto_comentada: a ? { cobertura: a.cobertura, ausentes: a.ausentes } : null,
    dificuldade_fonte: e.dificuldade_fonte || '', dificuldade_evidencia: e.dificuldade_evidencia || '',
    raciocinio_confere: e.raciocinio_confere ?? null, pendencia_explicacao: e.pendencia || '',
  });
}
fs.writeFileSync(D + '/' + cfg.finalName, JSON.stringify(final, null, 2));
fs.writeFileSync(D + '/manifesto.json', JSON.stringify(manifest, null, 1));
console.log('final', final.length, '->', cfg.finalName);
