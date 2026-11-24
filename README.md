# Ferreto pyRevit

Extensão de exemplo do **Curso Ferreto: Produtividade, Automação e IA no Revit MEP** (Aula 18, "Seu primeiro plugin com pyRevit").

Ela cria a aba **Ferreto** no Revit com o botão **Criar Pranchas**, que cria várias pranchas de uma vez: você escolhe a família de prancha e digita a lista (ou importa de uma planilha do Excel).

## Requisitos

- Revit com o [pyRevit](https://github.com/pyrevitlabs/pyRevit) instalado.

## Instalar

No terminal (PowerShell ou Prompt de Comando):

```
pyrevit extend ui Ferreto https://github.com/PablloDantas/ferreto-pyrevit.git
```

Depois, no Revit, vá na aba **pyRevit** e clique em **Reload**. A aba **Ferreto** aparece.

## Usar

1. Abra o modelo e clique em **Ferreto > Criar Pranchas**.
2. Escolha a família de prancha padrão.
3. Escreva uma prancha por linha, no formato `número | nome | família (opcional)`:

```
HID-01 | PLANTA HIDRÁULICA - TÉRREO
HID-02 | PLANTA HIDRÁULICA - SUPERIOR
SAN-01 | PLANTA SANITÁRIA - TÉRREO | Família da prancha: Tipo
```

4. Ou clique em **Importar do Excel** e escolha uma planilha `.xlsx` com as colunas Número, Nome e Família (opcional). Veja o modelo em `pranchas-exemplo.xlsx`.
5. Clique em **Criar pranchas**. No fim, uma tabela mostra o que foi criado e o que foi pulado. Número que já existe no modelo é pulado.

Tudo roda numa transação só: um Ctrl+Z desfaz a criação inteira.

## Estrutura

```
Ferreto.tab/                     a aba
  Pranchas.panel/                o painel
    Criar Pranchas.pushbutton/   o botão
      script.py                  o código
      janela.xaml                a janela
      icon.png                   o ícone
      bundle.yaml                título e dica do botão
```

Feito pela [Ascent](https://ascent.app.br) para o curso da Ferreto Engenharia.
