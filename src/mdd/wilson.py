# from pyvis.network import Network
import networkx as nx
import random
from time import time


class WilsonGraph(nx.Graph):
    def __init__(self):
        super().__init__()

    def get_alpha(self):
        """
        get the maximal weight of g:
        alpha=max over all vertices x in g: w(x)
        w(x)=sum over all vertices y in g (without x of course): w(x,y)
        where w(x,y) is the weight of edge x->y
        """
        # möglicherweise Parallelisierbar
        temp = time()
        gewichtl = []
        for v in self.nodes:
            gewicht = 0
            for e in self.edges(v):
                gewicht += self.edges[e]['weight']
            gewichtl += [gewicht]
        alpha = max(gewichtl)
        #print('alpha', time()-temp)
        return alpha

    def LERW(self, alpha: float, start, sinks, q=0):
        """Loop erased random walk: returns a LERW started in start, that is killed with q-exponential rate or if it
        walks into a sink vertex """
        temp_time = time()
        activenodeid = start
        # Jetzt starte Skelettprozess (=Irrfahrt/random walk in diskreter Zeit)
        trajectory = [start]
        neighweights = {}
        # Starte Irrfahrt:
        # Die Idee ist: Wir werden eine Zufallszahl in (0,1) erzeugen und dann eine der folgenden
        # Aktionen machen:
        # 1. Wir gehen zu einem Nachbarn, und zwar umso wahrscheinlicher, je größer das Kantengewicht ist
        # 2. Wir killen den LERW (mit Rate q, dh umso wahrscheinlicher, je größer q)
        # 3. Wir bleiben stehen

        while True:

            for e in self.edges(activenodeid):
                if e[0] == activenodeid:
                    neighbor = e[1]
                else:
                    neighbor = e[0]
                neighweights[neighbor] = self.edges[e]['weight'] / (alpha+q)
            # now choose which node to go
            chosennodeid = activenodeid
            temp = 0
            r = random.random()
            for n in neighweights: # Here we might go to one of the neighbours
                temp += neighweights[n]
                if r < temp:
                    chosennodeid = n
                    break
            if r > 1 - q / (alpha+q): # LERW gekillt, weil Lebenszeit (q-exponentialverteilt) vorbei
                #print('LERW1', time() - temp_time)
                return trajectory
            if chosennodeid in sinks: # LERW gekillt, weil in Senke gelaufen
                trajectory += [chosennodeid]
                #print('LERW2', time() - temp_time)
                return trajectory

            # Hier überprüfen wir, ob die Irrfahrt keine Schlaufen hat, falls ja: Neuer Knoten wird Trajektorie hinzugefügt,
            # falls nein: entstandene Schlaufe wird gelöscht
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
            neighweights = {}

    # DAS HAUPTPROBLEM SCHEINT NEIGHWEIGHTS ZU SEIN, ICH BERECHNE GLAUBE ICH STÄNDIG DASSELBE WIEDER, DAS KÖNNTE MAN EINMAL MACHEN UND DANN LASSEN
    #PS: Ist aber nicht so, ich habe dasselbe in Wilson2 gemacht, ohne immer wieder neighweights zu erstellen und es ist nicht besser...

    def wilson(self, sinks, q=0):
        """Applies Wilson's Algorithm to a given graph with given sinks and killing rate q
        Wilson's Algorithm outputs a random forest obeying a specific distribution

        returns a graph where roots of the forest are yellow/black and vertices, that are no roots are navy/green"""
        temp_time = time()
        # Graph vorbereiten, auf Standardwerte setzen
        alpha = self.get_alpha()
        for v in self.nodes:
            self.nodes[v]['color'] = 'red'
        for v in sinks:
            self.nodes[v]['color'] = 'black'
        sinks = set(sinks)
        activenodes = (set(self.nodes) - sinks)
        # print(activenodes)
        for e in self.edges:
            self.edges[e]['hidden'] = True
        counter = 0

        edges_that_form_the_spanning_forest = []
        temp_time1 = 0
        while bool(activenodes):
            counter += 1
            # choose a random vertex and start a LERW
            # MUSS NICHT WIRKLICH ZUFÄLLIG SEIN, ABER WENN MAN STATT RANDOM:CHOICE EINFACH NEXT(ITER(...)) NIMMT WIRD ES AUCH NICHT WIRKLICH SCHNELLER
            start = random.choice(list(activenodes))
            # print('start= ', start)

            path = self.LERW(alpha, start, sinks, q)
            # Färbe nun alle Knoten nach folgendem Schema:
            # Wurzeln werden gelb gefärbt
            # Nichtwurzeln werden navy gefärbt
            # Falls wir in eine Nichtwurzel laufen, färben wir grün
            temp = time()
            for v in path[:-1]:
                self.nodes[v]['color'] = 'navy'
            if self.nodes[(path[-1])]['color'] in ['navy', 'green']:
                self.nodes[(path[-1])]['color'] = 'green'
            else:
                self.nodes[(path[-1])]['color'] = 'yellow'

            for i in range(len(path)-1):
                if self.edges[path[i],path[i+1]]:
                    self.edges[path[i],path[i+1]]['hidden']=False
                else:
                    self.edges[path[i+1], path[i]]['hidden'] = False
            # for e in self.edges:
            #     for i in range(len(path) - 1):
            #         if (e[0] == path[i] and e[1] == path[i + 1]) or (
            #                 e[0] == path[i + 1] and e[1] == path[i]):
            #             self.edges[path[i][path[i+1]]['hidden'] = False
            #             # e['from'] = path[i]
            #             # e['to'] = path[i + 1]
            #             edges_that_form_the_spanning_forest += [e]
            temp_time1 += time() - temp
            # Vertices of the path are now also sinks, since they belong to the constructed random forest
            sinks.update(path)
            activenodes = activenodes - sinks

        print('counter=', counter)
        print('wison_graphic', temp_time1)
        wilson_time = time() - temp_time
        print('wison_without_graphics', wilson_time - temp_time1)
        print('wison', wilson_time)
        return edges_that_form_the_spanning_forest

    def get_edgedistribution(self, sinks, q=0, samplesize=1000):
        """Habe ich vor Urzeiten geschrieben, nicht wirklich wichtig...
        tells us how often each edge is in the random spanning forest """
        print('Jetzt sind wir in der Funktion')
        for e in self.get_edges():
            e['value'] = 0
        for v in self.get_nodes():
            self.nodes[self.get_nodes().index(v)]['value'] = 0
        for i in range(samplesize):
            edgelist = self.wilson(self, sinks, q)
            for e in edgelist:
                e['value'] += 1
            for v in self.get_nodes():
                if self.get_node(v)['color'] == 'yellow':
                    self.get_node(v)['value'] += 1

    def color_leaves(self):
        """
        Vor Urzeiten geschrieben, nicht wichtig
        Colors leaves of a given forest (leaves=edges with exactly one outgoing edge (oriented towords the root)"""
        for v in self.get_nodes():
            temp = 0
            isleaf = True
            for e in self.get_edges():
                if (e['to'] == v or e['from'] == v) and e['hidden'] == False:
                    temp += 1
                    if temp == 2:
                        isleaf = False
                        break
            if isleaf:
                if self.get_node(v)['color'] == 'yellow':
                    pass
                else:
                    self.get_node(v)['color'] = 'red'
