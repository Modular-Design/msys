from pyvis.network import Network
import networkx as nx
import random


def get_alpha(g):
    gewichtl = []
    for v in g.nodes:
        gewicht = 0
        for e in g.edges(v):
            gewicht += g.edges[e]['weight']
        gewichtl += [gewicht]
    alpha = max(gewichtl)
    return alpha
#
#
# def createNeighweights(g):
#     for n in g.nodes:
#         for e in g.edges(activenodeid):
#             if e[0] == activenodeid:
#                 neighbor = e[1]
#             else:
#                 neighbor = e[0]
#             neighweights[neighbor] = g.edges[e]['weight'] / alpha
#         # now choose which node to go
#         chosennodeid = activenodeid



def LERW(g, alpha, start, sinks, q=0):
    activenodeid = start
    # Jetzt starte Skelettprozess
    trajectory = [start]
    while True:
        r = random.random()
        if r > 1 - q / (alpha+q):
            #print('Breche ab mit Trajektorie: ', end='')
            #print(trajectory)

            return trajectory
        chosennodeid=activenodeid
        #print("##########")
        #print(activenodeid)
        #print(g[activenodeid])
        temp=0
        for nbr in g[activenodeid]:
            #print("activenodeid",activenodeid,"->",nbr)
            temp += g[activenodeid][nbr]['weight']
            #print("r",r)
            #print("temp",temp)
            #print("temp/(alpha+q)",temp/(alpha+q))
            if r < temp/(alpha+q):
                chosennodeid = nbr
                #print(nbr)

                break
        if chosennodeid in sinks:
            trajectory += [chosennodeid]

            #print('In folgende Senke gelaufen',end='')
            #print(chosennodeid)
            #print(trajectory)
            return trajectory
        # print(trajectory)
        # if chosennodeid == activenodeid:
        #     print('Auf Stelle geblieben')
        # else:
        #     print('Neuer Knoten ist ', end='')
        #     print(chosennodeid)

        if chosennodeid in trajectory:
            while chosennodeid in trajectory:
                trajectory.pop()
            trajectory += [chosennodeid]
            activenodeid = chosennodeid
        else:
            trajectory += [chosennodeid]
            activenodeid = chosennodeid
            # print('trajectory grows')
        # print('Jetzt aktiver Knoten ist:',activenodeid)


# print(g.edges)
# print(g.nodes)
# liste = LERW(g, 10, '2,3', ['2,6', '4,2'], q=.1)
# print(liste)
#

# liste = LERW(h, 3, sinks=[0], q=0)
# print(liste)
# print(h.get_node('delta'))
# print(h.get_nodes())

def wilson(g, sinks, q=0):

    # Graph vorbereiten, auf Standardwerte setzen
    # g.show_buttons()
    alpha = get_alpha(g)
    for v in g.nodes:
        g.nodes[v]['color'] = 'red'
    for v in sinks:
        g.nodes[v]['color'] = 'black'
    sinks = set(sinks)
    activenodes = (set(g.nodes) - sinks)
    # print(activenodes)
    for e in g.edges:
        g.edges[e]['hidden'] = True
    counter = 0
    edgelist = []
    while bool(activenodes):
        counter += 1
        # choose a random/arbitrary vertex and start a LERW (doesn't have to be RANDOM RANDOM)

        #start = random.choice(list(activenodes))
        start=next(iter(activenodes))
        # print('start= ', start)

        path = LERW(g, alpha, start, sinks, q)
        # print('path', path)
        for v in path[:-1]:
            g.nodes[v]['color'] = 'navy'
        if g.nodes[(path[-1])]['color'] in ['navy', 'green']:
            g.nodes[(path[-1])]['color'] = 'green'
        else:
            g.nodes[(path[-1])]['color'] = 'yellow'

        for e in g.edges:
            for i in range(len(path) - 1):
                if (e[0] == path[i] and e[1] == path[i + 1]) or (
                        e[0] == path[i + 1] and e[1] == path[i]):
                    g.edges[e]['hidden'] = False
                    # e['from'] = path[i]
                    # e['to'] = path[i + 1]
                    edgelist += [e]
        # print('sinks')
        # print(sinks)
        sinks.update(path)
        # print(sinks)
        # print('activenodes', activenodes, end=' -> ')
        activenodes = activenodes - sinks
        # print(activenodes)
        # print('counter = ', counter)
        # name = 'wilson' + str(counter) + '.html'
        # g.show(name)
    print("counter=",counter)
    return edgelist

