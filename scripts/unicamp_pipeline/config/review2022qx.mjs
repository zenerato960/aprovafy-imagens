// Revisão manual — UNICAMP 2022, 1ª fase, Provas Q e X (f12022Q_X.pdf). Conferido visualmente página a página.
const PI = 'Sempre que necessário aproxime π = 3.';
const SOLAR = 'Texto comum às questões 57 e 58.\nEm 2018, a NASA lançou a sonda Solar Parker com o objetivo de estudar o Sol. Para isso, ao longo de suas órbitas, a sonda se aproximará gradativamente da estrela, coletando dados a cada passagem. Em abril de 2021, a Solar Parker fez sua oitava aproximação, atingindo dois novos recordes de artefatos realizados pelo homem: maior velocidade e máxima aproximação do Sol.';
const APOLO = 'Texto comum às questões 59 e 60.\nEm abril de 2021 faleceu o astronauta norte-americano Michael Collins, integrante da missão Apolo 11, que levou o primeiro homem à Lua. Enquanto os dois outros astronautas da missão, Neil Armstrong e Buzz Aldrin, desceram até a superfície lunar, Collins permaneceu em órbita lunar pilotando o Módulo de Comando Columbia.';
export default {
  6: { crops: [] },
  43: { crops: [] },
  10: { crops: [[5, 363, 251, 520, 374], [5, 357, 412, 524, 551]], obs: 'Texto I (André Vallias) e Texto II (Hélio Oiticica) na imagem, nesta ordem; as fontes estão no enunciado.' },
  12: { crops: [[6, 26, 551, 278, 776]] },
  14: { crops: [[6, 308, 523, 575, 593]] },
  15: {
    crops: [[7, 79, 130, 229, 236], [7, 81, 255, 228, 361]],
    enunciado: 'As figuras abaixo ilustram, respectivamente, os gráficos das funções y = f(x) e y = g(x).\nEntão f(g(−1)) − g(f(1)) vale:',
  },
  16: {
    enunciado: 'Dados os números reais positivos a₁, a₂, …, aₙ, a média geométrica M destes termos é calculada por:\nM = ⁿ√(a₁ … aₙ).\nA média geométrica de 1, 10, 100, …, 10²² é:',
    obs: 'Raiz de índice n escrita como ⁿ√( ).',
  },
  19: {
    enunciado: 'Um círculo está inscrito em um quadrilátero ABCD. Seja T o ponto de tangência do lado DA com o círculo. Sabe-se que as medidas dos lados AB, BC e CD formam, nesta ordem, uma progressão aritmética crescente de números inteiros e que a medida do lado DA é 3. Considerando que a medida do segmento TA é um número inteiro, as medidas dos lados AB, BC e CD são, respectivamente:',
  },
  17: {
    alternativas: [
      'a porcentagem mínima da população que deve ser vacinada para controlar a epidemia é sempre maior que 50%.',
      'para uma vacina, quanto maior R₀, menor a porcentagem mínima da população que deve ser vacinada para controlar a epidemia.',
      'para uma vacina, quanto maior R₀, maior a porcentagem mínima da população que deve ser vacinada para controlar a epidemia.',
      'para um dado R₀, quanto maior a efetividade da vacina, maior a porcentagem mínima da população que deve ser vacinada para controlar a epidemia.',
    ],
    obs: 'Alternativas transcritas a partir da página (a extração automática embaralhou as linhas por causa dos subscritos de R₀).',
  },
  20: {
    enunciado: 'Considere a matriz\nA = [1 k; 3 k²]\ne seja B = A + Aᵀ, onde Aᵀ é a transposta da matriz A.\nSobre o sistema\nB·[x; y] = [2021; 2022]\né correto afirmar que:',
    obs: 'Matriz escrita em linha: [1 k; 3 k²] = 1ª linha (1, k), 2ª linha (3, k²); vetores coluna [x; y] e [2021; 2022].',
  },
  21: { crops: [[8, 78, 270, 230, 338]], replace: [['Pedra: Papel: Tesoura:\n👊 ✋ ✌\n', '']], obs: 'Os emojis de pedra, papel e tesoura estão na imagem.' },
  22: { enunciado: 'A parábola y = −x² + bx + c intercepta o eixo x nos pontos (p, 0) e (q, 0). Sabe-se que ela intercepta uma única vez cada uma das retas dadas pelas equações y = 2x + 1 e y = 1 − x/2. O valor de p + q é:' },
  23: { enunciado: 'O polinômio p(x) = 2x³ + ax² + bx + c é divisível por 2x² − x + 4. O valor de c + 2b − a é:' },
  24: {
    crops: [[8, 330, 184, 551, 548]],
    alternativas: ['400√(2 − √2) − 60√(2 + √2) ≈ 195,3', '200√(2 − √2) − 15√(2 + √2) ≈ 125,4', '200√(2 − √2) + 15√(2 + √2) ≈ 180,8', '200√(3 − √3) − 15√(3 + √3) ≈ 192,6'],
  },
  26: { crops: [[9, 43, 665, 265, 772], [9, 340, 38, 526, 264]], obs: 'Imagem com o infográfico da pesquisa e, abaixo, o post de Rishi Budhrani (texto em inglês do post incluído na imagem).' },
  27: { crops: [[9, 309, 569, 401, 672]] },
  28: { crops: [[10, 15, 262, 157, 358]] },
  30: {
    crops: [[11, 59, 107, 245, 213], [11, 59, 228, 245, 330], [11, 57, 347, 244, 458], [11, 57, 477, 244, 582]],
    cropLayout: 'grid', alternativas: ['Imagem a.', 'Imagem b.', 'Imagem c.', 'Imagem d.'],
    replace: [['https://www.ted.com/talks/iseult_gillespie_why_should_you_ read_sylvia _plath', 'https://www.ted.com/talks/iseult_gillespie_why_should_you_read_sylvia_plath']],
    obs: 'Alternativas exclusivamente visuais: as quatro ilustrações, na ordem a, b (linha de cima) e c, d (linha de baixo), estão na imagem.',
    cropLabels: ['a)', 'b)', 'c)', 'd)'],
  },
  31: { crops: [[11, 24, 624, 157, 700]] },
  33: { crops: [[12, 26, 358, 290, 527]] },
  34: { crops: [[12, 323, 124, 560, 308]] },
  35: { crops: [[12, 298, 658, 576, 813]] },
  36: { crops: [[13, 33, 535, 264, 640]] },
  38: { crops: [[13, 308, 622, 575, 701]] },
  39: { crops: [[14, 16, 333, 283, 499]] },
  40: { crops: [[14, 313, 228, 569, 596]] },
  41: { crops: [[15, 26, 184, 282, 417]] },
  42: {
    crops: [[15, 313, 38, 571, 325]],
    obs: 'Questão ANULADA pela Comvest: erro de plotagem no mapa do Bioma 3 (a área indicada é semidesértica, e não desértica, como consta da alternativa c).',
  },
  44: { crops: [[16, 31, 352, 278, 535]] },
  45: { crops: [[16, 313, 140, 576, 532]] },
  47: { crops: [[17, 300, 40, 572, 205]] },
  49: { crops: [[18, 26, 244, 286, 466]] },
  57: {
    enunciado: PI + '\n' + SOLAR + '\nUma sonda viaja a uma velocidade de módulo constante igual a v = 5×10⁵ km/h (aproximadamente a velocidade atingida pela sonda em abril de 2021), tangenciando a superfície da Terra ao longo da Linha do Equador. Em uma hora, aproximadamente quantas voltas a sonda dá em torno da Terra?\nDado: Raio da Terra R_Terra = 6,0×10³ km.',
  },
  58: {
    enunciado: PI + '\n' + SOLAR + '\nA força gravitacional exercida pelo Sol sobre a sonda Solar Parker tem módulo dado por F_Sol = GMm/r², sendo G ≈ 6,7×10⁻¹¹ N·m²/kg² a constante gravitacional universal, M = 2,0×10³⁰ kg a massa do Sol, m a massa da sonda, e r a distância entre a sonda e o centro do Sol. Sendo r = 1,0×10⁷ km (aproximadamente a distância atingida pela sonda em abril de 2021), qual é o módulo da aceleração gravitacional do Sol na referida posição?',
    alternativas: ['6,7×10⁻²⁹ m/s².', '1,34 m/s².', '9,8 m/s².', '2,0×10¹⁰ m/s².'],
  },
  59: {
    enunciado: PI + '\n' + APOLO + '\nA órbita do Columbia era aproximadamente circular, e o módulo da aceleração gravitacional na órbita era g_orb = 1,4 m/s². A força resultante centrípeta é desempenhada pela força gravitacional exercida pela Lua, ou seja, F⃗_cp = m_Columbia·g⃗_orb. Sendo o módulo da velocidade do Columbia v = 1600 m/s, qual foi aproximadamente o período T da órbita?',
  },
  60: {
    enunciado: PI + '\n' + APOLO + '\nA viagem desde o Columbia até a superfície da Lua foi realizada no Módulo Lunar Eagle, formado por dois estágios: um usado na descida e outro, na subida. A massa seca do estágio de subida, ou seja, sem contar a massa do combustível (quase totalmente consumido na viagem de volta), era m ≈ 2500 kg. Considere que o módulo da aceleração gravitacional seja aproximadamente constante e dado por g ≈ g_orb = 1,4 m/s² desde a superfície lunar até a órbita do Columbia, que se situava a uma altitude h = 110 km. Qual é a variação da energia potencial gravitacional do estágio de subida (massa seca que reencontra o Columbia) na viagem de volta?',
    alternativas: ['3,85×10⁵ J.', '2,75×10⁸ J.', '3,85×10⁸ J.', '2,75×10⁹ J.'],
  },
  61: {
    crops: [[22, 22, 79, 277, 244]],
    enunciado: PI + '\nA figura a seguir mostra a temperatura da tigela de uma panela de arroz elétrica em função do tempo de cozimento. Ligando-se a panela, uma resistência elétrica aumenta a temperatura da tigela contendo arroz e água até que a água entre em ebulição. Depois que toda a água é consumida ─ por evaporação e por absorção pelo arroz ─, a temperatura da tigela volta a subir, o que é detectado por um sensor, e a panela é então desligada. A potência elétrica dissipada pela resistência elétrica, na forma de calor, é P = 400 W, constante durante todo o cozimento. Quanto vale a energia elétrica dissipada desde o início do processo até que toda a água seja consumida?',
  },
  62: {
    crops: [[22, 20, 479, 287, 664]],
    enunciado: PI + '\nA autoclave, um equipamento de esterilização de objetos por meio de vapor de água em alta temperatura e pressão, foi inventada por Charles Chamberland, a pedido de Louis Pasteur. A figura a seguir mostra a curva da pressão máxima de vapor da água em função da temperatura. Para temperaturas e pressões do lado esquerdo da curva, a água encontra-se na fase líquida; do lado direito, a água está na fase de vapor. Nos pontos sobre a curva, as fases líquida e de vapor coexistem. A pressão de funcionamento de uma determinada autoclave é p = 3,0 atm. Se toda a água está na fase de vapor, o que se pode dizer sobre a sua temperatura θ?\nDado: 1,0 atm = 100 kPa.',
    alternativas: ['θ pode ter qualquer valor maior que 100 °C.', 'θ pode ter qualquer valor maior que 100 °C e menor que 133 °C.', 'θ pode ter qualquer valor menor que 100 °C ou maior que 133 °C.', 'θ pode ter qualquer valor maior que 133 °C.'],
  },
  63: {
    crops: [[22, 313, 252, 566, 324]],
    replace: [['Considere um campo elétrico uniforme de módulo 4,0 ×10⁻² V/m em uma região do espaço. A E₀ =\ndiferença', 'Considere um campo elétrico uniforme de módulo E₀ = 4,0×10⁻² V/m em uma região do espaço. A diferença']],
  },
  64: {
    crops: [[22, 454, 486, 577, 578]],
    enunciado: 'Uma imagem capturada recentemente pela sonda Perseverance na superfície de Marte mostrou o que parece ser um arco-íris no céu daquele planeta. Na Terra, um arco-íris surge como resultado da decomposição da luz branca do Sol por refração nas gotículas quase esféricas de água, suspensas na atmosfera. Em Marte, contudo, não há chuva. Portanto, a origem do arco-íris ainda é controversa. Em relação ao fenômeno de formação do arco-íris na Terra, quando a luz solar incide em uma gotícula de água, é correto afirmar que',
  },
  65: { replace: [['Acessado em 08/06/ 2021.', 'Acessado em 08/06/2021.']] },
  66: { crops: [[23, 315, 154, 568, 255], [23, 330, 262, 560, 282]], cropGap: 0, replace: [['\nFlor completa Flor I Flor II\n', '\n']], obs: 'Rótulos "Flor completa", "Flor I" e "Flor II" incluídos na imagem, sob as respectivas figuras.' },
  69: { crops: [[24, 309, 77, 579, 378], [24, 313, 385, 589, 551]] },
  70: { crops: [[25, 37, 220, 271, 267]] },
  72: { crops: [[25, 309, 211, 577, 417]] },
};
