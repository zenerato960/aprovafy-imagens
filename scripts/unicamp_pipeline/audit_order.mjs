// Auditoria de ordem/integridade das alternativas e de figuras possivelmente omitidas.
// 1) Cada alternativa (normalizada, sem espaços) deve aparecer como trecho contíguo no texto da Prova Comentada
//    (que reproduz a questão). Alternativas não encontradas são listadas para conferência visual.
// 2) Questões cujo enunciado anuncia um elemento visual ("a seguir", "abaixo", "imagem", "figura", "post"...)
//    e que não têm recorte são listadas.
// Uso: node audit_order.mjs <config.json>
import fs from 'fs';
const cfg = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const draft = JSON.parse(fs.readFileSync(cfg.outDir + '/draft.json', 'utf8'));
const com = JSON.parse(fs.readFileSync(cfg.outDir + '/comentada.json', 'utf8'));
const key = s => s.normalize('NFKD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]/g, '');
const alt = [], vis = [];
for (const d of draft) {
  const c = key([com[d.num - 1], com[d.num], com[d.num + 1]].filter(Boolean).map(x => x.texto).join(' '));
  if (c) d.alternativas.forEach((a, i) => {
    const k = key(a);
    if (k.length < 25) return; // curtas/numéricas: sem informação de ordem
    // trecho do meio (evita diferenças de pontuação final)
    const mid = k.slice(Math.floor(k.length * 0.25), Math.floor(k.length * 0.75));
    if (!c.includes(mid)) alt.push(`Q${d.num}${'abcd'[i]}`);
  });
  const t = d.enunciado.toLowerCase();
  if (!d.crops.length && /(a seguir|abaixo|imagem|figura|gráfico|mapa|tabela|charge|cartaz|post|tirinha|ilustra|foto)/.test(t)) vis.push(d.num);
}
console.log('alternativas sem trecho contíguo na comentada:', alt.join(' ') || 'nenhuma');
console.log('questões que anunciam elemento visual sem recorte:', vis.join(',') || 'nenhuma');
