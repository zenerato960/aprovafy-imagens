# Relatório de auditoria — UNICAMP 2024, 1ª fase (Conhecimentos Gerais), Provas Q e Y

Gerado automaticamente por `scripts/unicamp_pipeline/report.mjs` a partir de `manifesto.json` e `validacao.json`.

## Identificação

| Item | Valor |
|---|---|
| Prova | UNICAMP — Vestibular 2024, 1ª fase (Conhecimentos Gerais) (aplicada em outubro de 2023) |
| Versão | Provas Q e Y (mesma sequência de questões e gabarito) |
| PDF oficial | https://www.comvest.unicamp.br/vest2024/F1/f12024Q_Y.pdf |
| Gabarito oficial | https://www.comvest.unicamp.br/wp-content/uploads/2023/10/Q_Y.pdf (PROVAS Q e Y) |
| Conferência adicional | Prova Comentada oficial Comvest: https://www.comvest.unicamp.br/wp-content/uploads/2024/11/F1_2024_Prova-Q_Y-3.pdf |

## Extração

| Métrica | Valor |
|---|---|
| Questões esperadas | 72 |
| Questões extraídas | 72 |
| Aprovadas | 72 |
| Pendentes | 0 |
| Anuladas | 0 |
| Duplicadas internas | 0 |
| Revisadas manualmente (texto e/ou recorte) | 34 |

Status por questão: aprovada: 72

## Imagens

| Métrica | Valor |
|---|---|
| Questões com imagem | 27 |
| Recortes (regiões de página) | 35 |
| Imagens aprovadas visualmente | 27 (folhas de contato + auditoria lado a lado) |
| Imagens publicadas | 27 |
| URLs testadas (HTTP 200, PNG, SHA-256 idêntico ao validado) | 27/27 |
| Diretório no repositório | `imagens/unicamp/2024/qy_auditado/` |
| Padrão de URL | `https://raw.githubusercontent.com/zenerato960/aprovafy-imagens/715e50f8021bb873f72b45732066efcf34718a03/imagens/unicamp/2024/qy_auditado/questao_NNN.png` |

## Classificação

Dificuldade: Fácil 24 · Média 30 · Difícil 18 — fonte: estimativa 23 · comentada 49 ("comentada" = classificação declarada na Prova Comentada oficial; "estimativa" = estimativa pedagógica).

Matérias: Português 5 · Literatura 7 · História 7 · Química 5 · Biologia 9 · Geografia 7 · Física 7 · Sociologia 3 · Filosofia 3 · Matemática 12 · Inglês 7

## GitHub

| Item | Valor |
|---|---|
| Repositório | zenerato960/aprovafy-imagens (público) |
| Branch | `unicamp-2020-2021-auditado` |
| Commit | `715e50f` |
| Status | Branch publicada; `main` não foi alterada |

## Fontes e decisões

- **Prova:** 1ª fase do Vestibular Unicamp 2024 (Conhecimentos Gerais), Provas Q e Y: 72 questões com 4 alternativas. A fonte de verdade é o caderno oficial `f12024Q_Y.pdf`, baixado da Comvest. O arquivo `unicamp2024_1fase_prova_QY.pdf` que estava em Downloads tem conteúdo equivalente, mas hash diferente, e não foi usado.
- **Gabarito:** `Q_Y.pdf` ("PROVAS Q e Y"), publicado pela Comvest em 30/10/2023. Não há questões anuladas.
- **Prova Comentada** (`F1_2024_Prova-Q_Y-3.pdf`): é da mesma versão Q/Y. A "Alternativa Correta" confere com o gabarito em **72/72** questões.
- **Hifenização:** as quebras silábicas foram decididas com base no caderno e na Prova Comentada (265 decisões em `hyphen-log.txt`), com duas correções manuais: "ex-portar" vira "exportar", e "roller-coaster" é mantido com hífen.
- **Textos comuns** (Q1–2, Q20–21, Q34–37, Q39–40) e a nota "Use os valores aproximados: g = 10 m/s² e π = 3" (Q34–Q40) foram replicados nas questões correspondentes. O dado "c = 3,0×10⁸ m/s" vale só para a Q37.
- **Fórmulas e notação** (Q34–Q40, Q62, Q65): transcritas a partir da página. Os glifos "≈" e "−", que vinham com códigos de fonte, foram corrigidos; na Q65 as raízes (√26…√29) tinham sido perdidas na extração.
- **Q19:** as legendas das duas imagens estão impressas em colunas estreitas lado a lado, o que embaralhou a extração. Foram transcritas manualmente.
- **Q69 e Q72:** o texto citado (o e-mail gerado pelo ChatGPT e o trecho de *The Color Purple*) fica numa moldura que o extrator tratava como figura. Ele foi transcrito no enunciado, e não recortado como imagem.
- **Alternativas em imagem:** Q26 (quatro pares de gráficos de sobrevivência, com legenda) e Q67 (quatro adereços de cabeça indígenas).

