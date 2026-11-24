---
name: criar-plugin-pyrevit
description: Cria um botão de pyRevit (pushbutton) para o Revit a partir de um pedido em linguagem de projetista, com a estrutura de pastas, o script.py e o bundle.yaml. Use quando pedirem um plugin, um botão ou uma ferramenta pyRevit para a aba do escritório.
---

# Criar um botão de pyRevit

Você cria um botão de pyRevit que roda dentro do Revit. O projetista instala, testa numa cópia do modelo e decide se vai para a equipe.

## Antes de escrever

Confirme, perguntando só o que faltar:

1. **Nome da extensão, da aba e do painel** onde o botão entra (ex.: `Escritorio.extension`, aba `Escritorio`, painel `Pranchas`).
2. **O que o botão faz**, em uma frase.
3. **Entrada:** o que o usuário escolhe (seleção no modelo, lista, janela, arquivo Excel).
4. **Regras e casos especiais** (já existe, está vazio, tipo diferente).

Se o pedido estiver ambíguo, devolva primeiro o pedido reescrito em quatro linhas (Objetivo, Entrada, Regras, Debug) e espere o OK.

## Estrutura

```
Escritorio.extension/
  Escritorio.tab/
    Pranchas.panel/
      Nome do Botao.pushbutton/
        script.py
        bundle.yaml     (title, tooltip, author)
        icon.png        (32 x 32, fundo transparente)
```

## Como escrever o script.py

- Primeira linha: `# -*- coding: utf-8 -*-`.
- Use `from pyrevit import revit, DB, forms, script`, com `doc = revit.doc` e `out = script.get_output()`.
- Entrada do usuário pelo `forms` do pyRevit (`forms.SelectFromList`, `forms.pick_file`, `forms.ask_for_string`) antes de usar janela própria.
- Toda escrita no modelo dentro de uma única transação: `with revit.Transaction("Nome da ação"):`.
- Nome de tipo: leia com `get_Parameter(DB.BuiltInParameter.SYMBOL_NAME_PARAM).AsString()`. O `Element.Name` falha em alguns tipos no pyRevit.
- Nunca apague elementos sem perguntar com `forms.alert(..., yes=True, no=True)`.
- No fim, mostre um resumo com `out.print_table`: o que foi feito e o que foi pulado, com o motivo.

## Entrega

1. A árvore de pastas e o conteúdo de cada arquivo.
2. Como instalar para testar: `pyrevit extensions paths add <pasta>` e recarregar o pyRevit.
3. Como conferir no modelo.
4. Para a equipe: subir a pasta num repositório git e instalar com `pyrevit extend ui <Nome> <link do repositório>`.

## Quando deu erro

Peça o texto da janela de erro do pyRevit, explique a causa em uma frase e devolva o `script.py` inteiro corrigido.

## Quando atualizar esta skill

Se o projetista corrigir algo que vale para todo botão do escritório (nome da aba, padrão de ícone, um erro da API que se repete), proponha a mudança nesta skill e peça para salvar.

Se a correção vale só para este botão, é uma **exceção**: aplique no script e não mude a skill.
