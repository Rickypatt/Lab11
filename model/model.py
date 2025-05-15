import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._prodotti = DAO.getAllProdotti()
        self._idMap = {}
        for p in self._prodotti:
            self._idMap[p.Product_number] = p
        self.edges = []

    def buildGraph(self,colore,anno):
        self._graph.clear()
        nodes = DAO.getNodes(colore, self._idMap)
        self._graph.add_nodes_from(nodes)
        self.addArchi(colore,anno)

    def addArchi(self,colore,anno):
        self.edges = DAO.getEdges(colore,anno, self._idMap)
        for e in self.edges:
            if self._graph.has_node(e[0]) and self._graph.has_node(e[1]):
                self._graph.add_edge(e[0], e[1], weight=e[2])


    def getYears(self):
        return DAO.getAllYears()

    def getColors(self):
        return DAO.getAllColors()

    def getNumNodi(self):
        return self._graph.number_of_nodes()

    def getNumArchi(self):
        return self._graph.number_of_edges()

    def getBestSolution(self, source):
        self._bestPath = []
        parziale = [source]
        self.ricorsione(parziale, list(self._graph.neighbors(source)))
        return self._bestPath

    def ricorsione(self, parziale, successori):  # successori è la lista di nodi successori ammissibili
        if len(successori) == 0:
            if len(self._bestPath) < len(parziale):
                self._bestPath = copy.deepcopy(parziale)
                # print(self._bestPath)
        else:
            for n in successori:
                parziale.append(n)
                successoriAmmissibili = self.getSuccessoriAmmissibili(parziale, n)
                self.ricorsione(parziale, successoriAmmissibili)
                parziale.pop()

    def getSuccessoriAmmissibili(self, parziale, source):
        ammissibili = []
        pesoUltimo = self._graph[parziale[-2]][parziale[-1]]["weight"]  # prendo il peso dell'ultimo arco
        for node in list(self._graph.neighbors(source)):
            if self.checkArchi(parziale, node):
                pesoNuovo = self._graph[parziale[-1]][node]["weight"]  # prendo il peso dell'arco che voglio aggiungere
                if pesoNuovo >= pesoUltimo:
                    ammissibili.append(node)
        return ammissibili

    def checkArchi(self, parziale, nodo):
        for i in range(0, len(parziale) - 1):
            nodo1 = parziale[i]
            nodo2 = parziale[i + 1]
            if (nodo1, nodo2) == (parziale[-1], nodo) or (nodo2, nodo1) == (parziale[-1], nodo):
                return False
        return True

