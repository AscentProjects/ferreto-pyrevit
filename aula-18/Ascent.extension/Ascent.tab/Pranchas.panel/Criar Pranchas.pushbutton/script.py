# -*- coding: utf-8 -*-
"""Cria várias pranchas de uma vez a partir de uma lista
(digitada ou importada de uma planilha .xlsx)."""

__title__ = "Criar\nPranchas"

import os
import re
import posixpath

import clr
clr.AddReference("System")
clr.AddReference("System.Xml")
clr.AddReference("System.IO.Compression")

from System import Environment
from System.Collections.Generic import List
from System.IO import FileStream, FileMode, FileAccess, FileShare, StreamReader
from System.IO.Compression import ZipArchive, ZipArchiveMode
from System.Text import Encoding, NormalizationForm
from System.Globalization import CharUnicodeInfo, UnicodeCategory
from System.Xml import XmlDocument, XmlNodeType

from pyrevit import revit, DB, forms, script


# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------
NOME_TRANSACAO = u"Criar pranchas em lote"
CARACTERES_PROIBIDOS = u"\\:{}[]|;<>?`~"

CRIADA = u"Criada"
PULADA = u"Pulada"
ERRO = u"Erro"

PASTA_BOTAO = os.path.dirname(__file__)
ARQUIVO_XAML = os.path.join(PASTA_BOTAO, "janela.xaml")


class ErroExcel(Exception):
    """Erro de leitura da planilha com mensagem pronta para o usuário."""
    pass


# ---------------------------------------------------------------------------
# Utilidades de texto
# ---------------------------------------------------------------------------
def sem_acentos(texto):
    """Remove acentos (á -> a, ç -> c) mantendo o resto do texto."""
    if not texto:
        return u""
    try:
        # Caminho .NET (sempre disponível no IronPython)
        decomposto = texto.Normalize(NormalizationForm.FormD)
        return u"".join(
            ch for ch in decomposto
            if CharUnicodeInfo.GetUnicodeCategory(ch) != UnicodeCategory.NonSpacingMark
        )
    except Exception:
        # Reserva: módulo unicodedata do Python
        import unicodedata
        decomposto = unicodedata.normalize("NFKD", texto)
        return u"".join(ch for ch in decomposto if not unicodedata.combining(ch))


def normalizar(texto):
    """Chave para comparar cabeçalhos: sem acento, sem espaços, minúsculo.
    Ignora o que estiver entre parênteses e a pontuação, então
    'Família (opcional)', 'Número:' etc. também são reconhecidos."""
    texto = re.sub(u"\\(.*?\\)", u"", sem_acentos(texto or u""))
    return re.sub(u"[^0-9a-z]", u"", texto.lower())


def mensagem_erro(exc):
    """Mensagem legível de uma exceção Python ou .NET (sem traceback)."""
    msg = getattr(exc, "Message", None)
    if not msg:
        try:
            msg = exc.args[0] if exc.args else u""
        except Exception:
            msg = u""
    if not msg:
        msg = u"{}".format(exc)
    return msg or exc.__class__.__name__


def escapar(texto):
    """Escapa texto para a tabela do pyRevit (markdown/HTML), sem quebrar
    a tabela se houver | * _ ` < > etc. no conteúdo."""
    if texto is None:
        return u""
    texto = u"{}".format(texto).replace(u"&", u"&amp;")
    trocas = {
        u"<": u"&lt;", u">": u"&gt;", u"|": u"&#124;", u"*": u"&#42;",
        u"_": u"&#95;", u"`": u"&#96;", u"\\": u"&#92;", u"[": u"&#91;",
        u"]": u"&#93;", u"#": u"&#35;",
    }
    return u"".join(trocas.get(ch, ch) for ch in texto)


# ---------------------------------------------------------------------------
# Leitura de .xlsx sem bibliotecas externas
# (um .xlsx é um ZIP com arquivos XML; usamos ZipArchive e XmlDocument do .NET)
# ---------------------------------------------------------------------------
def _filhos(no, nome_local):
    """Elementos filhos diretos com o nome local informado (ignora namespace)."""
    return [n for n in no.ChildNodes
            if n.NodeType == XmlNodeType.Element and n.LocalName == nome_local]


