import networkx as nx
from wilson import *
#import Wilson2
import pyvis
import time
# import pytest

#Hier teste ich, wie lange der Algorithmus braucht... z.B. Wilson.py vs Wilson2.py
#Das Einzige, was da anders ist, ist der LERW (siehe Kommentare in Wilson.py)

#Hinweis: Wenn du ihn auch auf anderen Graphen testen möchtest, bietet networkx eine Menge Lösungen an.
#Um den Graph zu visualisieren, nutze ich pyvis. Das ist aber eigentlich unnötig, man könnte es auch anders machen


wilson_graph = SquareWilson(50)

temp = time.time()
for _ in range(4):
    wilson_graph.wilson(['2,4'], 1)
temp = time.time()-temp
print(temp)
h = pyvis.network.Network('1000px', '1000px')
h.from_nx(wilson_graph)
h.show_buttons()
h.toggle_physics(False)
h.show('h.html')


# g=Wilson.create_nx_graph(30)
# h2=pyvis.network.Network('1000px', "1000px")
# h2.from_nx(g)
# h2.show_buttons()
# h2.toggle_physics(False)
# h2.show('h_unveraendert.html')