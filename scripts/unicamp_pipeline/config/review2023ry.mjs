// Revisão manual — UNICAMP 2023, 1ª fase, Provas R e Y (f12023R_Y.pdf). Conferido visualmente página a página.
const G = 'Use os valores aproximados: g = 10 m/s² e π = 3.';
const MOBIUS = 'Texto comum às questões 31 e 32.\nUma transformação de Möbius é um quociente de polinômios de grau 1. Essas transformações são muito importantes em computação gráfica e também na área da engenharia conhecida como “processamento de sinais”.\nConsidere a função\ny = f(x) = (x + 1)/(x − 1),\ndefinida para x ∈ ℝ, x ≠ 1, que é uma versão simplificada de uma transformação de Möbius.';
const g = ['Gráfico a.', 'Gráfico b.', 'Gráfico c.', 'Gráfico d.'];
export default {
  3: {
    crops: [[3, 307, 49, 563, 253]],
    obs: 'Questão ANULADA pela Comvest (gabarito definitivo V2 e nota oficial sobre a questão 23 da prova Q, que é esta mesma questão): pela ambiguidade do enunciado — a subsidência em Maceió é irreversível, enquanto a alternativa b, apontada inicialmente pela banca, descreve a subsidência reversível de solos argilosos.',
  },
  4: { crops: [[3, 308, 659, 566, 769]] },
  6: {
    crops: [[4, 27, 704, 290, 807], [4, 307, 52, 566, 160]], cropGap: 0, cropAlign: 'left',
    enunciado: 'A tabela a seguir destaca, para o ano de 2019, os 11 municípios brasileiros que mais emitiram gases do efeito estufa causadores do aquecimento global, conforme o total emitido de CO₂ em toneladas.\n(Fonte: www.seeg.eco.br; IBGE Cidades – Acessado em: 24/06/2022.)\nA partir da análise dos dados anteriores e de seu conhecimento, é correto afirmar que os municípios com',
    obs: 'A tabela (11 municípios; emissão de CO₂, área territorial e densidade demográfica) está na imagem, unindo as duas partes impressas em colunas diferentes.',
  },
  9: { crops: [[5, 68, 672, 250, 800]] },
  13: {
    crops: [[6, 70, 153, 240, 257]],
    replace: [['Na referida figura, estão representados o peso ρ\nρ ρ\nP do bloco, a força normal N, a força de atrito f_(at) aplicada pela superfície da pele no bloco de massa m e uma força exter- ρ\nna F aplicada na mola.', 'Na referida figura, estão representados o peso P⃗ do bloco, a força normal N⃗, a força de atrito f⃗_at aplicada pela superfície da pele no bloco de massa m e uma força externa F⃗ aplicada na mola.']],
  },
  14: { crops: [[6, 33, 528, 288, 661]], replace: [['T_(Ceres)', 'T_Ceres']] },
  15: { crops: [[6, 452, 111, 549, 226]] },
  16: {
    crops: [[6, 320, 376, 553, 505]],
    replace: [
      ['um vidro de índice de refração = 1,8. Quando θ₁ = 90 ,^o temos o máximo valor conhecido n₂\npara o ângulo de refração θ₂,', 'um vidro de índice de refração conhecido n₂ = 1,8. Quando θ₁ = 90°, temos o máximo valor para o ângulo de refração θ₂,'],
      ['sen56^o = 0,8; cos56^o = 0,6; tg56^o = 1,3', 'sen 56° = 0,8; cos 56° = 0,6; tg 56° = 1,3'],
      ['θ_C = 56^o', 'θ_C = 56°'],
    ],
    alternativas: [
      'n₁ = 1,44, e se trocarmos esse líquido por um de índice de refração maior, o ângulo crítico será maior que 56°.',
      'n₁ = 1,44, e se trocarmos esse líquido por um de índice de refração maior, o ângulo crítico será menor que 56°.',
      'n₁ = 2,25, e se trocarmos esse líquido por um de índice de refração maior, o ângulo crítico será maior que 56°.',
      'n₁ = 2,25, e se trocarmos esse líquido por um de índice de refração maior, o ângulo crítico será menor que 56°.',
    ],
  },
  20: { crops: [[7, 326, 414, 555, 579]] },
  22: { crops: [[8, 33, 680, 285, 808]] },
  24: { crops: [[9, 30, 49, 288, 327]] },
  26: {
    crops: [[9, 350, 262, 523, 351], [9, 350, 369, 523, 461], [9, 350, 478, 523, 573], [9, 350, 589, 523, 684]],
    cropLayout: 'grid',
    enunciado: 'A seguir, são apresentadas quatro funções, definidas para x ∈ ℝ; são também apresentados quatro esboços de gráficos.\nFunções:\nf(x) = sen(x) + π/4\ng(x) = cos(x + π/4) − sen(x + π/4)\nh(x) = sen(x − π/4)\np(x) = cos(x) + sen(x)\nGráficos: (i), (ii), (iii) e (iv), na imagem.\nA opção que descreve corretamente a correspondência entre as funções e seus gráficos é:',
    obs: 'Os quatro gráficos estão na imagem em grade: (i) e (ii) na linha de cima, (iii) e (iv) na de baixo.',
  },
  27: { crops: [[10, 32, 264, 286, 505]] },
  30: { crops: [[10, 337, 355, 536, 465]] },
  31: {
    enunciado: MOBIUS + '\nSobre a função inversa de f(x), é correto afirmar que',
    alternativas: ['f⁻¹(x) = f(x), para x ≠ 1.', 'f⁻¹(x) = 1/f(x), para x ≠ ±1.', 'f⁻¹(x) = −f(x), para x ≠ 1.', 'f⁻¹(x) = f(−x), para x ≠ 1.'],
  },
  32: {
    enunciado: MOBIUS + '\nConsidere a sequência x₁, x₂, ..., definida por x₁ = 6, e para cada n ≥ 1, temos xₙ₊₁ = f(xₙ), ou seja,\n• x₁ = 6,\n• x₂ = f(x₁) = 7/5,\n• x₃ = f(x₂),\ne assim sucessivamente. Então, a soma dos 100 primeiros termos desta sequência vale',
  },
  33: { enunciado: 'Para qual valor de a o sistema de equações lineares\n{ ax − y = |a|\n{ (4 − 5a²)x + ay = 1\nadmite infinitas soluções?' },
  34: { crops: [[11, 76, 698, 256, 808]], alternativas: ['24/25.', '5/6.', '1/2.', '√3/2.'] },
  36: { crops: [[11, 373, 539, 500, 680]] },
  37: { crops: [[12, 29, 69, 288, 247]] },
  40: { crops: [[13, 29, 285, 288, 484], [13, 29, 501, 288, 641]] },
  45: { crops: [[15, 65, 123, 241, 331], [15, 65, 360, 241, 630]], obs: 'Texto A e Texto B (postagens) na imagem, nesta ordem.' },
  49: { crops: [[16, 29, 445, 288, 637]], obs: 'Texto 2 (fotografia) na imagem.' },
  48: { crops: [[16, 29, 445, 288, 637]], obs: 'Texto 2 (fotografia) na imagem.' },
  52: {
    crops: [[17, 305, 290, 566, 388], [17, 305, 411, 566, 501], [17, 305, 521, 566, 611], [17, 305, 629, 566, 722]],
    cropLayout: 'grid', alternativas: g,
    obs: 'Alternativas exclusivamente gráficas: os quatro gráficos (mortes diárias × tempo), cada um com sua letra a)–d), a e b em cima, c e d embaixo.',
  },
  53: { crops: [[18, 29, 98, 288, 227]] },
  57: { crops: [[19, 29, 554, 288, 785]] },
  64: { obs: 'A Prova Comentada indica "d" para esta questão, mas o gabarito oficial definitivo indica "c" (e também "c" para a mesma questão na versão Q, nº 12). Prevalece o gabarito oficial.' },
  66: {
    crops: [[22, 29, 553, 290, 728]],
    replace: [
      ['onde a terra, a água e o ar estão em vulnerabilidade. Façamos da Química o caminho para a sustentabilidade” (MOTA,', 'onde a terra, a água e o ar estão em vulnerabilidade.\nFaçamos da Química o caminho para a sustentabilidade”\n(MOTA,'],
      ['Síntese do biodiesel:\nC H O + 3 C H OH → 3 C H O + C H O\n57 104 6 2 5 20 38 2 3 8 3\nSíntese do etanol:\nC H O + H O → 4 C H OH + 4 CO\n12 22 11 2 2 5 2\n', 'Síntese do biodiesel:\nC₅₇H₁₀₄O₆ + 3 C₂H₅OH → 3 C₂₀H₃₈O₂ + C₃H₈O₃\nSíntese do etanol:\nC₁₂H₂₂O₁₁ + H₂O → 4 C₂H₅OH + 4 CO₂\n'],
      ['C₅₇H₁₀₄O₆ = 884; C₂H₅OH = 46; C H O = 310; C H O = 92; C H O = 342; H O = 18; CO\n20 38 2 3 8 3 12 22 11 2 2\n= 44.', 'C₅₇H₁₀₄O₆ = 884; C₂H₅OH = 46; C₂₀H₃₈O₂ = 310; C₃H₈O₃ = 92; C₁₂H₂₂O₁₁ = 342; H₂O = 18; CO₂ = 44.'],
    ],
    obs: 'A TPQVS (Texto 1) está na imagem.',
  },
  67: {
    crops: [[22, 29, 553, 290, 728]],
    replace: [['onde a terra, a água e o ar estão em vulnerabilidade. Façamos da Química o caminho para a sustentabilidade” (MOTA,', 'onde a terra, a água e o ar estão em vulnerabilidade.\nFaçamos da Química o caminho para a sustentabilidade”\n(MOTA,'],
      ['Considerando a proposta da Química Verde, as frases em negrito', 'Frases em negrito no poema original: “para transformar o mundo com delicadeza.”; “desenvolvendo processos de alta eficiência.”; “para o fóssil ela tem a substituição;”; “onde a terra, a água e o ar estão em vulnerabilidade.”\nConsiderando a proposta da Química Verde, as frases em negrito']],
    obs: 'O negrito do original não existe em texto puro; os quatro versos em negrito são listados explicitamente antes do comando. A TPQVS (Texto 1) está na imagem.',
  },
  68: {
    crops: [[23, 73, 126, 216, 146], [23, 46, 152, 243, 283], [23, 46, 290, 264, 383], [23, 46, 393, 257, 513], [23, 46, 525, 256, 672]],
    cropAlign: 'left',
    replace: [['Legenda:\nA\nB\nC\nD\n', '']],
    obs: 'Na imagem: legenda (H, C, O) e os esquemas A, B, C e D, nesta ordem.',
  },
  69: { crops: [[23, 325, 359, 535, 532]] },
  71: { crops: [[24, 45, 600, 250, 775]] },
  72: { crops: [[24, 307, 286, 384, 331], [24, 319, 419, 554, 614]], obs: 'Na imagem: os símbolos do carbono e do nitrogênio e o gráfico com as faixas A, B e C.' },
};
