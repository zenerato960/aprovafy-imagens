// Revisão manual — UNICAMP 2021, 1ª fase, dia 1, Provas E e G (f12021E_G.pdf). Conferido visualmente página a página.
const NOTA = 'Nas questões de 33 a 40, sempre que necessário, use π = 3 e g = 10 m/s².';
const fig = (k, pre = 'Figura') => ['a', 'b', 'c', 'd'].map(l => `${pre} ${l}.`);
const r = {
  20: {
    crops: [[8, 313, 145, 588, 294], [8, 313, 309, 588, 460], [8, 313, 476, 588, 625], [8, 313, 646, 588, 795]],
    cropLayout: 'grid', alternativas: fig(), obs: 'Alternativas exclusivamente gráficas: as quatro ilustrações, com as letras a–d, estão na imagem.',
  },
  22: {
    enunciado: 'A soma dos valores de x que resolvem a equação (1/2 + 1/3)/(x/4 + 1/x) = 1/2 é igual a',
    obs: 'Fração composta escrita em linha: numerador (1/2 + 1/3), denominador (x/4 + 1/x).',
  },
  23: {
    crops: [[9, 28, 407, 140, 500], [9, 28, 503, 140, 597], [9, 28, 601, 140, 695], [9, 28, 695, 140, 790]],
    cropLayout: 'grid', alternativas: fig(0, 'Gráfico'), obs: 'Alternativas exclusivamente gráficas: os quatro gráficos, com as letras a–d, estão na imagem.',
  },
  27: { alternativas: ['b² + ac = a² + c².', 'a² + bc = b² + c².', 'a² − bc = b² + c².', 'b² − ac = a² + c².'] },
  29: {
    enunciado: 'Considere a, b, c, d termos consecutivos de uma progressão aritmética de números reais com razão r ≠ 0. Denote por D o determinante da matriz [a b; c d]. É correto afirmar que D/r² vale',
    alternativas: ['−1', '−2.', '−3.', '−4.'],
    obs: 'Matriz 2×2 escrita em linha: [a b; c d] = 1ª linha (a, b), 2ª linha (c, d). A alternativa a) não tem ponto final no original.',
  },
  33: { enunciado: NOTA + '\nAo passar pelo sensor magnético, a velocidade linear de um ponto de uma fita cassete é v = 0,045 m/s. Depois de passar pelo sensor, a fita é enrolada em uma bobina circular de diâmetro d = 6,0 cm. Em quanto tempo a bobina completa uma volta?' },
  34: {
    crops: [[10, 358, 640, 548, 768]],
    enunciado: NOTA + '\nA figura abaixo mostra o braço de um toca-discos de vinil. Nela são indicadas, nos seus respectivos pontos de atuação, as seguintes forças: peso do braço (P⃗_B), peso do contrapeso (P⃗_C) e força normal aplicada pelo suporte do braço (N⃗). Para que o braço fique em equilíbrio, é necessário que a soma dos torques seja igual a zero. No caso do braço da figura, o módulo do torque de cada força em relação ao ponto O (suporte do braço) é igual ao produto do módulo da força pela distância do ponto de aplicação da força até O. Adote torque positivo para forças que tendem a acelerar o braço no sentido horário e torque negativo para o sentido anti-horário. Sendo |P⃗_C| = 1,5 N, |P⃗_B| = 0,3 N e |N⃗| = 1,8 N, qual deve ser a distância D do contrapeso ao ponto O para que o braço fique em equilíbrio?',
  },
  35: {
    enunciado: NOTA + '\nA força normal aplicada pela agulha de um toca-discos sobre o disco tem módulo igual a |N⃗| = 2,0×10⁻² N. A área de contato entre a agulha e o disco é igual a 1,6×10⁻³ mm². Qual é a pressão exercida pela agulha sobre o disco?\nDado: 1,0 atm = 1,0×10⁵ N/m².',
    alternativas: ['1,25×10⁻⁴ atm.', '3,20×10⁻³ atm.', '3,20×10¹ atm.', '1,25×10² atm.'],
  },
  36: {
    enunciado: NOTA + '\nA força de atrito cinético entre a agulha e um disco de vinil tem módulo |F⃗_at| = 8,0×10⁻³ N. Sendo o módulo da força normal |N⃗| = 2,0×10⁻² N, o coeficiente de atrito cinético, μ_c, entre a agulha e o disco é igual a',
    alternativas: ['1,6×10⁻⁵.', '5,0×10⁻².', '4,0×10⁻¹.', '2,5×10⁰.'],
  },
  37: {
    enunciado: NOTA + '\nEm fevereiro de 2020, a estação meteorológica de Key West, na Flórida (EUA), registrou uma revoada de pássaros migrantes que se assemelhava a uma grande tempestade. Considere uma nuvem de pássaros de forma cilíndrica, de raio R₀ = 145000 m e altura h = 100 m, e densidade de pássaros d_p = 6,0×10⁻⁷ pássaros/m³. Suponha ainda que cada pássaro tenha massa m_p = 0,5 kg e velocidade v₀ = 20 m/s, todos voando na mesma direção e sentido. Assim, a energia cinética da revoada de pássaros é igual a',
    alternativas: ['3,8×10⁸ J.', '1,9×10⁷ J.', '5,2×10³ J.', '1,3×10¹ J.'],
  },
  38: {
    enunciado: NOTA + '\nUm microchip de massa m = 2,0×10⁻⁶ g é composto majoritariamente de silício. Durante um minuto de funcionamento, o circuito elétrico do dispositivo dissipa, na forma térmica, uma quantidade de energia Q = 0,96 mJ. Considere que o calor específico do silício é c_Si = 800 J/kg°C. Caso não houvesse nenhum mecanismo de escoamento de calor para fora do dispositivo, em quanto sua temperatura aumentaria após esse tempo de funcionamento?',
    alternativas: ['4,8×10¹ °C.', '1,6×10² °C.', '6,0×10² °C.', '1,2×10³ °C.'],
  },
  39: {
    crops: [[11, 324, 228, 558, 372]],
    enunciado: NOTA + '\nA diferença de potencial elétrico, U, é proporcional à corrente elétrica, i, em um trecho de um circuito elétrico resistivo, com constante de proporcionalidade dada pela resistência equivalente, R_eq, no trecho do circuito. Além disso, no caso de resistores dispostos em série, a resistência equivalente é dada pela soma das resistências (R_eq = R₁ + R₂ + ...). A corrente elétrica, i_B, no trecho B do circuito abaixo é três vezes maior que a corrente elétrica no trecho A, ou seja, i_B/i_A = 3. Quanto vale a resistência R_B2?',
  },
  40: {
    crops: [[11, 322, 603, 564, 706]],
    replace: [['d _(BR) ≈ 1,2λ _(BR)', 'd_BR ≈ 1,2λ_BR'], ['Blu- Ray', 'Blu-Ray'], ['Nas questões de 33 a 40, sempre que necessário, use\n', NOTA + '\n']],
  },
  41: {
    crops: [[12, 66, 144, 258, 368], [12, 26, 444, 272, 808]],
    alternativas: ['Conjunto de triângulos a.', 'Conjunto de triângulos b.', 'Conjunto de triângulos c.', 'Conjunto de triângulos d.'],
    obs: 'Alternativas gráficas: cada alternativa é uma sequência de três triângulos do fogo (ações A, B e C), na imagem com as letras a–d.',
  },
  64: { crops: [[18, 336, 644, 577, 781]] },
  68: { crops: [[20, 28, 256, 300, 815]] },
  70: { crops: [[21, 10, 16, 296, 216]] },
  71: {
    crops: [[21, 24, 604, 292, 824], [21, 303, 16, 515, 62], [21, 303, 62, 594, 238]], cropGap: 0, cropAlign: 'left',
    obs: 'Imagem com o Mapa 1 seguido do Mapa 2. O topo do Mapa 2 foi recortado separadamente para excluir a logomarca do cabeçalho, sem perda de conteúdo.',
  },
};
export default r;