def _filho(no, nome_local):
    lista = _filhos(no, nome_local)
    return lista[0] if lista else None


def _ler_xml(entradas, caminho, obrigatorio=True):
    """Lê um XML de dentro do ZIP. Retorna XmlDocument ou None."""
    entrada = entradas.get(caminho.lower())
    if entrada is None:
        if obrigatorio:
            raise ErroExcel(
                u"O arquivo não parece ser uma planilha do Excel válida "
                u"(parte interna ausente: {}).".format(caminho))
        return None
    leitor = StreamReader(entrada.Open(), Encoding.UTF8)
    try:
        texto = leitor.ReadToEnd()
    finally:
        leitor.Close()
    xml = XmlDocument()
    xml.LoadXml(texto)
    return xml


def _relacoes(entradas, caminho_rels):
    """Lê um arquivo .rels e devolve lista de (Id, Type, Target)."""
    xml = _ler_xml(entradas, caminho_rels, obrigatorio=False)
    if xml is None:
        return []
    return [(r.GetAttribute("Id"), r.GetAttribute("Type"), r.GetAttribute("Target"))
            for r in xml.SelectNodes("//*[local-name()='Relationship']")]


def _resolver_alvo(pasta_base, alvo):
    """Transforma o Target de um .rels em caminho dentro do ZIP."""
    alvo = alvo.replace(u"\\", u"/")
    if alvo.startswith(u"/"):
        return alvo.lstrip(u"/")
    return posixpath.normpath(posixpath.join(pasta_base, alvo))


def _decodificar_escapes(texto):
    """O Excel grava caracteres de controle como _x000D_; desfaz isso."""
    return re.sub(u"_x([0-9A-Fa-f]{4})_", lambda m: unichr_(int(m.group(1), 16)), texto)


def unichr_(codigo):
    try:
        return unichr(codigo)  # IronPython 2
    except NameError:
        return chr(codigo)     # IronPython 3


def _texto_rico(no):
    """Concatena todos os <t> de um <si>/<is>, ignorando a fonética (<rPh>)."""
    partes = [t.InnerText for t in no.SelectNodes(
        ".//*[local-name()='t'][not(ancestor::*[local-name()='rPh'])]")]
    return _decodificar_escapes(u"".join(partes))


def _indice_coluna(ref):
    """'A1' -> 1, 'AB12' -> 28. Retorna None se a referência não tiver letras."""
    m = re.match(u"([A-Za-z]+)", ref or u"")
    if not m:
        return None
    indice = 0
    for letra in m.group(1).upper():
        indice = indice * 26 + (ord(letra) - ord(u"A") + 1)
    return indice


def _numero_para_texto(valor, largura_zeros):
    """Converte o valor numérico gravado no XML em texto:
    101 -> '101' (nunca '101.0'); 1 com formato '000' -> '001'."""
    bruto = (valor or u"").strip()
    try:
        f = float(bruto)
        if abs(f) < 1e15 and f == int(f):
            texto = u"{}".format(int(f))
        else:
            texto = u"%.15g" % f
    except (ValueError, OverflowError):
        return bruto
    if largura_zeros and texto.isdigit():
        texto = texto.zfill(largura_zeros)
    return texto


def _larguras_zeros(xml_estilos):
    """Para cada estilo de célula, a quantidade de dígitos de formatos do tipo
    '000' / '0000' (zeros à esquerda). 0 quando não se aplica."""
    if xml_estilos is None:
        return []
    formatos = {}
    for nf in xml_estilos.SelectNodes("//*[local-name()='numFmts']/*[local-name()='numFmt']"):
        formatos[nf.GetAttribute("numFmtId")] = nf.GetAttribute("formatCode")
    larguras = []
    for xf in xml_estilos.SelectNodes("//*[local-name()='cellXfs']/*[local-name()='xf']"):
        codigo = (formatos.get(xf.GetAttribute("numFmtId"), u"") or u"").replace(u'"', u"").strip()
        larguras.append(len(codigo) if re.match(u"^0+$", codigo) and len(codigo) > 1 else 0)
    return larguras


