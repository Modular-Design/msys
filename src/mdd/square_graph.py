from .wilson import WilsonGraph

class SquareWilson(WilsonGraph):
    def __init__(self, n: int):
        super().__init__()
        zeilen = n
        spalten = n
        for i in range(zeilen):
            for j in range(spalten):
                self.add_node(str(i) + ',' + str(j), x=60 * i, y=70 * j)

        for i in range(zeilen - 1):
            for j in range(spalten - 1):
                self.add_edge(str(i) + ',' + str(j), str(i + 1) + ',' + str(j), weight=1)
                self.add_edge(str(i) + ',' + str(j), str(i) + ',' + str(j + 1), weight=1)
