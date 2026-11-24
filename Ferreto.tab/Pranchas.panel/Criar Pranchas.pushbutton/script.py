# -*- coding: utf-8 -*-
"""Cria varias pranchas de uma vez: escolha a familia de prancha e
digite (ou importe do Excel) o numero e o nome de cada uma."""

import os
from pyrevit import revit, DB, forms, script

doc = revit.doc
out = script.get_output()


def carimbos():
    tipos = DB.FilteredElementCollector(doc) \
        .OfCategory(DB.BuiltInCategory.OST_TitleBlocks) \
        .WhereElementIsElementType().ToElements()
    res = {}
    for t in tipos:
        nome = "{}: {}".format(t.FamilyName, t.get_Parameter(DB.BuiltInParameter.SYMBOL_NAME_PARAM).AsString())
        res[nome] = t
    return res


def ler_excel(caminho):
    import xlrd
    livro = xlrd.open_workbook(caminho)
    aba = livro.sheet_by_index(0)
    linhas = []
    for i in range(1, aba.nrows):
        vals = [aba.cell_value(i, c) for c in range(aba.ncols)]
        num = vals[0]
        if isinstance(num, float) and num.is_integer():
            num = str(int(num)).zfill(2)
        num = str(num).strip()
        nome = (u"{}".format(vals[1]).strip() if len(vals) > 1 else u"")
        familia = (u"{}".format(vals[2]).strip() if len(vals) > 2 else u"")
        if num:
            linhas.append((num, nome, familia))
    return linhas


class Janela(forms.WPFWindow):
    def __init__(self):
        forms.WPFWindow.__init__(self, os.path.join(os.path.dirname(__file__), "janela.xaml"))
        self.tipos = carimbos()
        self.cb_familia.ItemsSource = sorted(self.tipos.keys())
        if self.tipos:
            self.cb_familia.SelectedIndex = 0
        self.linhas = None

    def importar_excel(self, sender, args):
        caminho = forms.pick_file(file_ext="xlsx")
        if not caminho:
            return
        self.linhas = ler_excel(caminho)
        self.tb_lista.Text = u"\n".join(
            u"{} | {}".format(n, nm) + (u" | {}".format(f) if f else u"")
            for n, nm, f in self.linhas)

    def criar(self, sender, args):
        self.linhas = []
        for linha in self.tb_lista.Text.splitlines():
            partes = [p.strip() for p in linha.split("|")]
            if partes and partes[0]:
                self.linhas.append((partes[0],
                                    partes[1] if len(partes) > 1 else u"",
                                    partes[2] if len(partes) > 2 else u""))
        self.padrao = self.cb_familia.SelectedItem
        self.Close()

    def cancelar(self, sender, args):
        self.linhas = None
        self.Close()


j = Janela()
j.ShowDialog()

if j.linhas:
    existentes = set(s.SheetNumber for s in DB.FilteredElementCollector(doc).OfClass(DB.ViewSheet))
    criadas, avisos = [], []
    with revit.Transaction("Criar pranchas em lote"):
        for num, nome, familia in j.linhas:
            if num in existentes:
                avisos.append(u"{}: número já existe, pulei.".format(num))
                continue
            chave = familia or j.padrao
            tipo = j.tipos.get(chave) or next(
                (t for k, t in j.tipos.items() if k.startswith(chave + ":")), None)
            if tipo is None:
                avisos.append(u"{}: família '{}' não encontrada, pulei.".format(num, chave))
                continue
            folha = DB.ViewSheet.Create(doc, tipo.Id)
            folha.SheetNumber = num
            if nome:
                folha.Name = nome
            existentes.add(num)
            criadas.append([num, nome, chave])
    out.print_md(u"### {} pranchas criadas".format(len(criadas)))
    if criadas:
        out.print_table(criadas, columns=[u"Número", u"Nome", u"Família"])
    for a in avisos:
        out.print_md(u"- " + a)
