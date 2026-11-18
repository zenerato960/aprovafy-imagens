# Relatório de auditoria — UNICAMP 2022, 1ª fase (Conhecimentos Gerais), Provas Q e X

Gerado automaticamente por `scripts/unicamp_pipeline/report.mjs` a partir de `manifesto.json` e `validacao.json`.

## Identificação

| Item | Valor |
|---|---|
| Prova | UNICAMP — Vestibular 2022, 1ª fase (Conhecimentos Gerais) (aplicada em outubro de 2021) |
| Versão | Provas Q e X (mesma sequência de questões e gabarito) |
| PDF oficial | https://www.comvest.unicamp.br/vest2022/F1/f12022Q_X.pdf |
| Gabarito oficial | https://www.comvest.unicamp.br/wp-content/uploads/2021/11/gabarito_2022_DIVULGA.pdf (pág. 1, PROVAS Q e X) |
| Conferência adicional | Prova Comentada oficial Comvest: https://www.comvest.unicamp.br/wp-content/uploads/2022/09/CQ_F1_TODAS.pdf |

## Extração

| Métrica | Valor |
|---|---|
| Questões esperadas | 72 |
| Questões extraídas | 72 |
| Aprovadas | 72 |
| Pendentes | 0 |
| Anuladas | 1 |
| Duplicadas internas | 0 |
| Revisadas manualmente (texto e/ou recorte) | 45 |

Status por questão: aprovada: 72

## Imagens

| Métrica | Valor |
|---|---|
| Questões com imagem | 35 |
| Recortes (regiões de página) | 43 |
| Imagens aprovadas visualmente | 35 (folhas de contato + auditoria lado a lado) |
| Imagens publicadas | 35 |
| URLs testadas (HTTP 200, PNG, SHA-256 idêntico ao validado) | 35/35 |
| Diretório no repositório | `imagens/unicamp/2022/qx_auditado/` |
| Padrão de URL | `https://raw.githubusercontent.com/zenerato960/aprovafy-imagens/dfd7983aab2ccacb85883e89e2333b0f605d308b/imagens/unicamp/2022/qx_auditado/questao_NNN.png` |

## Classificação

Dificuldade: Fácil 22 · Média 34 · Difícil 16 — fonte: comentada 66 · estimativa 6 ("comentada" = classificação declarada na Prova Comentada oficial; "estimativa" = estimativa pedagógica).

Matérias: Literatura 6 · Português 6 · Matemática 12 · Inglês 8 · Química 8 · Geografia 7 · Sociologia 1 · História 8 · Física 8 · Biologia 8

## GitHub

| Item | Valor |
|---|---|
| Repositório | zenerato960/aprovafy-imagens (público) |
| Branch | `unicamp-2020-2021-auditado` |
| Commit | `dfd7983` |
| Status | Branch publicada; `main` não foi alterada |

## Fontes e decisões

- **Prova:** 1ª fase do Vestibular Unicamp 2022 (Conhecimentos Gerais), Provas Q e X: 72 questões com 4 alternativas. Fonte de verdade: caderno oficial `f12022Q_X.pdf`. O arquivo `unicamp2022_1fase_vs5.pdf` que estava em Downloads é uma resolução de cursinho e não foi usado.
- **Gabarito:** `gabarito_2022_DIVULGA.pdf`, página 1 ("PROVAS Q e X").
- **Questão anulada: Q42.** O gabarito oficial traz a nota: *"A COMVEST optou por anular a questão, em virtude de um erro de plotagem no mapa referente ao bioma 3. No mapa que destaca o bioma 3, a área indicada é semidesértica e não, desértica, tal como consta da alternativa C."* O JSON usa `"Anulado"`, e a explicação reproduz essa justificativa oficial. A Prova Comentada mantém o cabeçalho "Alternativa Correta: C", mas no próprio comentário registra que a questão foi "anulada por um erro no mapa". Prevalece a anulação.
- **Prova Comentada 2022** (`CQ_F1_TODAS.pdf`): só as questões 41–48 têm cabeçalho "Questão N" legível. Por isso, o trecho de cada questão foi localizado pela busca do início do enunciado no texto da comentada (`comentada_match.mjs`). Foram localizadas 67/72 questões; as 5 restantes (Q16, Q19, Q20, Q22, Q23) são de matemática com fórmulas que a comentada codifica de forma ilegível. Em todas as questões em que a comentada declara a letra, ela coincide com o gabarito, exceto a Q42, que foi anulada.
- **Textos comuns** ("USE O TEXTO A SEGUIR PARA RESPONDER ÀS QUESTÕES 7 E 8" etc.) e a nota "Sempre que necessário aproxime π = 3." foram replicados nas questões a que se aplicam (7–8, 17–18, 36–37, 57–58, 59–60; π nas questões 57–62).
- **Fórmulas** (Q15, Q16, Q19, Q20, Q22–Q24, Q57–Q63): transcritas manualmente a partir da visualização da página. A Q19 tinha as letras dos vértices ilegíveis na extração ("AAAA") e foi transcrita como ABCD, DA, AB, BC e CD, conforme a imagem da página.
- **Alternativas em imagem:** na Q30, as quatro ilustrações ficam na imagem, em grade (a, b em cima; c, d embaixo).
- **Imagens compartilhadas:** o mural de Denilson Baniwa (Texto I) aparece nas questões 7 e 8, que usam esse texto comum. A Q6 (O Ateneu) não tem imagem.

