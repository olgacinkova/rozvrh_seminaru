import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mpl
import networkx as nx
from itertools import combinations

"""def nacti_zaky(soubor):
    # nacita vstupni soubor zaci.csv
    # výstupem 
    df = pd.read_csv(soubor)
    id = list(df.id) # id zaku
    tridy = list(df.trida) # kam patri
    zaci = []
    for i in range(len(id)):
        zak = id.pop(0)
        trida = tridy.pop(0)
        zaci[zak] = trida
        print(zaci)
    return zaci
"""

def zaci_tridy(soubor):
    # načítá soubor zaci.csv
    # do jakých tříd chodí žáci
    # výstup: dictionary ve formátu třída : množina jejích žáků
    df = pd.read_csv(soubor)
    id = list(df.id) # id žáků
    tridy = list(df.trida) # do jaké třídy patří
    kam_trida = dict() # dictionary, kdo kam chodí
    for i in range(len(id)): # projdu všechny žáky
        trida = tridy.pop(0).replace(" ", "")
        zak = id. pop(0) #id prvního žáka ze seznamu
        if trida in kam_trida: # pokud už je třída v dictionary
            kam_trida[trida].add(zak) # přidá do množiny nového žáka
        else:
            kam_trida[trida] =set() # vytvoří novou prázdnou množinu pro třídu
            kam_trida[trida].add(zak) # přidá do množiny rovnou prvního žáka
    return kam_trida

def zaci_seminare(soubor):
    # načítá vstupní soubor zapsani.csv
    # výstupem je dict, kde je vždy zak množina seminářů, kam chodí
    df = pd.read_csv(soubor) # načtu soubor jako dataframe
    id = list(df.zak) # seznam id žáků (sloupec)
    seminare = list(df.seminar) # seznam seminářů žáků (sloupec)
    kam_seminar = dict() # výstupní dictionary
    for i in range(len(id)): # pro každého žáka
        zak = id.pop(0) # aktuální žák
        seminar = seminare.pop(0) # seminář, na který chodí
        if zak in kam_seminar: # pokud už žák má množinu v dictu
            kam_seminar[zak].add(seminar) # přidám do množiny nový seminář
        else:
            kam_seminar[zak] =set() # vytvoří novou prázdnou množinu
            kam_seminar[zak].add(seminar) # přidám tam nový seminář
    return kam_seminar

def id_ucitelu(soubor):
    # bere na vstupu seznam seminářů s učiteli
    # ke každému učiteli vymyslí id čísl
    # o
    # výstup dict, kde je ke každému učiteli množina seminářů, které učí
    df = pd.read_csv(soubor) # načtu seznam seminářů jako dataframe
    id_seminaru = list(df.id) # id seminářů
    j= list(df.ucitel) # jména učitelů
    jmena = set() # množina jmen učitelů
    for jm in j:
        for x in jm.split(","): # obcas je nekde vic ucitelu u jednoho seminare
            x = x.replace(" ","")
            jmena.add(x)
    ucitele = dict() # dict, kde je učitel a k němu množina jeho seminářů
    i = 1
    for jm in jmena: # každému učiteli vymyslí jeho id
        ucitele[jm] = i
        i += 1

    seminare = dict() # dictionary, kde je vždy učitel k němu množina jeho seminářů
    for x in range(len(id_seminaru)): # pro každý seminář
        seminar = id_seminaru.pop(0) # aktuální seminář
        ucitel = j.pop(0) # aktuální učitel
        ucitel = ucitel.replace(' ','' ) # odstraním pro jistotu mezery ze jmen učitelů 
        ucitel = ucitel.split(",") # u některých seminářů je víc učitelů - rozdělím je
        if type(ucitel) == list: # pokud víc než jeden učitel
            for x in ucitel: # vezmu jednoho učitele
                id_ucitele = ucitele[x] # kouknu na jeho id
                if id_ucitele in seminare: # pokud má už množinu svých seminářů
                    seminare[id_ucitele].add(seminar) # přidám další seminář
                else: # pokud učitel ještě nemá množinu svých seminářů
                    seminare[id_ucitele] = set() # vytvořím mu prázdnou množinu
                    seminare[id_ucitele].add(seminar) # rovnou do množiny přidám seminář
        else:
            id_ucitele = ucitele[ucitel] # vezmu aktuálního učitele
            if id_ucitele in seminare: # to stejné, co v ifu výše
                seminare[id_ucitele].add(seminar)
            else:
                seminare[id_ucitele] = set()
                seminare[id_ucitele].add(seminar)
    # vrací dict učitelů a jejich id, dict učitelů a množin jejich seminářů, seznam id seminaru
    return ucitele, seminare, id_seminaru