def _valor_celula(c, compartilhadas, larguras):
    """Valor de uma célula <c> como texto."""
    tipo = c.GetAttribute("t")
    no_v = _filho(c, "v")
    v = no_v.InnerText if no_v is not None else u""

    if tipo == "s":                      # texto compartilhado
        try:
            return compartilhadas[int(v)]
        except (ValueError, IndexError):
            return u""
    if tipo == "inlineStr":              # texto embutido na célula
        no_is = _filho(c, "is")
        return _texto_rico(no_is) if no_is is not None else u""
    if tipo in ("str", "e"):             # resultado de fórmula / erro (#N/D)
        return _decodificar_escapes(v)
    if tipo == "b":                      # booleano
        return u"VERDADEIRO" if v == "1" else u"FALSO"
    if not v:
        return u""
    # Número (ou data, que também é número no Excel)
    largura = 0
    estilo = c.GetAttribute("s")
    if estilo.isdigit() and int(estilo) < len(larguras):
        largura = larguras[int(estilo)]
    return _numero_para_texto(v, largura)


def _limpar(texto):
    """Quebras de linha e tabulações viram espaço; tira espaços das pontas."""
    if not texto:
        return u""
    return re.sub(u"[\r\n\t]+", u" ", texto).strip()


def ler_primeira_aba(caminho):
    """Lê a primeira aba de um .xlsx.
    Retorna lista de (numero_da_linha, {indice_coluna: texto})."""
    fluxo = None
    arquivo = None
    try:
        try:
            # FileShare.ReadWrite permite ler mesmo com a planilha aberta no Excel
            fluxo = FileStream(caminho, FileMode.Open, FileAccess.Read, FileShare.ReadWrite)
        except Exception as e:
            raise ErroExcel(u"Não foi possível abrir o arquivo.\n\n{}".format(mensagem_erro(e)))
        try:
            arquivo = ZipArchive(fluxo, ZipArchiveMode.Read)
            entradas = dict((e.FullName.replace(u"\\", u"/").lstrip(u"/").lower(), e)
                            for e in arquivo.Entries)
        except Exception:
            raise ErroExcel(
                u"O arquivo não é um .xlsx válido.\n\n"
                u"Planilhas .xls (Excel 97-2003) e arquivos protegidos por senha "
                u"não são suportados. Abra no Excel e use Salvar como > .xlsx.")

        # 1) Onde está o workbook (normalmente xl/workbook.xml)
        caminho_wb = u"xl/workbook.xml"
        for _id, tipo, alvo in _relacoes(entradas, u"_rels/.rels"):
            if tipo.endswith(u"/officeDocument"):
                caminho_wb = _resolver_alvo(u"", alvo)
                break
        pasta_wb = posixpath.dirname(caminho_wb)
        rels_wb = _relacoes(entradas, posixpath.join(
            pasta_wb, u"_rels", posixpath.basename(caminho_wb) + u".rels"))

        # 2) Primeira aba (ordem das abas = ordem dos <sheet> no workbook)
        wb = _ler_xml(entradas, caminho_wb)
        abas = wb.SelectNodes("//*[local-name()='sheets']/*[local-name()='sheet']")
        if abas.Count == 0:
            raise ErroExcel(u"A planilha não tem nenhuma aba.")
        rid = u""
        for atributo in abas[0].Attributes:
            if atributo.LocalName == "id" and "relationships" in atributo.NamespaceURI:
                rid = atributo.Value
        caminho_aba = None
        caminho_textos = posixpath.join(pasta_wb, u"sharedStrings.xml")
        caminho_estilos = posixpath.join(pasta_wb, u"styles.xml")
        for id_rel, tipo, alvo in rels_wb:
            if id_rel == rid:
                caminho_aba = _resolver_alvo(pasta_wb, alvo)
            elif tipo.endswith(u"/sharedStrings"):
                caminho_textos = _resolver_alvo(pasta_wb, alvo)
            elif tipo.endswith(u"/styles"):
                caminho_estilos = _resolver_alvo(pasta_wb, alvo)
        if not caminho_aba:
            caminho_aba = posixpath.join(pasta_wb, u"worksheets/sheet1.xml")

        # 3) Textos compartilhados e estilos (opcionais)
        compartilhadas = []
        xml_textos = _ler_xml(entradas, caminho_textos, obrigatorio=False)
        if xml_textos is not None:
            compartilhadas = [_texto_rico(si) for si in
                              xml_textos.SelectNodes("//*[local-name()='sst']/*[local-name()='si']")]
        larguras = _larguras_zeros(_ler_xml(entradas, caminho_estilos, obrigatorio=False))

        # 4) Linhas e células
        aba = _ler_xml(entradas, caminho_aba)
        linhas = []
        proxima_linha = 1
        for row in aba.SelectNodes("//*[local-name()='sheetData']/*[local-name()='row']"):
            r = row.GetAttribute("r")
            numero = int(r) if r.isdigit() else proxima_linha
            proxima_linha = numero + 1
            celulas = {}
            proxima_coluna = 1
            for c in _filhos(row, "c"):
                coluna = _indice_coluna(c.GetAttribute("r")) or proxima_coluna
                proxima_coluna = coluna + 1
                celulas[coluna] = _limpar(_valor_celula(c, compartilhadas, larguras))
            linhas.append((numero, celulas))
        return linhas

    except ErroExcel:
        raise
    except Exception as e:
        raise ErroExcel(u"Não foi possível ler a planilha.\n\nDetalhe: {}".format(mensagem_erro(e)))
    finally:
        if arquivo is not None:
            arquivo.Dispose()
        if fluxo is not None:
            fluxo.Close()


