// Corrige quebras de linha literais dentro de strings "...\n..." que edições via shell deixaram em arquivos .mjs:
// troca join("<LF>") e split("<LF>") e '<LF>' de 1 caractere pela sequência de escape \n.
const fs = require('fs');
const f = process.argv[2];
let s = fs.readFileSync(f, 'utf8');
const before = s;
s = s.replace(/join\("\n"\)/g, 'join("\\n")').replace(/\+ "\n"/g, '+ "\\n"').replace(/join\('\n'\)/g, "join('\\n')");
fs.writeFileSync(f, s);
console.log(before === s ? 'nada alterado' : 'corrigido');
