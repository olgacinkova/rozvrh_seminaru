from fce_pro_seminare_rocniky import *
# from barveni import *
from copy import *
from prioritizace_barev import prioritizovane_barveni


class Seminar:
    def __init__(self, id_seminare):
        self.__id = id_seminare
        self.pro_ktere_rocniky: set = set()  # muze byt pro vice rocniku
        self.kteri_zaci_tam_chodi: set = set()
        self.kdo_seminar_uci: set = set()  # muze ucit i vice ucitelu

    @property
    def id(self):
        return self.__id

    def uloz_pro_ktere_rocniky(self, soubor_seminare):  # nacita soubor seminare.csv
        df = pd.read_csv(soubor_seminare)  # načtu soubor jako dataframe
        index = self.__id - 1
        radek = df.loc[index]
        if radek['pro5'] == 1:
            self.pro_ktere_rocniky.add(5)
        if radek['pro6'] == 1:
            self.pro_ktere_rocniky.add(6)
        if radek['pro7'] == 1:
            self.pro_ktere_rocniky.add(7)
        if radek['pro8'] == 1:
            self.pro_ktere_rocniky.add(8)

    def uloz_kteri_zaci_tam_chodi(self, soubor_zapsani):  # nacita soubor zapsani
        df = pd.read_csv(soubor_zapsani, delimiter=';')
        for zak, seminar in zip(df.zak, df.seminar):
            if seminar == self.__id:
                self.kteri_zaci_tam_chodi.add(zak)

    # nacita soubor seminare.csv a promennou id_vsech_ucitelu
    def uloz_kdo_seminar_uci(self, soubor_seminare, id_vsech_ucitelu):
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
            self.kdo_seminar_uci.add(id_ucitele)

    def uloz_data_pro_seminar(self, soubor_zapsani, soubor_seminare, id_vsech_ucitelu):
        self.uloz_kdo_seminar_uci(soubor_seminare, id_vsech_ucitelu)
        self.uloz_kteri_zaci_tam_chodi(soubor_zapsani)
        self.uloz_pro_ktere_rocniky(soubor_seminare)


