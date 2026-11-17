# Pipeline UNICAMP (Comvest) → Aprovafy

Ordem de execução (Node ≥ 20; `npm install` nesta pasta; caminhos de `config/*.json` relativos à pasta de trabalho original):

1. `node extract.mjs config/unicamp2020.json`: texto por coordenadas, 2 colunas, índices, figuras candidatas (`raw.json`/`raw.txt`).
2. `node annotate.mjs config/unicamp2020.json`: páginas com grade em pt e caixas candidatas, para revisão visual.
3. Revisão manual em `config/review2020.mjs` (correções de texto, caixas de recorte, alternativas em imagem).
4. `node draft.mjs config/unicamp2020.json`: rascunho revisado (`draft.json`).
5. `node crops.mjs config/unicamp2020.json`: recortes (216 dpi) + imagens de auditoria; `node contact.mjs <img> <saída>`: folhas de contato.
6. `node gabarito.mjs <gabarito.pdf> <pág> gabarito.json` e `node comentada.mjs <prova_comentada.pdf> comentada.json`: fontes oficiais.
7. `node audit_text.mjs` / `node audit_omit.mjs`: auditoria independente contra a Prova Comentada oficial.
8. `node assemble.mjs config/unicamp2020.json <urlBase>`: JSON final (12 campos) + `manifesto.json`.
9. `node validate.mjs config/unicamp2020.json --online`: schema, conteúdo, gabarito, imagens e URLs (HTTP, PNG, SHA-256).
10. `node report.mjs config/unicamp2020.json <branch> <commit> <urlBase>`: `relatorio.md`.
