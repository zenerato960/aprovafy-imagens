// Revisão manual — UNICAMP 2021, 1ª fase, dia 2, Provas Q e Z (f12021Q_Z.pdf). Conferido visualmente página a página.
const NOTA = 'Nas questões de 49 a 56, sempre que necessário, use π = 3 e g = 10 m/s².';
const SN = 'Texto comum para questões 49 e 50.\nRecentemente, uma equipe internacional de cientistas detectou a explosão de uma estrela conhecida como SN2016aps, que teria sido a explosão de supernova mais brilhante já registrada.';
const FERMI = 'Texto comum para questões 52 e 53.\nEm março de 2020, a Unicamp e o Fermi National Accelerator Laboratory (Fermilab), dos Estados Unidos, assinaram um acordo de cooperação científica com o objetivo de desenvolver tanques para conter argônio líquido a baixíssimas temperaturas (criostatos). Esses tanques abrigarão detectores para o estudo dos neutrinos.';
const UV = 'Texto comum para questões 54, 55 e 56.\nLâmpadas de luz ultravioleta (UV) são indicadas para higienização e esterilização de objetos e ambientes em razão do seu potencial germicida.';
export default {
  27: { crops: [[10, 316, 768, 567, 806], [11, 28, 97, 292, 250]] },
  29: { crops: [[11, 313, 160, 572, 345]] },
  31: { crops: [[12, 28, 362, 281, 494], [12, 28, 500, 281, 632]] },
  38: {
    enunciado: 'Sejam a, b, c termos consecutivos de uma progressão geométrica sem nenhum termo nulo e p(x) o polinômio de grau 2 dado por p(x) = a + bx + cx². Se a é positivo, qual das figuras abaixo pode representar corretamente o gráfico de p(x)?',
    crops: [[14, 27, 342, 155, 432], [14, 27, 434, 155, 524], [14, 27, 528, 155, 622], [14, 27, 634, 155, 727]],
    cropLayout: 'grid', alternativas: ['Gráfico a.', 'Gráfico b.', 'Gráfico c.', 'Gráfico d.'],
    obs: 'Alternativas exclusivamente gráficas: os quatro gráficos de y = p(x), com as letras a–d, estão na imagem.',
  },
  40: {
    enunciado: 'Se θ ∈ (0, π/2), a expressão\n[(cos(θ) + sen(θ))/sen(θ) + (cos(θ) − sen(θ))/cos(θ)] / [(cos(θ) + sen(θ))/cos(θ) + (cos(θ) − sen(θ))/sen(θ)]\né equivalente a',
    obs: 'Fração composta escrita em linha (numerador e denominador entre colchetes).',
  },
  41: { alternativas: ['0° < θ ≤ 30°.', '30° < θ ≤ 45°.', '45° < θ ≤ 60°.', '60° < θ ≤ 90°.'] },
  42: { enunciado: 'A figura abaixo exibe três círculos tangentes dois a dois e os três tangentes a uma mesma reta. Os raios dos círculos maiores têm comprimento R e o círculo menor tem raio de comprimento r.\nA razão R/r é igual a', crops: [[14, 361, 471, 521, 554]], alternativas: ['3.', '√10.', '4.', '2√5.'] },
  43: { replace: [['log₁₀ 2 ൎ 0,3 e log₁₀ 5 ൎ 0,7', 'log₁₀ 2 ≈ 0,3 e log₁₀ 5 ≈ 0,7']] },
  44: {
    enunciado: 'Para qual valor de a a equação matricial\n[a −1; a−2 a]·[x; y] = [3; a−4]\nnão admite solução?',
    obs: 'Matrizes escritas em linha: [a −1; a−2 a] = 1ª linha (a, −1), 2ª linha (a−2, a); vetores coluna [x; y] e [3; a−4].',
  },
  45: { enunciado: 'Sabendo que 10^0,3 < 2 < 10^0,31 e que x é tal que ²⁰²¹√(10^(3x+5)) = 20, então', obs: 'Raiz de índice 2021: ²⁰²¹√(10^(3x+5)).' },
  48: { alternativas: ['∜2√3.', '∛2√3.', '√2∛3.', '√2∜3.'] },
  49: {
    enunciado: NOTA + '\n' + SN + '\nA SN2016aps dista da Terra 4,0 bilhões de anos-luz, enquanto a supernova DES16C2nm, localizada a 10,5 bilhões de anos-luz de distância da Terra, é a mais distante já descoberta. Considere que uma explosão das duas supernovas ocorra simultaneamente. Quando o sinal luminoso da explosão da supernova mais próxima for detectado na Terra, a radiação luminosa da supernova DES16C2nm estará a uma distância da Terra aproximadamente igual a\nDados: 1 ano ≈ 3,0×10⁷ s; Velocidade da luz: c = 3,0×10⁸ m/s.',
    alternativas: ['6,5×10⁹ km.', '9,0×10¹⁵ km.', '3,6×10¹⁶ km.', '5,9×10²² km.'],
  },
  32: { replace: [['Hb _((aq)) + O2 (aq) → HbO2 (aq)', 'Hb(aq) + O₂(aq) → HbO₂(aq)']] },
  46: { enunciado: 'Considere que as medidas dos lados de um triângulo retângulo estão em progressão geométrica. Sendo a a medida do menor lado e A a área desse triângulo, é correto afirmar que', alternativas: ['A = a²·√(2√5+2)/4.', 'A = a²·√(2√5−2)/4.', 'A = a²·√(2√5+2)/2.', 'A = a²·√(2√5−2)/2.'] },
  50: { replace: [['Nas questões de 49 a 56, sempre que necessário, use\nRecentemente', NOTA + '\nTexto comum para questões 49 e 50.\nRecentemente']] },
  51: {
    enunciado: NOTA + '\nUma cápsula destinada a levar astronautas à Estação Espacial Internacional (ISS) tem massa m = 7500 kg, incluindo as massas dos próprios astronautas. A cápsula é impulsionada até a órbita da ISS por um foguete lançador e por propulsores próprios para os ajustes finais. O aumento da energia potencial gravitacional devido ao deslocamento da cápsula desde a superfície da Terra até a aproximação com a ISS é dado por ΔU = 3,0×10¹⁰ J. A velocidade da ISS é v_ISS ≈ 8000 m/s. A velocidade inicial da cápsula em razão do movimento de rotação da Terra pode ser desprezada. Sem levar em conta a energia perdida pelo atrito com o ar durante o lançamento, pode-se dizer que o trabalho realizado pelo foguete e pelos propulsores sobre a cápsula é de',
    alternativas: ['2,1×10¹¹ J.', '2,4×10¹¹ J.', '2,7×10¹¹ J.', '5,1×10¹¹ J.'],
  },
  52: {
    enunciado: NOTA + '\n' + FERMI + '\nA temperatura do argônio nos tanques é T_Ar = −184 °C. Usualmente, a grandeza “temperatura” em física é expressa na escala Kelvin (K). Sabendo-se que as temperaturas aproximadas do ponto de ebulição (T_E) e do ponto de solidificação (T_S) da água à pressão atmosférica são, respectivamente, T_E ≈ 373 K e T_S ≈ 273 K, a temperatura do argônio nos tanques será igual a',
  },
  53: {
    enunciado: NOTA + '\n' + FERMI + '\nA pressão exercida na base de certo tanque do Fermilab pela coluna de argônio líquido no seu interior é P = 5,6×10⁴ N/m². A densidade do argônio líquido no tanque é d = 1400 kg/m³. Assim, a altura do tanque será de',
  },
  54: {
    crops: [],
    enunciado: NOTA + '\n' + UV + '\nConsidere uma lâmpada UV de potência P = 100 W que funcione por Δt = 15 minutos durante o processo de esterilização de um objeto. A energia elétrica consumida pela lâmpada nesse processo é igual a',
  },
  55: {
    enunciado: NOTA + '\n' + UV + '\nEm outro processo de esterilização, uma lâmpada UV de potência P = 60 W funciona sob uma diferença de potencial elétrico U = 100 V. A potência elétrica pode ser expressa também em kVA, sendo 1 kVA = 1000 V × 1 A = 1000 W. A corrente elétrica i do circuito que alimenta a lâmpada é igual a',
  },
  56: {
    crops: [[16, 313, 451, 574, 653]],
    enunciado: NOTA + '\n' + UV + '\nA ação germicida da luz UV varia conforme o comprimento de onda (λ) da radiação. O gráfico a seguir mostra a eficiência germicida da luz UV em função de λ, em sua atuação durante certo tempo sobre um agente patogênico.\nPode-se afirmar que a frequência da luz UV que gera eficiência germicida máxima neste caso é\nDado: Velocidade da luz: c = 3,0×10⁸ m/s.',
    alternativas: ['0,9×10⁶ Hz.', '8,1×10¹⁰ Hz.', '5,4×10¹² Hz.', '1,1×10¹⁵ Hz.'],
  },
  62: { crops: [[18, 72, 601, 287, 820]] },
  65: { crops: [[19, 28, 484, 283, 703]], replace: [['populares Donald Trump Republicano 304 62.980.160 Hillary Clinton Democrata 227 65.845.063 Evan McMullin Independente 0 728.830 0 4.488.931 0 1.457.050\n', '']], obs: 'O mapa e a tabela de resultados (candidatos, partidos, delegados e votos populares) estão na imagem.' },
  68: { crops: [[20, 28, 280, 292, 534], [20, 28, 538, 292, 788]] },
};
