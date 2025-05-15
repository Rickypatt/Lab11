import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self.choiceDDProduct = None
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
        self._view.txtOut.controls.append(ft.Text(f"N nodi: {self._model.getNumNodi()}, N vertici: {self._model.getNumArchi()}"))

        for e in self._model.edges[:3]:
            self._view.txtOut.controls.append(
                ft.Text(f"Arco da {e[0].Product_number} a {e[1].Product_number}, peso={e[2]}"))

        self._view.txtOut.controls.append(
            ft.Text(f"I nodi ripetuti sono {self.getArchiRipetuti()}"))

        self.fillDDProduct()
        self._view.update_page()

    def getArchiRipetuti(self):
        count = {}
        for e in self._model.edges[:3]:
            p1,p2,peso = e

            if p1 in count:
                count[p1] += 1
            else:
                count[p1] = 1

            if p2 in count:
                count[p2] += 1
            else:
                count[p2] = 1

        rep = []

        for p in count:
            if count[p] > 1:
                rep.append(p.Product_number)

        return rep

    def fillDDProduct(self):
        nodes = self._model._graph.nodes
        for n in nodes:
            self._view._ddnode.options.append(
                ft.dropdown.Option(key=n.Product_number, data=n, on_click=self.readDDProduct))
        self._view.update_page()
        return

    def readDDProduct(self, e):
        self.choiceDDProduct = e.control.data

    def handle_search(self, e):
        if self.choiceDDProduct is None:
            self._view.create_alert("Selezionare un prodotto")
            self._view.update_page()
            return
        path = self._model.getBestSolution(self.choiceDDProduct)
        self._view.txtOut2.controls.clear()
        self._view.txtOut2.controls.append(ft.Text(
            f"Numero archi percorso più lungo: {len(path) - 1}"))  # perchè path mi restituisce il percorso con i nodi, io voglio gli archi che sono il numero di nodi -1
        self._view.update_page()
        return



