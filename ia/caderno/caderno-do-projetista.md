# Caderno do projetista: esgoto, caixas e reservatório

Versão resumida para o Curso Ferreto (Aula 20). Junta, num lugar só:

- **regras de norma**, escritas com as nossas palavras a partir da ABNT NBR 8160:1999 (esgoto sanitário) e da ABNT NBR 5626:2020 (água fria e quente);
- **padrões do escritório**, tirados do Caderno de Padrões da Ascent, que nasceram de erros reais em revisão de projeto.

**Não substitui a norma.** Serve para treinar a IA a responder dúvidas e conferir projetos. Antes de assinar, confira o trecho no texto oficial da ABNT.

## Como ler o código

| Começa com | De onde vem | Como achar o trecho |
|---|---|---|
| `NBR8160-` | ABNT NBR 8160:1999, esgoto sanitário | Coluna **Onde achar**: item da norma e página impressa no rodapé do PDF |
| `NBR5626-` | ABNT NBR 5626:2020, água fria e quente | Coluna **Onde achar**: item da norma e página impressa no rodapé do PDF |
| `AP-` ou `EX-` | Padrão do escritório (Caderno de Padrões Ascent) | É decisão interna, não está em norma. AP = nasce no anteprojeto, EX = no executivo; ESG = esgoto, HID = hidráulica, GER = geral |

O número depois do prefixo só ordena as regras deste caderno. Quem localiza o trecho é o item da norma.

## Como a IA deve usar este caderno

1. **Para tirar dúvida:** responda separando o que é norma (com o código e o item) e o que é padrão do escritório (com o código AP ou EX). Se a resposta depender de um dado que não veio (número de pavimentos, de cozinhas, de pessoas), pergunte antes.
2. **Para conferir um projeto:** para cada elemento, percorra as regras do grupo e responda **atende**, **não atende** ou **sem dado para conferir**, com o valor encontrado e o código da regra.
3. Não invente valores. Se o dado não veio, diga qual informação falta.
4. No fim, liste o que não atende, em ordem de gravidade. Regra de norma vem antes de padrão do escritório.

---

## 1. Prumada de esgoto (tubo de queda) e ventilação

