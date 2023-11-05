import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from itertools import combinations

def nacti_zaky(soubor):
    # nacita vstupni soubor zaci.csv
    df = pd.read_csv(soubor)
    id = list(df.id) # id zaku
    tridy = list(df.trida) # kam patri
    zaci = []
    for i in range(len(id)):
        zak = id.pop(0)
        trida = tridy.pop(0)
        zaci[zak] = trida
    return zaci


def zaci_tridy(soubor):
    # nacita soubor zaci
    #do jakych trid chodi zaci
    # vystup: dict, trida : mnozina jejich zaku
    df = pd.read_csv(soubor)
    id = list(df.id) # id zaku
    tridy = list(df.trida) # kam patri
    kam_trida = dict()
    for i in range(len(id)):
        trida = tridy.pop(0).replace(" ", "")
        zak = id. pop(0) #id zaka
        if trida in kam_trida:
            kam_trida[trida].add(zak) # prida do mnoziny noveho zaka
        else:
            kam_trida[trida] =set() # vytvori novou prazdnou mnozinu
            kam_trida[trida].add(zak) # prida do mnoziny rovnou prvniho zaka
    return kam_trida

def zaci_seminare(soubor):
    # nacita vstupni soubor zapsani.csv
    # vystupem je dict, kde je vzdy zak a jeho seminare
    df = pd.read_csv(soubor)
    id = list(df.zak) # id zaka
    seminare = list(df.seminar) # kam patri
    kam_seminar = dict()
    for i in range(len(id)):
        zak = id.pop(0)
        seminar = seminare.pop(0)
        if zak in kam_seminar:
            kam_seminar[zak].add(seminar) # prida do mnoziny novy seminar
        else:
            kam_seminar[zak] =set() # vytvori novou prazdnou mnozinu
            kam_seminar[zak].add(seminar) 
    return kam_seminar

def id_ucitelu(soubor):
    # bere na vstupu seznam seminaru s uciteli
    # ke kazdemu uciteli vymysli id cislo
    # vystup dict, kde je ke kazdemu uciteli 
    # mnozina seminaru, ktere uci
    df = pd.read_csv(soubor)
    s = list(df.id) # id seminaru
    id_seminaru = list(df.id)
    j= list(df.ucitel) # jmena ucitelu
    jmena = set()
    for jm in j:
        for x in jm.split(","): # obcas je nekde vic ucitelu u jednoho seminare
            x = x.replace(" ","")
            jmena.add(x)
    ucitele = dict()
    i = 1
    for jm in jmena:
        ucitele[jm] = i
        i += 1
    ## odstranim to, co tam dela neplechu, co je nejednoznacne
    #del ucitele['budeupřesněno']
    #del ucitele['příp.M.Roháčková(podleúvazku)']
    seminare = dict()
    for x in range(len(s)):
        seminar = s.pop(0)
        ucitel = j.pop(0)
        ucitel = ucitel.replace(' ','') 
        ucitel = ucitel.split(",") # blbne to, kdyz je ucitelu u jednoho seminare vic nez jeden
        print(ucitel)
        if type(ucitel) == list:
            for x in ucitel:
                id_ucitele = ucitele[x]
                if id_ucitele in seminare:
                    seminare[id_ucitele].add(seminar)
                else:
                    seminare[id_ucitele] = set()
                    seminare[id_ucitele].add(seminar)
        else:
            id_ucitele = ucitele[ucitel]
            if id_ucitele in seminare:
                seminare[id_ucitele].add(seminar)
            else:
                seminare[id_ucitele] = set()
                seminare[id_ucitele].add(seminar)

    return ucitele, seminare, id_seminaru

def udelej_graf(ucitele, seminare, id_seminaru, kam_seminar):
    P = nx.Graph() # ma neorientovane grafy
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


def main():
    ks = zaci_seminare("zapsani.csv")
    kt = zaci_tridy("zaci.csv")
    ucitele, seminare, id_seminaru = id_ucitelu("seminare.csv")
    print(seminare, id_seminaru)
    print(udelej_graf(ucitele, seminare, id_seminaru, ks))
    return

if __name__ == "__main__":
    main()