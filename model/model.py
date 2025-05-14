import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._prodotti = DAO.getAllProdotti()
        self._idMap = {}
        for p in self._prodotti:
            self._idMap[p.Product_number] = p

    def buildGraph(self,colore,anno):
        nodes = DAO.getNodes(colore, self._idMap)
        self._graph.add_nodes_from(nodes)
        print(self._graph.nodes)
        self.addArchi(anno)
        print(self._graph.number_of_nodes())

    def addArchi(self,anno):
        edges = DAO.getEdges(anno, self._idMap)
        for e in edges:
            if e[0] in self._graph and e[1] in self._graph:
                if self._graph.has_edge(e[0],e[1]):
                    self._graph[e[0]][e[1]]["weight"] += 1
                else:
                    self._graph.add_edge(e[0],e[1], weight = 1)


    def getYears(self):
        return DAO.getAllYears()

    def getColors(self):
        return DAO.getAllColors()

    def getNumNodi(self):
        return self._graph.number_of_nodes()

    def getNumArchi(self):
        return self._graph.number_of_edges()