def planilha_para_linhas(caminho):
    """Lê o .xlsx e devolve as linhas no formato 'número | nome | carimbo'."""
    linhas = ler_primeira_aba(caminho)

    cabecalho = None
    for numero, celulas in linhas:
        if numero == 1:
            cabecalho = celulas
            break
    if not cabecalho or not any(cabecalho.values()):
        raise ErroExcel(u"A linha 1 da primeira aba está vazia.\n\n"
                        u"Ela deve ter os cabeçalhos Número, Nome e (opcional) Família.")

    # Acha as colunas pelo nome (primeira ocorrência vale)
    colunas = {}
    for indice in sorted(cabecalho):
        chave = normalizar(cabecalho[indice])
        if chave in (u"numero", u"nome", u"familia") and chave not in colunas:
            colunas[chave] = indice

    faltando = [rotulo for chave, rotulo in ((u"numero", u"Número"), (u"nome", u"Nome"))
                if chave not in colunas]
    if faltando:
        encontrados = u", ".join(u'"{}"'.format(cabecalho[i]) for i in sorted(cabecalho)
                                 if cabecalho[i]) or u"(nenhum)"
        raise ErroExcel(u"Coluna obrigatória não encontrada na linha 1: {}.\n\n"
                        u"Cabeçalhos encontrados: {}\n\nNada foi importado."
                        .format(u", ".join(faltando), encontrados))

    resultado = []
    for numero, celulas in sorted(linhas, key=lambda item: item[0]):
        if numero <= 1:
            continue
        num = celulas.get(colunas[u"numero"], u"")
        nome = celulas.get(colunas[u"nome"], u"")
        familia = celulas.get(colunas[u"familia"], u"") if u"familia" in colunas else u""
        if not (num or nome or familia):
            continue  # linha vazia
        partes = [num, nome] + ([familia] if familia else [])
        resultado.append(u" | ".join(partes))
    return resultado


# ---------------------------------------------------------------------------
# Carimbos (Title Blocks)
# ---------------------------------------------------------------------------
def nome_do_elemento(elemento):
    """Nome do tipo; contorna o problema do .Name no IronPython."""
    try:
        return elemento.Name
    except Exception:
        pass
    try:
        return DB.Element.Name.GetValue(elemento)
    except Exception:
        pass
    parametro = elemento.get_Parameter(DB.BuiltInParameter.SYMBOL_NAME_PARAM)
    return parametro.AsString() if parametro else u""


