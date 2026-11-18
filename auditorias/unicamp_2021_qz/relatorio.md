# Relatório de auditoria — UNICAMP 2021, 1ª fase (Conhecimentos Gerais), Provas Q e Z (dia 2: Biológicas e Saúde)

Gerado automaticamente por `scripts/unicamp_pipeline/report.mjs` a partir de `manifesto.json` e `validacao.json`.

## Identificação

| Item | Valor |
|---|---|
| Prova | UNICAMP — Vestibular 2021, 1ª fase (Conhecimentos Gerais) (aplicada em janeiro de 2021, dia 2) |
| Versão | Provas Q e Z (dia 2: Biológicas e Saúde) (mesma sequência de questões e gabarito) |
| PDF oficial | https://www.comvest.unicamp.br/vest2021/F1/f12021Q_Z.pdf |
| Gabarito oficial | https://www.comvest.unicamp.br/wp-content/uploads/2021/01/DIA2_gabarito_2020.pdf (pág. 1, PROVAS Q e Z) |
| Conferência adicional | Prova Comentada oficial Comvest: https://www.comvest.unicamp.br/wp-content/uploads/2022/01/F1_Comentada_Conhec_Gerais_Biologicas_Saude_Q-Z.pdf |

## Extração

| Métrica | Valor |
|---|---|
| Questões esperadas | 72 |
| Questões extraídas | 72 |
| Aprovadas | 72 |
| Pendentes | 0 |
| Anuladas | 1 |
| Duplicadas internas | 0 |
| Revisadas manualmente (texto e/ou recorte) | 24 |

Status por questão: aprovada: 72

## Imagens

| Métrica | Valor |
|---|---|
| Questões com imagem | 23 |
| Recortes (regiões de página) | 29 |
| Imagens aprovadas visualmente | 23 (folhas de contato + auditoria lado a lado) |
| Imagens publicadas | 23 |
| URLs testadas (HTTP 200, PNG, SHA-256 idêntico ao validado) | 23/23 |
| Diretório no repositório | `imagens/unicamp/2021/dia2_qz/` |
| Padrão de URL | `https://raw.githubusercontent.com/zenerato960/aprovafy-imagens/cfe829e2c9cc6d87a3e4b08785766087704d67a3/imagens/unicamp/2021/dia2_qz/questao_NNN.png` |

## Classificação

Dificuldade: Média 27 · Fácil 24 · Difícil 21 — fonte: comentada 66 · estimativa 6 ("comentada" = classificação declarada na Prova Comentada oficial; "estimativa" = estimativa pedagógica).

Matérias: Literatura 6 · Português 6 · Inglês 8 · Biologia 8 · Química 7 · Física 9 · Matemática 12 · História 8 · Geografia 7 · Sociologia 1

## GitHub

| Item | Valor |
|---|---|
| Repositório | zenerato960/aprovafy-imagens (público) |
| Branch | `unicamp-2020-2021-auditado` |
| Commit | `cfe829e` |
| Status | Branch publicada; `main` não foi alterada |

## Fontes e decisões

- **Prova:** 1ª fase do Vestibular Unicamp 2021, **dia 2** (Conhecimentos Gerais para Biológicas e Saúde), Provas Q e Z: 72 questões com 4 alternativas cada. O dia 1 está no lote `unicamp_2021_eg`.
- **Fonte de verdade do texto:** caderno oficial `f12021Q_Z.pdf`, que é idêntico, byte a byte (mesmo tamanho), ao arquivo `comvest-…-prova.pdf` que já estava em Downloads.
- **Gabarito:** arquivo oficial `DIA2_gabarito_2020.pdf`. O nome tem "2020", mas o documento é o gabarito do dia 2 do Vestibular 2021, publicado em 08/01/2021. Foi usada a página 1 ("PROVAS Q e Z"), conferida contra a Prova Comentada oficial: 0 divergências nas 71 questões com alternativa.
- **Questão anulada: Q48.** O gabarito oficial marca "*" com a legenda "* Questão anulada", e a Prova Comentada registra "Questão anulada" sem justificativa. O JSON usa `"alternativa_correta": "Anulado"`, como no modelo, e a explicação informa a anulação sem atribuir causa.
- **Fórmulas** (Q38, Q40–Q46, Q48–Q56): transcritas manualmente a partir da visualização ampliada. Os textos comuns ("Texto comum para questões 49 e 50", "52 e 53", "54, 55 e 56") e a observação "use π = 3 e g = 10 m/s²" foram replicados em cada questão.
- **Notação em texto puro:** frações compostas e matrizes em linha (`[a −1; a−2 a]·[x; y] = [3; a−4]`), raiz de índice 2021 escrita como ²⁰²¹√(10^(3x+5)) e índices com sublinhado.
- **Alternativas em imagem:** na Q38, os quatro gráficos de y = p(x), com as letras a–d, ficam na imagem.
- **Falsos positivos removidos:** caixas de destaque em torno de "100 W", "15 minutos" e "3,0×10⁸ m/s" (Q54 e Q56) não são figuras e não foram recortadas.