| Código | Regra | O que conferir | Onde achar |
|---|---|---|---|
| NBR8160-01 | Tubo de queda num único alinhamento sempre que possível. Desvio só com peças de até 90°, de preferência curva de raio longo ou duas curvas de 45°. | Peças em cada mudança de direção da prumada. | item 4.2.4.1, p. 5 |
| NBR8160-02 | Diâmetro pela soma das UHC dos aparelhos ligados. Referência: DN 75 até 30 UHC e DN 100 até 240 UHC em prédios de até três pavimentos; acima de três, DN 100 vai até 500 UHC. | DN da prumada x soma das UHC. | item 5.1.3.1 e Tabela 6, p. 17 e 18 |
| NBR8160-03 | Desvio com mais de 45° da vertical: o trecho de cima é um tubo de queda próprio, o horizontal é dimensionado como coletor e o de baixo pela soma de tudo, nunca menor que o horizontal. | Ângulo do desvio e DN de cada trecho. | item 5.1.3.2, p. 17 |
| NBR8160-04 | **Zonas de sobrepressão** (prédios de dois ou mais andares com pias, tanques ou máquinas que fazem espuma): não ligar ramal de esgoto nem de ventilação nos trechos abaixo. Em DN 100, 40 diâmetros são 4,0 m e 10 diâmetros são 1,0 m. | Posição das ligações dos ramais. | itens 4.2.4.2 e 4.2.4.3 e Figura 1, p. 5 e 6 |
| | a) 40 diâmetros antes de um desvio para a horizontal; b) 10 diâmetros depois desse desvio; c) 40 diâmetros antes do próximo desvio horizontal; d) 40 diâmetros acima da base do tubo de queda e o coletor logo depois dela; e) antes e depois do primeiro desvio horizontal: 40 diâmetros no coletor ou 10 no subcoletor; f) 40 diâmetros da coluna de ventilação a partir da ligação na base. | | |
| NBR8160-05 | Pias de cozinha e máquinas de lavar louça em andares sobrepostos descem num tubo de queda só delas, com ventilação primária, até uma caixa de gordura coletiva. Caixa de gordura individual nos andares não pode. | Se a prumada da cozinha é exclusiva e onde termina. | itens 4.2.4.4 e 4.2.6.1, p. 5 e 6 |
| NBR8160-06 | A ventilação primária passa da cobertura: pelo menos 0,30 m acima do telhado ou da laje comum e 2,00 m acima de laje usada como terraço. | Altura do terminal x cobertura. | item 4.3.6 b) e Figura 3, p. 7 e 10 |
| NBR8160-07 | Terminal de ventilação a pelo menos 4,00 m de janela, porta ou vão, a não ser que fique 1,00 m acima da verga. | Distância do terminal às aberturas. | item 4.3.6 a), p. 7 |
| NBR8160-08 | Ventilação vertical e numa prumada única; desvio com curvas de até 90° e aclive mínimo de 1%. | Traçado da ventilação. | itens 4.3.9 e 4.3.13, p. 10 |
| AP-ESG-04 | Não superdimensione prumada: dimensione pela soma das UHC, não pelo hábito de pôr 100 mm em tudo. | DN x UHC. | Caderno Ascent |
| AP-ESG-05 | Onde a norma exige 100 mm, tem que ser 100 mm. Errar para menos é mais grave que errar para mais. | DN mínimo. | Caderno Ascent |
| AP-ESG-02 | Junte as colunas de ventilação sempre que der e evite a fachada. | Quantidade e posição das colunas. | Caderno Ascent |
| AP-GER-09 | Trecho horizontal de ventilação sempre com 1% subindo para a coluna. 0% não é aceito. | Inclinação da ventilação. | Caderno Ascent |
| AP-GER-08 | Esgoto e ventilação em PVC série normal; pluvial em série reforçada. Exceção: o ramal da pia até a caixa de gordura pode ser série reforçada. | Material de cada sistema. | Caderno Ascent |

## 2. Pontos de inspeção (cleanout) e caixas de inspeção

| Código | Regra | O que conferir | Onde achar |
|---|---|---|---|
| NBR8160-09 | Todo trecho de tubulação, embutido ou não, acessível por um dispositivo de inspeção. | Se cada trecho tem inspeção. | item 4.2.6.2, p. 6 |
| NBR8160-10 | No máximo 25,00 m entre dois dispositivos de inspeção. | Distância entre inspeções. | item 4.2.6.2 a), p. 6 |
| NBR8160-11 | No máximo 15,00 m entre a ligação com a rede pública e a inspeção mais próxima. | Distância da última inspeção ao ramal predial. | item 4.2.6.2 b), p. 6 |
| NBR8160-12 | Ramais de bacias, caixas de gordura e caixas sifonadas: no máximo 10,00 m até um dispositivo de inspeção. | Comprimento desses ramais. | item 4.2.6.2 c), p. 6 |
| NBR8160-13 | Dispositivo de inspeção junto às curvas da base do tubo de queda, de preferência antes delas. É o cleanout da prumada. | Se há tubo operculado ou peça com tampa na base. | item 4.2.6.2, p. 7 |
| NBR8160-14 | Dispositivo de inspeção com abertura para equipamento de desobstrução, tampa hermética removível e, embutido em área de uso, sem tampa saliente. | Tipo da peça e acabamento. | item 4.2.6.2, p. 7 |
| NBR8160-15 | Desvio, mudança de declividade e junção de tubulação enterrada só com caixa de inspeção ou poço de visita. | Cada mudança na rede enterrada. | item 4.2.6.2, p. 6 |
| NBR8160-16 | Prédio com mais de dois pavimentos: caixa de inspeção a pelo menos 2,00 m do tubo de queda. | Distância caixa x prumada. | item 4.2.6.2, p. 6 |
| NBR8160-17 | Caixa de inspeção: até 1,00 m de profundidade; lado interno mínimo de 0,60 m (ou diâmetro de 0,60 m); tampa removível e vedada; fundo que escoa rápido. | Dimensões e profundidade. | item 5.1.5.3, p. 19 |
| NBR8160-18 | Mais de 1,00 m de profundidade é poço de visita: lado ou diâmetro mínimo de 1,10 m, com degraus. | Profundidade x tipo. | item 5.1.5.3, p. 19 |
| NBR8160-19 | Coletor e subcoletor de preferência retos, com desvios de até 45° e inspeção; declividade mínima de 2% até DN 75 e de 1% a partir de DN 100, máxima de 5%; coletor predial com DN 100 no mínimo. | Traçado, declividade e DN da rede horizontal. | itens 4.2.3.2, 4.2.5.1, 4.2.5.2 e 5.1.4.1, p. 4, 5 e 17 |
| AP-GER-10 | Nenhuma tubulação passa por dentro de caixa de inspeção, gordura ou areia, a não ser a que chega ou sai dela. | Recalque e alimentador desviando por fora. | Caderno Ascent |
| AP-ESG-03 | Afastamento padrão das caixas (até paredes e entre elas), igual em todas. | Afastamentos. | Caderno Ascent |
| AP-GER-04 | Sem ponta aberta nem toco de tubo no modelo. Exceção: o tubo que chega à caixa fica com a ponta solta nela. | Conectores abertos. | Caderno Ascent |

