from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mpl
import networkx as nx
from itertools import combinations


def parsuj_tridu(trida: str):  # napr z 4.A udela 5
    """
    Udělá ze stringu, kde je napsáno, co je to za třídu (např. "5.A"), int, kde je jen, kolikátý je to ročník. 
    Pozor: k ročníku pak přičte 1, protože se žáci vždy přihlašují na semináře o rok dříve, než tam začnou chodit.

    Parametry: 
            trida (str): String, kde je napsáno, co je to za třídu (např. "5.A").
    """
    return int(trida.lstrip()[0])


def nacti_zaky_rocniku(soubor):
    """
    Načítá ze souboru zaci.csv dictionary, kde je pro každý ročník množina žáků, která do něj chodí.

    Parametry:
        soubor (.csv): Soubor ve formátu csv, kde jsou uloženy informace o žácích. Jmenuje se zaci.csv

    Vrací:
        dict: Dictionary, kde je pro každý ročník (int) množina žáků, která do něj chodí.
    """
    # načítá soubor zaci
    # do jakých tříd chodí žáci
    # výstup: dictionary ve formátu rocnik : množina jeho žáků
    df = pd.read_csv(soubor, delimiter=';')
    kam_rocnik = dict()  # dictionary - kdo kam chodí
    for zak, rocnik in zip(df.id, df.trida):  # projdu všechny žáky
        if rocnik in kam_rocnik:  # pokud už je třída v dictionary
            kam_rocnik[rocnik].add(zak)  # přidá do množiny nového žáka
        else:
            # vytvoří novou prázdnou množinu pro třídu
            kam_rocnik[rocnik] = set()
            kam_rocnik[rocnik].add(zak)  # přidá do množiny rovnou prvního žáka
    # do jakeho rocniku chodi (resp. kam budou chodit pristi rok) kteri zaci
    kam_rocnik = {5: set(), 6: set(), 7: set(), 8: set()}
    for rocnik in kam_rocnik.keys():
        cilovy_rocnik = parsuj_tridu(rocnik) + 1
        for e in kam_rocnik[rocnik]:  # presunu zaky dane tridy do daneho rocniku
            kam_rocnik[cilovy_rocnik].add(e)

    return kam_rocnik


def nacti_zaky_seminaru(soubor):
    """"
    Načítá ze souboru zapsani.csv dictionary, kde je vždy žák a množina seminářů, kam chodí. 

    Parametry:
        soubor (.csv): Soubor ve formátu csv, kde jsou uloženy informace o zapsaných. Jmenuje se zapsani.csv

    Vrací:
        dict: Dictionary, kde je vždy žák a množina seminářů, kam chodí. 
    """
    # načítá vstupní soubor zapsani.csv
    # výstupem je dict, kde je vždy zak množina seminářů, kam chodí
    df = pd.read_csv(soubor, delimiter=';')  # načtu soubor jako dataframe
    kam_seminar = dict()  # výstupní dictionary
    for zak, seminar in zip(df.zak, df.seminar):
        if zak in kam_seminar:  # pokud už žák má množinu v dictu
            kam_seminar[zak].add(seminar)  # přidám do množiny nový seminář
        else:
            kam_seminar[zak] = set()  # vytvoří novou prázdnou množinu
            kam_seminar[zak].add(seminar)  # přidám tam nový seminář
    return kam_seminar


def nacti_id_vsech_seminaru(soubor):
    """
    Načítá ze souboru seminare.csv seznam ID všech seminářů.

    Parametry:
        soubor (.csv): Soubor ve formátu csv, kde jsou uloženy informace o seminářích. Jmenuje se seminare.csv

    Vrací:
        list: Seznam ID všech seminářů. 
    """
    # bere na vstupu soubor seminare.csv
    # udela seznam id vsech seminaru
    df = pd.read_csv(soubor)  # načtu seznam seminářů jako dataframe
    id_vsech_seminaru = list(df.id)  # id seminářů
    return id_vsech_seminaru


