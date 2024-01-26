from nacti_vstup import *
from barveni import *
class Seminar:
    def __init__(self, id_seminare):
        self.__id = id_seminare 
        self.pro_ktere_rocniky: set = set() # muze byt pro vice rocniku
        self.kteri_zaci_tam_chodi: set = set()
        self.kdo_seminar_uci: set = set() # muze ucit i vice ucitelu

    @property
    def id(self):
        return self.__id

    def uloz_pro_ktere_rocniky(self, soubor_seminare): # nacita soubor seminare.csv
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
        
    def uloz_kteri_zaci_tam_chodi(self, soubor_zapsani): #nacita soubor zapsani
        df = pd.read_csv(soubor_zapsani, delimiter=';') 
        for zak, seminar in zip(df.zak, df.seminar):
            if seminar == self.__id:
                self.kteri_zaci_tam_chodi.add(zak)

    def uloz_kdo_seminar_uci(self, soubor_seminare, id_vsech_ucitelu): # nacita soubor seminare.csv a promennou id_vsech_ucitelu
        df = pd.read_csv(soubor_seminare)
        radek = self.__id -1 
        sloupec = 'ucitel'
        jmeno_ucitele = df.at[radek,sloupec]
        jmeno_ucitele = str(jmeno_ucitele)
        jmeno_ucitele = jmeno_ucitele.replace(" ", "")
        jmeno_ucitele = jmeno_ucitele.split(",") # protoze muze byt vic ucitelu na jednom seminari
        for j in jmeno_ucitele:
            id_ucitele = id_vsech_ucitelu[j]
            self.kdo_seminar_uci.add(id_ucitele)

    def uloz_data_pro_seminar(self, soubor_zapsani, soubor_seminare, id_vsech_ucitelu):
        self.uloz_kdo_seminar_uci(soubor_seminare, id_vsech_ucitelu)
        self.uloz_kteri_zaci_tam_chodi(soubor_zapsani)
        self.uloz_pro_ktere_rocniky(soubor_seminare)


class Rocnik:
    def __init__(self, kolikaty): # kvuli spojeni kvinty a sexty
        if type(kolikaty) == int:
            # aby mohl byt zadan i samostatny int a nemusel byt []
            self.__kolikaty = [kolikaty]
        elif type(kolikaty) == list:
            self.__kolikaty = kolikaty
        else:
            raise Exception("Spatny argument")
        
        self.zaci: set = set() # mnozina zaku, kteri chodi do daneho rocniku
        self.ucitele: set = set()  # mnozina ucitelu uci seminare daneho rocniku
        self.id_seminaru_rocniku: set = set()
        self.graf = None
        self.ucitele_a_jejich_seminare: dict = dict()
        self.zaci_a_jejich_seminare: dict = dict()
     
    def uloz_zaci(self, zaci_rocniku):
        for rocnik in self.__kolikaty:
            self.zaci = self.zaci.union(zaci_rocniku[rocnik])
    
    def uloz_ucitele(self, vsechny_seminare):
        for e in vsechny_seminare:
            self.ucitele = self.ucitele.union(e.kdo_seminar_uci)
    
    def uloz_id_seminaru_rocniku(self, seminare_rocniky):
        # udela seznam id seminaru daneho rocniku
        for rocnik in self.__kolikaty:
            self.id_seminaru_rocniku = self.id_seminaru_rocniku.union(seminare_rocniky[rocnik])
    
    def uloz_ucitele_a_jejich_seminare(self, ucitele_seminaru, vsechny_seminare):
        for ucitel in self.ucitele:
            mnozina_seminaru_konkretniho_ucitele = ucitele_seminaru[ucitel]
            self.ucitele_a_jejich_seminare[ucitel] = mnozina_seminaru_konkretniho_ucitele
        for mnozina in self.ucitele_a_jejich_seminare.values(): # projdu kazdemu uciteli rocniku jeho mnozinu seminaru
            for konkretni_seminar in mnozina: # pro kazdy seminar v mnozine zkontroluju, zda je pro dany rocnik
                if vsechny_seminare[konkretni_seminar - 1].pro_ktere_rocniky == self.__kolikaty: #pokud je seminar pro dany rocnik
                    self.ucitele_a_jejich_seminare[mnozina].discard(konkretni_seminar)
    
    def uloz_zaky_a_jejich_seminare(self, zaci_seminaru, vsechny_seminare):
        for zak in self.zaci:
            if zak in zaci_seminaru.keys(): # protoze zak cislo 35 tam neni
                mnozina_seminaru_konkretniho_zaka = zaci_seminaru[zak]
                self.zaci_a_jejich_seminare[zak] = mnozina_seminaru_konkretniho_zaka

        """for mnozina in self.zaci_a_jejich_seminare.values(): # projdu kazdemu zakovi rocniku jeho mnozinu seminaru
            for konkretni_seminar in mnozina: # pro kazdy seminar v mnozine zkontroluju, zda je pro dany rocnik
                breakpoint()
                if vsechny_seminare[konkretni_seminar - 1].pro_ktere_rocniky == self.__kolikaty: #pokud je seminar pro dany rocnik
                    self.zaci_a_jejich_seminare[mnozina].discard(konkretni_seminar)"""

    """def uloz_graf(self):
        self.graf = udelej_graf_pro_jeden_rocnik(self.ucitele_a_jejich_seminare, self.id_seminaru_rocniku, self.zaci)
        ### to do: udelat funkci udelej_graf jenze pro jeden rocnik
        ### zopakovat si algoritmus na prirazovani do bloku
    """
    def uloz_data_pro_rocnik(self, zaci_rocniku, zaci_seminaru, seminare_rocniky, vsechny_seminare, ucitele_seminaru):
        self.uloz_zaci(zaci_rocniku)
        self.uloz_ucitele(vsechny_seminare)
        self.uloz_id_seminaru_rocniku(seminare_rocniky)
        self.uloz_ucitele_a_jejich_seminare(ucitele_seminaru, vsechny_seminare)
        self.uloz_zaky_a_jejich_seminare(zaci_seminaru, vsechny_seminare)
        #self.uloz_graf()