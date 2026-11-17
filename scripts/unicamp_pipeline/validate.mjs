// Validador independente do JSON final (não reutiliza o código de extração).
// Uso: node validate.mjs <config.json> [--online]
// Verifica schema (12 campos, tipos, valores permitidos), conteúdo, gabarito oficial, imagens e (com --online) URLs.
// Saída: <outDir>/validacao.json com status por questão; código de saída 1 se houver erro crítico.
import fs from 'fs';
import crypto from 'crypto';
const [, , cf, flag] = process.argv;
const cfg = JSON.parse(fs.readFileSync(cf, 'utf8'));
const D = cfg.outDir;
const raw = fs.readFileSync(D + '/' + cfg.finalName, 'utf8');
const data = JSON.parse(raw);
const gab = JSON.parse(fs.readFileSync(D + '/gabarito.json', 'utf8')).respostas;
const man = JSON.parse(fs.readFileSync(D + '/manifesto.json', 'utf8'));
const FIELDS = ['vestibular', 'materia', 'sub_materia', 'ano', 'dificuldade', 'tipo', 'topico', 'enunciado', 'url_imagem', 'alternativas', 'alternativa_correta', 'explicacao'];
const MAT = { 'Linguagens': ['Inglês', 'Português', 'Literatura', 'Artes', 'Espanhol', 'Língua Portuguesa'], 'Ciências Humanas': ['História', 'Geografia', 'Filosofia', 'Sociologia'], 'Ciências da Natureza': ['Biologia', 'Química', 'Física'], 'Matemática': ['Matemática'] };
const DIF = ['Fácil', 'Média', 'Difícil'];
const NALT = cfg.numAlternativas;
const LETRAS = 'ABCDE'.slice(0, NALT).split('');
const errosGlobais = [];
if (!Array.isArray(data)) errosGlobais.push('raiz não é array');
if (/base64|data:image/i.test(raw)) errosGlobais.push('Base64 encontrado no JSON');
if (data.length !== cfg.totalQuestoes) errosGlobais.push(`contagem ${data.length} ≠ ${cfg.totalQuestoes}`);
const seen = new Map();
const res = [];
for (let i = 0; i < data.length; i++) {
  const q = data[i], m = man[i], E = [], W = [];
  const num = m?.numero_original;
  const keys = Object.keys(q);
  if (keys.length !== 12 || FIELDS.some((f, k) => keys[k] !== f)) E.push('campos/ordem diferentes do modelo: ' + keys.join(','));
  for (const f of FIELDS) if (f !== 'ano' && typeof q[f] !== 'string') E.push(`campo ${f} não é string`);
  if (typeof q.ano !== 'number' || q.ano !== cfg.ano) E.push('ano inválido');
  if (q.vestibular !== cfg.vestibular) E.push('vestibular inválido');
  if (q.tipo !== 'Fechada') E.push('tipo inválido');
  if (!MAT[q.materia]) E.push('materia inválida: ' + q.materia);
  else if (!MAT[q.materia].includes(q.sub_materia)) E.push(`sub_materia ${q.sub_materia} incompatível com ${q.materia}`);
  if (!DIF.includes(q.dificuldade)) E.push('dificuldade inválida: ' + q.dificuldade);
  if (q.enunciado.trim().length < 15) E.push('enunciado vazio/curto');
  const alts = q.alternativas.split('|');
  if (alts.length !== NALT) E.push(`${alts.length} alternativas (esperado ${NALT})`);
  if (alts.some(a => !a.trim())) E.push('alternativa vazia');
  if (alts.some(a => /^[a-eA-E]\)\s/.test(a))) E.push('alternativa com rótulo a)/b)… embutido');
  if (new Set(alts.map(a => a.trim().toLowerCase())).size !== alts.length) W.push('alternativas repetidas');
  const okResp = [...LETRAS, 'Anulado'];
  if (!okResp.includes(q.alternativa_correta)) E.push('alternativa_correta inválida: ' + q.alternativa_correta);
  if (gab[num] !== q.alternativa_correta) E.push(`gabarito oficial ${gab[num]} ≠ JSON ${q.alternativa_correta}`);
  if (m.resposta_comentada && m.resposta_comentada !== gab[num]) W.push(`comentada ${m.resposta_comentada} ≠ gabarito ${gab[num]}`);
  const ex = q.explicacao.trim();
  if (ex.length < 60) E.push('explicação ausente/curta');
  if (/^a alternativa correta é [a-e] porque/i.test(ex) || /corresponde ao conteúdo/i.test(ex)) E.push('explicação genérica');
  const txt = q.enunciado + q.alternativas + q.explicacao;
  if (/[ऀ-෿ሀ-᏿-�]/.test(txt)) E.push('caractere corrompido (glifo de fonte matemática/PUA)');
  if (/\^\(|_\(/.test(txt)) W.push('notação ^( ) ou _( ) remanescente');
  if (/\s{2,}/.test(q.enunciado.replace(/\n/g, ' '))) W.push('espaços duplos');
  if (/(figura|gráfico|imagem|charge|tirinha|mapa|cartaz|tabela|esquema|ilustração|fotomicrografia|quadro)\b/i.test(q.enunciado + q.alternativas) && !m.imagem) W.push('menciona elemento visual mas não tem imagem (conferir se o elemento é textual)');
  if (m.imagem) {
    if (!q.url_imagem) E.push('imagem existe mas url_imagem vazia');
    else if (!/^https:\/\/\S+\.png$/.test(q.url_imagem)) E.push('url_imagem com formato inválido');
    const p = D + '/' + m.imagem.arquivo_local;
    if (!fs.existsSync(p)) E.push('arquivo de imagem local ausente');
    else {
      const b = fs.readFileSync(p);
      if (b.slice(0, 8).toString('hex') !== '89504e470d0a1a0a') E.push('arquivo não é PNG');
      if (crypto.createHash('sha256').update(b).digest('hex') !== m.imagem.sha256) E.push('hash da imagem diverge do manifesto');
      if (m.imagem.largura < 150 || m.imagem.altura < 100) W.push('imagem pequena');
    }
  } else if (q.url_imagem) E.push('url_imagem sem imagem no manifesto');
  const key = q.enunciado.replace(/\s+/g, ' ').slice(0, 300) + '|' + q.alternativas;
  if (seen.has(key)) E.push('duplicata da questão ' + seen.get(key)); else seen.set(key, num);
  if (m.raciocinio_confere === false) W.push('explicação: raciocínio do redator não conferiu com o gabarito — revisar');
  if (m.pendencia_explicacao) W.push('pendência da explicação: ' + m.pendencia_explicacao);
  res.push({ num, erros: E, avisos: W });
}
// numeração completa
const nums = man.map(m => m.numero_original);
for (let n = 1; n <= cfg.totalQuestoes; n++) if (!nums.includes(n)) errosGlobais.push('questão ausente: ' + n);

if (flag === '--online') {
  for (let i = 0; i < data.length; i++) {
    const q = data[i]; if (!q.url_imagem) continue;
    const r = res[i];
    try {
      const resp = await fetch(q.url_imagem);
      const ct = resp.headers.get('content-type') || '';
      const b = Buffer.from(await resp.arrayBuffer());
      const sha = crypto.createHash('sha256').update(b).digest('hex');
      r.url = { status: resp.status, content_type: ct, bytes: b.length, sha_confere: sha === man[i].imagem.sha256 };
      if (resp.status !== 200) r.erros.push('URL HTTP ' + resp.status);
      else if (b.slice(0, 8).toString('hex') !== '89504e470d0a1a0a') r.erros.push('URL não retorna PNG (' + ct + ')');
      else if (!r.url.sha_confere) r.erros.push('conteúdo da URL difere do arquivo validado');
    } catch (e) { r.erros.push('URL inacessível: ' + e.message); }
  }
}
const out = { arquivo: cfg.finalName, total: data.length, errosGlobais, online: flag === '--online', questoes: res, resumo: { com_erro: res.filter(r => r.erros.length).map(r => r.num), com_aviso: res.filter(r => r.avisos.length).map(r => r.num) } };
fs.writeFileSync(D + '/validacao.json', JSON.stringify(out, null, 1));
console.log('erros globais:', errosGlobais.length ? errosGlobais : 'nenhum');
for (const r of res) if (r.erros.length || r.avisos.length) console.log(`Q${r.num}`, r.erros.length ? 'ERRO: ' + r.erros.join('; ') : '', r.avisos.length ? 'AVISO: ' + r.avisos.join('; ') : '');
console.log(`questões sem erro: ${res.filter(r => !r.erros.length).length}/${res.length}` + (flag === '--online' ? ` | URLs testadas: ${res.filter(r => r.url).length}, OK: ${res.filter(r => r.url && r.url.status === 200 && r.url.sha_confere).length}` : ''));
process.exit(errosGlobais.length || res.some(r => r.erros.length) ? 1 : 0);
