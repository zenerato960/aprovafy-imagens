// Substitui caracteres de controle BACKSPACE (0x08) acidentais por "\b" literal (fronteira de palavra em regex).
const fs = require('fs');
const f = process.argv[2];
const buf = fs.readFileSync(f, 'utf8');
const BS = String.fromCharCode(8);
const out = buf.split(BS).join(String.fromCharCode(92) + 'b');
fs.writeFileSync(f, out);
console.log('ocorrências:', buf.split(BS).length - 1);
