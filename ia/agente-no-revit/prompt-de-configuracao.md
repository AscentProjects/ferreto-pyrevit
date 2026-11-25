# Prompt de configuração: Claude + Revit (Aula 21)

Este prompt transforma o Claude no seu assistente de instalação. Ele lê como está o seu computador, consulta a documentação **da versão do pyRevit e da extensão que você tem instaladas** e devolve duas coisas, só com o que falta na sua máquina:

- **Comandos de terminal** (PowerShell), um bloco por vez, para você rodar.
- **Guia de passos manuais**, com os menus do Revit e do Claude Desktop.

Ele não instala nem altera nada sozinho: quem roda os comandos é você, e ele espera a saída de cada bloco antes de seguir. É o mesmo caminho que fazemos na prática da Aula 21.

## Como usar

1. Abra o **Claude Desktop** (ou o Claude Code, se você usa) num chat novo.
   - Se o Claude conseguir ler as pastas do seu computador (pasta conectada ou Claude Code aberto na sua pasta de usuário), ele faz o diagnóstico lendo os arquivos.
   - Se não conseguir, ele te entrega um bloco de PowerShell só de leitura: rode, copie a saída e cole no chat.
2. Copie o prompt abaixo (botão de copiar no canto do bloco) e cole no chat.
3. Siga bloco a bloco. Cole a saída de cada comando de volta no chat, inclusive quando der erro.

Tenha à mão: o Revit que você vai usar no curso instalado e o Claude Desktop instalado e com login feito.

## O prompt