## 3. Caixa de gordura

| Código | Regra | O que conferir | Onde achar |
|---|---|---|---|
| NBR8160-20 | Recomendada sempre que o esgoto tiver gordura. Se a prefeitura não exigir, fica a critério do projetista. | Se a pia da cozinha passa por caixa de gordura. | item 4.2.6.1, p. 6 |
| NBR8160-21 | Local de fácil acesso e ventilado; impermeável, com tampa de fecho hermético e de material que o esgoto não ataque. | Localização e especificação. | itens 4.2.6 e 4.2.6.1, p. 6 |
| NBR8160-22 | Duas câmaras, de entrada e de saída, separadas por septo fixo. | Se a caixa tem septo. | item 5.1.5.1.2, p. 18 |
| NBR8160-23 | Tipo pelo número de cozinhas: 1 cozinha, pequena (CGP) ou simples (CGS); 2 cozinhas, simples ou dupla (CGD); de 3 a 12, dupla; mais de 12 ou cozinha comercial, especial (CGE). | Tipo x cozinhas atendidas. | item 5.1.5.1.1, p. 18 |
| NBR8160-24 | Mínimos por tipo (diâmetro interno / septo submerso / retenção / saída): CGP 0,30 m / 0,20 m / 18 L / DN 75; CGS 0,40 m / 0,20 m / 31 L / DN 75; CGD 0,60 m / 0,35 m / 120 L / DN 100. | Dimensões e DN de saída. | item 5.1.5.1.3, p. 18 e 19 |
| NBR8160-25 | Caixa especial (CGE): retenção V = 2N + 20 litros (N = pessoas no turno de maior movimento), altura molhada 0,60 m, septo submerso 0,40 m, saída DN 100. | Só em cozinha comercial ou mais de 12 cozinhas. | item 5.1.5.1.3 d), p. 19 |

## 4. Reservatórios de água fria

