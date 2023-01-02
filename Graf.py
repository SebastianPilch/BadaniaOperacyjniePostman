import random

class Edge:
    def __init__(self, Paczkomat1, Paczkomat2, edge=1):
        self.Paczkomat_out_ = Paczkomat1
        self.Paczkomat_in_ = Paczkomat2
        self.time_ = edge

    def __eq__(self, other):
        if (self.Paczkomat_in_ == other.Paczkomat_in_) and (self.Paczkomat_out_ == other.Paczkomat_out_):
            return True
        else:
            return False

    def __lt__(self, other):
        return True if self.time_ < other.time_ else False

    def __gt__(self, other):
        return True if self.time_ > other.time_ else False

    def __le__(self, other):
        return True if self.time_ <= other.time_ else False

    def __ge__(self, other):
        return True if self.time_ >= other.time_ else False

    def __str__(self):
        return '{' + str(self.Paczkomat_out_) + '->' + str(self.Paczkomat_in_) + ',' + str(self.time_) + '}'


class MapaPolaczen:
    def __init__(self):
        self.PaczkomatList = []
        self.Dict_ = {}
        self.PaczkomatDict = {}

    def __str__(self):
        str_mat = '------GRAPH------,' + str(self.order()) + '\n'
        for i in self.Dict_.keys():
            str_mat += '[' + str(i) + ': '
            for j in range(len(self.Dict_[i])):
                str_mat += str(self.Dict_[i][j])
                if j != len(self.Dict_[i]) - 1:
                    str_mat += ',  '
            str_mat += ']\n'
        return str_mat + '-------------------'

    def InsertPaczkomat(self, vertex):
        """
        Dodawanie poaczkomatu
        """
        self.PaczkomatDict[vertex] = self.order()
        self.Dict_[vertex] = []
        self.PaczkomatList.append(vertex)

    def InsertEdges(self, vertex1, vertex2, edge):
        """
        Dodawanie krawędzi
        """
        idx_1 = self.getPaczkomatIdx(vertex1)
        idx_2 = self.getPaczkomatIdx(vertex2)
        self.Dict_[vertex1].append(Edge(self.getPaczkomat(idx_1), self.getPaczkomat(idx_2), edge))

    def deletePaczkomat(self, vertex):
        """
        Usuwanie paczkomatu z grafu
        """
        v_id = self.getPaczkomatIdx(vertex)
        del self.Dict_[vertex]
        self.PaczkomatList.remove(vertex)
        del self.PaczkomatDict[vertex]
        for i in self.PaczkomatDict.keys():
            if self.PaczkomatDict[i] > v_id:
                self.PaczkomatDict[i] -= 1
            for j in range(len(self.Dict_[i])):
                if self.Dict_[i][j].Paczkomat_in_ == vertex:
                    del self.Dict_[i][j]
                    break

    def deleteEdge(self, vertex1, vertex2):
        """
        Usuwanie krawędzi z grafu
        """
        edge = Edge(vertex1, vertex2, None)
        for i in range(len(self.Dict_[vertex1])):
            if self.Dict_[vertex1][i] == edge:
                del self.Dict_[vertex1][i]
                break

    def getPaczkomatIdx(self, vertex):
        """
        Zwraca id paczkomatu po nazwie
        """
        return self.PaczkomatDict[vertex]

    def getPaczkomat(self, vertex_id):
        """
        Zwraca nazwę paczkomatu po id
        """
        return self.PaczkomatList[vertex_id]

    def neighbours(self, vertex_id):
        """
        Zwraca sąsiadów paczkomatu w formie paczkomatów
        """
        neighbours = []
        vertex = self.getPaczkomat(vertex_id)
        for i in self.Dict_.keys():
            for edge in self.Dict_[i]:
                if edge.Paczkomat_in_ == vertex and edge.Paczkomat_out_ not in neighbours:
                    neighbours.append(edge.Paczkomat_out_)
                if edge.Paczkomat_out_ == vertex and edge.Paczkomat_in_ not in neighbours:
                    neighbours.append(edge.Paczkomat_in_)
        return neighbours

    def size(self):
        """
        Liczba wzystkich ścieżek między paczkomatami
        """
        return len(self.edges())

    def order(self):
        """
        Wymiar grafu, liczba wszystkich paczkomatów
        """
        return len(self.PaczkomatList)

    def edges(self):
        """
        zwraca listę krawędzi
        """
        lst = []
        for i in self.Dict_.keys():
            for j in range(len(self.Dict_[i])):
                lst.append(self.Dict_[i][j])
        return lst


def UtworzMape(ListaAdresow, min_odleglosc, max_oleglosc):
    """ Utworzenie grafu """
    Mapa = MapaPolaczen()
    for i in ListaAdresow:
        Mapa.InsertPaczkomat(i)
    visited = []
    for i in ListaAdresow:
        visited.append(i)
        for j in ListaAdresow:
            if i != j and j not in visited:
                r = random.randint(min_odleglosc, max_oleglosc)
                Mapa.InsertEdges(i, j, r)
                Mapa.InsertEdges(j, i, r)
    return Mapa

