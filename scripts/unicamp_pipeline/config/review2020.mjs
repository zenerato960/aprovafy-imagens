// Revisão manual da UNICAMP 2020 (1ª fase, Provas Q e X) — conferida contra o PDF oficial f12020Q_X.pdf.
// crops: [página, x0, y0, x1, y1] em pt (origem no topo). cropLayout: 'stack' (vertical) | 'row' | 'grid'.
// replace: substituições exatas no enunciado extraído; enunciado/alternativas: texto integral transcrito.
const OBS70 = 'Obs.: para as questões de 70 a 79, aproxime π = 3,0 sempre que necessário.';
const DART = 'As agências espaciais NASA (norte-americana) e ESA (europeia) desenvolvem um projeto para desviar a trajetória de um asteroide através da colisão com uma sonda especialmente enviada para esse fim. A previsão é que a sonda DART (do inglês, “Teste de Redirecionamento de Asteroides Duplos”) será lançada com a finalidade de se chocar, em 2022, com Didymoon, um pequeno asteroide que orbita um asteroide maior chamado Didymos.';

export default {
  1: { crops: [[3, 28, 101, 168, 186]] },
  2: { crops: [[3, 62, 434, 246, 666]] },
  3: { crops: [[3, 313, 165, 572, 321]] },
  4: { crops: [[3, 413, 518, 469, 573]] },
  5: { crops: [[4, 26, 341, 282, 597]] },
  6: { crops: [[4, 314, 105, 440, 190]] },
  7: { replace: [['John Milton and Freedom of Speech on Campus By Daniel F. Sullivan A few years ago', 'John Milton and Freedom of Speech on Campus\nBy Daniel F. Sullivan\nA few years ago']] },
  8: { crops: [[5, 39, 308, 270, 608]] },
  12: {
    crops: [[6, 26, 682, 282, 762]],
    replace: [['dinoflagelados. Amostra B', 'dinoflagelados.\nAmostra B'], ['marinhos. Amostra C', 'marinhos.\nAmostra C'], ['plâncton. Amostra D', 'plâncton.\nAmostra D']],
  },
  14: { crops: [[6, 340, 667, 542, 798]] },
  16: { crops: [[7, 317, 197, 566, 411], [7, 321, 450, 561, 642]] },
  19: { crops: [[8, 313, 247, 577, 391]] },
  25: { crops: [[10, 48, 525, 268, 693]] },
  26: { crops: [[10, 313, 311, 571, 470]] },
  28: { crops: [[11, 30, 405, 278, 686]] },
  34: { replace: [['2/3 , independentemente', '2/3, independentemente']], alternativas: ['2/3.', '4/9.', '20/27.', '16/81.'] },
  35: { alternativas: ['a = −1.', 'a = −1/2.', 'a = 1/2.', 'a = 1.'] },
  38: {
    enunciado: 'Tendo em vista que a e b são números reais positivos, a ≠ b, considere a função f(x) = abˣ, definida para todo número real x. Logo, f(2) é igual a',
    alternativas: ['√(f(1)f(3)).', 'f(3)/f(0).', 'f(0)f(1).', 'f(0)³.'],
  },
  39: {
    enunciado: 'Sabendo que p é um número real, considere a matriz A = [p 2; 0 p] e sua transposta Aᵀ. Se A + Aᵀ é singular (não invertível), então',
    alternativas: ['p = 0.', '∣p∣ = 1.', '∣p∣ = 2.', 'p = 3.'],
    obs: 'Matriz 2×2 escrita em linha: [p 2; 0 p] = 1ª linha (p, 2), 2ª linha (0, p). Barras de módulo grafadas com ∣ (U+2223) porque | é o separador de alternativas.',
  },
  40: {
    crops: [[13, 144, 480, 246, 598]],
    enunciado: 'A figura abaixo exibe o triângulo ABC, em que AB = BC e AD é uma altura de comprimento h. A área do triângulo ABC é igual a',
    alternativas: ['h².', '√2h².', '√3h².', '2h².'],
  },
  41: { crops: [[13, 120, 677, 265, 767]], alternativas: ['1/2.', '1/3.', '1/4.', '1/5.'] },
  42: { crops: [[13, 328, 166, 554, 294]] },
  44: { alternativas: ['√2√3.', '∜2√3.', '√2∜3.', '∜2∜3.'] },
  45: {
    replace: [['800 ^oC', '800 °C'], ['327,5 ^oC', '327,5 °C'], ['1750 ^oC', '1750 °C']],
    crops: [[14, 26, 244, 222, 355], [14, 26, 386, 222, 494], [14, 26, 527, 222, 636], [14, 26, 668, 222, 776]],
    cropLayout: 'grid',
    alternativas: [
      'Curva do gráfico a. O potencial de contaminação estaria associado à evaporação do chumbo em alta temperatura.',
      'Curva do gráfico b. O potencial de contaminação estaria associado à ebulição do chumbo em alta temperatura.',
      'Curva do gráfico c. O potencial de contaminação estaria associado à ebulição do chumbo em alta temperatura.',
      'Curva do gráfico d. O potencial de contaminação estaria associado à evaporação do chumbo em alta temperatura.',
    ],
    obs: 'Alternativas compostas por gráfico + texto: os quatro gráficos (com as letras a–d) estão na imagem; o texto de cada alternativa remete ao gráfico de mesma letra.',
  },
  46: {
    crops: [[14, 368, 238, 520, 390], [14, 331, 393, 552, 539]],
    enunciado: 'O “Ebulidor de Franklin” é um brinquedo constituído de dois bulbos de vidro conectados por um tubo espiralado, preenchido com líquido colorido. Seu uso consiste em encostar a mão na base do bulbo inferior, fazendo com que o líquido seja aquecido e ascenda para o bulbo superior. Popularmente, a libido de uma pessoa é avaliada com base na quantidade de líquido que ascende. O sucesso de venda, obviamente, é maior quanto mais positivamente o brinquedo indicar uma “alta libido”. Abaixo apresenta-se um gráfico da pressão de vapor em função da temperatura para dois líquidos, A e B, que poderiam ser utilizados para preencher o “Ebulidor de Franklin”.\nConsiderando essas informações, é correto afirmar que a pressão no interior do brinquedo',
  },
  47: {
    crops: [[15, 31, 163, 284, 326]],
    enunciado: 'O Termômetro de Galileu (Figura A) é uma forma criativa de se estimar a temperatura ambiente. Ele consiste em uma coluna de vidro preenchida com um líquido. Em seu interior, são colocadas várias bolas de vidro colorido calibradas e marcadas para a leitura da temperatura. As bolas de vidro sobem ou descem em função da temperatura. A sensibilidade do Termômetro de Galileu reside na sua capacidade de separar duas leituras de temperaturas. A figura B é um gráfico de densidade em função da temperatura para água e etanol, dois líquidos que poderiam ser usados no termômetro.\nDe acordo com essas informações e os conhecimentos de química, a leitura correta da temperatura do termômetro representado na Figura A pode ser indicada pela bola de vidro que se situa',
  },
  48: {
    crops: [[15, 313, 79, 570, 297]],
    enunciado: 'As caldeiras são utilizadas para alimentar máquinas nos mais diversos processos industriais, para esterilização de equipamentos e instrumentos em hospitais, hotéis, lavanderias, entre outros usos. A temperatura elevada da água da caldeira mantém compostos solubilizados na água de alimentação que tendem a se depositar na superfície de troca térmica da caldeira. Esses depósitos, ou incrustações, diminuem a eficiência do equipamento e, além de aumentar o consumo de combustível, podem ainda resultar em explosões. A tabela e a figura a seguir apresentam, respectivamente, informações sobre alguns tipos de incrustações em caldeiras, e a relação entre a espessura da incrustação e o consumo de combustível para uma eficiência constante.\nConsiderando as informações apresentadas, é correto afirmar que as curvas A e B podem representar, respectivamente, informações sobre incrustações',
  },
  51: {
    crops: [[16, 26, 418, 240, 555], [16, 26, 598, 240, 737], [16, 313, 82, 528, 221], [16, 313, 254, 528, 393]],
    cropLayout: 'grid',
    alternativas: [
      'Gráfico a. Essa influência se acentua na região dos polos, em razão da temperatura da água do mar.',
      'Gráfico b. Essa influência se acentua na região dos trópicos, em razão da temperatura da água do mar.',
      'Gráfico c. Essa influência se acentua na região dos polos, em razão da temperatura da água do mar.',
      'Gráfico d. Essa influência se acentua na região dos trópicos, em razão da temperatura da água do mar.',
    ],
    obs: 'Alternativas compostas por gráfico (concentração de CO₂ e pH × ano) + texto: os quatro gráficos com as letras a–d estão na imagem.',
  },
  52: {
    crops: [[16, 316, 616, 562, 792]],
    enunciado: 'Um dos pilares da nanotecnologia é o fato de as propriedades dos materiais dependerem do seu tamanho e da sua morfologia. Exemplo: a maior parte do H₂ produzido industrialmente advém da reação de reforma de hidrocarbonetos: CH₄(g) + H₂O(g) → 3H₂(g) + CO(g). Uma forma de promover a descontaminação do hidrogênio é reagir o CO com largo excesso de água:\nCO(g) + H₂O(g) → CO₂(g) + H₂(g); ΔH = −41,6 kJ mol⁻¹.\nA figura abaixo mostra resultados da velocidade (em unidade arbitrária, ua) dessa conversão em função da temperatura, empregando-se um nanocatalisador com duas diferentes morfologias.\nConsiderando essas informações, é correto afirmar que, com essa tecnologia, a descontaminação do hidrogênio por CO é mais eficiente na presença do catalisador em forma de',
  },
  54: {
    crops: [[17, 313, 79, 569, 153]],
    enunciado: 'Para ser usado em um implante dentário, um metal ou liga precisa apresentar excelente compatibilidade com o organismo, alta resistência mecânica e boa flexibilidade, entre outros atributos. Imagine que dois metais, A e B, tenham sido testados quanto à sua aplicação em um implante, e o metal A foi considerado a melhor opção.\nEsse resultado é compatível com o fato de que o metal A tem',
  },
  56: { obs: 'Equação de combustão do propano reproduzida como no original (sem coeficiente estequiométrico no O₂).' },
  59: { crops: [[18, 335, 390, 554, 753]] },
  63: {
    crops: [],
    enunciado: 'O poema abaixo vem impresso na orelha do livro Psia, de Arnaldo Antunes.\nPsia é feminino\nde psiu;\nque serve para chamar a atenção\nde alguém, ou para pedir\nsilêncio.\nEu berro as palavras\nno microfone\nda mesma maneira com que\nas desenho, com cuidado,\nna página.\nPara transformá-las em coisas,\nem vez de substituírem\nas coisas.\nCalos na língua; de calar.\nAlguma coisa entre a piscina e a pia.\nUm hiato a menos.\n(Arnaldo Antunes, Psia. São Paulo: Iluminuras, 2012.)\nNa orelha do livro, Antunes apresenta ao leitor seu processo de criação poética. É correto dizer que o autor se propõe a',
  },
  64: {
    crops: [[20, 26, 464, 291, 559]],
    replace: [
      ['https://www.tecmundo.com.br/ internet/133690-voce-notou-net flix-parece-evitando-termo-maratonar.htm', 'https://www.tecmundo.com.br/internet/133690-voce-notou-netflix-parece-evitando-termo-maratonar.htm'],
      ['Acessado em 01/06/ 2019.', 'Acessado em 01/06/2019.'],
    ],
  },
  65: { replace: [['https://cinegnose. Blogs pot.com/', 'https://cinegnose.blogspot.com/'], ['01/03 /2019', '01/03/2019']] },
  66: { replace: [['https://cinegnose. Blogs pot.com/', 'https://cinegnose.blogspot.com/'], ['01/03 /2019', '01/03/2019']] },
  67: { crops: [[20, 313, 698, 576, 797]] },
  68: { replace: [['http://notarodape. blogspot. com/ search/label/Cotidiano', 'http://notarodape.blogspot.com/search/label/Cotidiano']] },
  69: {
    crops: [[21, 335, 455, 554, 609]],
    replace: [['https://gq.globo.com/Cultura/ noticia/2019/05/ laerte-e-angeli-participam-de-exposicao-ao-ar-livre-na-avenida-paulista.html', 'https://gq.globo.com/Cultura/noticia/2019/05/laerte-e-angeli-participam-de-exposicao-ao-ar-livre-na-avenida-paulista.html']],
  },
  70: {
    enunciado: OBS70 + '\nA volta da França é uma das maiores competições do ciclismo mundial. Num treino, um ciclista entra num circuito reto e horizontal (movimento em uma dimensão) com velocidade constante e positiva. No instante t₁, ele acelera sua bicicleta com uma aceleração constante e positiva até o instante t₂. Entre t₂ e t₃, ele varia sua velocidade com uma aceleração também constante, porém negativa. Ao final do percurso, a partir do instante t₃, ele se mantém em movimento retilíneo uniforme. De acordo com essas informações, o gráfico que melhor descreve a velocidade do atleta em função do tempo é',
    crops: [[22, 26, 274, 228, 402], [22, 26, 415, 228, 543], [22, 26, 559, 228, 688], [22, 26, 693, 228, 822]],
    cropLayout: 'grid',
    alternativas: ['Gráfico a.', 'Gráfico b.', 'Gráfico c.', 'Gráfico d.'],
    obs: 'Alternativas exclusivamente gráficas (velocidade × tempo): os quatro gráficos com as letras a–d estão na imagem.',
  },
  71: {
    crops: [],
    enunciado: OBS70 + '\nTexto comum às questões 71, 72 e 73.\n' + DART + '\nA massa da sonda DART será de m_sonda = 300 kg, e ela deverá ter a velocidade v_sonda = 6 km/s imediatamente antes de atingir Didymoon. Assim, a energia cinética da sonda antes da colisão será igual a',
    alternativas: ['1,8×10³ J.', '5,4×10³ J.', '1,8×10⁶ J.', '5,4×10⁹ J.'],
  },
  72: { enunciado: OBS70 + '\nTexto comum às questões 71, 72 e 73.\n' + DART + '\nNuma colisão inelástica da sonda DART com o asteroide Didymoon,' },
  73: {
    crops: [],
    enunciado: OBS70 + '\nTexto comum às questões 71, 72 e 73.\n' + DART + '\nO asteroide satélite Didymoon descreve uma órbita circular em torno do asteroide principal Didymos. O raio da órbita é r = 1,6 km e o período é T = 12 h. A aceleração centrípeta do satélite vale',
    alternativas: ['8,0×10⁻¹ km/h².', '4,0×10⁻¹ km/h².', '3,125×10⁻¹ km/h².', '6,667×10⁻² km/h².'],
  },
  74: {
    crops: [[23, 56, 211, 247, 349]],
    enunciado: OBS70 + '\nAs escadas flutuantes em cascata feitas em concreto armado são um elemento arquitetônico arrojado, que confere leveza a uma estrutura intrinsecamente massiva. Essas escadas são apoiadas somente na extremidade superior (normalmente em uma parede) e no chão. O esquema abaixo mostra as forças aplicadas na escada pela parede (F⃗_P) e pelo chão (F⃗_C), além da força peso (mg⃗) aplicada pela Terra, todas pertencentes a um plano vertical.\nCom base nesse esquema, é correto afirmar que',
    alternativas: [
      'F_P cosθ_P = F_C cosθ_C e F_P senθ_P + F_C senθ_C = mg.',
      'F_P senθ_P = F_C senθ_C e F_P cosθ_P + F_C cosθ_C = mg.',
      'F_P cosθ_P = F_C cosθ_C e F_P + F_C = mg.',
      'F_P = F_C e F_P senθ_P + F_C senθ_C = mg.',
    ],
  },
  75: {
    crops: [],
    enunciado: OBS70 + '\nO CO₂ dissolvido em bebidas carbonatadas, como refrigerantes e cervejas, é o responsável pela formação da espuma nessas bebidas e pelo aumento da pressão interna das garrafas, tornando-a superior à pressão atmosférica. O volume de gás no “pescoço” de uma garrafa com uma bebida carbonatada a 7 °C é igual a 24 ml, e a pressão no interior da garrafa é de 2,8×10⁵ Pa. Trate o gás do “pescoço” da garrafa como um gás perfeito. Considere que a constante universal dos gases é de aproximadamente 8 J/mol·K e que as temperaturas nas escalas Kelvin e Celsius relacionam-se da forma T(K) = θ(°C) + 273. O número de moles de gás no “pescoço” da garrafa é igual a',
    alternativas: ['1,2×10⁵.', '3,0×10³.', '1,2×10⁻¹.', '3,0×10⁻³.'],
  },
  76: {
    crops: [[23, 376, 226, 508, 298]],
    replace: [['com uma bola de massa e mesma carga q.', 'com uma bola de massa 2m e mesma carga q.']],
  },
  77: {
    crops: [],
    enunciado: OBS70 + '\nEm 2019 foi divulgada a primeira imagem de um buraco negro, obtida pelo uso de vários radiotelescópios. Também recentemente, uma equipe da NASA propôs a utilização de telescópios de infravermelho para detectar antecipadamente asteroides que se aproximam da Terra. Considere que um radiotelescópio detecta ondas eletromagnéticas provenientes de objetos celestes distantes na frequência de f_rádio = 1,5 GHz, e que um telescópio de infravermelho detecta ondas eletromagnéticas originadas em corpos do sistema solar na frequência de f_infravermelho = 30 THz. Qual é a razão entre os correspondentes comprimentos de onda no vácuo, λ_rádio/λ_infravermelho?',
    alternativas: ['5,0×10⁻⁵.', '6,7×10⁻⁵.', '2,0×10⁴.', '6,0×10¹².'],
  },
  78: {
    crops: [[24, 26, 224, 212, 340], [24, 26, 360, 214, 499], [24, 26, 508, 230, 643], [24, 26, 661, 218, 796]],
    cropLayout: 'grid',
    replace: [['Nessas figuras, ( f ) e ( f’ ) representam', 'Nessas figuras, (f) e (f’) representam'], ['( o ) o objeto e ( i ) a imagem', '(o) o objeto e (i) a imagem']],
    alternativas: ['Figura a.', 'Figura b.', 'Figura c.', 'Figura d.'],
    obs: 'Alternativas exclusivamente gráficas (traçado de raios na lupa): as quatro figuras com as letras a–d estão na imagem.',
  },
  79: {
    crops: [[24, 353, 209, 529, 273], [24, 322, 300, 560, 372]],
    enunciado: OBS70 + '\nEm analogia com um circuito elétrico, a transpiração foliar é regulada pelo conjunto de resistências (medidas em segundos/metro) existentes na rota do vapor d’água entre os sítios de evaporação próximos à parede celular no interior da folha e a atmosfera. Simplificadamente, há as resistências dos espaços intercelulares de ar (r_eia), as induzidas pela presença dos estômatos (r_est) e da cutícula (r_cut) e a promovida pela massa de ar próxima à superfície das folhas (r_cl). O esquema abaixo representa as resistências mencionadas.\nA tabela a seguir apresenta os valores das resistências de duas espécies de plantas (espécie 1 e espécie 2).\nTendo em vista os dados apresentados e considerando que a condutância é o inverso da resistência, assinale a alternativa que indica a espécie com menor transpiração e sua respectiva condutância total à difusão do vapor d’água entre os sítios de evaporação e a atmosfera.',
    alternativas: ['espécie 1; 48 x 10⁻⁴ m/s.', 'espécie 1; 125 x 10⁻⁴ m/s.', 'espécie 2; 30 x 10⁻⁴ m/s.', 'espécie 2; 200 x 10⁻⁴ m/s.'],
  },
  81: {
    crops: [[25, 27, 251, 141, 401]],
    enunciado: 'Que dizer das personagens? Creio que têm a força e ao mesmo tempo a fraqueza da caricatura. Mas, pensando melhor, não poderemos também alegar em defesa do romancista que a caricatura é uma tendência reconhecida e aceita da arte moderna, principalmente da pintura? Não haverá muito de deformação na obra de grandes pintores como Portinari, Di Cavalcante e Segall – todos eles inconformados com a sociedade em que vivem?\n(Adaptado de Erico Verissimo, Prefácio, em Caminhos Cruzados. São Paulo: Companhia das Letras, 2016, p. 20-21.)\nTarsila do Amaral, A negra, 1923. Coleção Museu de Arte Contemporânea da Universidade de São Paulo, São Paulo.\nA ideia de deformação aplica-se ao quadro de Tarsila e ao romance de Érico Veríssimo, porque tal procedimento artístico acentua',
  },
  86: {
    crops: [[26, 312, 96, 573, 264]],
    enunciado: 'Jean-Baptiste Debret, Retrato de El Rei Dom João VI, 1817. Museu Nacional de Belas Artes, Rio de Janeiro.\nHyacinthe Rigaud, Retrato de Luís XIV, 1701. Museu do Louvre, Paris.\nA partir das fontes visuais reproduzidas e de seus conhecimentos, assinale a alternativa correta.',
  },
};
