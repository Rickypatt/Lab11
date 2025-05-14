import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []

    def fillDDAnno(self):
        self._listYear = self._model.getYears()
        for y in self._listYear:
            self._view._ddyear.options.append(ft.dropdown.Option(y))
        self._view.update_page()

    def fillDDColore(self):
        self._listColor = self._model.getColors()
        self._listColor.sort()
        for c in self._listColor:
            self._view._ddcolor.options.append(ft.dropdown.Option(c))
        self._view.update_page()


    def handle_graph(self, e):
        colore = self._view._ddcolor.value
        anno = self._view._ddyear.value

        if colore is None:
            self._view.txtOut.controls.clear()
            self._view.txtOut.controls.append(ft.Text("Attenzione! Non hai selezionato un colore"))
            self._view.update_page()
            return
        if anno is None:
            self._view.txtOut.controls.clear()
            self._view.txtOut.controls.append(ft.Text("Attenzione! Non hai selezionato un anno"))
            self._view.update_page()
            return

        self._model.buildGraph(colore,anno)
        self._view.txtOut.controls.clear()
        self._view.txtOut.controls.append(ft.Text("Grafo creato correttamente!"))
        self._view.txtOut.controls.append(ft.Text(f"N nodi: {self._model.getNumNodi}, N vertici: {self._model.getNumArchi}"))
        self._view.update_page()








    def fillDDProduct(self):
        pass


    def handle_search(self, e):
        pass
