# Relatório de auditoria — UNICAMP 2021, 1ª fase (Conhecimentos Gerais), Provas E e G (dia 1: Ciências Humanas/Artes e Exatas/Tecnológicas)

Gerado automaticamente por `scripts/unicamp_pipeline/report.mjs` a partir de `manifesto.json` e `validacao.json`.

## Identificação

| Item | Valor |
|---|---|
| Prova | UNICAMP — Vestibular 2021, 1ª fase (Conhecimentos Gerais) (aplicada em janeiro de 2021, dia 1) |
| Versão | Provas E e G (dia 1: Ciências Humanas/Artes e Exatas/Tecnológicas) (mesma sequência de questões e gabarito) |
| PDF oficial | https://www.comvest.unicamp.br/vest2021/F1/f12021E_G.pdf |
| Gabarito oficial | https://www.comvest.unicamp.br/wp-content/uploads/2021/01/DIA1_gabarito_2021.pdf (pág. 1, PROVAS E e G) |
| Conferência adicional | Prova Comentada oficial Comvest: https://www.comvest.unicamp.br/wp-content/uploads/2021/09/F1-Comentada-Conhec-Gerais-Exatas-Tecno-Humanas-Artes.pdf |

## Extração

| Métrica | Valor |
|---|---|
| Questões esperadas | 72 |
| Questões extraídas | 72 |
| Aprovadas | 72 |
| Pendentes | 0 |
| Anuladas | 0 |
| Duplicadas internas | 0 |
| Revisadas manualmente (texto e/ou recorte) | 18 |

Status por questão: aprovada: 72

## Imagens

| Métrica | Valor |
|---|---|
| Questões com imagem | 26 |
| Recortes (regiões de página) | 36 |
| Imagens aprovadas visualmente | 26 (folhas de contato + auditoria lado a lado) |
| Imagens publicadas | 26 |
| URLs testadas (HTTP 200, PNG, SHA-256 idêntico ao validado) | 26/26 |
| Diretório no repositório | `imagens/unicamp/2021/dia1_eg/` |
| Padrão de URL | `https://raw.githubusercontent.com/zenerato960/aprovafy-imagens/cfe829e2c9cc6d87a3e4b08785766087704d67a3/imagens/unicamp/2021/dia1_eg/questao_NNN.png` |

## Classificação

Dificuldade: Fácil 23 · Média 23 · Difícil 26 — fonte: comentada 72 ("comentada" = classificação declarada na Prova Comentada oficial; "estimativa" = estimativa pedagógica).

Matérias: Artes 1 · Literatura 6 · Português 4 · Sociologia 2 · Inglês 8 · Matemática 12 · Física 8 · Química 8 · Biologia 8 · História 8 · Geografia 7

## GitHub

| Item | Valor |
|---|---|
| Repositório | zenerato960/aprovafy-imagens (público) |
| Branch | `unicamp-2020-2021-auditado` |
| Commit | `cfe829e` |
| Status | Branch publicada; `main` não foi alterada |

## Fontes e decisões

- **Prova:** a 1ª fase do Vestibular Unicamp 2021 foi aplicada em dois dias, com provas diferentes por área. Este lote é o **dia 1** (Conhecimentos Gerais para Ciências Humanas/Artes e Exatas/Tecnológicas), Provas E e G: 72 questões com 4 alternativas cada. O dia 2 (Provas Q e Z) está em um lote separado, `unicamp_2021_qz`.
- **Fonte de verdade do texto:** caderno oficial `f12021E_G.pdf`. O arquivo `unicamp2021_1fase_1dia.pdf` que estava em Downloads é uma resolução de cursinho e não foi usado.
- **Gabarito:** `DIA1_gabarito_2021.pdf`, página 1 ("PROVAS E e G"), conferido contra a "Alternativa Correta" da Prova Comentada oficial: **0 divergências** em 72 questões. Não houve questões anuladas.
- **Fórmulas** (Q22, Q27, Q29, Q33–Q40): o PDF as codifica como objetos de equação, cuja extração sai fora de ordem. Elas foram transcritas manualmente a partir da visualização ampliada da página. A observação "use π = 3 e g = 10 m/s²" foi replicada nas questões 33–40.
- **Notação em texto puro:** índices com sublinhado (P⃗_B, F⃗_at, μ_c, R_eq, i_B, d_BR), vetores com seta combinante, matriz em linha `[a b; c d]` e frações compostas entre parênteses.
- **Alternativas em imagem:** Q20 (ilustrações), Q23 (gráficos) e Q41 (triângulos do fogo). As figuras de cada alternativa, com as letras a–d originais, ficam na imagem da questão.
- **Q71:** a logomarca do cabeçalho da página fica sobre o canto superior do Mapa 2. Por isso o mapa foi recortado em duas faixas, coladas sem espaço, que excluem a logomarca sem perder conteúdo.