## Auditorias executadas

1. Revisão visual de todas as páginas e zoom nas fórmulas.
2. Validação visual dos 23 recortes. Foram ajustadas as caixas da Q31 (rótulo "10000" do eixo, que estava cortado) e da Q62 (faixa do cabeçalho "QUESTÃO 62").
3. Comparação palavra a palavra com a Prova Comentada oficial: 65/72 questões com cobertura ≥ 97%. As 7 restantes (Q50–Q56) variam porque a comentada não repete os textos comuns e a nota de π/g.
4. Validador de schema, conteúdo, gabarito e imagens, e teste online das URLs.
5. Comparação com a extração anterior (V11): as mesmas 72 questões e as mesmas respostas, incluindo a Q48 anulada. **Este JSON deve substituir os registros correspondentes da V11.**

## Limitações

- O código do app Aprovafy não estava disponível. Não foi verificado se o importador aceita `"Anulado"`, nem o banco ou a interface.

## Controle por questão

| Nº | Págs. | Gabarito oficial | JSON | Comentada | Imagem | Dificuldade (fonte) | Status | Observações |
|---|---|---|---|---|---|---|---|---|
| 1 | 3 | C | C | C | — | Média (comentada) | aprovada |  |
| 2 | 3 | B | B | B | — | Média (comentada) | aprovada |  |
| 3 | 3 | D | D | D | — | Fácil (estimativa) | aprovada |  |
| 4 | 3 | B | B | B | — | Média (comentada) | aprovada |  |
| 5 | 4 | B | B | B | — | Média (comentada) | aprovada | menciona elemento visual mas não tem imagem (conferir se o elemento é textual) |
| 6 | 4 | B | B | B | — | Média (comentada) | aprovada |  |
| 7 | 4 | D | D | D | — | Difícil (comentada) | aprovada |  |
| 8 | 4,5 | A | A | A | — | Difícil (comentada) | aprovada |  |
| 9 | 5 | B | B | B | — | Fácil (comentada) | aprovada |  |
| 10 | 5 | A | A | A | — | Média (comentada) | aprovada |  |
| 11 | 5 | C | C | C | — | Média (comentada) | aprovada |  |
| 12 | 5,6 | B | B | B | — | Fácil (comentada) | aprovada |  |
| 13 | 6 | C | C | C | sim | Fácil (comentada) | aprovada |  |
| 14 | 6 | D | D | D | sim | Fácil (comentada) | aprovada |  |
| 15 | 6,7 | D | D | D | — | Média (comentada) | aprovada |  |
| 16 | 7 | B | B | B | — | Média (comentada) | aprovada |  |
| 17 | 7 | B | B | B | sim | Fácil (comentada) | aprovada |  |
| 18 | 7,8 | C | C | C | sim | Difícil (comentada) | aprovada |  |
| 19 | 8 | A | A | A | — | Difícil (comentada) | aprovada |  |
| 20 | 8 | A | A | A | sim | Fácil (comentada) | aprovada |  |
| 21 | 9 | C | C | C | sim | Difícil (comentada) | aprovada |  |
| 22 | 9 | B | B | B | — | Média (comentada) | aprovada |  |
| 23 | 9 | A | A | A | sim | Fácil (comentada) | aprovada |  |
| 24 | 9,10 | D | D | D | — | Difícil (comentada) | aprovada |  |
| 25 | 10 | B | B | B | sim | Média (comentada) | aprovada |  |
| 26 | 10 | C | C | C | — | Média (comentada) | aprovada |  |
| 27 | 10,11 | B | B | B | sim | Difícil (comentada) | aprovada |  |
| 28 | 11 | B | B | B | — | Fácil (comentada) | aprovada |  |
| 29 | 11 | B | B | B | sim | Difícil (comentada) | aprovada |  |
| 30 | 11,12 | C | C | C | sim | Fácil (comentada) | aprovada |  |
| 31 | 12 | C | C | C | sim | Fácil (comentada) | aprovada |  |
| 32 | 12 | A | A | A | sim | Média (comentada) | aprovada |  |
| 33 | 12,13 | C | C | C | sim | Média (comentada) | aprovada |  |
| 34 | 13 | D | D | D | sim | Média (comentada) | aprovada |  |
| 35 | 13 | B | B | B | sim | Média (comentada) | aprovada |  |
| 36 | 13 | C | C | C | — | Média (comentada) | aprovada |  |
| 37 | 14 | C | C | C | — | Difícil (comentada) | aprovada |  |
| 38 | 14 | A | A | A | sim | Média (comentada) | aprovada | Alternativas exclusivamente gráficas: os quatro gráficos de y = p(x), com as letras a–d, estão na imagem. |
| 39 | 14 | C | C | C | — | Difícil (comentada) | aprovada |  |
| 40 | 14 | B | B | B | — | Difícil (comentada) | aprovada | Fração composta escrita em linha (numerador e denominador entre colchetes). |
| 41 | 14 | B | B | B | — | Difícil (comentada) | aprovada |  |
| 42 | 14 | C | C | C | sim | Difícil (comentada) | aprovada |  |
| 43 | 14 | C | C | C | — | Média (comentada) | aprovada |  |
| 44 | 15 | D | D | D | — | Difícil (comentada) | aprovada | Matrizes escritas em linha: [a −1; a−2 a] = 1ª linha (a, −1), 2ª linha (a−2, a); vetores coluna [x; y] e [3; a−4]. |
| 45 | 15 | B | B | B | — | Média (estimativa) | aprovada | Raiz de índice 2021: ²⁰²¹√(10^(3x+5)). / notação ^( ) ou _( ) remanescente |
| 46 | 15 | A | A | A | — | Difícil (comentada) | aprovada |  |
| 47 | 15 | D | D | D | — | Difícil (comentada) | aprovada |  |
| 48 | 15 | Anulado | Anulado | — | — | Média (estimativa) | aprovada |  |
| 49 | 15 | D | D | D | — | Difícil (comentada) | aprovada |  |
| 50 | 15 | A | A | A | — | Média (comentada) | aprovada |  |
| 51 | 15,16 | C | C | C | — | Difícil (comentada) | aprovada |  |
| 52 | 16 | B | B | B | — | Fácil (comentada) | aprovada |  |
| 53 | 16 | B | B | B | — | Média (comentada) | aprovada |  |
| 54 | 16 | C | C | C | — | Fácil (comentada) | aprovada |  |
| 55 | 16 | B | B | B | — | Fácil (comentada) | aprovada |  |
| 56 | 16 | D | D | D | sim | Média (comentada) | aprovada |  |
| 57 | 17 | A | A | A | — | Fácil (estimativa) | aprovada |  |
| 58 | 17 | C | C | C | — | Fácil (estimativa) | aprovada |  |
| 59 | 17 | B | B | B | — | Fácil (comentada) | aprovada |  |
| 60 | 17,18 | D | D | D | — | Fácil (comentada) | aprovada |  |
| 61 | 18 | B | B | B | — | Fácil (comentada) | aprovada | menciona elemento visual mas não tem imagem (conferir se o elemento é textual) |
| 62 | 18 | A | A | A | sim | Fácil (comentada) | aprovada |  |
| 63 | 18 | C | C | C | — | Fácil (comentada) | aprovada |  |
| 64 | 18,19 | B | B | B | — | Fácil (comentada) | aprovada |  |
| 65 | 19 | C | C | C | sim | Difícil (comentada) | aprovada | O mapa e a tabela de resultados (candidatos, partidos, delegados e votos populares) estão na imagem. |
| 66 | 19 | C | C | C | — | Média (comentada) | aprovada |  |
| 67 | 19,20 | C | C | C | — | Fácil (estimativa) | aprovada |  |
| 68 | 20 | B | B | B | sim | Média (comentada) | aprovada |  |
| 69 | 20,21 | D | D | D | sim | Difícil (comentada) | aprovada |  |
| 70 | 21 | C | C | C | — | Difícil (comentada) | aprovada | menciona elemento visual mas não tem imagem (conferir se o elemento é textual) / pendência da explicação: Texto das alternativas veio desordenado na extração; a justificativa foi conferida com a comentada. |
| 71 | 21 | B | B | B | — | Média (comentada) | aprovada |  |
| 72 | 21 | A | A | A | — | Fácil (comentada) | aprovada |  |
