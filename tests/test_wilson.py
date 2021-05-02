import time

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from pyvis.network import Network

# import Wilson
# import Wilson2
# 
# 
# # Nicht anschauen, ist nur Schrott, führe test2.py aus
# 
# def laufzeitenanalyse():
#     narray = [2 * x + 6 for x in range(30)]
#     laufzeitenbuild = []
#     laufzeitenwilson = []
#     for n in narray:
#         print('Sind bei n=', n)
#         laufzeitbuild = 0
#         laufzeitwilson = 0
#         for _ in range(5):
#             temp = time.time()
#             g = Wilson.create_nx_graph(n)
#             print('Bauzeit: ', time.time() - temp)
#             laufzeitbuild += time.time() - temp
#             temp = time.time()
#             Wilson2.wilson(g, ['2,4'], .02)
#             laufzeitwilson += time.time() - temp
#             print('Wilsonzeit: ', time.time() - temp)
#         laufzeitenbuild.append(laufzeitbuild)
#         laufzeitenwilson.append(laufzeitwilson)
#     print('n=', narray)
#     print('wilson', laufzeitenwilson)
#     print('build', laufzeitenbuild)
#     laufzeitenbuild = [x ** .25 for x in laufzeitenbuild]
#     laufzeitenwilson = [x ** .25 for x in laufzeitenwilson]
#     # plt.plot(narray, laufzeitenwilson, label='wilson')
#     plt.plot(narray, laufzeitenwilson, label='4th root (wilson)')
# 
#     # plt.plot(narray, laufzeitenbuild, label='build')
#     plt.plot(narray, laufzeitenbuild, label='4th root (build)')
#     plt.legend()
#     plt.show()
# 
#     # Wilson.color_leaves(g)
#     # g.show('g.html')
# 
# 
# def haeufigkeitsanalyse():
#     N = 7
#     st = nx.star_graph(N)
#     st.add_edge(2, 4)
#     st.add_edge(3, 4)
#     st.add_edge(1, 7)
#     for xx, yy in st.edges:
#         st[xx][yy]['weight'] = 1.
#     temp = np.zeros(N + 1)
#     for i in range(60000):
#         Wilson2.wilson(st, [], .1)
#         anzahlwurzeln = 0
#         for n in st.nodes:
#             if st.nodes[n]['color'] == 'yellow':
#                 anzahlwurzeln += 1
#         if anzahlwurzeln == 1:
#             for n in st.nodes:
#                 if st.nodes[n]['color'] == 'yellow':
#                     temp[n] += 1
#     print(temp)
#     nt2 = Network()
#     nt2.from_nx(st)
#     nt2.show('star.html')
