import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mpl
import networkx as nx
from itertools import combinations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

def ZaciTridy(soubor):
    # načítá soubor zaci.csv
    # do jakých tříd chodí žáci
    # výstup: dictionary ve formátu třída : množina jejích žáků
    df = pd.read_csv(soubor)
    id = list(df.id) # id žáků
    tridy = list(df.trida) # do jaké třídy patří
    kam_trida = dict() # dictionary - kdo kam chodí
    for i in range(len(id)): # projdu všechny žáky
        trida = tridy.pop(0).replace(" ", "")
        zak = id. pop(0) #id prvního žáka ze seznamu
        if trida in kam_trida: # pokud už je třída v dictionary
            kam_trida[trida].add(zak) # přidá do množiny nového žáka
        else:
            kam_trida[trida] =set() # vytvoří novou prázdnou množinu pro třídu
            kam_trida[trida].add(zak) # přidá do množiny rovnou prvního žáka
    # do jakeho rocniku chodi kteri zaci
    kam_rocnik = {5:set(), 6:set(), 7:set(), 8:set()}
    for x in kam_trida.keys():
        if x == '4.A' or x == '4.B' or x == '4.C':
            for e in kam_trida[x]: # presunu zaky dane tridy do daneho rocniku
                kam_rocnik[5].add(e)
        if x == '5.A' or x == '5.B' or x == '5.C':
            for e in kam_trida[x]:# presunu zaky dane tridy do daneho rocniku
                kam_rocnik[6].add(e)
        if x == '6.A' or x == '6.B' or x == '6.C':
            for e in kam_trida[x]:# presunu zaky dane tridy do daneho rocniku
                kam_rocnik[7].add(e)
        if x == '7.A' or x == '7.B' or x == '7.C':
            for e in kam_trida[x]: # presunu zaky dane tridy do daneho rocniku
                kam_rocnik[8].add(e)
    return kam_rocnik

def ZaciSeminare(soubor):
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

def IdUcitelu(soubor):
    # bere na vstupu seznam seminářů s učiteli
    # ke každému učiteli vymyslí id číslo
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

def KterySeminarProKteryRocnik(soubor):
    # udela dict rocnik_seminar, kde bude pro kazdy rocnik, jake seminare jsou pro nej
    rocnik_seminar = {5:set(), 6: set(), 7:set(), 8:set()}
    df = pd.read_csv(soubor) # načtu soubor jako dataframe
    for index, radek in df.iterrows():
        if radek['pro5'] == 1:
            id_seminare = radek['id']
            rocnik_seminar[5].add(id_seminare)
        if radek['pro6'] == 1:
            id_seminare = radek['id']
            rocnik_seminar[6].add(id_seminare)
        if radek['pro7'] == 1:
            id_seminare = radek['id']
            rocnik_seminar[7].add(id_seminare)
        if radek['pro8'] == 1:
            id_seminare = radek['id']
            rocnik_seminar[8].add(id_seminare)
    return rocnik_seminar

def UdelejGraf(seminare, id_seminaru, kam_seminar):
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


@dataclass
class Rocnik:
    rocnik: int
    ucitele_rocniku: Optional[dict] = None
    seminare_rocniku: Optional[set] = None
    zaci_rocniku: Optional[set] = None
    kam_rocnik: Optional[dict] = None
    G: Optional[nx.Graph] = None

    def __post_init__(self):
        # Initialize kam_rocnik if it's None
        if self.kam_rocnik is None:
            self.kam_rocnik = {}

    def data_pro_dany_rocnik(self, cislo_rocniku, rocnik_seminar, kam_seminar, seminare):
        self.zaci_rocniku = kam_seminar[cislo_rocniku]
        self.seminare_rocniku = rocnik_seminar[cislo_rocniku]
        self.ucitele_rocniku = dict()
        for ucitel in seminare.keys():
            seminare_ucitele = seminare[ucitel]
            overlap = seminare_ucitele.intersection(self.seminare_rocniku)
            if len(overlap) > 0:
                self.ucitele_rocniku[ucitel] = overlap
        for zak in self.zaci_rocniku:
            aktualni_seminare = kam_seminar[zak]
            self.kam_rocnik[zak] = aktualni_seminare
        return

    def udelej_graf(self, seminare, id_seminaru, kam_seminar):
        P = nx.MultiGraph()
        P.add_nodes_from(id_seminaru)

        # Create teacher edges
        for ucitel, seminare_ucitele in self.ucitele_rocniku.items():
            hrany_ucitel = combinations(seminare_ucitele, 2)
            P.add_edges_from(hrany_ucitel, weight=100)

        # Create student edges
        for zak, seminare_zaka in self.kam_rocnik.items():
            hrany_zak = combinations(seminare_zaka, 2)
            P.add_edges_from(hrany_zak, weight=1)

        # Convert to a simple graph
        G = nx.Graph(P)

        # Visualization logic here (if needed)

        # Return the created graph
        return G
    
def main():
    
    
    return

if __name__ == "__main__":
    main()