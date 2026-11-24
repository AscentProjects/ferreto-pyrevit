# Ferreto pyRevit

Extensão de exemplo do **Curso Ferreto: Produtividade, Automação e IA no Revit MEP** (Aula 18, "Seu primeiro plugin com pyRevit").

Ela cria a aba **Ferreto** no Revit com o botão **Criar Pranchas**, que cria várias pranchas de uma vez: você escolhe a família de prancha e digita a lista (ou importa de uma planilha do Excel).

## Requisitos

- Revit com o [pyRevit](https://github.com/pyrevitlabs/pyRevit) instalado.

## Downloads

### Modelo de planilha: [modelo-pranchas.xlsx](https://github.com/AscentProjects/ferreto-pyrevit/raw/master/modelo-pranchas.xlsx)

Uma prancha por linha: Número, Nome e Família. A coluna Família traz a lista suspensa com as pranchas do template Ferreto; em branco, o botão usa a família padrão escolhida na janela.

![Modelo de planilha com as colunas Número, Nome e Família, e as opções da lista suspensa](docs/modelo-pranchas.png)

### Família de prancha: [PRANCHA PARAMÉTRICA FERRETO - V03.1.rfa](https://github.com/AscentProjects/ferreto-pyrevit/raw/master/familias/PRANCHA%20PARAM%C3%89TRICA%20FERRETO%20-%20V03.1.rfa)

Família de prancha da Ferreto Engenharia, com os tipos A0, A1, A1 Estendido e A2, disponibilizada com autorização dela. Carregue no projeto antes de usar o botão. O carimbo puxa os dados das Informações do projeto.

![Prancha A1 da família Ferreto V03.1](docs/familia-v031.png)

![Detalhe do carimbo da família Ferreto V03.1](docs/familia-v031-carimbo.png)

## Recursos de IA (Aula 19)

- [Cheat sheet de IA para projetistas (PDF)](https://github.com/AscentProjects/ferreto-pyrevit/raw/master/ia/cheat-sheet-ia.pdf): os termos do bloco (modelo, contexto, agente, skill, plugin de IA, MCP) e os pedidos que usamos nas aulas, numa página.
- [Skill revisar-pranchas](ia/skills/revisar-pranchas/SKILL.md): exemplo de skill com o checklist de revisão da documentação antes da entrega. Copie a pasta para as skills do seu Claude e adapte ao padrão do seu escritório.
- [Skill criar-script-dynamo](ia/skills/criar-script-dynamo/SKILL.md): escreve o nó Python do Dynamo a partir do seu pedido, com entrada, regras e log de erros (Aula 17).
- [Skill criar-plugin-pyrevit](ia/skills/criar-plugin-pyrevit/SKILL.md): monta um botão de pyRevit, com a estrutura de pastas, o script e a instalação para a equipe (Aula 18).

Cada skill termina dizendo quando atualizá-la e quando a correção é só uma exceção daquele projeto.

![Cheat sheet de IA para projetistas](docs/cheat-sheet-ia.png)

## Instalar

No terminal (PowerShell ou Prompt de Comando):

```
pyrevit extend ui Ferreto https://github.com/AscentProjects/ferreto-pyrevit.git
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

4. Ou clique em **Importar do Excel** e escolha uma planilha `.xlsx` com as colunas Número, Nome e Família (opcional). Use o modelo `modelo-pranchas.xlsx`: a coluna Família já traz a lista das pranchas do template Ferreto.
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
