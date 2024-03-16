from fce_pro_seminare_rocniky import *
# from barveni import *
from copy import *
from prioritizace_barev import prioritizovane_barveni


class Seminar:
    """
    Obsahuje vše o jednotlivých seminářích.

    Atributy:
    id (int): Identifikační číslo semináře.
    pro_ktere_rocniky (set): Množina ročníků, pro které seminář je.
    kteri_zaci_tam_chodi (set): Množina žáků, kteří na seminář chodí (jsou tam přihlášení).
    kdo_seminar_uci (set): Množina učitelů, kteří seminář učí. (Většinou jen jeden učitel na seminář, ale občas dva.) 
    """

    def __init__(self, id_seminare: int) -> None:
        """
        Konstruktor pro Seminar.

        Parametry:
            id seminare (int): Identifikační číslo semináře.
        """
        self.__id: int = id_seminare
        self.pro_ktere_rocniky: set = set()  # muze byt pro vice rocniku
        self.kteri_zaci_tam_chodi: set = set()
        self.kdo_seminar_uci: set = set()  # muze ucit i vice ucitelu

    @property
    def vrat_id(self) -> int:
        """
        Vrací identifikační číslo semináře.
        """
        return self.__id

    def uloz_pro_ktere_rocniky(self, soubor_seminare: str) -> None:
        """
        Ukládá, pro které ročníky je seminář určen. 

        Parametry:
            soubor_seminare (.csv): Soubor ve formátu csv, kde jsou informace o každém semináři. Jmenuje se seminare.csv
        """

        # načtu soubor jako dataframe
        df = pd.read_csv(soubor_seminare, delimiter=";")
        id_seminare: int = self.vrat_id
        row = df[df['id'] == id_seminare]
        if row['pro5'].iloc[0] == 1:
            self.pro_ktere_rocniky.add(5)  # kvinta
            print(f"seminar {id_seminare} je pro {self.pro_ktere_rocniky}")
        if row['pro6'].iloc[0] == 1:
            self.pro_ktere_rocniky.add(6)  # sexta
            print(f"seminar {id_seminare} je pro {self.pro_ktere_rocniky}")
        if row['pro7'].iloc[0] == 1:
            self.pro_ktere_rocniky.add(7)  # septima
            print(f"seminar {id_seminare} je pro {self.pro_ktere_rocniky}")
        if row['pro8'].iloc[0] == 1:
            self.pro_ktere_rocniky.add(8)  # oktáva
            print(f"seminar {id_seminare} je pro {self.pro_ktere_rocniky}")
    


    def uloz_kteri_zaci_tam_chodi(self, soubor_zapsani):
        """
        Ukládá, kteří žáci na seminář chodí. 

        Parametry:
            soubor_zapsani (.csv): Soubor ve formátu csv, kde jsou informace o zapsaných žácích. Jmenuje se zapsani.csv
        """
        df = pd.read_csv(soubor_zapsani, delimiter=';')
        for zak, seminar in zip(df.zak, df.seminar):
            if seminar == self.__id:
                self.kteri_zaci_tam_chodi.add(zak)

    # nacita soubor seminare.csv a promennou id_vsech_ucitelu
    """def uloz_kdo_seminar_uci(self, soubor_seminare, id_vsech_ucitelu):
        
        Ukládá, kteří učitelé seminář učí.

        Parametry: 
            soubor_seminare (.csv): Soubor ve formátu csv, kde jsou informace o každém semináři. Jmenuje se seminare.csv
            id_vsech_ucitelu (dict): Dictionary, kde je učitel a k němu jeho ID.
        df = pd.read_csv(soubor_seminare)
        radek = self.__id - 1
        sloupec = 'ucitel'
        jmeno_ucitele = df.at[radek, sloupec]
        jmeno_ucitele = str(jmeno_ucitele)
        jmeno_ucitele = jmeno_ucitele.replace(" ", "")
        # protoze muze byt vic ucitelu na jednom seminari
        jmeno_ucitele = jmeno_ucitele.split(",")
        for j in jmeno_ucitele:
            id_ucitele = id_vsech_ucitelu[j]
            self.kdo_seminar_uci.add(id_ucitele)"""

    def uloz_kdo_seminar_uci(self, soubor_seminare, id_vsech_ucitelu):
        """
        Ukládá, kteří učitelé seminář učí.

        Parametry: 
            soubor_seminare (.csv): Soubor ve formátu csv, kde jsou informace o každém semináři. Jmenuje se seminare.csv
            id_vsech_ucitelu (dict): Dictionary, kde je učitel a k němu jeho ID.
        """
        df = pd.read_csv(soubor_seminare, delimiter=";")
        id_seminare: int = self.vrat_id
        row = df[df['id'] == id_seminare] # pro ten dany seminar
        jmeno_ucitele = row['ucitel'].iloc[0]
        jmeno_ucitele = str(jmeno_ucitele).replace(" ", "")
        # Protože může být více učitelů na jednom semináři
        jmeno_ucitele = jmeno_ucitele.split(",")

        for j in jmeno_ucitele:
                id_ucitele = id_vsech_ucitelu[j]
                self.kdo_seminar_uci.add(id_ucitele)

    def uloz_data_pro_seminar(self, soubor_zapsani, soubor_seminare, id_vsech_ucitelu):
        """
        Spustí postupně všechny metody třídy Seminar. 
        Uloží tak, kdo seminář učí, kteří žáci tam chodí a pro které ročníky je seminář určen.

        Parametry:
            soubor_zapsani (.csv): Soubor ve formátu csv, kde jsou informace o zapsaných žácích. Jmenuje se zapsani.csv
            soubor_seminare (.csv): Soubor ve formátu csv, kde jsou informace o každém semináři. Jmenuje se seminare.csv
            id_vsech_ucitelu (dict): Dictionary, kde je učitel a k němu jeho ID.
        """
        self.uloz_kdo_seminar_uci(soubor_seminare, id_vsech_ucitelu)
        self.uloz_kteri_zaci_tam_chodi(soubor_zapsani)
        self.uloz_pro_ktere_rocniky(soubor_seminare)


