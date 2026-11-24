---
name: escrever-memorial
description: Escreve o memorial descritivo de um sistema hidrossanitário (água fria, esgoto, ventilação) a partir dos dados exportados do modelo e do caderno do projetista. Use quando pedirem um memorial descritivo, o texto descritivo de um ambiente ou de um sistema, ou para descrever o projeto para a entrega.
---

# Escrever o memorial descritivo

Você escreve o memorial descritivo de um sistema ou ambiente de instalações prediais. O memorial descreve o que foi projetado. Quem revisa e assina é o projetista.

## Entrada

- Os dados do modelo, exportados em tabela ou colados no chat: trechos com DN, material, comprimento, declividade e cotas; pontos de utilização com altura; registros; reservatórios; caixas e inspeções.
- O caderno do projetista (`caderno/caderno-do-projetista.md`), com as regras de norma e os padrões do escritório.
- O escopo: qual ambiente ou sistema entra no memorial.

## Estrutura

1. **Objeto:** o que o memorial cobre (ambiente, sistemas, pavimento).
2. **Normas e referências:** as normas usadas (ex.: ABNT NBR 5626:2020 e NBR 8160:1999) e o caderno do escritório.
3. **Água fria:** origem (reservatório, rede pressurizada ou por gravidade), caminho até o ambiente, materiais e diâmetros, registros e pontos de utilização com altura.
4. **Esgoto e ventilação:** aparelhos e ralos, ramais de descarga e de esgoto (DN e declividade), tubo de queda, subcoletor até a saída, pontos de inspeção e ventilação até o terminal.
5. **Pontos a confirmar:** tudo o que faltou nos dados ou que não atende ao caderno, com o código da regra.

## Regras

- Escreva só o que está nos dados. Valor que não veio vira item em "Pontos a confirmar", nunca estimativa.
- Diâmetro em DN, comprimento em metros com duas casas, declividade em %, altura de ponto em metros em relação ao piso acabado.
- Material com o nome comercial genérico (ex.: "PVC soldável marrom", "CPVC", "PVC série normal"), sem marca, a não ser que o projetista peça.
- Para cada trecho que você descrever, confira a regra do caderno que se aplica. Se não atender, não esconda: leve para "Pontos a confirmar" com o código (ex.: `NBR8160-13`).
- Erro de modelagem (tubo desconectado, declividade de 100% num degrau) não entra no texto do memorial. Vai numa lista à parte, "Ajustes de modelo", para o projetista corrigir.
- Frases curtas, voz ativa, sem adjetivo. O memorial descreve, não vende.

## Saída

O memorial em markdown, com as cinco seções acima e no máximo duas páginas. No fim, a lista "Ajustes de modelo", se houver.

## Quando atualizar esta skill

Se o projetista corrigir algo que vale para todo memorial do escritório (a ordem das seções, um termo, como citar a norma), proponha a mudança nesta skill e peça para salvar.

Se a correção vale só para este projeto ("neste cliente o memorial vai sem a seção de normas"), é uma **exceção**: aplique no memorial e não mude a skill.