class CatalogoCarimbos(object):
    """Todos os tipos de carimbo do modelo e a lógica para achar um pelo texto."""

    def __init__(self, documento):
        itens = []
        coletor = (DB.FilteredElementCollector(documento)
                   .OfCategory(DB.BuiltInCategory.OST_TitleBlocks)
                   .WhereElementIsElementType())
        for simbolo in coletor:
            if not isinstance(simbolo, DB.FamilySymbol):
                continue
            familia = simbolo.FamilyName or u""
            tipo = nome_do_elemento(simbolo) or u""
            itens.append((u"{} : {}".format(familia, tipo), familia.strip(), tipo.strip(), simbolo))
        # Ordem alfabética sem diferenciar maiúsculas e acentos
        itens.sort(key=lambda i: (sem_acentos(i[0]).lower(), i[0]))

        self.rotulos = [i[0] for i in itens]
        self.por_rotulo = {}
        self.por_par = {}
        self.por_tipo = {}
        for rotulo, familia, tipo, simbolo in itens:
            self.por_rotulo[rotulo] = simbolo
            self.por_par[(familia, tipo)] = (rotulo, simbolo)
            self.por_tipo.setdefault(tipo, []).append((rotulo, simbolo))

    def resolver(self, texto):
        """Retorna (rotulo, simbolo, erro). Aceita 'Família : Tipo' ou só o tipo
        (se for único). Nunca troca pelo padrão sem avisar."""
        if u":" in texto:
            # Família e tipo não podem conter ':' no Revit, então dividir é seguro
            familia, tipo = texto.split(u":", 1)
            achado = self.por_par.get((familia.strip(), tipo.strip()))
            if achado:
                return achado[0], achado[1], None
            return None, None, u'Carimbo "{}" não existe no modelo.'.format(texto)

        candidatos = self.por_tipo.get(texto, [])
        if len(candidatos) == 1:
            return candidatos[0][0], candidatos[0][1], None
        if len(candidatos) > 1:
            return None, None, (u'Carimbo "{}" é ambíguo: esse tipo existe em {} famílias ({}). '
                                u'Use "Família : Tipo".'.format(
                                    texto, len(candidatos),
                                    u"; ".join(r for r, _s in candidatos)))
        return None, None, u'Carimbo "{}" não existe no modelo.'.format(texto)


# ---------------------------------------------------------------------------
# Validação (tudo antes de abrir a transação)
# ---------------------------------------------------------------------------
def numeros_existentes(documento):
    """{numero_minusculo: (numero_original, é_placeholder)} de todas as pranchas."""
    existentes = {}
    for folha in DB.FilteredElementCollector(documento).OfClass(DB.ViewSheet):
        numero = folha.SheetNumber or u""
        existentes[numero.strip().lower()] = (numero, folha.IsPlaceholder)
    return existentes


def caracteres_invalidos(texto):
    """Lista (sem repetir) dos caracteres proibidos presentes no texto."""
    achados = []
    for ch in texto:
        if ch in CARACTERES_PROIBIDOS and ch not in achados:
            achados.append(ch)
    return achados


def validar_lista(texto, rotulo_padrao, catalogo, existentes):
    """Interpreta cada linha da caixa de texto e devolve uma lista de registros.
    status None = válida, aguardando criação."""
    registros = []
    aceitos = {}  # numero_minusculo -> linha de origem da primeira ocorrência válida

    for indice, bruta in enumerate(texto.splitlines(), 1):
        linha = bruta.strip()
        if not linha:
            continue  # linhas em branco são ignoradas

        campos = [c.strip() for c in linha.split(u"|")]
        registro = {
            "linha": indice,
            "numero": campos[0] if campos else u"",
            "nome": campos[1] if len(campos) > 1 else u"",
            "carimbo": u"",
            "simbolo": None,
            "status": PULADA,
            "motivo": u"",
            "folha_id": None,
        }
        registros.append(registro)

        # Formato
        if len(campos) < 2 or len(campos) > 3:
            registro["motivo"] = (u'Fora do formato: esperado "número | nome | carimbo" '
                                  u'(2 ou 3 campos), encontrado(s) {}.'.format(len(campos)))
            continue

        numero, nome = campos[0], campos[1]
        carimbo_txt = campos[2] if len(campos) == 3 else u""
        registro["carimbo"] = carimbo_txt or rotulo_padrao

        # Campos vazios
        if not numero:
            registro["motivo"] = u"Número vazio."
            continue
        if not nome:
            registro["motivo"] = u"Nome vazio."
            continue

        # Caracteres que o Revit não aceita
        ruins = caracteres_invalidos(numero)
        if ruins:
            registro["motivo"] = u"Número com caractere não permitido: {}".format(u"  ".join(ruins))
            continue
        ruins = caracteres_invalidos(nome)
        if ruins:
            registro["motivo"] = u"Nome com caractere não permitido: {}".format(u"  ".join(ruins))
            continue

        # Número já existe no modelo (inclusive placeholder)
        chave = numero.lower()
        if chave in existentes:
            original, placeholder = existentes[chave]
            registro["motivo"] = u'Já existe {} com o número "{}" no modelo.'.format(
                u"uma prancha placeholder" if placeholder else u"uma prancha", original)
            continue

        # Número repetido na própria lista
        if chave in aceitos:
            registro["motivo"] = u"Número repetido na lista (já usado na linha {}).".format(aceitos[chave])
            continue

        # Carimbo
        if carimbo_txt:
            rotulo, simbolo, erro = catalogo.resolver(carimbo_txt)
            if erro:
                registro["motivo"] = erro
                continue
        else:
            rotulo, simbolo = rotulo_padrao, catalogo.por_rotulo[rotulo_padrao]

        registro["carimbo"] = rotulo
        registro["simbolo"] = simbolo
        registro["status"] = None
        aceitos[chave] = indice

    return registros