class Rocnik:
    def __init__(self, kolikaty):  # kvuli spojeni kvinty a sexty
        if type(kolikaty) == int:
            # aby mohl byt zadan i samostatny int a nemusel byt []
            self.__kolikaty = [kolikaty]
        elif type(kolikaty) == list:
            self.__kolikaty = kolikaty
        else:
            raise Exception("Spatny argument")

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
        for rocnik in self.__kolikaty:
            self.zaci = self.zaci.union(zaci_rocniku[rocnik])

    def uloz_ucitele(self, vsechny_seminare):
        for e in vsechny_seminare:
            self.ucitele = self.ucitele.union(e.kdo_seminar_uci)

    def uloz_id_seminaru_rocniku(self, seminare_rocniky):
        # udela seznam id seminaru daneho rocniku
        for rocnik in self.__kolikaty:
            self.id_seminaru_rocniku = self.id_seminaru_rocniku.union(
                seminare_rocniky[rocnik])

    def uloz_ucitele_a_jejich_seminare(self, ucitele_seminaru, vsechny_seminare):
        for ucitel in self.ucitele:
            mnozina_seminaru_konkretniho_ucitele = ucitele_seminaru[ucitel]
            self.ucitele_a_jejich_seminare[ucitel] = mnozina_seminaru_konkretniho_ucitele
        # projdu kazdemu uciteli rocniku jeho mnozinu seminaru
        for mnozina in self.ucitele_a_jejich_seminare.values():
            for konkretni_seminar in mnozina:  # pro kazdy seminar v mnozine zkontroluju, zda je pro dany rocnik
                # pokud je seminar pro dany rocnik
                if vsechny_seminare[konkretni_seminar - 1].pro_ktere_rocniky == self.__kolikaty:
                    self.ucitele_a_jejich_seminare[mnozina].discard(
                        konkretni_seminar)

    def uloz_zaky_a_jejich_seminare(self, zaci_seminaru, vsechny_seminare):
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
        self.graf = udelej_graf_pro_jeden_rocnik(
            self.ucitele_a_jejich_seminare, self.id_seminaru_rocniku, self.zaci_a_jejich_seminare)

        color_for_all_nodes = 8  # 8 neni zadny blok - tahle barva = jeste neobarveno
        # dictionary, kde je vzdy vrchol a jeho barva - tady vsechny vrcholy stejne barevne
        colors = {node: color_for_all_nodes for node in self.graf.nodes()}
        nx.set_node_attributes(self.graf, colors, 'color')

        self.graf_dict = nx.to_dict_of_dicts(self.graf)

    def zobraz_graf(self):
        nazev_okna = "graf pro " + str(self.__kolikaty[0])
        print(self.graf_dict)
        plt.get_current_fig_manager().set_window_title(nazev_okna)
        # plt.title(nazev_okna)
        pos = nx.spring_layout(self.graf)  # rozmístění vrcholů a hran
        nx.draw_networkx_nodes(self.graf, pos)  # nakreslím vrcholy
        nx.draw_networkx_edges(
            self.graf, pos, edge_color="red")  # nakreslím hrany
        nx.draw_networkx_labels(self.graf, pos)
        nx.draw_networkx_edge_labels(
            self.graf, pos, edge_labels={
                (u, v): d["weight"] for u, v, d in self.graf.edges(data=True)}
        )  # u každé hrany zobrazuji její hodnotu
        plt.box(False)
        # plt.show()
        # self.graf.show()
        plt.show()

    def zobraz_obarveny_graf(self, node_colors, labels):
        print(self.obarveny_graf_dict)
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

        # nazev_okna = str(self.__kolikaty) + "obarveny graf"
        nazev_okna = "obarvený graf pro " + str(self.__kolikaty[0])
        plt.get_current_fig_manager().set_window_title(nazev_okna)
        # plt.title(nazev_okna)
       # self.obarveny_graf.show()
        plt.show()

    def uloz_data_pro_rocnik(self, zaci_rocniku, zaci_seminaru,
                             seminare_rocniky, vsechny_seminare, ucitele_seminaru):
        self.uloz_zaci(zaci_rocniku)
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
        self.obarveny_graf = deepcopy(self.graf)
        serazene_hrany = sorted(self.obarveny_graf.edges(
            data=True), key=lambda x: x[2]['weight'])
        # obarvím graf hladovým barvicím algoritmem
        chrom = 0
        graph_coloring = prioritizovane_barveni(
            self.obarveny_graf, povolene_bloky_seminaru, colors= self.graf_colors)
        unique_colors = set(graph_coloring.values())
        graph_color_to_mpl_color = dict(zip(unique_colors, mpl.TABLEAU_COLORS))
        node_colors = [graph_color_to_mpl_color[graph_coloring[n]]
                       for n in self.obarveny_graf.nodes()]
        pouzite_barvy = set(node_colors)
        chrom = len(pouzite_barvy)  # chromaticke cislo = kolik barev pouzito
        labels = {e: self.obarveny_graf.edges[e]['weight']
                  for e in self.obarveny_graf.edges}
        while chrom > B:
            if len(serazene_hrany) == 0:
                raise Exception(
                    "moc malinke pozadovane chromaticke cislo :( to nejde obarvit")
            nejmensi = serazene_hrany.pop(0)  # hrana s nejmensi hodnotou
            self.graf.remove_edge(nejmensi[0], nejmensi[1])
            graph_coloring = prioritizovane_barveni(
                self.obarveny_graf, povolene_bloky_seminaru, colors= self.obarveny_graf_colors)
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

        print("obarveno")

        # plt.show() # zobrazí graf
        return (node_colors, labels)