```text
Você vai me ajudar a ligar o Claude ao Revit no meu computador com Windows, usando o pyRevit e a extensão MCP Server for Revit Python. Sou projetista, não programador: explique cada passo em linguagem simples, em português.

Objetivo: no fim, num chat do Claude, eu pergunto "Você consegue ver o Revit? Me diga o nome do modelo aberto e quantos níveis ele tem." e você responde com os dados do meu modelo.

REGRAS
1. Você só lê. Não instale, não apague e não edite nada por conta própria. Quando algo precisar mudar, me entregue o comando para eu rodar no PowerShell ou o passo manual para eu fazer.
2. Um bloco de comandos por vez. Para cada bloco, diga o que ele faz, se muda algo no computador e o que devo ver na saída. Espere eu colar a saída antes de seguir.
3. Use os caminhos reais do meu computador (meu usuário, minhas versões do Revit, as pastas do pyRevit) que você encontrar. Nada de "C:\caminho\para\...".
4. Só fontes oficiais: pyRevit do GitHub pyrevitlabs/pyRevit, a extensão do GitHub mcp-servers-for-revit/mcp-server-for-revit-python e o uv da Astral (astral.sh). Nenhum instalador de site de terceiros.
5. Nunca peça senha, token ou chave, e não copie para o chat chaves ou tokens que aparecerem em arquivos. O Routes do pyRevit deve escutar só em localhost: nunca abra porta para a rede ou para a internet.
6. Nada como administrador, a não ser que não exista outro jeito. Se precisar, explique o motivo antes.
7. Antes de mexer num arquivo de configuração que já existe, me dê o comando que faz uma cópia de segurança dele.
8. Se eu tiver mais de um Revit instalado, pergunte qual eu uso no curso.

ETAPA 1: DIAGNÓSTICO
Descubra, lendo as pastas do meu computador ou, se você não consegue ler arquivos aqui, me dando um único bloco de PowerShell de diagnóstico, só de leitura, para eu rodar e colar a saída:
a) As versões do Revit instaladas (C:\Program Files\Autodesk\Revit 20xx).
b) Se o pyRevit está instalado e a versão exata: "pyrevit --version" e "pyrevit env". Anote a pasta da instalação, os Revits a que ele está ligado e a pasta de extensões.
c) Se a extensão MCP Server for Revit Python já está na pasta de extensões do pyRevit (normalmente %APPDATA%\pyRevit\Extensions), com que nome de pasta e qual versão (pyproject.toml, extension.json ou o último commit).
d) Como está o Routes no %APPDATA%\pyRevit\pyRevit_config.ini (seção [routes]: enabled, host e porta).
e) Se o uv está instalado ("uv --version" e "where.exe uv") e qual Python a extensão pede (.python-version e pyproject.toml).
f) Onde fica o arquivo de configuração do Claude Desktop e quais servidores ele já tem em "mcpServers". Normalmente é %APPDATA%\Claude\claude_desktop_config.json; na versão da Microsoft Store pode estar em %LOCALAPPDATA%\Packages\Claude_*\LocalCache\Roaming\Claude\.
Devolva o diagnóstico numa tabela curta: item, o que encontrou, ok ou falta.

ETAPA 2: DOCUMENTAÇÃO DA VERSÃO INSTALADA
Antes de escrever qualquer comando, consulte a documentação que corresponde às versões que você encontrou, nesta ordem:
1. O que está na minha máquina: README.md, README_UV.md e pyproject.toml da extensão instalada (ou, se ela ainda não estiver instalada, os do repositório oficial), e os arquivos de ajuda da instalação do pyRevit.
2. A ajuda do pyRevit instalado: "pyrevit --help", "pyrevit extend --help", "pyrevit configs --help" e "pyrevit configs routes --help". Use só comandos que aparecem nessa ajuda.
3. Se você tiver acesso à web: as notas da versão instalada no GitHub do pyRevit (a release com o mesmo número), a documentação oficial (docs.pyrevitlabs.io) e o README do repositório da extensão.
Se a documentação da versão instalada disser algo diferente deste prompt, vale a documentação. Diga qual fonte você usou em cada passo e avise se o meu pyRevit está desatualizado ou se o Revit que eu uso não está ligado a ele.

ETAPA 3: O PLANO
Com o diagnóstico e a documentação, me entregue duas partes, só com o que falta no meu computador (pule o que já está ok).

PARTE A, COMANDOS DE TERMINAL (PowerShell), numerados. Cubra o que se aplicar:
- instalar ou atualizar o pyRevit e ligá-lo ao Revit que eu uso;
- instalar a extensão MCP Server for Revit Python (por exemplo com "pyrevit extend ui", se a ajuda da minha versão tiver esse comando);
- ligar o Routes só em localhost (por exemplo "pyrevit configs routes enable", se existir na minha versão) e conferir a porta;
- instalar o uv pelo instalador oficial e conferir com "uv --version" num PowerShell novo;
- fazer a cópia de segurança do claude_desktop_config.json e montar o bloco "Revit Connector" com o caminho real do main.py da extensão (barras invertidas dobradas no JSON), junto com os servidores que eu já tenho, sem apagar nenhum. Mostre o arquivo inteiro como deve ficar e o comando para conferir se o JSON está válido (por exemplo Get-Content ... -Raw | ConvertFrom-Json).
Para o comando do servidor, use o que o README da extensão instalada indica. Se ele falhar por causa da versão do pacote mcp, a combinação que funcionou no curso em 25/11/2026 foi: uv run --with "mcp[cli]<2" --with httpx mcp run "<caminho do main.py>".

PARTE B, GUIA DE PASSOS MANUAIS, numerado, com os nomes de menu como aparecem na minha versão:
- abrir o Revit e conferir a aba do pyRevit e a da extensão;
- recarregar o pyRevit (Reload) ou reiniciar o Revit;
- conferir o Routes nas configurações do pyRevit e testar no navegador o endereço de status que a documentação da extensão indicar (normalmente http://localhost:48884/revit_mcp/status/);
- conectar a ponte, se a extensão pedir (por exemplo MCP › Bridge › Connect);
- fechar o Claude Desktop de verdade (ícone perto do relógio, Sair), abrir de novo e conferir em Settings › Developer que o Revit Connector está rodando;
- o teste final com a pergunta do objetivo.
Para cada passo, acrescente um "se travar aqui" curto: SmartScreen ou antivírus bloqueando download, "uv" ou "pyrevit" não reconhecido (PowerShell aberto antes da instalação), Routes desligado, Revit fechado, Claude Desktop não reiniciado, JSON inválido.

ETAPA 4: ACOMPANHAR
Siga comigo bloco a bloco. Se uma saída mostrar erro, explique em uma frase o que aconteceu e me dê o próximo comando para corrigir. Quando o teste final passar, me dê um resumo de três linhas do que ficou instalado e onde, para eu guardar.

Comece pela Etapa 1.
```

## Depois de configurado

Siga para os [pedidos de conferência e correção](README.md#pedidos-de-conferência) pelo caderno do projetista. Trabalhe numa cópia do modelo e salve antes de pedir qualquer alteração.

## Se travar

A tabela [Onde costuma travar](README.md#onde-costuma-travar) traz os tropeços mais comuns. Se não resolver, cole no mesmo chat a mensagem de erro inteira e peça o próximo passo.