def udelej_graf(ucitele, seminare, id_seminaru, kam_seminar):
    # tvorba neorientovaného grafu, kde vrcholy jsou semináře
    # semináře budou spojeny hranou, pokud sdílí žáka nebo učitele
    # hrany jsou ohodnocené: žák má hodnotu 1, učitel má hodnotu 100
    P = nx.MultiGraph() # multigraf = má mezi dvojicí vrcholů víc než dvě hrany
    P.add_nodes_from(id_seminaru)

    ### profesorske hrany
    for x in seminare.keys():
        # pro kazdy prvek z mnoziny seminaru u jednoho profesora
        # propojit vsechny se vsemi, protoze sdili profesora
        vrcholy = seminare[x]
        hrany = combinations(vrcholy, 2) # vsechny mozne dvojice
        P.add_edges_from(hrany, weight = 100)
    
    ### studentske hrany
    for x in kam_seminar.keys():
        # pro kazdy prvek z mnoziny seminaru u jednoho zaka
        # propojit vsechny se vsemi, protoze sdili zaka
        vrcholy = kam_seminar[x]
        hrany = combinations(vrcholy, 2) # vsechny mozne dvojice
        P.add_edges_from(hrany, weight = 1)

    # graf se souctem hran z P
    G = nx.Graph()
    for u, v, data in P.edges(data=True):
        if G.has_edge(u, v):
        # If an edge already exists, add the weights
            G[u][v]['weight'] += data['weight']
        else:
        # If the edge doesn't exist, create a new one
            G.add_edge(u, v, weight=data['weight'])
    # tisknu vystup
    for u, v, data in G.edges(data=True):
        weight = data['weight']
        print(f"Edge: ({u}, {v}), Weight: {weight}")
    # Vizualizace
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos, edge_color="red")
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels={(u, v): d["weight"] for u, v, d in G.edges(data=True)}
    )
    plt.show()
    return G

def obarvi_graf(G):
        # Apply greedy coloring
    graph_coloring = nx.greedy_color(G)
    unique_colors = set(graph_coloring.values())

    # Assign colors to nodes based on the greedy coloring
    graph_color_to_mpl_color = dict(zip(unique_colors, mpl.TABLEAU_COLORS))
    node_colors = [graph_color_to_mpl_color[graph_coloring[n]] for n in G.nodes()]
    labels = {e: G.edges[e]['weight'] for e in G.edges}
    pos = nx.spring_layout(G, seed=14)
    nx.draw(
        G,
        pos, 
        with_labels=True,
        node_size=500,
        node_color=node_colors,
        edge_color="grey",
        font_size=12,
        font_color="#333333",
        width=2
    )
    labels = {e: G.edges[e]['weight'] for e in G.edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()
    return G


"""def main():
    ks = zaci_seminare("zapsani.csv")
    kt = zaci_tridy("zaci.csv")
    ucitele, seminare, id_seminaru = id_ucitelu("seminare.csv")
    print(seminare, id_seminaru)
    graf = udelej_graf(ucitele, 
                      seminare, id_seminaru, ks)
    print(obarvi_graf(graf))
    return

if __name__ == "__main__":
    main()
    """