class Rocnik:
    """
    Obsahuje vše o jednotlivých ročnících.

    Atributy:
        __kolikaty (int/list): Který ročník, to je. (Může být i pro dva ročníky zároveň, kvůli spojení kvinty a sexty.)
        poradi (list): Pořadí, ve kterém mám přiřazovat barvy vrcholům (bloky seminářům).
        zaci (set): Množina žáků, kteří chodí do daného ročníku.
        ucitele (set): Množina učitelů, kteří učí semináře daného ročníku.
        id_seminaru_rocniku (set): Množina ID všech seminářů ročníku.
        ucitele_a_jejich_seminare (dict): Dictionary, kde je vždy učitel a množina seminářů, které učí.
        zaci_a_jejich_seminare (dict): Dictionary, kde je vždy žák a množina seminářů, kam chodí.
        graf (networkx graph): Graf, kde vrcholy jsou semináře. Semináře které sdílí učitele a/nebo žáky jsou spojeny ohodnocenou hranou. Za každého sdíleného učitele se hodnota hrany zvyšuje o 100, za každého sdíleného žáka o 1.
        graf_dict (dict): Stejný graf jako self.graf, ale převedený do formátu dictionary dle nx.to_dict_of_dicts()
        graf_colors (dict): Dictionary, kde je vždy vrchol grafu a jeho barva. Jde o tzv. neobarvený graf, proto jsou barvy všech vrcholů stejné. Všechny vrcholy mají barvu 8. 
        obarveny_graf (networkx graph): Graf self.graf po obarvení vrcholů, tak aby žádné vrcholy se stejnou barvou nebyly spojeny hranou.
        obarveny_graf_dict (dict): Obarvený graf převedený do formátu dictionary dle nx.to_dict_of_dicts()
        obarveny_graf_colors (dict): Dictionary, kde je vždy vrchol grafu a jeho barva.

    """

    def __init__(self, kolikaty: int | list):  # kvuli spojeni kvinty a sexty
        """
        Konstruktor třídy Rocnik.

        Parametry:
            kolikaty (int/list): O kolikátý ročník, popř. kolikáté ročníky, se jedná. 
        """
        if type(kolikaty) == int:
            # aby mohl byt zadan i samostatny int a nemusel byt []
            self.__kolikaty = [kolikaty]
        elif type(kolikaty) == list:
            self.__kolikaty = kolikaty
        else:
            raise Exception("Spatny argument")

        self.poradi: list = []
        self.zaci: set = set()  # mnozina zaku, kteri chodi do daneho rocniku
        self.ucitele: set = set()  # mnozina ucitelu uci seminare daneho rocniku
        self.id_seminaru_rocniku: set = set()
        self.ucitele_a_jejich_seminare: dict = dict()
        self.zaci_a_jejich_seminare: dict = dict()
        self.graf = None
        self.graf_dict: dict = dict()  # graf ve formatu dle nx.to_dict_of_dicts
        self.graf_colors: dict = dict()  # dictionary, kde je vzdy vrchol a jeho barva
        self.obarveny_graf = None
        # graf ve formatu dle nx.to_dict_of_dicts
        self.obarveny_graf_dict: dict = dict()
        # dictionary, kde je vzdy vrchol a jeho barva
        self.obarveny_graf_colors: dict = dict()

    def uloz_zaci(self, zaci_rocniku):
        """
        Načítá atribut zaci, který byl inicializován v konstruktoru. Čerpá data ze souboru ve formátu csv.

        Parametry: 
            zaci_rocniku (dict): Dictionary, kde je ulozeno, ktery zak chodi do ktere tridy. Je to vystup funkce nacti_zaky_rocniku, 
                kterou v modulu spousteni.py volam na soubor zaci.csv
        """
        for rocnik in self.__kolikaty:
            self.zaci = self.zaci.union(zaci_rocniku[rocnik])

    def uloz_poradi(self):
        if self.__kolikaty == [5, 6]:  # kvinta a sexta
            self.poradi = [2, 4, 6, 1, 3, 5, 7, 8,
                           9, 10, 11, 12]  # maji mit dva bloky
        if self.__kolikaty == 7:  # septima
            self.poradi = [1, 3, 5, 2, 4, 6, 7, 8,
                           9, 10, 11, 12]  # maji mit 5 bloku
        else:  # oktava
            self.poradi = [1, 3, 5, 2, 4, 6, 7, 8,
                           9, 10, 11, 12]  # maji mit 9 bloku

    def uloz_ucitele(self, vsechny_seminare: list):
        """
        Načítá atribut ucitele, který byl inicializován v konstruktoru. Čerpá data o učitelích, ze seznamu objektů jednotlivých seminářů.

        Parametry: 
            vsechny_seminare (list): Seznamu objektů jednotlivých seminářů.
        """
        for e in vsechny_seminare:
            self.ucitele = self.ucitele.union(e.kdo_seminar_uci)

    def uloz_id_seminaru_rocniku(self, seminare_rocniky: dict):
        """
        Načítá atribut id_seminaru_rocniku, který byl inicializován v konstruktoru. Udělá seznam ID seminářů pro ročník.

        Parametry: 
            seminare_rocniky (dict): Dictionary, kde je pro každý ročník, jaké semináře jsou pro něj. Vrací jej funkce ktery_seminar_pro_ktery_rocnik, když je volána na soubor seminare.csv.
        """
        for rocnik in self.__kolikaty:
            self.id_seminaru_rocniku = self.id_seminaru_rocniku.union(
                seminare_rocniky[rocnik])

    def uloz_ucitele_a_jejich_seminare(self, ucitele_seminaru: dict, vsechny_seminare: list):
        """
        Načítá atribut ucitele_a_jejich_seminare, který byl inicializován v konstruktoru. 

        Parametry: 
            ucitele_seminaru (dict): Dictionary učitelů a množin jejich seminářů. Vrací jej funkce nacti_ucitele_seminaru volaná na soubor seminare.csv
            vsechny_seminare (list): Seznamu objektů jednotlivých seminářů.
        """
        for ucitel in self.ucitele:
            mnozina_seminaru_konkretniho_ucitele = ucitele_seminaru[ucitel]
            self.ucitele_a_jejich_seminare[ucitel] = mnozina_seminaru_konkretniho_ucitele
        # projdu kazdemu uciteli rocniku jeho mnozinu seminaru
        for ucitel, mnozina in self.ucitele_a_jejich_seminare.items():
            for konkretni_seminar in mnozina.copy():  # pro kazdy seminar v mnozine zkontroluju, zda je pro dany rocnik
                # pokud je seminar pro dany rocnik
                if vsechny_seminare[konkretni_seminar - 1].pro_ktere_rocniky == self.__kolikaty:
                    mnozina.remove(konkretni_seminar)

                print(mnozina)
    """ def uloz_ucitele_a_jejich_seminare(self, ucitele_seminaru: dict, vsechny_seminare: list):
        
        Načítá atribut ucitele_a_jejich_seminare, který byl inicializován v konstruktoru. 

        Parametry: 
            ucitele_seminaru (dict): Dictionary, učitelů a množin jejich seminářů. Vrací jej funkce nacti_ucitele_seminaru volaná na soubor seminare.csv
            vsechny_seminare (list): Seznamu objektů jednotlivých seminářů.
        
        for ucitel in self.ucitele:
            mnozina_seminaru_konkretniho_ucitele = ucitele_seminaru[ucitel]
            self.ucitele_a_jejich_seminare[ucitel] = mnozina_seminaru_konkretniho_ucitele
        # projdu kazdemu uciteli rocniku jeho mnozinu seminaru
        for mnozina in self.ucitele_a_jejich_seminare.values():
            for konkretni_seminar in mnozina:  # pro kazdy seminar v mnozine zkontroluju, zda je pro dany rocnik
                # pokud je seminar pro dany rocnik
                if vsechny_seminare[konkretni_seminar - 1].pro_ktere_rocniky == self.__kolikaty:
                    self.ucitele_a_jejich_seminare[mnozina].discard(
                        konkretni_seminar)"""

    def uloz_zaky_a_jejich_seminare(self, zaci_seminaru, vsechny_seminare):
        """
        Načítá atribut zaci_a_jejich_seminare, který byl inicializován v konstruktoru. 

        Parametry: 
            zaci_seminaru (dict): Dictionary, kde je vždy žák a množina seminářů, kam chodí. Je to výstup funkce nacti_zaky_seminaru volané na soubor zapsani.csv
            vsechny_seminare (list): Seznamu objektů jednotlivých seminářů.
        """

        for zak in self.zaci:
            if zak in zaci_seminaru.keys():  # protoze zak cislo 35 tam neni
                mnozina_seminaru_konkretniho_zaka = zaci_seminaru[zak]
                self.zaci_a_jejich_seminare[zak] = mnozina_seminaru_konkretniho_zaka

        # projdu kazdemu zakovi rocniku jeho mnozinu seminaru
        for mnozina in self.zaci_a_jejich_seminare.values():
            for konkretni_seminar in mnozina:  # pro kazdy seminar v mnozine zkontroluju, zda je pro dany rocnik
                # pokud je seminar pro dany rocnik
                if vsechny_seminare[konkretni_seminar - 1].pro_ktere_rocniky == self.__kolikaty:
                    self.zaci_a_jejich_seminare[mnozina].discard(
                        konkretni_seminar)

    def uloz_graf(self):
        """
        Ukládá atributy graf a graf_dict, které byl inicializovány v konstruktoru. Je to networkx graf pro jeden ročník. Ještě neobarvený. Pak uloží graf jako dictionary of dictionaries (výstup funkce nx.to_dict_of_dicts)
        """

        self.graf = udelej_graf_pro_jeden_rocnik(
            self.ucitele_a_jejich_seminare, self.id_seminaru_rocniku, self.zaci_a_jejich_seminare)

        color_for_all_nodes = 8  # 8 neni zadny blok - tahle barva = jeste neobarveno
        # dictionary, kde je vzdy vrchol a jeho barva - tady vsechny vrcholy stejne barevne
        colors = {node: color_for_all_nodes for node in self.graf.nodes()}
        nx.set_node_attributes(self.graf, colors, 'color')
        self.graf_dict = nx.to_dict_of_dicts(self.graf)

    def zobraz_graf(self):
        """
        Zobrazuje v okně networkx graf pro jeden ročník. Ještě neobarvený.
        """
        plt.clf()
        pos = nx.spring_layout(self.graf)  # rozmístění vrcholů a hran
        nx.draw_networkx_nodes(self.graf, pos)  # nakreslím vrcholy
        nx.draw_networkx_edges(
            self.graf, pos, edge_color="red")  # nakreslím hrany
        nx.draw_networkx_labels(self.graf, pos)
        nx.draw_networkx_edge_labels(
            self.graf, pos, edge_labels={
                (u, v): d["weight"] for u, v, d in self.graf.edges(data=True)}
        )  # u každé hrany zobrazuji její hodnotu
        nazev_okna = "graf pro " + str(self.__kolikaty[0])
        plt.get_current_fig_manager().set_window_title(nazev_okna)
        plt.box(False)
        plt.show()

    def zobraz_obarveny_graf(self, node_colors, labels):
        """
        Zobrazuje v okně networkx graf pro jeden ročník obarvený prioritizovaným barvením.
        ############################## TUDU: jsou tam opravdu třeba node_colors a labels???
        """
        plt.clf()
        pos = nx.spring_layout(self.obarveny_graf)
        # nazev_okna = "obarveny graf"
        # plt.title(nazev_okna)
        nx.draw(
            self.obarveny_graf,
            pos,
            with_labels=True,
            node_size=500,
            node_color=node_colors,
            edge_color="grey",
            font_size=12,
            font_color="#333333",
            width=2
        )
        nx.draw_networkx_edge_labels(
            self.obarveny_graf, pos, edge_labels=labels)
        nazev_okna = "obarvený graf pro " + str(self.__kolikaty[0])
        plt.get_current_fig_manager().set_window_title(nazev_okna)
        plt.box(False)
        plt.show()

    def zobraz_libovolny_graf(self, node_colors, labels, is_colored: bool):
        """
        Zobrazuje obarvený nebo neobarvený graf v networkx okně. 

        Parametry: 
            node_colors (dict):
        """

        if is_colored == True:
            jaky = "obarvený"
            graf = self.obarveny_graf
        else:
            jaky = "ještě neobarvený"
            graf = self.graf

        plt.clf()
        pos = nx.spring_layout(graf)
        # nazev_okna = "obarveny graf"
        # plt.title(nazev_okna)
        nx.draw(
            self.graf,
            pos,
            with_labels=True,
            node_size=500,
            node_color=node_colors,
            edge_color="grey",
            font_size=12,
            font_color="#333333",
            width=2
        )
        nx.draw_networkx_edge_labels(
            graf, pos, edge_labels=labels)

        nazev_okna = jaky + "graf pro" + str(self.__kolikaty[0])
        plt.get_current_fig_manager().set_window_title(nazev_okna)
        plt.box(False)
        plt.show()

    def uloz_data_pro_rocnik(self, zaci_rocniku, zaci_seminaru,
                             seminare_rocniky, vsechny_seminare, ucitele_seminaru):
        self.uloz_zaci(zaci_rocniku)
        self.uloz_poradi()
        self.uloz_ucitele(vsechny_seminare)
        self.uloz_id_seminaru_rocniku(seminare_rocniky)
        self.uloz_ucitele_a_jejich_seminare(ucitele_seminaru, vsechny_seminare)
        self.uloz_zaky_a_jejich_seminare(zaci_seminaru, vsechny_seminare)
        self.uloz_graf()

    # B = pozadovane chrom. c.
    def obarvi_graf_lip(self, B, povolene_bloky_seminaru):
        # obarvím graf
        # jaké je chromatické číslo (barevnost grafu)?
        # pokud je menší nebo stejné jako B: vratim obarveny graf a jeho chrom cislo
        # pokud je větší než B:
        # odeberu z grafu hranu s nejmenší hodnotou a opakuju predchozi kroky
        # pokud odebraná hrana má hodnotu profesora, vratim graf a jeho chrom cislo

        # vytvorim seznam hran podle velikosti - zacina hranou s nejmensi hodnotou

        # abych nezmenila puvodni graf
        pocet_odstranenych_hran = 0
        self.obarveny_graf = deepcopy(self.graf)
        serazene_hrany = sorted(self.obarveny_graf.edges(
            data=True), key=lambda x: x[2]['weight'])
        # obarvím graf hladovým barvicím algoritmem
        chrom = 0

        graph_coloring = prioritizovane_barveni(
            self.obarveny_graf, povolene_bloky_seminaru, colors=self.graf_colors, poradi=self.poradi)
        self.obarveny_graf_colors = graph_coloring
        print("BARVICKYYY znovu")
        print(self.obarveny_graf_colors)
        unique_colors = set(graph_coloring.values())
        graph_color_to_mpl_color = dict(zip(unique_colors, mpl.TABLEAU_COLORS))
        node_colors = [graph_color_to_mpl_color[graph_coloring[n]]
                       for n in self.obarveny_graf.nodes()]
        pouzite_barvy = set(node_colors)
        chrom = len(pouzite_barvy)  # chromaticke cislo = kolik barev pouzito
        labels = {e: self.obarveny_graf.edges[e]['weight']
                  for e in self.obarveny_graf.edges}
        while chrom > B:
            print(chrom)
            if len(serazene_hrany) == 0:
                raise Exception(
                    "moc malinke pozadovane chromaticke cislo :( to nejde obarvit")
            nejmensi = serazene_hrany.pop(0)  # hrana s nejmensi hodnotou
            print("ODSTRANĚNÁ HRANA" + str(nejmensi))
            self.graf.remove_edge(nejmensi[0], nejmensi[1])
            pocet_odstranenych_hran += 1
            graph_coloring = prioritizovane_barveni(
                self.obarveny_graf, povolene_bloky_seminaru, colors=self.obarveny_graf_colors)
            self.obarveny_graf_colors = graph_coloring
            print("BARVICKYYY znovu")
            print(self.obarveny_graf_colors)
            unique_colors = set(graph_coloring.values())
            graph_color_to_mpl_color = dict(
                zip(unique_colors, mpl.TABLEAU_COLORS))
            node_colors = [graph_color_to_mpl_color[graph_coloring[n]]
                           for n in self.obarveny_graf.nodes()]
            pouzite_barvy = set(node_colors)
            chrom = len(pouzite_barvy)
            labels = {e: self.obarveny_graf.edges[e]['weight']
                      for e in self.obarveny_graf.edges}
        self.obarveny_graf_dict = nx.to_dict_of_dicts(self.obarveny_graf)
        print("počet hran, které byly odstraněny při barvení grafu pro " +
              str(self.__kolikaty[0]) + "je" + str(pocet_odstranenych_hran))
        # plt.show() # zobrazí graf
        return node_colors, labels
