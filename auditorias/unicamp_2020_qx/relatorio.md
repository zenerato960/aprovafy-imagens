# Relatório de auditoria — UNICAMP 2020, 1ª fase (Conhecimentos Gerais), Provas Q e X

Gerado automaticamente por `scripts/unicamp_pipeline/report.mjs` a partir de `manifesto.json` e `validacao.json`.

## Identificação

| Item | Valor |
|---|---|
| Prova | UNICAMP — Vestibular 2020, 1ª fase (Conhecimentos Gerais) (aplicada em novembro de 2019) |
| Versão | Provas Q e X (mesma sequência de questões e gabarito) |
| PDF oficial | https://www.comvest.unicamp.br/vest2020/F1/f12020Q_X.pdf |
| Gabarito oficial | https://www.comvest.unicamp.br/wp-content/uploads/2019/11/gabarito2020.pdf (pág. 1, PROVAS Q e X) |
| Conferência adicional | Prova Comentada oficial Comvest: https://www.comvest.unicamp.br/wp-content/uploads/2020/10/prova_comentada_F1_2020.pdf |

## Extração

| Métrica | Valor |
|---|---|
| Questões esperadas | 90 |
| Questões extraídas | 90 |
| Aprovadas | 90 |
| Pendentes | 0 |
| Anuladas | 0 |
| Duplicadas internas | 0 |
| Revisadas manualmente (texto e/ou recorte) | 51 |

Status por questão: aprovada: 90

## Imagens

| Métrica | Valor |
|---|---|
| Questões com imagem | 35 |
| Recortes (regiões de página) | 50 |
| Imagens aprovadas visualmente | 35 (folhas de contato + auditoria lado a lado) |
| Imagens publicadas | 35 |
| URLs testadas (HTTP 200, PNG, SHA-256 idêntico ao validado) | 35/35 |
| Diretório no repositório | `imagens/unicamp/2020/qx/` |
| Padrão de URL | `https://raw.githubusercontent.com/zenerato960/aprovafy-imagens/2523f9fd9b53184603acc7b67996398226e0d87f/imagens/unicamp/2020/qx/questao_NNN.png` |

## Classificação

Dificuldade: Fácil 37 · Média 30 · Difícil 23 — fonte: comentada 90 ("comentada" = classificação declarada na Prova Comentada oficial; "estimativa" = estimativa pedagógica).

Matérias: Inglês 7 · História 11 · Física 12 · Biologia 11 · Geografia 9 · Sociologia 1 · Português 7 · Matemática 13 · Química 10 · Literatura 8 · Artes 1

## GitHub

| Item | Valor |
|---|---|
| Repositório | zenerato960/aprovafy-imagens (público) |
| Branch | `unicamp-2020-2021-auditado` |
| Commit | `2523f9f` |
| Status | Branch publicada; `main` não foi alterada |

## Fontes e decisões

- **Fonte de verdade do texto:** caderno oficial Comvest `f12020Q_X.pdf` (Provas Q e X, 90 questões, 4 alternativas cada). Os PDFs `unicamp2020_1fase.pdf` que estavam em Downloads são resoluções comentadas de cursinho e **não** foram usados como fonte.
- **Gabarito:** `gabarito2020.pdf`, página 1 ("PROVAS Q e X"). Conferido também contra a "Alternativa Correta" da Prova Comentada oficial: **0 divergências** em 89 questões identificadas ali (a Q80 ficou unida à Q79 no texto da comentada; a resposta da Q80 vem do gabarito). Não há questões anuladas nesta versão.
- **Ano:** `ano = 2020` = ano do Vestibular Unicamp 2020 (1ª fase aplicada em novembro de 2019), mesma convenção dos registros UNICAMP já existentes.
- **Extração:** texto por coordenadas (pdfjs), reconstrução de 2 colunas, sobrescritos/subscritos detectados por posição e tamanho (ex.: ²²²X, C₃H₈, mol⁻¹), glifos de fontes Symbol/Cambria Math mapeados para Unicode. Fórmulas que o PDF codifica como objetos de equação (Q38–Q44, Q70–Q79) foram transcritas manualmente e conferidas em zoom.
- **Notação em texto puro:** índices sem equivalente Unicode foram escritos com sublinhado (F_P, θ_P, m_sonda, f_rádio, r_eia); matriz da Q39 em linha `[p 2; 0 p]`; vetores com seta combinante (F⃗_P, mg⃗).
- **Textos-base compartilhados:** o texto comum das Q65–66 e das Q71–73 e a observação "aproxime π = 3,0" (Q70–79) foram replicados em cada questão, porque cada registro é independente no Aprovafy.
- **Alternativas em imagem (Q45, Q51, Q70, Q78):** o modelo só tem um `url_imagem`; os quatro gráficos foram compostos numa única imagem em grade 2×2, com as letras a)–d) originais preservadas, e o texto da alternativa remete à figura ("Gráfico a.", "Curva do gráfico a. …").
- **Imagens múltiplas (Q16, Q46, Q79):** composição vertical única, preservando a ordem da prova.
- **Elementos tabulares/gráficos com texto** (tabelas das Q48, Q54, Q79; gráficos das Q46, Q47, Q52): o conteúdo fica na imagem; os rótulos não foram repetidos no enunciado.

