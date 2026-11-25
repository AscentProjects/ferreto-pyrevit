# Ascent · Criar Pranchas (pyRevit)

Botão do pyRevit que cria várias pranchas de uma vez a partir de uma lista digitada ou importada do Excel.
Feito para pyRevit 5.x, Revit 2026 e o motor IronPython padrão. Não precisa de bibliotecas externas nem do Excel instalado.

## Estrutura

```
Ascent.extension/
├── LEIA-ME.md
└── Ascent.tab/
    └── Pranchas.panel/
        └── Criar Pranchas.pushbutton/
            ├── script.py      lógica: leitura do Excel, validação, criação e relatório
            ├── janela.xaml    janela WPF
            └── icon.png       ícone do botão (96×96)
```

## Instalação

1. Copie `Ascent.extension` para `%APPDATA%\pyRevit\Extensions`.
2. No Revit, clique em **pyRevit → Reload**. A aba **Ascent** aparece com o botão **Criar Pranchas**.

## Recursos

**Janela**
- Menu "Carimbo padrão" com todos os tipos de carimbo do modelo, no formato `Família : Tipo`, em ordem alfabética, com o primeiro já selecionado.
- Caixa de texto com várias linhas e rolagem, uma prancha por linha: `número | nome | carimbo (opcional)`.
- **Importar do Excel** preenche a caixa para revisão antes de criar.
- Se o modelo não tiver nenhum carimbo carregado, avisa e não abre a janela.

**Importação do Excel (.xlsx)**
- Lê a primeira aba. A linha 1 é o cabeçalho.
- Acha as colunas Número, Nome e Família pelo nome, sem diferenciar maiúsculas, acentos, espaços ou pontuação. Também ignora o que está entre parênteses: "Família (opcional)" funciona.
- A ordem das colunas pode variar e colunas extras são ignoradas. Se faltar Número ou Nome, avisa e não importa nada.
- Tudo é lido como texto: `101` não vira `101.0`, e `001` continua `001` (texto ou formato `000`).
- Linhas vazias são ignoradas. Funciona com a planilha aberta no Excel.
- Erros de leitura (.xls antigo, arquivo com senha, arquivo corrompido) aparecem como mensagem clara, sem traceback.

**Carimbo por linha**
- Aceita `Família : Tipo` (com ou sem espaço antes dos dois-pontos) ou só o nome do tipo, se ele for único no modelo.
- Em branco: usa o carimbo do menu. Se o carimbo não existe ou é ambíguo, a linha é pulada. Nunca troca pelo padrão sem avisar.

**Validação (antes de abrir a transação)**
A linha é pulada, com o motivo registrado, quando:
- o número já existe no modelo, inclusive em pranchas placeholder (sem diferenciar maiúsculas);
- o número está repetido na lista (cria a primeira ocorrência válida);
- o número ou o nome está vazio;
- a linha tem menos de 2 ou mais de 3 campos;
- o número ou o nome tem caractere que o Revit não aceita: `\ : { } [ ] | ; < > ? ` ~`

**Criação**
- Uma única transação, "Criar pranchas em lote": um Ctrl+Z desfaz tudo.
- Cada prancha roda numa subtransação. Se uma falhar, ela não fica pela metade no modelo e as outras continuam.
- Define só número, nome e carimbo.

**Relatório (janela de saída do pyRevit)**
- Resumo: criadas, puladas e com erro.
- Tabela com Linha de origem, Número, Nome, Carimbo, Status e Motivo.
- O número de cada prancha criada é um link que abre a prancha.

## Template de Excel

| Número | Nome | Família (opcional) |
|---|---|---|
| HID-01 | PLANTA HIDRÁULICA - TÉRREO | PRANCHA PARAMÉTRICA FERRETO - V03.1 : A1 |
| HID-02 | PLANTA HIDRÁULICA - SUPERIOR | *(vazio = carimbo do menu)* |
