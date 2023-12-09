import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mpl
import networkx as nx
from itertools import combinations
class Rocnik():
    def __init__(self, rocnik, zaci):
        self.rocnik = rocnik # jaky rocnik to je
        self.zaci = zaci # kteri zaci tam chodi
    def udelej_graf(seminare, id_seminaru, kam_seminar):
        # tvorba neorientovaného grafu, kde vrcholy jsou semináře
        # semináře budou spojeny hranou, pokud sdílí žáka nebo učitele
        # hrany jsou ohodnocené: žák má hodnotu 1, učitel má hodnotu 100
        P = nx.MultiGraph() # multigraf = má mezi dvojicí vrcholů víc než dvě hrany
        P.add_nodes_from(id_seminaru) # každý vrchol je jeden seminář (resp. id semináře)

        ### učitelské hrany
        for x in seminare.keys(): # pro každého profesora
            vrcholy = seminare[x] # množina seminářů profesora
            hrany = combinations(vrcholy, 2) # všechny možné dvojice seminářů v množině 
            P.add_edges_from(hrany, weight = 100) # pro každou dvojici udělá hranu o hodnotě 100 (úplný graf)
        
        ### žákovské hrany
        for x in kam_seminar.keys(): # pro každý prvek z množiny seminářů u jednoho žáka
            vrcholy = kam_seminar[x] # množina seminářů žáka
            hrany = combinations(vrcholy, 2) # všechny možné dvojice seminářů v množině 
            P.add_edges_from(hrany, weight = 1) # pro každou dvojici udělá hranu o hodnotě 1 (úplný graf)

        # graf se součtem hodnot hran z P
        # udělá s multigrafu P normální ohodnocený graf
        G = nx.Graph()
        for u, v, data in P.edges(data=True): # pro všechny vrcholy
            if G.has_edge(u, v): # pokud hrana existuje
                G[u][v]['weight'] += data['weight'] # přidám k váze hrany
            else:
                G.add_edge(u, v, weight=data['weight']) # pokud hrana neexistuje, vytvořím ji
        # tisknu graf na textový výstup - není nutné
        #for u, v, data in G.edges(data=True):
        #    weight = data['weight']
        #    print(f"hrana: ({u}, {v}), hodnota: {weight}")
            

        # vizualizace grafu
        pos = nx.spring_layout(G) # rozmístění vrcholů a hran
        nx.draw_networkx_nodes(G, pos) # nakreslím vrcholy
        nx.draw_networkx_edges(G, pos, edge_color="red") # nakreslím hrany
        nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels={(u, v): d["weight"] for u, v, d in G.edges(data=True)}
        ) # u každé hrany zobrazuji její hodnotu
        plt.show()
        return G
    # Instance method
    def description(self):

        return f"{self.name} is {self.age} years old"