def nacti_id_vsech_ucitelu(soubor):
    """
    Načítá ze souboru seminare.csv ID všech učitelů. 

    Parametry:
        soubor (.csv): Soubor ve formátu csv, kde jsou uloženy informace o seminářích. Jmenuje se seminare.csv

    Vrací: 
        dict: Dictionary, kde je vždy jméno učitele a k tomu jeho ID. První učitel ma ID 1.
    """
    # bere na vstupu soubor seminare.csv
    df = pd.read_csv(soubor)  # načtu seznam seminářů jako dataframe
    j = list(df.ucitel)  # jména učitelů
    jmena = set()  # množina jmen učitelů
    for jm in j:
        for x in jm.split(","):  # obcas je nekde vic ucitelu u jednoho seminare
            x = x.replace(" ", "")
            jmena.add(x)

    id_vsech_ucitelu = dict()  # dict, kde je učitel a k němu jeho id
    for id, jmeno in enumerate(jmena, 1):  # ocisluje ucitele, zacina 1
        id_vsech_ucitelu[jmeno] = id
    return id_vsech_ucitelu


def nacti_ucitele_seminaru(soubor):
    """
    Načítá ze souboru seminare.csv dict, kde je ke každému učiteli množina seminářů, které učí. 

    Parametry: 
        soubor (.csv): Soubor ve formátu csv, kde jsou uloženy informace o seminářích. Jmenuje se seminare.csv

    Vrací:
        dict: Dictionary učitelů a množin jejich seminářů.
        
    """

    # výstup dict, kde je ke každému učiteli množina seminářů, které učí
    # bere na vstupu soubor seminare.csv
    # udela seznam id vsech seminaru
    df = pd.read_csv(soubor)  # načtu seznam seminářů jako dataframe
    id_vsech_seminaru = list(df.id)  # id seminářů
    j = list(df.ucitel)  # jména učitelů
    jmena = set()  # množina jmen učitelů
    for jm in j:
        for x in jm.split(","):  # obcas je nekde vic ucitelu u jednoho seminare
            x = x.replace(" ", "")
            jmena.add(x)

    id_vsech_ucitelu = dict()  # dict, kde je učitel a k němu jeho id
    for id, jmeno in enumerate(jmena, 1):  # ocisluje ucitele, zacina 1
        id_vsech_ucitelu[jmeno] = id
    # TUDU : use defaultdict(set)
    seminare_ucitelu = dict()  # dictionary, kde je vždy učitel k němu množina jeho seminářů
    for x in range(len(id_vsech_seminaru)):  # pro každý seminář
        seminar = id_vsech_seminaru.pop(0)  # aktuální seminář
        ucitel = j.pop(0)  # aktuální učitel
        # odstraním pro jistotu mezery ze jmen učitelů
        ucitel = ucitel.replace(' ', '')

        # u některých seminářů je víc učitelů - rozdělím je
        ucitel = ucitel.split(",")
        if type(ucitel) == list:  # pokud víc než jeden učitel
            for x in ucitel:  # vezmu jednoho učitele
                id_ucitele = id_vsech_ucitelu[x]  # kouknu na jeho id
                if id_ucitele in seminare_ucitelu:  # pokud má už množinu svých seminářů
                    seminare_ucitelu[id_ucitele].add(
                        seminar)  # přidám další seminář
                else:  # pokud učitel ještě nemá množinu svých seminářů
                    # vytvořím mu prázdnou množinu
                    seminare_ucitelu[id_ucitele] = set()
                    # rovnou do množiny přidám seminář
                    seminare_ucitelu[id_ucitele].add(seminar)
        else:
            id_ucitele = id_vsech_ucitelu[ucitel]  # vezmu aktuálního učitele
            if id_ucitele in seminare_ucitelu:  # to stejné, co v ifu výše
                seminare_ucitelu[id_ucitele].add(seminar)
            else:
                seminare_ucitelu[id_ucitele] = set()
                seminare_ucitelu[id_ucitele].add(seminar)
    # vrací dict učitelů a množin jejich seminářů
    return seminare_ucitelu