## Auditorias executadas

1. Revisão visual das 19 páginas com grade de coordenadas.
2. Validação visual dos 27 recortes. Foram corrigidos: Q19 (legenda duplicada), Q20 (eixo cortado), Q21 e Q30 (logomarca do cabeçalho), Q26 (texto do enunciado no recorte) e Q33 (fonte cortada).
3. Comparação palavra a palavra com a Prova Comentada: 57/72 questões com cobertura ≥ 97%. As restantes se explicam por textos comuns e notas que a comentada não repete, e por fórmulas ilegíveis nela.
4. Validador de schema, conteúdo, gabarito e imagens, e teste online das URLs.
5. Comparação com a extração anterior (V11): as mesmas 72 questões e as mesmas letras de resposta. **Este JSON deve substituir os registros UNICAMP 2024 da V11.**

## Limitações

- O código do app Aprovafy não estava disponível. Não foi verificado o importador, o banco de produção nem a interface.

## Controle por questão

| Nº | Págs. | Gabarito oficial | JSON | Comentada | Imagem | Dificuldade (fonte) | Status | Observações |
|---|---|---|---|---|---|---|---|---|
| 1 | 3 | B | B | B | — | Fácil (estimativa) | aprovada | fragmentos curtos no enunciado (conferir): "‘Nevou’ no Rio" |
| 2 | 3 | A | A | A | — | Fácil (estimativa) | aprovada |  |
| 3 | 3 | C | C | C | sim | Fácil (comentada) | aprovada | Texto 2 (quadrinhos de André Dahmer) na imagem. |
| 4 | 3,4 | A | A | A | sim | Média (estimativa) | aprovada | Texto 1 (anúncio da Fliportela) e Texto 2 (águia da Portela) na imagem, nesta ordem. |
| 5 | 4 | D | D | D | — | Difícil (estimativa) | aprovada |  |
| 6 | 4 | D | D | D | — | Média (estimativa) | aprovada |  |
| 7 | 4,5 | C | C | C | — | Média (estimativa) | aprovada |  |
| 8 | 5 | C | C | C | — | Média (estimativa) | aprovada |  |
| 9 | 5 | D | D | D | — | Difícil (estimativa) | aprovada |  |
| 10 | 5 | B | B | B | — | Fácil (estimativa) | aprovada |  |
| 11 | 5,6 | C | C | C | — | Difícil (estimativa) | aprovada | fragmentos curtos no enunciado (conferir): "As estrelas" "Esmaiado: esmaecido, pálido" "Aprisco: curral" / menciona elemento visual mas não tem imagem (conferir se o elemento é textual) |
| 12 | 6 | C | C | C | — | Média (estimativa) | aprovada |  |
| 13 | 6,7 | A | A | A | — | Fácil (estimativa) | aprovada |  |
| 14 | 7 | A | A | A | — | Média (estimativa) | aprovada |  |
| 15 | 7 | B | B | B | — | Fácil (estimativa) | aprovada |  |
| 16 | 7 | C | C | C | — | Fácil (estimativa) | aprovada | menciona elemento visual mas não tem imagem (conferir se o elemento é textual) |
| 17 | 7,8 | C | C | C | sim | Média (estimativa) | aprovada |  |
| 18 | 8 | D | D | D | — | Fácil (estimativa) | aprovada |  |
| 19 | 8 | C | C | C | sim | Média (estimativa) | aprovada | Na imagem, lado a lado: a foto do Papa gerada por IA (esquerda) e o panfleto sobre Maria Antonieta (direita). As legendas, impressas em colunas estreitas, foram transcritas no enunciado. |
| 20 | 9 | C | C | C | sim | Média (comentada) | aprovada |  |
| 21 | 9 | D | D | D | sim | Fácil (comentada) | aprovada | fragmentos curtos no enunciado (conferir): "com base em seu potencial" |
| 22 | 9,10 | A | A | A | — | Difícil (comentada) | aprovada |  |
| 23 | 10 | D | D | D | sim | Difícil (comentada) | aprovada |  |
| 24 | 10 | C | C | C | sim | Difícil (comentada) | aprovada |  |
| 25 | 10,11 | B | B | B | sim | Fácil (comentada) | aprovada |  |
| 26 | 11 | A | A | A | sim | Média (comentada) | aprovada | Alternativas exclusivamente gráficas: cada alternativa é um par de gráficos (i) E. coli e (ii) S. aureus, sobrevivência (%) × tempo (h), para curcumina livre (●) e combinada com octaarginina (○). A legenda e os quatro pares, com as letras a–d, estão na imagem, nesta ordem. |
| 27 | 11 | A | A | A | — | Média (comentada) | aprovada |  |
| 28 | 11 | C | C | C | — | Difícil (comentada) | aprovada |  |
| 29 | 12 | D | D | D | sim | Média (comentada) | aprovada |  |
| 30 | 12 | C | C | C | sim | Fácil (comentada) | aprovada |  |
| 31 | 12,13 | B | B | B | — | Fácil (comentada) | aprovada |  |
| 32 | 13 | A | A | A | sim | Fácil (comentada) | aprovada |  |
| 33 | 13 | C | C | C | sim | Fácil (comentada) | aprovada |  |
| 34 | 14 | A | A | A | — | Média (comentada) | aprovada |  |
| 35 | 14 | B | B | B | — | Difícil (comentada) | aprovada |  |
| 36 | 14 | C | C | C | — | Fácil (comentada) | aprovada |  |
| 37 | 14 | A | A | A | sim | Média (estimativa) | aprovada |  |
| 38 | 14 | B | B | B | — | Média (comentada) | aprovada |  |
| 39 | 14,15 | D | D | D | sim | Média (comentada) | aprovada | alternativas repetidas |
| 40 | 15 | B | B | B | sim | Média (comentada) | aprovada |  |
| 41 | 15 | D | D | D | — | Média (comentada) | aprovada |  |
| 42 | 15 | B | B | B | sim | Difícil (estimativa) | aprovada |  |
| 43 | 15,16 | A | A | A | — | Difícil (comentada) | aprovada |  |
| 44 | 16 | C | C | C | sim | Difícil (comentada) | aprovada |  |
| 45 | 16 | B | B | B | — | Fácil (comentada) | aprovada |  |
| 46 | 16 | B | B | B | sim | Média (comentada) | aprovada |  |
| 47 | 16 | A | A | A | sim | Difícil (comentada) | aprovada | fragmentos curtos no enunciado (conferir): "ledôneas. Nas figuras A" |
| 48 | 17 | D | D | D | — | Fácil (comentada) | aprovada |  |
| 49 | 17 | C | C | C | sim | Média (estimativa) | aprovada | Texto 1 (cartaz da Coalizão Negra por Direitos) na imagem. |
| 50 | 17 | B | B | B | — | Média (estimativa) | aprovada |  |
| 51 | 17,18 | D | D | D | — | Média (comentada) | aprovada |  |
| 52 | 18 | C | C | C | — | Difícil (comentada) | aprovada | fragmentos curtos no enunciado (conferir): "Excerto 1" "Excerto 2" |
| 53 | 18 | C | C | C | — | Fácil (comentada) | aprovada |  |
| 54 | 18 | C | C | C | — | Fácil (comentada) | aprovada |  |
| 55 | 18 | D | D | D | — | Fácil (comentada) | aprovada |  |
| 56 | 18,19 | B | B | B | — | Fácil (comentada) | aprovada |  |
| 57 | 19 | C | C | C | sim | Média (comentada) | aprovada |  |
| 58 | 19 | C | C | C | — | Difícil (comentada) | aprovada |  |
| 59 | 19 | C | C | C | — | Média (comentada) | aprovada |  |
| 60 | 19 | B | B | B | — | Difícil (comentada) | aprovada |  |
| 61 | 19 | B | B | B | — | Média (comentada) | aprovada |  |
| 62 | 19 | B | B | B | — | Média (comentada) | aprovada |  |
| 63 | 19 | D | D | D | sim | Difícil (comentada) | aprovada |  |
| 64 | 19 | C | C | C | — | Média (comentada) | aprovada |  |
| 65 | 20 | C | C | C | sim | Difícil (comentada) | aprovada |  |
| 66 | 20 | C | C | C | sim | Fácil (comentada) | aprovada | Texto 2 (cartaz "Quick, hire one. Anti-Black racism happens here. Let's confront it.") na imagem. |
| 67 | 20 | D | D | D | sim | Média (estimativa) | aprovada | Alternativas exclusivamente visuais (quatro adereços de cabeça indígenas). Na imagem: a e b na coluna da esquerda, c e d na da direita, como no caderno. |
| 68 | 20 | D | D | D | — | Fácil (comentada) | aprovada |  |
| 69 | 21 | C | C | C | — | Média (comentada) | aprovada |  |
| 70 | 21 | B | B | B | — | Difícil (comentada) | aprovada |  |
| 71 | 21 | A | A | A | — | Média (comentada) | aprovada |  |
| 72 | 21 | C | C | C | — | Fácil (comentada) | aprovada |  |