| Código | Regra | O que conferir | Onde achar |
|---|---|---|---|
| NBR5626-01 | Volume total para pelo menos 24 h de consumo normal, mais a reserva de incêndio se ficar junto. | Volume x consumo diário. | item 6.5.6.2, p. 14 |
| NBR5626-02 | Sem exagero, para a água continuar potável. Sem cálculo do limite, recomenda-se até três dias de consumo. | Volume x consumo diário. | item 6.5.6.3, p. 15 |
| NBR5626-03 | Com reservatório inferior e superior, dividir a capacidade para o uso normal, a falta de água da rede e a manutenção. | Divisão de volume. | item 6.5.6.4, p. 15 |
| NBR5626-04 | Reservatório elevado em dois ou mais compartimentos independentes, para limpar um sem parar o prédio. Residência unifamiliar isolada está dispensada. | Compartimentos. | item 6.5.6.5, p. 15 |
| NBR5626-05 | Opaco ou protegido da luz, estanque, com tampa opaca bem presa; nenhuma abertura por onde entre líquido, poeira ou inseto. | Especificação e tampa. | item 6.5.5, p. 14 |
| NBR5626-06 | Entrada e saída posicionadas para renovar a água e não deixar água parada. | Posição entrada x saída. | item 6.5.6.6, p. 15 |
| NBR5626-07 | Controle automático de nível na entrada (boia ou similar) e registro antes do reservatório; no recalque, registro antes do reservatório superior. | Boia e registros. | itens 6.5.8.1 e 6.5.8.2, p. 15 e 16 |
| NBR5626-08 | Nível máximo da água abaixo da geratriz inferior do extravasor (e do aviso, se houver). | Cota do nível x extravasor. | item 6.5.8.3, p. 16 |
| NBR5626-09 | Tubulação de limpeza com registro de fácil acesso perto da saída. | Limpeza com registro. | item 6.5.9.1, p. 16 |
| NBR5626-10 | Extravasor com diâmetro que escoe o excesso sem entupir; aviso de extravasão descarregando em local visível; pontas com tela. | Extravasor, aviso e tela. | itens 6.5.9.3 a 6.5.9.7, p. 16 e 17 |
| NBR5626-11 | Extravasor, limpeza e aviso nunca ligados direto ao esgoto ou à água pluvial. | Destino dessas tubulações. | item 6.5.9.10, p. 17 |
| NBR5626-12 | Acesso fácil ao interior para inspeção e limpeza, com espaço em volta para a manutenção. | Abertura e espaço livre. | item 6.5.10, p. 17 |
| NBR5626-13 | Enchimento: repor o consumo diário em até 6 h; em residência unifamiliar, até 3 h. | Vazão de alimentação x volume. | item 6.7.2, p. 21 |
| NBR5626-14 | Recalque com pelo menos duas bombas independentes, alternadas; sucção um pouco acima do fundo. | Só se houver recalque. | itens 6.5.11.2, 6.5.11.8 e 6.5.11.9, p. 18 |
| NBR5626-15 | Pressão dinâmica mínima de 10 kPa (1 mca) nos pontos de utilização e de 5 kPa (0,5 mca) na rede; estática máxima de 400 kPa (40 mca). A altura do reservatório precisa garantir isso no ponto mais desfavorável. | Desnível do fundo do reservatório ao ponto crítico. | itens 6.9.2 a 6.9.5, p. 22 |
| AP-HID-11 | No mínimo 30 cm livres acima da caixa d'água para tirar a tampa. | Espaço sobre a tampa. | Caderno Ascent |
| AP-HID-17 | Registros mínimos: na saída de consumo da caixa, na limpeza e um de gaveta em cada banheiro ou área molhada, antes dos ramais. | Registros. | Caderno Ascent |
| AP-HID-15 | Tês, registros e conexões do extravasor e da limpeza dentro da área técnica (castelinho). Só o tubo de descarga atravessa a parede. | Posição das conexões. | Caderno Ascent |
| AP-HID-08 | Extravasor e limpeza modelados no sistema de água fria. | Sistema dessas tubulações. | Caderno Ascent |
| AP-HID-18 | Entradas e saídas da caixa e da bomba no diâmetro do tubo, sem bucha de redução junto ao equipamento. | Diâmetros nos conectores. | Caderno Ascent |
| AP-HID-10 | Barrilete com 40 mm da saída da caixa até a primeira ramificação, ou dimensionado pela velocidade. | DN do barrilete. | Caderno Ascent |
| EX-HID-02 | Na prancha, anote volume e material de cada reservatório. | Anotação. | Caderno Ascent |
| EX-HID-09 | No corte do reservatório, cote a base de apoio e a laje e escreva para onde vão o extravasor e a limpeza. | Corte do reservatório. | Caderno Ascent |

---

Ascent · Caderno do projetista resumido para fins didáticos. Normas: ABNT NBR 8160:1999 e ABNT NBR 5626:2020; confira sempre a versão vigente no site da ABNT. O Caderno de Padrões completo é interno e cresce a cada revisão de projeto.
