from nacti_vstup import *
from barveni import *

class Seminar:
    def __init__(self, id_seminare):
        self.__id_seminare = id_seminare 
        self.pro_ktere_rocniky: int = None
        self.kteri_zaci_tam_chodi: set = set()
        self.kdo_seminar_uci: set = set()
    def uloz_pro_ktere_rocniky(self, soubor_seminare): # nacita soubor seminare.csv
        df = pd.read_csv(soubor_seminare)  # načtu soubor jako dataframe
        for radek in df.iterrows():
            if radek['pro5'] == 1:
                self.pro_ktere_rocniky = 5
            if radek['pro6'] == 1:
                self.pro_ktere_rocniky = 6
            if radek['pro7'] == 1:
                self.pro_ktere_rocniky = 7
            if radek['pro8'] == 1:
                self.pro_ktere_rocniky = 8
    def uloz_kteri_zaci_tam_chodi(self, soubor_zapsani): #nacita soubor zapsani
        df = pd.read_csv(soubor_zapsani) 
        for zak, seminar in zip(df.zak, df.seminar):
            if seminar == self.__id_seminare:
                self.kteri_zaci_tam_chodi.add(zak)
    def uloz_kdo_seminar_uci(self, soubor_seminare, id_vsech_ucitelu): # nacita soubor seminare.csv a promennou id_vsech_ucitelu
        df = pd.read_csv(soubor_seminare)
        radek = self.__id_seminare
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
        
        id_ucitelu_rocniku: dict = dict()
        self.zaci: set = set() # mnozina zaku, kteri chodi do daneho rocniku
        self.zaci_kam_na_seminare: dict = dict() # dictionary ktery zak chodi na ktery seminar
        self.ucitele: set = set()  # mnozina ucitelu uci seminare daneho rocniku
        self.id_seminaru_rocniku: list = []
    
    
    """def uloz_zaci(self, zaci_rocniku):
        for rocnik in self.__kolikaty:
            self.zaci.union(zaci_rocniku[rocnik])"""
    def uloz_zaci_kam_na_seminare(self):
        self.zaci = self.zaci_kam_na_seminare.keys()
    
    def uloz_ucitele(self, ucitele_seminaru):
        for rocnik in self.__kolikaty:
            self.ucitele.union(ucitele_seminaru[rocnik])
    
    def uloz_id_seminaru_rocniku(self, seminare_rocniky):
        # udela seznam id seminaru daneho rocniku
        for rocnik in self.__kolikaty:
            self.id_seminaru_rocniku.union(seminare_rocniky[rocnik])


    def graph(self):
         graf = udelej_graf(self.ucitele, self.id_seminaru_rocniku, self.zaci)
    
    def uloz_data_pro_rocnik(self, zaci_rocniku, zaci_seminaru,
                             ucitele_seminaru, seminare_rocniky):
        self.uloz_zaci_kam_na_seminare()
        #self.uloz_zaci(zaci_rocniku)
        self.uloz_ucitele(ucitele_seminaru)
        self.uloz_id_seminaru_rocniku(seminare_rocniky)



def main():

    zaci_seminaru = nacti_zaky_seminaru("zapsani")
    zaci_rocniku = nacti_zaky_rocniku("zaci")
    id_vsech_seminaru = nacti_id_vsech_seminaru("seminare.csv")
    id_vsech_ucitelu = nacti_id_vsech_ucitelu("seminare.csv")
    print(id_vsech_ucitelu)
    seminare_rocniku = ktery_seminar_pro_ktery_rocnik("seminare.csv")
    ucitele_seminaru = nacti_ucitele_seminaru("seminare.csv")
    seminare_rocniky = ktery_seminar_pro_ktery_rocnik("seminare.csv")
    # instance pro kazdy seminar schovane v listu vsechny_seminare

    vsechny_seminare: list = []
    vsechny_seminare = [Seminar(id) for id in id_vsech_seminaru]
    for e in vsechny_seminare:
        e.uloz_data_pro_seminar("zapsani" , "seminare.csv", id_vsech_ucitelu)
    breakpoint()


    # instance: jednotlive rocniky
    kvinta_sexta = Rocnik([5,6])
    kvinta_sexta.uloz_data_pro_rocnik(zaci_rocniku, zaci_seminaru,
                             ucitele_seminaru, seminare_rocniky)
    septima = Rocnik(7)
    septima.uloz_data_pro_rocnik(zaci_rocniku, zaci_seminaru,
                             ucitele_seminaru, seminare_rocniky)
    oktava = Rocnik([8])
    oktava.uloz_data_pro_rocnik(zaci_rocniku, zaci_seminaru,
                             ucitele_seminaru, seminare_rocniky)


    # kvinta a sexta muzou byt jako jedna instance, protoze s nimi manipuluji vzdy zaroven




    """graf = udelej_graf(ucitele_seminaru, id_vsech_seminaru, zaci_seminaru)
    obarvi_graf(graf)
    obarvi_graf_lip(graf, 7)
    print(seskup_seminare_do_bloku(graf))"""
    # co kdyz misto postupneho barveni seradim kazdy seminar v barve podle majoritniho rocniku
    # a podle toho budu obsazovat bloky
    # zjistim, jake
    return


if __name__ == "__main__":
    main()