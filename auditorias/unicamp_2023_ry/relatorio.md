# Relatório de auditoria — UNICAMP 2023, 1ª fase (Conhecimentos Gerais), Provas R e Y

Gerado automaticamente por `scripts/unicamp_pipeline/report.mjs` a partir de `manifesto.json` e `validacao.json`.

## Identificação

| Item | Valor |
|---|---|
| Prova | UNICAMP — Vestibular 2023, 1ª fase (Conhecimentos Gerais) (aplicada em novembro de 2022) |
| Versão | Provas R e Y (mesma sequência de questões e gabarito) |
| PDF oficial | https://www.comvest.unicamp.br/vest2023/F1/f12023R_Y.pdf |
| Gabarito oficial | https://www.comvest.unicamp.br/wp-content/uploads/2022/11/Gabarito_F1_VEST2023_V2.pdf (pág. 2, PROVAS R e Y) |
| Conferência adicional | Prova Comentada oficial Comvest: https://www.comvest.unicamp.br/wp-content/uploads/2023/06/F1.pdf |

## Extração

| Métrica | Valor |
|---|---|
| Questões esperadas | 72 |
| Questões extraídas | 72 |
| Aprovadas | 72 |
| Pendentes | 0 |
| Anuladas | 1 |
| Duplicadas internas | 0 |
| Revisadas manualmente (texto e/ou recorte) | 34 |

Status por questão: aprovada: 72

## Imagens

| Métrica | Valor |
|---|---|
| Questões com imagem | 30 |
| Recortes (regiões de página) | 44 |
| Imagens aprovadas visualmente | 30 (folhas de contato + auditoria lado a lado) |
| Imagens publicadas | 30 |
| URLs testadas (HTTP 200, PNG, SHA-256 idêntico ao validado) | 30/30 |
| Diretório no repositório | `imagens/unicamp/2023/ry_auditado/` |
| Padrão de URL | `https://raw.githubusercontent.com/zenerato960/aprovafy-imagens/48b0a447047bbd5d3f69fb1ef795ec2c1c915cfe/imagens/unicamp/2023/ry_auditado/questao_NNN.png` |

## Classificação

Dificuldade: Difícil 19 · Fácil 34 · Média 19 — fonte: comentada 59 · estimativa 13 ("comentada" = classificação declarada na Prova Comentada oficial; "estimativa" = estimativa pedagógica).

Matérias: Geografia 8 · Sociologia 1 · Física 8 · Biologia 7 · Matemática 12 · História 8 · Inglês 8 · Português 6 · Literatura 6 · Química 8

## GitHub

| Item | Valor |
|---|---|
| Repositório | zenerato960/aprovafy-imagens (público) |
| Branch | `unicamp-2020-2021-auditado` |
| Commit | `48b0a44` |
| Status | Branch publicada; `main` não foi alterada |

## Fontes e decisões

