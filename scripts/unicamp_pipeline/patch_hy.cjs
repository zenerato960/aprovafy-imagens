const fs = require('fs');
const f = 'extract.mjs';
let s = fs.readFileSync(f, 'utf8');
const r = (a, b) => { if (!s.includes(a)) throw new Error('nf: ' + a.slice(0, 50)); s = s.replace(a, b); };
r("/^(se|me|te|lhe|lhes|nos|vos|o|a|os|as|lo|la|los|las|no|na|nas)$/i.test(w2)", "/^(se|me|te|lhe|lhes|nos|vos|lo|la|los|las)$/i.test(w2)");
r("/^(anti|ex|pós|pré|pró|vice|recém|além|aquém|sem|bem|mal|auto|semi|micro|macro|super|inter|sub|sócio|afro|ítalo|luso|euro|latino|norte|sul|centro)$/i.test(w1)", "/^(ex|pós|pré|pró|vice|recém|além|aquém|sem|bem|sócio|afro|ítalo|luso|euro|latino|norte|sul|centro|avant|self|well|co)$/i.test(w1)");
fs.writeFileSync(f, s);
console.log('ok');
