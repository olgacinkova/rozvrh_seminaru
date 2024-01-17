from nacti_vstup import *
from barveni import *

class Seminar:
    def __init__(self, id_seminare):
        self.__id_seminare = id_seminare 
        self.pro_ktere_rocniky: int = None
        self.kteri_zaci_tam_chodi: set = set()
        self.kdo_seminar_uci: list = []
    def uloz_pro_ktere_rocniky(self, soubor): # nacita soubor seminare.csv
        

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
    def uloz_zaci(self):
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
        self.uloz_zaci_kam_na_seminare(zaci_seminaru)
        self.uloz_zaci(zaci_rocniku)
        self.uloz_ucitele(ucitele_seminaru)
        self.uloz_id_seminaru_rocniku(seminare_rocniky)



def main():

    zaci_seminaru = nacti_zaky_seminaru("zapsani")
    zaci_rocniku = nacti_zaky_rocniku("zaci")
    id_vsech_seminaru = nacti_id_vsech_seminaru("seminare.csv")
    id_vsech_ucitelu = nacti_id_vsech_ucitelu("seminare.csv")
    seminare_rocniku = ktery_seminar_pro_ktery_rocnik("seminare.csv")
    ucitele_seminaru = nacti_ucitele_seminaru("seminare.csv")
    seminare_rocniky = ktery_seminar_pro_ktery_rocnik("seminare.csv")
   
    # instance: jednotlive rocniky
    kvinta_sexta = Rocnik([5,6])
    breakpoint()
    kvinta_sexta.uloz_data_pro_rocnik(zaci_rocniku, zaci_seminaru,
                             ucitele_seminaru, seminare_rocniky)
    breakpoint()
    septima = Rocnik(7)
    septima.uloz_data_pro_rocnik(zaci_rocniku, zaci_seminaru,
                             ucitele_seminaru, seminare_rocniky)
    breakpoint()
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