## Correções identificadas na revisão das explicações

- **Q17:** a extração embaralhou as alternativas por causa dos subscritos de R₀. Foram transcritas a partir da página, e a explicação foi refeita sobre o texto correto.
- **Q26:** o print do post de Rishi Budhrani não tinha sido recortado. Agora ele faz parte da imagem, e a explicação foi refeita com o conteúdo do post.
- **Q3, Q31 e Q37:** o glossário, as fontes e as massas molares impressos depois da alternativa d foram movidos para o enunciado.
- **Q36 e Q40:** os rótulos dos gráficos e das estruturas foram removidos do enunciado (estão nas imagens).
- **Q20 e Q23:** a dificuldade foi ajustada para "Difícil", conforme a classificação final da Comvest na Prova Comentada.

## Auditorias executadas

1. Revisão visual das 23 páginas com grade de coordenadas.
2. Validação visual dos 35 recortes. Foram corrigidos: a Q6 (imagem atribuída por engano, removida), a Q10 (legendas cortadas), a Q36, a Q39 e a Q41 (texto vizinho), a Q42 (legenda cortada), a Q43 (falso positivo) e a Q47 (eixo de altitude cortado).
3. Comparação palavra a palavra com a Prova Comentada: 60/72 questões com cobertura ≥ 97%. As restantes se explicam por textos comuns e notas que a comentada não repete, e por fórmulas ilegíveis nela.
4. Validador de schema, conteúdo, gabarito e imagens, e teste online das URLs.
5. Comparação com a extração anterior (V11): as mesmas 72 questões e as mesmas respostas (incluindo a Q42 anulada). **Este JSON deve substituir os registros UNICAMP 2022 da V11.**

## Limitações

- O código do app Aprovafy não estava disponível. Não foi verificado o importador, o banco de produção nem a interface.

## Controle por questão

