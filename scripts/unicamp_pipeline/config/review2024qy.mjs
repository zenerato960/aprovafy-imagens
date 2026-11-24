// Revisão manual — UNICAMP 2024, 1ª fase, Provas Q e Y (f12024Q_Y.pdf). Conferido visualmente página a página.
const G = 'Use os valores aproximados: g = 10 m/s² e π = 3.';
const REENTRADA = 'Texto comum às questões 34, 35, 36 e 37.\nUma das etapas mais difíceis de um voo espacial tripulado é a reentrada na atmosfera terrestre. Ao reencontrar as camadas mais altas da atmosfera, a nave sofre forte desaceleração e sua temperatura externa atinge milhares de graus Celsius. Caso a reentrada não ocorra dentro das condições apropriadas, há risco de graves danos à nave, inclusive de explosão, e até mesmo risco de ela ser lançada de volta ao espaço.';
const NEURO = 'Texto comum às questões 39 e 40.\nA neurotransmissão no organismo humano pode ter origem química ou elétrica. O entendimento das sinapses elétricas ocorreu só mais recentemente, graças a estudos avançados das propriedades elétricas dos neurônios. As propriedades mecânicas dos neurônios – como a elasticidade – são, por seu turno, importantes para a compreensão do desenvolvimento deles.';
export default {
  3: { crops: [[3, 307, 63, 566, 149]], obs: 'Texto 2 (quadrinhos de André Dahmer) na imagem.' },
  4: { crops: [[3, 359, 457, 502, 675], [3, 353, 683, 520, 808]], obs: 'Texto 1 (anúncio da Fliportela) e Texto 2 (águia da Portela) na imagem, nesta ordem.' },
  11: { replace: [['Esmaiado: esmaecido, pálido Aprisco: curral Redil: curral para o gado ovino ou caprino; rebanho de ovelhas Tresmalhar: Afastar-se, perder-se do rebanho Flux: fluxo\nAvena: flauta pastoril', 'Esmaiado: esmaecido, pálido\nAprisco: curral\nRedil: curral para o gado ovino ou caprino; rebanho de ovelhas\nTresmalhar: Afastar-se, perder-se do rebanho\nFlux: fluxo\nAvena: flauta pastoril']] },
  17: { crops: [[7, 309, 490, 539, 690]] },
  19: {
    crops: [[8, 307, 70, 434, 240], [8, 452, 70, 566, 229]], cropLayout: 'row',
    enunciado: 'Imagem postada em março de 2023 no Reddit, uma comunidade de fóruns, na página específica do Midjourney. Essa página reúne criações feitas na ferramenta de Inteligência Artificial, ferramenta que permite criar imagens hiper-realistas a partir de uma descrição em texto. A imagem viralizou a partir do Twitter. O Papa nunca usou aquele casaco branco.\n(Disponível em: https://www.uol.com.br/tilt/noticias/redacao/2023/03/26/foto-do-papa-usando-casaco-estiloso-foi-criada-por-inteligencia-artificial.htm?cmpid=copiaecola. Acesso em 04/05/2023.)\nPanfleto anônimo produzido na França pré-revolucionária do final do século XVIII retratando a rainha Maria Antonieta em um romance com a sua amiga, a duquesa Yolande de Polignac. Tradução da legenda: Eu apenas respiro por você. Um beijo, meu belo anjo!\n(Biblioteca Nacional da França, sem data, RES 8-LB39-12153. Disponível em: https://gallica.bnf.fr/ark:/12148/btv1b6942376r.item. Acesso em 04/05/2023.)\nCom propósitos diferentes, ambas as imagens promovem a desinformação. Comparando historicamente os dois exemplos de desinformação, é correto afirmar que',
    obs: 'Na imagem, lado a lado: a foto do Papa gerada por IA (esquerda) e o panfleto sobre Maria Antonieta (direita). As legendas, impressas em colunas estreitas, foram transcritas no enunciado.',
  },
  20: { crops: [[9, 52, 286, 264, 458]] },
  21: { crops: [[9, 434, 49, 566, 440]] },
  23: { crops: [[10, 68, 286, 248, 416]] },
  24: { crops: [[10, 122, 530, 296, 817]] },
  25: { crops: [[10, 338, 420, 535, 732]] },
  26: {
    crops: [[11, 29, 328, 288, 472], [11, 29, 473, 288, 586], [11, 29, 587, 288, 700], [11, 29, 701, 288, 813]],
    alternativas: ['Conjunto de gráficos a.', 'Conjunto de gráficos b.', 'Conjunto de gráficos c.', 'Conjunto de gráficos d.'],
    obs: 'Alternativas exclusivamente gráficas: cada alternativa é um par de gráficos (i) E. coli e (ii) S. aureus, sobrevivência (%) × tempo (h), para curcumina livre (●) e combinada com octaarginina (○). A legenda e os quatro pares, com as letras a–d, estão na imagem, nesta ordem.',
  },
  29: { crops: [[12, 29, 82, 288, 227]] },
  30: { crops: [[12, 307, 58, 566, 355]] },
  32: { crops: [[13, 29, 445, 288, 627]] },
  33: { crops: [[13, 305, 181, 568, 497]] },
  34: { enunciado: G + '\n' + REENTRADA + '\nLogo ao reentrar na atmosfera terrestre, uma cápsula espacial passa a descrever, durante certo tempo, um movimento retilíneo uniformemente variado em que ela é freada com aceleração a = −5,0 m/s². Se no início dessa etapa (t = 0) do movimento a velocidade da cápsula é v₀ = 7000 m/s, qual é a distância percorrida até o tempo t = 200 s?' },
  35: { alternativas: ['−11,1 × 10¹⁰ J.', '−3,60 × 10¹⁰ J.', '−6,00 × 10⁶ J.', '−3,00 × 10⁶ J.'] },
  36: {
    replace: [['R ≈ 8 J/mol.K,\nqual é o volume', 'R ≈ 8 J/mol.K, qual é o volume']],
    alternativas: ['1,38 × 10⁻³ m³.', '9,00 × 10¹ m³.', '7,20 × 10² m³.', '2,88 × 10³ m³.'],
  },
  37: {
    crops: [[14, 339, 66, 534, 257]],
    replace: [['T_(ar), maior é a frequência', 'T_ar, maior é a frequência'], ['T_(ar) = 4800 K, qual é o comprimento de onda correspondente à frequência limite f₀ ?\nλ₀', 'T_ar = 4800 K, qual é o comprimento de onda λ₀ correspondente à frequência limite f₀?']],
  },
  38: {
    enunciado: G + '\nUm corpo em queda nas proximidades da superfície terrestre sofre a ação da força gravitacional e da força de resistência do ar, F⃗_ar; essa última atua em sentido oposto à força gravitacional. Nos primeiros instantes, F⃗_ar = 0⃗ se o corpo parte do repouso. À medida que a velocidade aumenta, F⃗_ar também aumenta. Com isso, a aceleração do corpo diminui gradativamente, tornando-se praticamente nula a partir de certo momento. Desse ponto em diante, o corpo passa a cair com velocidade constante, chamada de velocidade terminal. Um objeto de massa m = 200 g é solto a partir de certa altura e atinge a velocidade terminal após determinado tempo. Qual é o módulo da força de resistência do ar depois que o objeto atinge a velocidade terminal?',
  },
  39: {
    crops: [[15, 60, 49, 258, 198]],
    replace: [['(ddp, da ordem de 10 ^(–3) V)', '(ddp, da ordem de 10⁻³ V)'], ['(da ordem de 10 ^(–12) A)', '(da ordem de 10⁻¹² A)']],
  },
  40: {
    crops: [[15, 62, 398, 256, 501]],
    enunciado: G + '\n' + NEURO + '\nEm um experimento destinado a investigar propriedades elásticas, uma diminuta ponta aplica uma força F⃗ na superfície do neurônio, produzindo uma deformação ∆L de forma análoga a uma mola (ver figura). Foram estudados dois neurônios distintos, designados pelos índices 1 e 2, que foram submetidos à ação de forças idênticas (F⃗₁ = F⃗₂). As deformações observadas foram ∆L₁ = 20 nm e ∆L₂ = 30 nm. Se k₁ = 9,0 × 10⁻⁶ N/m é a constante elástica para o neurônio 1, pode-se deduzir que o valor de k₂ é',
    alternativas: ['4,0 × 10⁻⁶ N/m.', '6,0 × 10⁻⁶ N/m.', '13,5 × 10⁻⁶ N/m.', '20,25 × 10⁻⁶ N/m.'],
  },
  42: { crops: [[15, 307, 163, 566, 323]] },
  44: { crops: [[16, 29, 200, 289, 380]] },
  46: { crops: [[16, 342, 245, 531, 376]] },
  47: { crops: [[16, 414, 604, 562, 698]] },
  49: { crops: [[17, 60, 415, 257, 551]], obs: 'Texto 1 (cartaz da Coalizão Negra por Direitos) na imagem.' },
  57: { crops: [[19, 29, 219, 288, 299]] },
  63: { crops: [[19, 346, 505, 523, 610]] },
  65: { crops: [[20, 111, 85, 264, 174]], alternativas: ['√26.', '√27.', '√28.', '√29.'] },
  66: { crops: [[20, 75, 376, 245, 518]], obs: 'Texto 2 (cartaz "Quick, hire one. Anti-Black racism happens here. Let\'s confront it.") na imagem.' },
  67: {
    crops: [[20, 307, 163, 419, 280], [20, 307, 300, 419, 416], [20, 435, 163, 547, 281], [20, 435, 300, 545, 416]],
    cropLayout: 'grid',
    alternativas: ['Imagem a.', 'Imagem b.', 'Imagem c.', 'Imagem d.'],
    obs: 'Alternativas exclusivamente visuais (quatro adereços de cabeça indígenas). Na imagem: a e b na coluna da esquerda, c e d na da direita, como no caderno.',
  },
  69: { crops: [] },
  72: { crops: [] },
};