def ktery_seminar_pro_ktery_rocnik(soubor):
    """
    Načítá ze souboru seminare.csv dictionary, kde je pro každý ročník, množina seminářů pro něj určených. 

    Parametry: 
        soubor (.csv): Soubor ve formátu csv, kde jsou uloženy informace o seminářích. Jmenuje se seminare.csv

    Vrací: 
        dict: Dictionary, kde je pro každý ročník, množina seminářů pro něj určených. 
    """
    # bere seminare.csv
    # udela dict rocnik_seminar, kde bude pro kazdy rocnik, jake seminare jsou pro nej
    rocnik_seminar = {5: set(), 6: set(), 7: set(), 8: set()}
    df = pd.read_csv(soubor)  # načtu soubor jako dataframe
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


def udelej_graf(seminare_ucitelu, id_vsech_seminaru, kam_seminar):
    ############ tahle funkce nejspíš není potřeba, níže se nachází její modifikace udelej_graf_pro_jeden_rocnik, ktera je misto ni
    """
    Vytvoří ohodnocený neorientovaný graf, kde vrcholy jsou semináře (číslo vrcholu = ID semináře). 
    Semináře které sdílí učitele a/nebo žáky jsou spojeny ohodnocenou hranou. 
    Za každého sdíleného učitele se hodnota hrany zvyšuje o 100, za každého sdíleného žáka o 1.

    Parametry: 
        seminare_ucitelu (dict): Dictionary, kde je vždy učitel a množina jeho seminářů.
        id_seminaru (list): Seznam ID seminářů.
        kam_seminar (dict): Dictionary, kde je vždy žák a množina jeho seminářů.

    Vrací:
        networkx graf: ohodnocený neorientovaný graf, kde vrcholy jsou semináře.
    """
    # tvorba neorientovaného grafu, kde vrcholy jsou semináře
    # semináře budou spojeny hranou, pokud sdílí žáka nebo učitele
    # hrany jsou ohodnocené: žák má hodnotu 1, učitel má hodnotu 100
    P = nx.MultiGraph()  # multigraf = má mezi dvojicí vrcholů víc než dvě hrany
    # každý vrchol je jeden seminář (resp. id semináře)
    P.add_nodes_from(id_vsech_seminaru)

    # učitelské hrany
    for ucitel in seminare_ucitelu.keys():  # pro každého profesora
        vrcholy = seminare_ucitelu[ucitel]  # množina seminářů profesora
        # všechny možné dvojice seminářů v množině
        kombinace_vrcholu = combinations(vrcholy, 2)
        # pro každou dvojici udělá hranu o hodnotě 100 (úplný graf)
        P.add_edges_from(kombinace_vrcholu, weight=100)

    # žákovské hrany
    for zak in kam_seminar.keys():  # pro každý prvek z množiny seminářů u jednoho žáka
        vrcholy = kam_seminar[zak]  # množina seminářů žáka
        # všechny možné dvojice seminářů v množině
        kombinace_vrcholu = combinations(vrcholy, 2)
        # pro každou dvojici udělá hranu o hodnotě 1 (úplný graf)
        P.add_edges_from(kombinace_vrcholu, weight=1)

    # graf se součtem hodnot hran z P
    # udělá s multigrafu P normální ohodnocený graf
    G = nx.Graph()
    for u, v, data in P.edges(data=True):  # pro všechny vrcholy
        if G.has_edge(u, v):  # pokud hrana existuje
            G[u][v]['weight'] += data['weight']  # přidám k váze hrany
        else:
            # pokud hrana neexistuje, vytvořím ji
            G.add_edge(u, v, weight=data['weight'])
    # tisknu graf na textový výstup - není nutné
    # for u, v, data in G.edges(data=True):
    #    weight = data['weight']
    #    print(f"hrana: ({u}, {v}), hodnota: {weight}")

    # vizualizace grafu
    pos = nx.spring_layout(G)  # rozmístění vrcholů a hran
    nx.draw_networkx_nodes(G, pos)  # nakreslím vrcholy
    nx.draw_networkx_edges(G, pos, edge_color="red")  # nakreslím hrany
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels={(u, v): d["weight"]
                             for u, v, d in G.edges(data=True)}
    )  # u každé hrany zobrazuji její hodnotu
    return G