## Divergências e normalizações registradas

- **Q5:** a Prova Comentada traz o enunciado e a alternativa c) reescritos ("retirado do site"; "estimular a discussão a respeito de estereótipos"). O JSON segue o caderno aplicado ("publicado no site"; "estimular o combate aos estereótipos"), conferido visualmente.
- **Q56:** a equação de combustão do propano está no caderno sem o coeficiente do O₂ (`C₃H₈(g) + O₂(g) → 3CO₂(g) + 4H₂O(g)`); foi mantida como no original.
- **Referências bibliográficas:** foram removidos somente os espaços que a justificação do texto inseriu dentro de URLs (Q64, Q65/66, Q68, Q69) e as quebras de data ("01/06/ 2019"). Nenhuma outra palavra foi alterada.
- **Q24 (correção pós-publicação inicial):** o JSON publicado no commit 713722e tinha uma quebra de parágrafo indevida antes do travessão em "sociedade moderna – uma sociedade…". A regra do extrator foi corrigida, e só a Q24 mudou (verificado por diff das 90 questões).
- **Hifenização:** hifens de fim de linha foram mantidos como hífen real (meia-vida, castanha-do-brasil, presume-se) e retirados apenas em quebras silábicas das referências ("Aces-sado", "Acessa-do").

## Auditorias executadas

1. **Revisão visual página a página** (25 páginas com grade de coordenadas) e zoom nas fórmulas.
2. **Validação visual dos 35 recortes** em folhas de contato; 12 caixas foram ajustadas por conterem fragmentos de texto vizinho, e todos os recortes foram revalidados.
3. **Auditoria textual independente:** a transcrição foi comparada, palavra a palavra, com o texto da Prova Comentada oficial (outro PDF, outro layout). 79/90 questões tiveram cobertura ≥ 97%. As 11 restantes foram explicadas (textos-base compartilhados que a comentada não repete, a nota de π e a notação de expoentes). A checagem inversa, de omissões, não encontrou trechos de enunciado faltando, a não ser texto que está dentro das imagens e a reescrita da Q5 na comentada.
4. **Validador de schema e conteúdo** (`validate.mjs`): 12 campos na ordem do modelo, tipos, valores permitidos, 4 alternativas, gabarito oficial = JSON, ausência de glifos corrompidos, Base64 e duplicatas, e integridade (SHA-256) das imagens.
5. **Teste online das URLs:** HTTP 200, assinatura PNG e SHA-256 do conteúdo baixado igual ao do arquivo validado.
6. **Comparação com a extração anterior (V11):** as mesmas 90 questões e **as mesmas letras de resposta** do gabarito oficial. A V11 tinha 26 imagens com caminhos relativos inexistentes no repositório, 209 explicações-placeholder no conjunto 2020–2025 e dificuldade "Média" em tudo. **Este JSON deve substituir os registros UNICAMP 2020 da V11, não ser somado a eles.**

## Limitações

- O código do app Aprovafy (importador e banco) não estava disponível nesta máquina. Por isso, não foram verificados o catálogo de valores aceitos (dificuldade, tópico), a aceitação de `"Anulado"` pelo importador nem a existência prévia de registros no banco de produção. Também não houve teste visual na interface real.
- A explicação e a classificação (matéria, tópico, dificuldade estimada) foram redigidas com apoio de subagentes e revisadas pelo agente principal; a dificuldade marcada como "comentada" reproduz a avaliação declarada pela Comvest.

## Controle por questão