| Nº | Págs. | Gabarito oficial | JSON | Comentada | Imagem | Dificuldade (fonte) | Status | Observações |
|---|---|---|---|---|---|---|---|---|
| 1 | 3 | D | D | D | — | Fácil (comentada) | aprovada |  |
| 2 | 3 | A | A | A | — | Média (comentada) | aprovada | menciona elemento visual mas não tem imagem (conferir se o elemento é textual) |
| 3 | 3 | B | B | B | — | Média (comentada) | aprovada |  |
| 4 | 3,4 | D | D | D | — | Fácil (comentada) | aprovada |  |
| 5 | 4 | D | D | D | — | Média (comentada) | aprovada |  |
| 6 | 4 | C | C | C | — | Fácil (comentada) | aprovada |  |
| 7 | 4,5 | C | C | C | sim | Fácil (comentada) | aprovada |  |
| 8 | 5 | D | D | — | sim | Média (comentada) | aprovada |  |
| 9 | 5 | B | B | — | sim | Fácil (comentada) | aprovada |  |
| 10 | 5 | D | D | — | sim | Média (comentada) | aprovada | Texto I (André Vallias) e Texto II (Hélio Oiticica) na imagem, nesta ordem; as fontes estão no enunciado. |
| 11 | 6 | C | C | C | — | Média (comentada) | aprovada | menciona elemento visual mas não tem imagem (conferir se o elemento é textual) |
| 12 | 6 | A | A | — | sim | Difícil (comentada) | aprovada |  |
| 13 | 6 | D | D | — | — | Média (comentada) | aprovada |  |
| 14 | 6 | B | B | B | sim | Média (comentada) | aprovada |  |
| 15 | 7 | D | D | — | sim | Média (comentada) | aprovada |  |
| 16 | 7 | A | A | — | — | Média (comentada) | aprovada | Raiz de índice n escrita como ⁿ√( ). / notação ^( ) ou _( ) remanescente |
| 17 | 7 | C | C | — | — | Média (comentada) | aprovada | Alternativas transcritas a partir da página (a extração automática embaralhou as linhas por causa dos subscritos de R₀). |
| 18 | 7 | B | B | — | — | Difícil (comentada) | aprovada |  |
| 19 | 7 | B | B | — | — | Difícil (comentada) | aprovada |  |
| 20 | 7,8 | C | C | — | — | Difícil (comentada) | aprovada | Matriz escrita em linha: [1 k; 3 k²] = 1ª linha (1, k), 2ª linha (3, k²); vetores coluna [x; y] e [2021; 2022]. |
| 21 | 8 | D | D | — | sim | Difícil (comentada) | aprovada | Os emojis de pedra, papel e tesoura estão na imagem. |
| 22 | 8 | B | B | — | — | Difícil (comentada) | aprovada |  |
| 23 | 8 | A | A | — | — | Difícil (comentada) | aprovada |  |
| 24 | 8 | C | C | — | sim | Difícil (comentada) | aprovada |  |
| 25 | 9 | A | A | — | — | Fácil (comentada) | aprovada | menciona elemento visual mas não tem imagem (conferir se o elemento é textual) |
| 26 | 9 | D | D | — | sim | Fácil (comentada) | aprovada | Imagem com o infográfico da pesquisa e, abaixo, o post de Rishi Budhrani (texto em inglês do post incluído na imagem). / fragmentos curtos no enunciado (conferir): "Pode-se dizer que Budhrani" |
| 27 | 9,10 | B | B | B | sim | Fácil (comentada) | aprovada | fragmentos curtos no enunciado (conferir): "Em seu discurso, o ator" |
| 28 | 10 | B | B | — | sim | Média (comentada) | aprovada |  |
| 29 | 10 | D | D | D | — | Média (comentada) | aprovada |  |
| 30 | 10,11 | C | C | — | sim | Média (comentada) | aprovada | Alternativas exclusivamente visuais: as quatro ilustrações, na ordem a, b (linha de cima) e c, d (linha de baixo), estão na imagem. |
| 31 | 11 | A | A | — | sim | Fácil (comentada) | aprovada |  |
| 32 | 11,12 | A | A | A | — | Média (comentada) | aprovada |  |
| 33 | 12 | A | A | — | sim | Média (comentada) | aprovada |  |
| 34 | 12 | B | B | — | sim | Média (comentada) | aprovada |  |
| 35 | 12,13 | A | A | — | sim | Difícil (comentada) | aprovada |  |
| 36 | 13 | C | C | C | sim | Difícil (comentada) | aprovada |  |
| 37 | 13 | D | D | D | — | Difícil (comentada) | aprovada |  |
| 38 | 13,14 | A | A | A | sim | Difícil (comentada) | aprovada |  |
| 39 | 14 | D | D | D | sim | Fácil (comentada) | aprovada |  |
| 40 | 14 | B | B | — | sim | Média (comentada) | aprovada |  |
| 41 | 15 | B | B | B | sim | Média (comentada) | aprovada |  |
| 42 | 15 | Anulado | Anulado | C | sim | Média (estimativa) | aprovada | Questão ANULADA pela Comvest: erro de plotagem no mapa do Bioma 3 (a área indicada é semidesértica, e não desértica, como consta da alternativa c). / comentada C ≠ gabarito Anulado |
| 43 | 15,16 | D | D | D | — | Média (estimativa) | aprovada |  |
| 44 | 16 | C | C | C | sim | Fácil (comentada) | aprovada |  |
| 45 | 16,17 | A | A | A | sim | Fácil (comentada) | aprovada |  |
| 46 | 17 | B | B | B | — | Fácil (comentada) | aprovada |  |
| 47 | 17 | C | C | C | sim | Difícil (comentada) | aprovada |  |
| 48 | 17,18 | C | C | C | — | Fácil (comentada) | aprovada |  |
| 49 | 18 | D | D | — | sim | Fácil (comentada) | aprovada |  |
| 50 | 18 | A | A | — | — | Fácil (estimativa) | aprovada |  |
| 51 | 19 | A | A | — | — | Média (estimativa) | aprovada |  |
| 52 | 19 | B | B | — | — | Fácil (comentada) | aprovada | menciona elemento visual mas não tem imagem (conferir se o elemento é textual) |
| 53 | 19 | C | C | — | — | Fácil (comentada) | aprovada |  |
| 54 | 20 | C | C | — | — | Fácil (comentada) | aprovada |  |
| 55 | 20 | C | C | — | — | Fácil (estimativa) | aprovada |  |
| 56 | 20 | B | B | — | — | Média (estimativa) | aprovada |  |
| 57 | 21 | C | C | — | — | Média (comentada) | aprovada |  |
| 58 | 21 | B | B | — | — | Média (comentada) | aprovada |  |
| 59 | 21 | B | B | — | — | Média (comentada) | aprovada |  |
| 60 | 21 | C | C | — | — | Média (comentada) | aprovada |  |
| 61 | 21,22 | C | C | — | sim | Média (comentada) | aprovada |  |
| 62 | 22 | D | D | — | sim | Fácil (comentada) | aprovada |  |
| 63 | 22 | B | B | — | sim | Média (comentada) | aprovada |  |
| 64 | 22,23 | C | C | — | sim | Difícil (comentada) | aprovada |  |
| 65 | 23 | C | C | C | — | Difícil (comentada) | aprovada |  |
| 66 | 23 | C | C | C | sim | Média (comentada) | aprovada | Rótulos "Flor completa", "Flor I" e "Flor II" incluídos na imagem, sob as respectivas figuras. |
| 67 | 23,24 | B | B | B | — | Média (comentada) | aprovada |  |
| 68 | 24 | A | A | A | — | Média (comentada) | aprovada |  |
| 69 | 24 | D | D | D | sim | Fácil (comentada) | aprovada |  |
| 70 | 25 | C | C | C | sim | Média (comentada) | aprovada |  |
| 71 | 25 | D | D | D | — | Média (comentada) | aprovada |  |
| 72 | 25 | A | A | A | sim | Difícil (comentada) | aprovada |  |