def udelej_graf_pro_jeden_rocnik(ucitele_a_jejich_seminare, id_seminaru, zaci_a_jejich_seminare):
    """
    Vytvoří ohodnocený neorientovaný graf, kde vrcholy jsou semináře (číslo vrcholu = ID semináře). 
    Semináře které sdílí učitele a/nebo žáky jsou spojeny ohodnocenou hranou. 
    Za každého sdíleného učitele se hodnota hrany zvyšuje o 100, za každého sdíleného žáka o 1.

    Parametry: 
        ucitele_a_jejich_seminare (dict): Dictionary, kde je vždy učitel a množina jeho seminářů.
        id_seminaru (list): Seznam ID seminářů.
        zaci_a_jejich_seminare (dict): Dictionary, kde je vždy žák a množina jeho seminářů.

    Vrací:
        networkx graf: ohodnocený neorientovaný graf, kde vrcholy jsou semináře.
    """
    # tvorba neorientovaného grafu, kde vrcholy jsou semináře
    # semináře budou spojeny hranou, pokud sdílí žáka nebo učitele
    # hrany jsou ohodnocené: žák má hodnotu 1, učitel má hodnotu 100
    P = nx.MultiGraph()  # multigraf = má mezi dvojicí vrcholů víc než dvě hrany
    # každý vrchol je jeden seminář (resp. id semináře)
    P.add_nodes_from(id_seminaru)

    # učitelské hrany
    for ucitel in ucitele_a_jejich_seminare.keys():  # pro každého profesora
        # množina seminářů profesora
        vrcholy = ucitele_a_jejich_seminare[ucitel]
        # všechny možné dvojice seminářů v množině
        kombinace_vrcholu = combinations(vrcholy, 2)
        # pro každou dvojici udělá hranu o hodnotě 100 (úplný graf)
        P.add_edges_from(kombinace_vrcholu, weight=100)

    # žákovské hrany
    for zak in zaci_a_jejich_seminare.keys():  # pro každý prvek z množiny seminářů u jednoho žáka
        vrcholy = zaci_a_jejich_seminare[zak]
        # množina seminářů žáka
        # všechny možné dvojice seminářů v množině
        kombinace_vrcholu = combinations(vrcholy, 2)
        # pro každou dvojici udělá hranu o hodnotě 1 (úplný graf)
        P.add_edges_from(kombinace_vrcholu, weight=1)

    # graf se součtem hodnot hran z P
    # udělá s multigrafu P normální ohodnocený graf
    G = nx.Graph()
    for u, v, data in P.edges(data=True):  # pro všechny vrcholy
        if G.has_edge(u, v):  # pokud hrana existuje
            G[u][v]['weight'] += data['weight']  # přidám k váze hrany
        else:
            # pokud hrana neexistuje, vytvořím ji
            G.add_edge(u, v, weight=data['weight'])
    # tisknu graf na textový výstup - není nutné
    # for u, v, data in G.edges(data=True):
    #    weight = data['weight']
    #    print(f"hrana: ({u}, {v}), hodnota: {weight}")

    # vizualizace grafu
    pos = nx.spring_layout(G)  # rozmístění vrcholů a hran
    nx.draw_networkx_nodes(G, pos)  # nakreslím vrcholy
    nx.draw_networkx_edges(G, pos, edge_color="red")  # nakreslím hrany
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels={(u, v): d["weight"]
                             for u, v, d in G.edges(data=True)}
    )  # u každé hrany zobrazuji její hodnotu
    plt.box(False)
    # plt.show()
    return G