# ---------------------------------------------------------------------------
# Criação (uma única Transaction; uma SubTransaction por prancha)
# ---------------------------------------------------------------------------
def criar_pranchas(documento, registros):
    pendentes = [r for r in registros if r["status"] is None]
    if not pendentes:
        return  # nenhuma linha válida: não abre transação

    transacao = DB.Transaction(documento, NOME_TRANSACAO)
    transacao.Start()
    try:
        # Garante que os tipos de carimbo usados estão ativos
        ativou = False
        vistos = set()
        for r in pendentes:
            simbolo = r["simbolo"]
            if simbolo.UniqueId in vistos:
                continue
            vistos.add(simbolo.UniqueId)
            if not simbolo.IsActive:
                simbolo.Activate()
                ativou = True
        if ativou:
            documento.Regenerate()

        for r in pendentes:
            # A SubTransaction garante que uma prancha que falhou no meio
            # (ex.: criada mas sem conseguir definir o número) não fique no modelo
            sub = DB.SubTransaction(documento)
            sub.Start()
            try:
                folha = DB.ViewSheet.Create(documento, r["simbolo"].Id)
                folha.SheetNumber = r["numero"]
                folha.Name = r["nome"]
                sub.Commit()
                r["status"] = CRIADA
                r["folha_id"] = folha.Id
            except Exception as e:
                if sub.GetStatus() == DB.TransactionStatus.Started:
                    sub.RollBack()
                r["status"] = ERRO
                r["motivo"] = mensagem_erro(e)

        if any(r["status"] == CRIADA for r in pendentes):
            status = transacao.Commit()
            if status != DB.TransactionStatus.Committed:
                for r in pendentes:
                    if r["status"] == CRIADA:
                        r["status"] = ERRO
                        r["motivo"] = u"O Revit cancelou a transação ({}).".format(status)
                        r["folha_id"] = None
        else:
            transacao.RollBack()

    except Exception as e:
        if transacao.GetStatus() == DB.TransactionStatus.Started:
            transacao.RollBack()
        for r in pendentes:
            if r["status"] in (None, CRIADA):
                r["status"] = ERRO
                r["motivo"] = u"Transação desfeita: {}".format(mensagem_erro(e))
                r["folha_id"] = None