| Nº | Págs. | Gabarito oficial | JSON | Comentada | Imagem | Dificuldade (fonte) | Status | Observações |
|---|---|---|---|---|---|---|---|---|
| 1 | 3 | D | D | D | sim | Fácil (comentada) | aprovada |  |
| 2 | 3 | A | A | A | sim | Fácil (comentada) | aprovada |  |
| 3 | 3 | A | A | A | sim | Fácil (comentada) | aprovada |  |
| 4 | 3,4 | B | B | B | sim | Fácil (comentada) | aprovada |  |
| 5 | 4 | C | C | C | sim | Fácil (comentada) | aprovada |  |
| 6 | 4 | D | D | D | sim | Fácil (comentada) | aprovada |  |
| 7 | 4,5 | C | C | C | — | Média (comentada) | aprovada |  |
| 8 | 5 | D | D | D | sim | Média (comentada) | aprovada |  |
| 9 | 5 | D | D | D | — | Fácil (comentada) | aprovada |  |
| 10 | 5,6 | D | D | D | — | Média (comentada) | aprovada |  |
| 11 | 6 | A | A | A | — | Difícil (comentada) | aprovada |  |
| 12 | 6 | D | D | D | sim | Fácil (comentada) | aprovada |  |
| 13 | 6 | B | B | B | — | Difícil (comentada) | aprovada |  |
| 14 | 6,7 | B | B | B | sim | Média (comentada) | aprovada |  |
| 15 | 7 | C | C | C | — | Média (comentada) | aprovada |  |
| 16 | 7 | B | B | B | sim | Fácil (comentada) | aprovada |  |
| 17 | 8 | D | D | D | — | Média (comentada) | aprovada |  |
| 18 | 8 | A | A | A | — | Fácil (comentada) | aprovada |  |
| 19 | 8 | C | C | C | sim | Média (comentada) | aprovada |  |
| 20 | 9 | A | A | A | — | Difícil (comentada) | aprovada |  |
| 21 | 9 | B | B | B | — | Fácil (comentada) | aprovada |  |
| 22 | 9 | B | B | B | — | Difícil (comentada) | aprovada |  |
| 23 | 9 | A | A | A | — | Difícil (comentada) | aprovada |  |
| 24 | 10 | D | D | D | — | Difícil (comentada) | aprovada | menciona elemento visual mas não tem imagem (conferir se o elemento é textual) |
| 25 | 10 | D | D | D | sim | Fácil (comentada) | aprovada |  |
| 26 | 10 | D | D | D | sim | Fácil (comentada) | aprovada |  |
| 27 | 11 | C | C | C | — | Média (comentada) | aprovada |  |
| 28 | 11 | A | A | A | sim | Média (comentada) | aprovada |  |
| 29 | 11 | B | B | B | — | Média (comentada) | aprovada |  |
| 30 | 11 | B | B | B | — | Fácil (comentada) | aprovada | menciona elemento visual mas não tem imagem (conferir se o elemento é textual) |
| 31 | 12 | C | C | C | — | Difícil (comentada) | aprovada | menciona elemento visual mas não tem imagem (conferir se o elemento é textual) |
| 32 | 12 | C | C | C | — | Fácil (comentada) | aprovada |  |
| 33 | 12 | B | B | B | — | Difícil (comentada) | aprovada |  |
| 34 | 12 | C | C | C | — | Difícil (comentada) | aprovada |  |
| 35 | 12 | A | A | A | — | Fácil (comentada) | aprovada |  |
| 36 | 12 | D | D | D | — | Difícil (comentada) | aprovada |  |
| 37 | 12 | C | C | C | — | Fácil (comentada) | aprovada |  |
| 38 | 13 | A | A | A | — | Fácil (comentada) | aprovada |  |
| 39 | 13 | B | B | B | — | Média (comentada) | aprovada | Matriz 2×2 escrita em linha: [p 2; 0 p] = 1ª linha (p, 2), 2ª linha (0, p). Barras de módulo grafadas com ∣ (U+2223) porque / é o separador de alternativas. |
| 40 | 13 | A | A | A | sim | Difícil (comentada) | aprovada |  |
| 41 | 13 | B | B | B | sim | Média (comentada) | aprovada |  |
| 42 | 13 | C | C | C | sim | Média (comentada) | aprovada |  |
| 43 | 13 | D | D | D | — | Difícil (comentada) | aprovada |  |
| 44 | 13 | C | C | C | — | Média (comentada) | aprovada |  |
| 45 | 14 | D | D | D | sim | Média (comentada) | aprovada | Alternativas compostas por gráfico + texto: os quatro gráficos (com as letras a–d) estão na imagem; o texto de cada alternativa remete ao gráfico de mesma letra. |
| 46 | 14 | B | B | B | sim | Fácil (comentada) | aprovada |  |
| 47 | 14,15 | D | D | D | sim | Média (comentada) | aprovada |  |
| 48 | 15 | C | C | C | sim | Difícil (comentada) | aprovada |  |
| 49 | 15 | B | B | B | — | Fácil (comentada) | aprovada |  |
| 50 | 16 | A | A | A | — | Fácil (comentada) | aprovada |  |
| 51 | 16 | C | C | C | sim | Difícil (comentada) | aprovada | Alternativas compostas por gráfico (concentração de CO₂ e pH × ano) + texto: os quatro gráficos com as letras a–d estão na imagem. |
| 52 | 16,17 | A | A | A | sim | Fácil (comentada) | aprovada |  |
| 53 | 17 | C | C | C | — | Difícil (comentada) | aprovada |  |
| 54 | 17 | A | A | A | sim | Difícil (comentada) | aprovada |  |
| 55 | 17 | B | B | B | — | Fácil (comentada) | aprovada |  |
| 56 | 18 | D | D | D | — | Difícil (comentada) | aprovada | Equação de combustão do propano reproduzida como no original (sem coeficiente estequiométrico no O₂). |
| 57 | 18 | C | C | C | — | Média (comentada) | aprovada |  |
| 58 | 18 | D | D | D | — | Média (comentada) | aprovada |  |
| 59 | 18,19 | B | B | B | sim | Difícil (comentada) | aprovada |  |
| 60 | 19 | C | C | C | — | Fácil (comentada) | aprovada |  |
| 61 | 19 | D | D | D | — | Média (comentada) | aprovada |  |
| 62 | 19 | B | B | B | — | Média (comentada) | aprovada | menciona elemento visual mas não tem imagem (conferir se o elemento é textual) |
| 63 | 19,20 | C | C | C | — | Média (comentada) | aprovada |  |
| 64 | 20 | D | D | D | sim | Fácil (comentada) | aprovada |  |
| 65 | 20 | A | A | A | — | Fácil (comentada) | aprovada |  |
| 66 | 20 | C | C | C | — | Média (comentada) | aprovada |  |
| 67 | 20,21 | B | B | B | sim | Fácil (comentada) | aprovada |  |
| 68 | 21 | B | B | B | — | Média (comentada) | aprovada |  |
| 69 | 21 | A | A | A | sim | Média (comentada) | aprovada |  |
| 70 | 22 | A | A | A | sim | Fácil (comentada) | aprovada | Alternativas exclusivamente gráficas (velocidade × tempo): os quatro gráficos com as letras a–d estão na imagem. |
| 71 | 22 | D | D | D | — | Média (comentada) | aprovada |  |
| 72 | 22 | B | B | B | — | Difícil (comentada) | aprovada |  |
| 73 | 22 | B | B | B | — | Difícil (comentada) | aprovada |  |
| 74 | 23 | A | A | A | sim | Média (comentada) | aprovada |  |
| 75 | 23 | D | D | D | — | Difícil (comentada) | aprovada |  |
| 76 | 23 | C | C | C | sim | Difícil (comentada) | aprovada |  |
| 77 | 23 | C | C | C | — | Média (comentada) | aprovada | menciona elemento visual mas não tem imagem (conferir se o elemento é textual) |
| 78 | 24 | A | A | A | sim | Fácil (comentada) | aprovada | Alternativas exclusivamente gráficas (traçado de raios na lupa): as quatro figuras com as letras a–d estão na imagem. |
| 79 | 24 | B | B | B | sim | Difícil (comentada) | aprovada |  |
| 80 | 24,25 | D | D | — | — | Fácil (comentada) | aprovada |  |
| 81 | 25 | A | A | A | sim | Fácil (comentada) | aprovada |  |
| 82 | 25 | B | B | B | — | Fácil (comentada) | aprovada |  |
| 83 | 25 | D | D | D | — | Fácil (comentada) | aprovada |  |
| 84 | 26 | B | B | B | — | Média (comentada) | aprovada |  |
| 85 | 26 | A | A | A | — | Fácil (comentada) | aprovada | menciona elemento visual mas não tem imagem (conferir se o elemento é textual) |
| 86 | 26 | D | D | D | sim | Fácil (comentada) | aprovada |  |
| 87 | 26,27 | C | C | C | — | Média (comentada) | aprovada | menciona elemento visual mas não tem imagem (conferir se o elemento é textual) |
| 88 | 27 | C | C | C | — | Fácil (comentada) | aprovada |  |
| 89 | 27 | D | D | D | — | Fácil (comentada) | aprovada | menciona elemento visual mas não tem imagem (conferir se o elemento é textual) |
| 90 | 27 | B | B | B | — | Média (comentada) | aprovada |  |
