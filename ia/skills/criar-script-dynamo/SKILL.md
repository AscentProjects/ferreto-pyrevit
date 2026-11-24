---
name: criar-script-dynamo
description: Escreve um nó Python para o Dynamo do Revit a partir de um pedido em linguagem de projetista, com entrada, regras e log de erros. Use quando pedirem um script Dynamo, um nó Python, ou para automatizar uma tabela, parâmetro ou numeração no Revit pelo Dynamo.
---

# Criar um script Dynamo (nó Python)

Você escreve o código de um nó **Python Script** do Dynamo que roda dentro do Revit. Quem executa e confere no modelo é o projetista.

## Antes de escrever

Confirme, perguntando só o que faltar:

1. **Versão do Revit** (2022 a 2027). Do Revit 2022 em diante o motor padrão do nó é o CPython 3. Escreva para ele, a não ser que o projetista diga que usa IronPython.
2. **Entrada:** o que entra no nó (`IN[0]`, `IN[1]`...). Ex.: uma tabela selecionada, uma categoria, um nome de parâmetro.
3. **Regra:** o que fazer em cada elemento, e nos casos especiais (parâmetro vazio, elemento repetido, tipo diferente).
4. **Saída:** o que o nó devolve em `OUT` para o projetista conferir no nó Watch.

Se o pedido estiver ambíguo, devolva primeiro o pedido reescrito em quatro linhas (Objetivo, Entrada, Regras, Debug) e espere o OK.

## Como escrever

- Comece pelos imports de sempre: `clr`, `RevitAPI`, `RevitServices` (`DocumentManager` e `TransactionManager`).
- Toda escrita no modelo vai dentro de `TransactionManager.Instance.EnsureInTransaction(doc)` e `TransactionTaskDone()`.
- Leia o parâmetro pelo nome que o projetista deu, e diga no log quando não achar.
- Nunca apague elementos. Se a tarefa pedir isso, devolva a lista e deixe o projetista decidir.
- `OUT` devolve duas listas: o resultado (o que foi alterado, com o valor novo) e o log (o que foi pulado e por quê).
- Comentários curtos em português, um por bloco.

## Entrega

1. O código inteiro do nó, pronto para colar.
2. Como ligar: o que vai em cada entrada `IN[n]`.
3. Como conferir: o que olhar no Watch e no modelo.
4. Um aviso para testar numa cópia do arquivo antes de rodar no projeto.

## Quando deu erro

Peça o texto do erro do nó (ou o log em `OUT`), explique a causa em uma frase e devolva o código inteiro corrigido, não só o trecho.

## Quando atualizar esta skill

Se o projetista corrigir algo que vale para todo script do escritório (versão do Python, padrão de nome de parâmetro, um erro que se repete), proponha a mudança nesta skill e peça para salvar.

Se a correção vale só para este projeto ("aqui o código começa em 100"), é uma **exceção**: aplique no script e não mude a skill.
