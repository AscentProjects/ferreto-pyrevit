# Agente de IA no Revit (Aula 21)

Liga o Claude ao Revit pelo MCP, para a IA consultar e corrigir o modelo conferindo pelo [caderno do projetista](../caderno/caderno-do-projetista.md).

Tudo roda no seu computador. A ponte entre o Claude e o Revit só aceita conexão da própria máquina. Não exponha as portas para a rede nem para a internet.

## Instalação (uma vez só)

1. **pyRevit** instalado, como na Aula 18. Baixe só do site oficial do pyRevit.
2. No Revit, aba **pyRevit › Extensions**: instale a extensão **MCP Server for Revit Python** e recarregue o pyRevit (se precisar, reinicie o Revit). Repositório: https://github.com/mcp-servers-for-revit/mcp-server-for-revit-python
3. **pyRevit › Settings › Routes**: ligue o **Routes Server**. Ele escuta em `http://localhost:48884/`.
4. Instale o **uv** (o guia está no repositório da extensão). Depois, no Revit, clique em **MCP › Bridge › Connect** para autorizar a ponte.
5. No **Claude Desktop**: **Settings › Developer › Edit Config** e acrescente o servidor do Revit, trocando o caminho pelo do `main.py` da extensão no seu computador:

```json
{
  "mcpServers": {
    "Revit Connector": {
      "command": "uv",
      "args": ["run", "--frozen", "mcp", "run", "C:\\caminho\\para\\a\\extensao\\main.py"]
    }
  }
}
```

Salve e reinicie o Claude Desktop.

## Onde costuma travar

| Sintoma | O que fazer |
|---|---|
| O Windows (SmartScreen) ou o antivírus bloqueia o instalador | Confira que baixou do site oficial e libere em "Mais informações › Executar assim mesmo". |
| O login do Claude Desktop não volta para o app | Conclua a entrada no navegador, volte ao app e, se ele não reconhecer, feche e abra de novo. |
| A IA diz que não acha o Revit | Revit aberto, Routes ligado, ponte conectada (MCP › Bridge › Connect). Mudou a configuração? Reinicie o Claude Desktop. |

## Pedidos de conferência

Use num projeto do Claude que já tenha o caderno do projetista (veja as [instruções do projeto](../projeto/instrucoes-do-projeto.md)). Trabalhe numa cópia do arquivo enquanto estiver testando.

**Prumada de esgoto**

```
Confira a prumada de esgoto [nome ou tubo de queda] pelo caderno do projetista: DN pela soma das UHC, desvios, ligações fora das zonas de sobrepressão, inspeção na base e ventilação acima da cobertura. Para cada regra, responda atende, não atende ou sem dado, com o valor encontrado e o código.
```

**Caixa de gordura**

```
Confira a caixa de gordura [nome] pelo caderno do projetista: tipo pelo número de cozinhas, dimensões mínimas, DN de saída e se algum tubo atravessa a caixa. Responda atende, não atende ou sem dado, com o código da regra.
```

**Reservatórios**

```
Confira os reservatórios de água fria pelo caderno do projetista: volume entre 24 h e três dias de consumo, boia e registro na entrada, extravasor, aviso e limpeza com destino correto, e 30 cm livres acima da tampa. Se faltar o número de moradores, pergunte.
```

**Corrigir o que achou**

```
Para cada item que não atende, proponha a correção no modelo e liste exatamente o que vai mudar. Não altere nada antes de eu aprovar. Depois de executar, rode a mesma conferência de novo.
```

## Cuidados

- Teste numa cópia do arquivo e salve antes de pedir uma alteração.
- Ela propõe, você aprova: peça a lista do que vai mudar antes de executar.
- Confira no modelo. A responsabilidade técnica continua sendo de quem assina.