- **Prova:** 1ª fase do Vestibular Unicamp 2023 (Conhecimentos Gerais), Provas R e Y: 72 questões com 4 alternativas. A fonte de verdade é o caderno oficial `f12023R_Y.pdf`, baixado da Comvest. O arquivo `unicamp2023_1fase_prova_RY.pdf` que estava em Downloads é outro arquivo (hash diferente) e não foi usado.
- **Gabarito:** `Gabarito_F1_VEST2023_V2.pdf` (versão 2, definitiva), página 2 ("PROVAS R e Y").
- **Questão anulada: Q3.** O gabarito definitivo marca "*" com a nota "Questão anulada pela Comvest. Todos os candidatos presentes na prova receberão 1 ponto pela questão". A nota oficial `Q23-prova-Q-geografia-Subsidencia-vers2.pdf` (é a mesma questão na versão Q) traz a justificativa: há ambiguidade no enunciado, porque a subsidência em Maceió é irreversível, enquanto a alternativa b, apontada inicialmente pela banca, descreve a subsidência reversível de solos argilosos. O JSON usa `"Anulado"`, e a explicação reproduz essa justificativa.
- **Prova Comentada** (`F1.pdf`): foi escrita para a **versão Q**, que tem outra numeração e, às vezes, outra ordem de alternativas. A "Alternativa Correta" da comentada foi traduzida para este caderno comparando o **texto** das alternativas, e não a letra. Foram localizadas 71/72 questões. Nas questões em que a tradução foi possível, todas conferem com o gabarito R/Y, com duas exceções:
  - **Q3:** anulada (a comentada mantém a letra original).
  - **Q64 (Racionais MC's, "Gênesis"):** a comentada indica a alternativa "à origem religiosa dos conflitos armados…" (d), mas o gabarito oficial definitivo indica **c** ("à origem divina do mundo contraposta aos problemas criados pelo homem"). Para a mesma questão na versão Q (nº 12), o gabarito oficial também indica C. **Prevalece o gabarito oficial definitivo.** O próprio comentário da banca descreve o sentido da alternativa c ("contrapõe o mundo supostamente criado por Deus … com o mundo vivido pelo Eu-lírico"), o que sugere erro na letra impressa na comentada.
- **Hifenização:** este caderno quebra palavras no fim da linha. A decisão entre juntar a palavra e manter o hífen foi automática e baseada em evidência: a forma inteira ou hifenizada encontrada no próprio caderno ou na Prova Comentada, pronomes enclíticos e prefixos. As 258 decisões estão registradas em `hyphen-log.txt`.
- **Textos comuns** ("Leia o texto a seguir para responder às questões…", 6 blocos) e a nota "Use os valores aproximados: g = 10 m/s² e π = 3" (Q9–Q16) foram replicados nas questões correspondentes.
- **Fórmulas** (Q13, Q16, Q26, Q31–Q34, Q66): transcritas manualmente a partir da página.
- **Q6:** a tabela dos 11 municípios está impressa em duas colunas. Ela foi recomposta numa única imagem, na ordem original.
- **Q67:** o comando se refere a "frases em negrito do poema". Como texto puro não tem negrito, os quatro versos em negrito estão listados explicitamente no enunciado.
- **Alternativas em imagem:** Q52 (quatro gráficos com as letras a–d, em grade). Na Q26, os gráficos (i)–(iv) também estão em grade.

## Auditorias executadas

1. Revisão visual das 22 páginas e zoom nas fórmulas.
2. Validação visual dos 30 recortes. Foram corrigidos: Q6 (texto abaixo da tabela), Q52 (letras das alternativas fora do recorte), Q66 e Q67 (página errada), Q69 e Q71 (rótulos dos eixos cortados).
3. Comparação palavra a palavra com a Prova Comentada: 64/72 questões com cobertura ≥ 97%. As restantes se explicam por textos comuns que a comentada não repete.
4. Auditoria da ordem das alternativas contra a comentada: nenhuma divergência.
5. Validador de schema, conteúdo, gabarito e imagens, e teste online das URLs.
6. Comparação com a extração anterior (V11): as mesmas 72 questões e as mesmas letras de resposta (incluindo a Q3 anulada e a Q64 = C). **Este JSON deve substituir os registros UNICAMP 2023 da V11.**

## Limitações

- O código do app Aprovafy não estava disponível. Não foi verificado o importador, o banco de produção nem a interface.

## Controle por questão

| Nº | Págs. | Gabarito oficial | JSON | Comentada | Imagem | Dificuldade (fonte) | Status | Observações |
|---|---|---|---|---|---|---|---|---|
| 1 | 3 | C | C | C | — | Difícil (comentada) | aprovada |  |
| 2 | 3 | C | C | C | — | Fácil (comentada) | aprovada |  |
| 3 | 3 | Anulado | Anulado | B | sim | Difícil (estimativa) | aprovada | Questão ANULADA pela Comvest (gabarito definitivo V2 e nota oficial sobre a questão 23 da prova Q, que é esta mesma questão): pela ambiguidade do enunciado — a subsidência em Maceió é irreversível, enquanto a alternativa b, apontada inicialmente pela banca, descreve a subsidência reversível de solos argilosos. / comentada B ≠ gabarito Anulado |
| 4 | 3,4 | A | A | — | sim | Média (comentada) | aprovada |  |
| 5 | 4 | A | A | A | — | Difícil (estimativa) | aprovada |  |
| 6 | 4 | D | D | D | sim | Fácil (comentada) | aprovada | A tabela (11 municípios; emissão de CO₂, área territorial e densidade demográfica) está na imagem, unindo as duas partes impressas em colunas diferentes. |
| 7 | 4,5 | B | B | — | — | Fácil (comentada) | aprovada |  |
| 8 | 5 | D | D | D | — | Fácil (comentada) | aprovada |  |
| 9 | 5 | C | C | C | sim | Fácil (comentada) | aprovada |  |
| 10 | 5 | D | D | — | — | Difícil (comentada) | aprovada |  |
| 11 | 5 | D | D | — | — | Média (comentada) | aprovada |  |
| 12 | 5 | C | C | C | — | Fácil (comentada) | aprovada |  |
| 13 | 5,6 | C | C | C | sim | Difícil (comentada) | aprovada |  |
| 14 | 6 | C | C | C | sim | Fácil (comentada) | aprovada |  |
| 15 | 6 | B | B | B | sim | Fácil (comentada) | aprovada |  |
| 16 | 6 | A | A | A | sim | Difícil (comentada) | aprovada |  |
| 17 | 7 | C | C | C | — | Fácil (comentada) | aprovada |  |
| 18 | 7 | C | C | C | — | Difícil (comentada) | aprovada |  |
| 19 | 7 | A | A | A | — | Média (comentada) | aprovada |  |
| 20 | 7,8 | D | D | D | sim | Difícil (comentada) | aprovada |  |
| 21 | 8 | A | A | A | — | Média (comentada) | aprovada |  |
| 22 | 8 | B | B | B | sim | Difícil (comentada) | aprovada |  |
| 23 | 8 | A | A | A | — | Fácil (comentada) | aprovada |  |
| 24 | 8,9 | B | B | B | sim | Fácil (comentada) | aprovada |  |
| 25 | 9 | B | B | B | — | Média (comentada) | aprovada |  |
| 26 | 9 | B | B | B | sim | Difícil (comentada) | aprovada | Os quatro gráficos estão na imagem em grade: (i) e (ii) na linha de cima, (iii) e (iv) na de baixo. |
| 27 | 10 | D | D | D | sim | Fácil (comentada) | aprovada |  |
| 28 | 10 | C | C | — | — | Difícil (comentada) | aprovada |  |
| 29 | 10 | B | B | B | — | Difícil (comentada) | aprovada |  |
| 30 | 10 | C | C | — | sim | Difícil (comentada) | aprovada |  |
| 31 | 11 | A | A | A | — | Difícil (comentada) | aprovada | fragmentos curtos no enunciado (conferir): "Considere a função" |
| 32 | 11 | B | B | — | — | Média (comentada) | aprovada | fragmentos curtos no enunciado (conferir): "Considere a função" |
| 33 | 11 | C | C | — | — | Média (comentada) | aprovada |  |
| 34 | 11 | A | A | A | sim | Média (comentada) | aprovada | fragmentos curtos no enunciado (conferir): "O valor de sen α é" |
| 35 | 11 | B | B | B | — | Difícil (comentada) | aprovada |  |
| 36 | 11 | B | B | B | sim | Média (comentada) | aprovada | fragmentos curtos no enunciado (conferir): "O valor de a + b é" |
| 37 | 12 | C | C | — | sim | Fácil (estimativa) | aprovada |  |
| 38 | 12 | B | B | B | — | Fácil (comentada) | aprovada |  |
| 39 | 12,13 | A | A | — | — | Média (comentada) | aprovada |  |
| 40 | 13 | D | D | — | sim | Fácil (comentada) | aprovada |  |
| 41 | 13 | C | C | — | — | Fácil (comentada) | aprovada |  |
| 42 | 14 | A | A | A | — | Fácil (comentada) | aprovada |  |
| 43 | 14 | A | A | A | — | Média (comentada) | aprovada |  |
| 44 | 14 | D | D | D | — | Média (estimativa) | aprovada |  |
| 45 | 15 | A | A | A | sim | Fácil (comentada) | aprovada | Texto A e Texto B (postagens) na imagem, nesta ordem. / fragmentos curtos no enunciado (conferir): "Texto A" |
| 46 | 15 | C | C | C | — | Fácil (comentada) | aprovada |  |
| 47 | 15,16 | B | B | B | — | Fácil (comentada) | aprovada |  |
| 48 | 16 | D | D | D | sim | Fácil (comentada) | aprovada | Texto 2 (fotografia) na imagem. |
| 49 | 16 | B | B | B | sim | Média (comentada) | aprovada | Texto 2 (fotografia) na imagem. |
| 50 | 16,17 | C | C | C | — | Fácil (comentada) | aprovada |  |
| 51 | 17 | B | B | B | — | Média (estimativa) | aprovada |  |
| 52 | 17 | A | A | — | sim | Média (comentada) | aprovada | Alternativas exclusivamente gráficas: os quatro gráficos (mortes diárias × tempo), cada um com sua letra a)–d), a e b em cima, c e d embaixo. |
| 53 | 18 | B | B | B | sim | Fácil (comentada) | aprovada |  |
| 54 | 18 | D | D | D | — | Fácil (comentada) | aprovada |  |
| 55 | 19 | D | D | D | — | Média (comentada) | aprovada |  |
| 56 | 19 | B | B | B | — | Fácil (comentada) | aprovada |  |
| 57 | 19 | A | A | A | sim | Fácil (comentada) | aprovada |  |
| 58 | 19 | B | B | B | — | Fácil (estimativa) | aprovada | menciona elemento visual mas não tem imagem (conferir se o elemento é textual) |
| 59 | 20 | B | B | B | — | Difícil (estimativa) | aprovada | menciona elemento visual mas não tem imagem (conferir se o elemento é textual) |
| 60 | 20 | B | B | B | — | Média (estimativa) | aprovada |  |
| 61 | 20 | B | B | B | — | Média (estimativa) | aprovada |  |
| 62 | 21 | A | A | A | — | Média (estimativa) | aprovada | menciona elemento visual mas não tem imagem (conferir se o elemento é textual) |
| 63 | 21 | A | A | A | — | Fácil (estimativa) | aprovada |  |
| 64 | 21 | C | C | D | — | Fácil (estimativa) | aprovada | A Prova Comentada indica "d" para esta questão, mas o gabarito oficial definitivo indica "c" (e também "c" para a mesma questão na versão Q, nº 12). Prevalece o gabarito oficial. / comentada D ≠ gabarito C |
| 65 | 22 | A | A | A | — | Fácil (comentada) | aprovada |  |
| 66 | 22 | D | D | — | sim | Difícil (comentada) | aprovada | A TPQVS (Texto 1) está na imagem. |
| 67 | 22 | A | A | A | sim | Fácil (comentada) | aprovada | O negrito do original não existe em texto puro; os quatro versos em negrito são listados explicitamente antes do comando. A TPQVS (Texto 1) está na imagem. |
| 68 | 23 | C | C | C | sim | Fácil (comentada) | aprovada | Na imagem: legenda (H, C, O) e os esquemas A, B, C e D, nesta ordem. |
| 69 | 23 | B | B | B | sim | Fácil (estimativa) | aprovada |  |
| 70 | 23,24 | A | A | A | — | Difícil (comentada) | aprovada |  |
| 71 | 24 | B | B | B | sim | Fácil (comentada) | aprovada |  |
| 72 | 24 | D | D | D | sim | Difícil (comentada) | aprovada | Na imagem: os símbolos do carbono e do nitrogênio e o gráfico com as faixas A, B e C. |