# ---------------------------------------------------------------------------
# Relatório na janela de saída do pyRevit
# ---------------------------------------------------------------------------
def mostrar_relatorio(registros):
    saida = script.get_output()
    criadas = sum(1 for r in registros if r["status"] == CRIADA)
    puladas = sum(1 for r in registros if r["status"] == PULADA)
    erros = sum(1 for r in registros if r["status"] == ERRO)

    saida.print_md(u"## Criar pranchas em lote")
    saida.print_md(u"**{} criada(s)** · **{} pulada(s)** · **{} com erro**".format(criadas, puladas, erros))
    if criadas:
        saida.print_md(u"Para desfazer tudo: Ctrl+Z (*{}*).".format(NOME_TRANSACAO))

    dados = []
    for r in registros:
        if r["status"] == CRIADA and r["folha_id"] is not None:
            numero = saida.linkify(r["folha_id"], title=r["numero"])
        else:
            numero = escapar(r["numero"])
        dados.append([
            u"{}".format(r["linha"]),
            numero,
            escapar(r["nome"]),
            escapar(r["carimbo"]),
            r["status"],
            escapar(r["motivo"]) or u"—",
        ])
    saida.print_table(
        table_data=dados,
        columns=[u"Linha de origem", u"Número", u"Nome", u"Carimbo", u"Status", u"Motivo"],
    )


# ---------------------------------------------------------------------------
# Janela
# ---------------------------------------------------------------------------
class JanelaPranchas(forms.WPFWindow):
    def __init__(self, arquivo_xaml, catalogo):
        forms.WPFWindow.__init__(self, arquivo_xaml)
        self.catalogo = catalogo
        self.resultado = None  # (texto, rotulo_padrao) quando clicar em Criar

        rotulos = List[str]()
        for rotulo in catalogo.rotulos:
            rotulos.Add(rotulo)
        self.cb_carimbo.ItemsSource = rotulos
        self.cb_carimbo.SelectedIndex = 0

        # Eventos ligados aqui (e não no XAML)
        self.bt_importar.Click += self.ao_importar
        self.bt_criar.Click += self.ao_criar
        self.bt_cancelar.Click += self.ao_cancelar
        self.tb_lista.Focus()

    def ao_importar(self, sender, args):
        caminho = forms.pick_file(files_filter=u"Planilhas do Excel (*.xlsx)|*.xlsx")
        if not caminho:
            return
        try:
            linhas = planilha_para_linhas(caminho)
        except ErroExcel as e:
            forms.alert(mensagem_erro(e), title=u"Importar do Excel")
            return
        except Exception as e:
            forms.alert(u"Não foi possível ler a planilha.\n\nDetalhe: {}".format(mensagem_erro(e)),
                        title=u"Importar do Excel")
            return
        if not linhas:
            forms.alert(u"A planilha não tem nenhuma linha com dados abaixo do cabeçalho.\n"
                        u"A lista não foi alterada.", title=u"Importar do Excel")
            return
        self.tb_lista.Text = Environment.NewLine.join(linhas)
        self.tx_status.Text = u"{} linha(s) importada(s) de {}. Revise antes de criar.".format(
            len(linhas), os.path.basename(caminho))

    def ao_criar(self, sender, args):
        texto = self.tb_lista.Text or u""
        if not texto.strip():
            forms.alert(u"A lista está vazia. Digite uma prancha por linha ou importe do Excel.",
                        title=u"Criar pranchas")
            return
        self.resultado = (texto, self.cb_carimbo.SelectedItem)
        self.Close()

    def ao_cancelar(self, sender, args):
        self.Close()


# ---------------------------------------------------------------------------
# Execução
# ---------------------------------------------------------------------------
def main():
    documento = revit.doc
    if documento is None or documento.IsFamilyDocument:
        forms.alert(u"Abra um modelo de projeto para criar pranchas.", exitscript=True)

    catalogo = CatalogoCarimbos(documento)
    if not catalogo.rotulos:
        forms.alert(u"Este modelo não tem nenhum carimbo (Title Block) carregado.\n\n"
                    u"Carregue uma família de carimbo e tente de novo.",
                    title=u"Criar pranchas", exitscript=True)

    janela = JanelaPranchas(ARQUIVO_XAML, catalogo)
    janela.ShowDialog()
    if not janela.resultado:
        return  # cancelado

    texto, rotulo_padrao = janela.resultado
    registros = validar_lista(texto, rotulo_padrao, catalogo, numeros_existentes(documento))
    if not registros:
        forms.alert(u"Nenhuma linha para processar.", title=u"Criar pranchas")
        return

    criar_pranchas(documento, registros)
    mostrar_relatorio(registros)


if __name__ == "__main__":
    main()