## Auditorias executadas

1. Revisão visual de todas as páginas, com grade de coordenadas, e zoom nas fórmulas.
2. Validação visual dos 26 recortes em folhas de contato. Foram ajustadas as caixas da Q70 (fio separador de colunas) e da Q71 (número da página e logomarca).
3. Comparação palavra a palavra com a Prova Comentada oficial: 64/72 questões com cobertura ≥ 97%. As 8 restantes têm explicação conhecida: a nota de π/g, que a comentada não repete; as alternativas gráficas da Q41; e o texto da comentada ilegível nas fórmulas da Q27.
4. Validador de schema, conteúdo, gabarito e imagens, e teste online das URLs (HTTP 200, PNG, SHA-256).
5. Comparação com a extração anterior (V11): as mesmas 72 questões e as mesmas respostas. **Este JSON deve substituir os registros correspondentes da V11.**

## Limitações

- O código do app Aprovafy não estava disponível. Não foi verificado o importador, o banco de produção nem a interface.

## Controle por questão

| Nº | Págs. | Gabarito oficial | JSON | Comentada | Imagem | Dificuldade (fonte) | Status | Observações |
|---|---|---|---|---|---|---|---|---|
| 1 | 3 | B | B | B | sim | Fácil (comentada) | aprovada |  |
| 2 | 3 | B | B | B | — | Média (comentada) | aprovada | menciona elemento visual mas não tem imagem (conferir se o elemento é textual) |
| 3 | 3 | D | D | D | — | Média (comentada) | aprovada |  |
| 4 | 4 | C | C | C | — | Difícil (comentada) | aprovada |  |
| 5 | 4 | A | A | A | — | Difícil (comentada) | aprovada |  |
| 6 | 4 | A | A | A | — | Difícil (comentada) | aprovada |  |
| 7 | 4 | C | C | C | — | Fácil (comentada) | aprovada |  |
| 8 | 5 | D | D | D | — | Fácil (comentada) | aprovada |  |
| 9 | 5 | C | C | C | sim | Fácil (comentada) | aprovada |  |
| 10 | 5 | A | A | A | — | Difícil (comentada) | aprovada |  |
| 11 | 5 | C | C | C | — | Difícil (comentada) | aprovada |  |
| 12 | 6 | D | D | D | sim | Média (comentada) | aprovada |  |
| 13 | 6 | B | B | B | sim | Fácil (comentada) | aprovada |  |
| 14 | 6 | A | A | A | sim | Fácil (comentada) | aprovada |  |
| 15 | 7 | A | A | A | sim | Difícil (comentada) | aprovada |  |
| 16 | 7 | A | A | A | — | Média (comentada) | aprovada |  |
| 17 | 7 | A | A | A | — | Fácil (comentada) | aprovada |  |
| 18 | 7,8 | B | B | B | — | Fácil (comentada) | aprovada | menciona elemento visual mas não tem imagem (conferir se o elemento é textual) |
| 19 | 8 | D | D | D | — | Fácil (comentada) | aprovada |  |
| 20 | 8 | C | C | C | sim | Fácil (comentada) | aprovada | Alternativas exclusivamente gráficas: as quatro ilustrações, com as letras a–d, estão na imagem. |
| 21 | 9 | C | C | C | — | Média (comentada) | aprovada |  |
| 22 | 9 | D | D | D | — | Média (comentada) | aprovada | Fração composta escrita em linha: numerador (1/2 + 1/3), denominador (x/4 + 1/x). |
| 23 | 9 | A | A | A | sim | Média (comentada) | aprovada | Alternativas exclusivamente gráficas: os quatro gráficos, com as letras a–d, estão na imagem. |
| 24 | 9 | C | C | C | — | Difícil (comentada) | aprovada |  |
| 25 | 9 | D | D | D | — | Difícil (comentada) | aprovada |  |
| 26 | 9 | B | B | B | — | Média (comentada) | aprovada |  |
| 27 | 9 | A | A | A | — | Difícil (comentada) | aprovada |  |
| 28 | 10 | C | C | C | sim | Difícil (comentada) | aprovada |  |
| 29 | 10 | B | B | B | — | Média (comentada) | aprovada | Matriz 2×2 escrita em linha: [a b; c d] = 1ª linha (a, b), 2ª linha (c, d). A alternativa a) não tem ponto final no original. |
| 30 | 10 | B | B | B | — | Difícil (comentada) | aprovada |  |
| 31 | 10 | A | A | A | — | Difícil (comentada) | aprovada |  |
| 32 | 10 | C | C | C | — | Média (comentada) | aprovada |  |
| 33 | 10 | C | C | C | — | Difícil (comentada) | aprovada |  |
| 34 | 10 | B | B | B | sim | Média (comentada) | aprovada |  |
| 35 | 11 | D | D | D | — | Difícil (comentada) | aprovada |  |
| 36 | 11 | C | C | C | — | Fácil (comentada) | aprovada |  |
| 37 | 11 | A | A | A | — | Difícil (comentada) | aprovada |  |
| 38 | 11 | C | C | C | — | Média (comentada) | aprovada |  |
| 39 | 11 | A | A | A | sim | Média (comentada) | aprovada |  |
| 40 | 11 | D | D | D | sim | Difícil (comentada) | aprovada |  |
| 41 | 12 | D | D | D | sim | Média (comentada) | aprovada | Alternativas gráficas: cada alternativa é uma sequência de três triângulos do fogo (ações A, B e C), na imagem com as letras a–d. |
| 42 | 12 | B | B | B | — | Difícil (comentada) | aprovada |  |
| 43 | 12 | D | D | D | sim | Média (comentada) | aprovada |  |
| 44 | 13 | C | C | C | — | Difícil (comentada) | aprovada |  |
| 45 | 13 | A | A | A | sim | Média (comentada) | aprovada |  |
| 46 | 13 | C | C | C | — | Difícil (comentada) | aprovada |  |
| 47 | 13 | A | A | A | — | Difícil (comentada) | aprovada |  |
| 48 | 14 | B | B | B | sim | Difícil (comentada) | aprovada |  |
| 49 | 14 | A | A | A | sim | Média (comentada) | aprovada |  |
| 50 | 14 | A | A | A | — | Difícil (comentada) | aprovada |  |
| 51 | 14,15 | B | B | B | — | Média (comentada) | aprovada |  |
| 52 | 15 | B | B | B | — | Fácil (comentada) | aprovada |  |
| 53 | 15 | D | D | D | sim | Média (comentada) | aprovada |  |
| 54 | 16 | C | C | C | — | Média (comentada) | aprovada |  |
| 55 | 16 | D | D | D | sim | Difícil (comentada) | aprovada |  |
| 56 | 16 | D | D | D | — | Difícil (comentada) | aprovada |  |
| 57 | 17 | C | C | C | — | Fácil (comentada) | aprovada |  |
| 58 | 17 | C | C | C | — | Média (comentada) | aprovada |  |
| 59 | 17 | A | A | A | — | Fácil (comentada) | aprovada |  |
| 60 | 17,18 | C | C | C | — | Média (comentada) | aprovada |  |
| 61 | 18 | D | D | D | sim | Fácil (comentada) | aprovada |  |
| 62 | 18 | A | A | A | — | Fácil (comentada) | aprovada |  |
| 63 | 18 | A | A | A | — | Fácil (comentada) | aprovada |  |
| 64 | 18,19 | B | B | B | sim | Fácil (comentada) | aprovada |  |
| 65 | 19 | C | C | C | sim | Fácil (comentada) | aprovada |  |
| 66 | 19 | D | D | D | sim | Fácil (comentada) | aprovada |  |
| 67 | 19,20 | C | C | C | — | Fácil (comentada) | aprovada |  |
| 68 | 20 | A | A | A | sim | Difícil (comentada) | aprovada |  |
| 69 | 20 | A | A | A | — | Média (comentada) | aprovada | menciona elemento visual mas não tem imagem (conferir se o elemento é textual) |
| 70 | 20,21 | B | B | B | sim | Difícil (comentada) | aprovada |  |
| 71 | 21 | C | C | C | sim | Fácil (comentada) | aprovada | Imagem com o Mapa 1 seguido do Mapa 2. O topo do Mapa 2 foi recortado separadamente para excluir a logomarca do cabeçalho, sem perda de conteúdo. |
| 72 | 21 | D | D | D | — | Fácil (comentada) | aprovada |  |
