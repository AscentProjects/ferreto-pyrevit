# Memorial descritivo: banheiro da suíte 03 (exemplo do curso)

Exemplo gerado com a IA na Aula 20 do Curso Ferreto, a partir dos dados exportados do modelo da casa do curso, e revisado pelo projetista. Usa a skill `escrever-memorial` e o `caderno-do-projetista.md`.

## 1. Objeto

Instalações de água fria, esgoto sanitário e ventilação do banheiro da suíte 03 (pavimento Térreo, 2,40 x 1,70 m, 4,08 m²) de uma residência unifamiliar com dois pavimentos habitáveis (Inferior e Térreo).

## 2. Normas e referências

- ABNT NBR 5626:2020, sistemas prediais de água fria e água quente.
- ABNT NBR 8160:1999, sistemas prediais de esgoto sanitário.
- Caderno do projetista do escritório (códigos citados entre parênteses).

## 3. Água fria

O banheiro recebe água por duas redes.

**Rede pressurizada (chuveiro, lavatório e ducha higiênica)**
- Origem: dois reservatórios de 2000 L no pavimento Inferior, com fundo 3,97 m abaixo do ponto do chuveiro. Por isso a rede é pressurizada.
- Pressurização: conjunto com duas bombas de 1,0 CV em paralelo (NBR5626-14).
- Distribuição: CPVC, DN 35 na saída do conjunto, DN 28 na subida ao Térreo e DN 22 nos ramais do banheiro.
- Pontos de utilização, em relação ao piso acabado:

| Ponto | DN | Altura |
|---|---|---|
| Chuveiro (misturador, água fria) | 22 | 1,07 m |
| Lavatório | 22 | 0,59 m |
| Ducha higiênica | 22 | 0,49 m |

**Rede por gravidade (válvula de descarga)**
- Origem: reservatório de aço inox de 500 L na cobertura, com fundo 2,49 m acima da válvula.
- Distribuição: PVC soldável marrom DN 60 na saída do reservatório e DN 50 no barrilete e na descida até a válvula, com registro de esfera na saída (DN 60) e no barrilete (DN 50).
- Ponto: válvula de descarga para baixa pressão, entrada DN 50 a 1,15 m do piso, com 5,43 m de tubulação desde o reservatório.

## 4. Esgoto e ventilação

**Aparelhos e ramais**
- Bacia sanitária: ramal de descarga DN 100, que desce 0,42 m e segue a 1%.
- Lavatório e ralo sifonado do box (grelha de 100 mm sobre sifão DN 50): ramais de descarga DN 50 a 2% (NBR8160-19).
- Os três ramais se juntam no ramal de esgoto DN 100 a 1%, que sai do banheiro sob a laje e corre 4,60 m até o tubo de queda.

**Tubo de queda e subcoletor**
- Tubo de queda DN 100, em PVC série normal (AP-GER-08), com 3,31 m até o pavimento Inferior.
- Subcoletor DN 100, a 1% e 2%, até a saída da rede, que tem válvula de retenção DN 100.
- Inspeção por tês com cap DN 100 (clean-out) ao longo do subcoletor. O primeiro ponto fica a 4,47 m da base do tubo de queda. Os seguintes ficam a 1,47 m, 9,75 m, 0,63 m e 7,38 m um do outro (NBR8160-10).

**Ventilação**
- Ramal de ventilação DN 50, em PVC série normal, ligado ao ramal do lavatório.
- Colunas VE-7 e VE-8 até o terminal na cobertura, com trechos horizontais a 1% (AP-GER-09).
- Terminal 0,33 m acima da laje de cobertura (NBR8160-06, para laje sem uso como terraço).

## 5. Pontos a confirmar pelo projetista

| Código | Situação | O que falta |
|---|---|---|
| NBR8160-13 | Não há dispositivo de inspeção na base do tubo de queda. O primeiro fica 4,47 m adiante, no subcoletor. | Prever inspeção junto à curva da base. |
| NBR8160-12 | O ramal da bacia tem 6,76 m até o tubo de queda, sem inspeção. Contando o tubo de queda, o primeiro ponto de inspeção fica a 14,75 m da bacia. | Decidir se o tubo de queda entra na conta dos 10,00 m. Com a inspeção na base (linha acima), o ramal fica dentro do limite. |
| NBR8160-15 | Se o subcoletor do Inferior for enterrado, as junções e os desvios pedem caixa de inspeção, não só tê com cap. | Confirmar se o trecho é enterrado ou aparente. |
| NBR8160-07 | Distância do terminal de ventilação à janela mais próxima. | A arquitetura não tem janelas modeladas. |
| NBR5626-15 | A válvula de descarga recebe 2,49 m de coluna d'água. | Confirmar no catálogo do fabricante a pressão mínima da válvula de baixa pressão. |
| AP-HID-17 | Não há registro de gaveta dentro do banheiro, antes dos ramais. Os registros da rede pressurizada ficam no Inferior. | Prever o registro do banheiro. |
| NBR5626-01 e 02 | Reserva total de 4500 L (2 x 2000 L e 500 L). | Número de moradores para conferir 24 h a 3 dias de consumo. |
| NBR5626-10 e 11 | Destino final do extravasor e da limpeza do reservatório de inox e aviso nos reservatórios de 2000 L. | Não estão definidos no modelo. |

## Ajustes de modelo

Erros de modelagem vistos na consulta, para corrigir no Revit antes da emissão. Não entram no texto do memorial.

1. Lacunas de 0,10 m e 0,03 m entre os reservatórios, o pressurizador e a rede.
2. Alimentação dos reservatórios de 2000 L a cerca de 0,1 m do conector, sem ligar.
3. Ducha higiênica, cuba do lavatório e válvula de descarga sem ligação à rede.
4. Tubo de queda separado do subcoletor por 0,21 m.
5. Conector de esgoto da bacia e saída da cuba sem ligação; sifão do box solto (0,02 m); segundo ralo isolado.
6. Quatro pontas abertas na ventilação (AP-GER-04).
7. Trechos do subcoletor com declividade de 100% (degraus) e um tubo vertical com declividade registrada.
