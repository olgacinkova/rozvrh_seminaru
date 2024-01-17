from nacti_vstup import *
from barveni import *

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
        self.seminare: set = set() # kdo chodi na ktery seminar
        self.ucitele: set = set()  # mnozina ucitelu uci seminare daneho rocniku
        self.id_seminaru_rocniku: list = []
    def uloz_zaky(self, zaci_rocniku):
        for rocnik in self.__kolikaty:
            self.zaci.union(zaci_rocniku[rocnik])
    
    def uloz_seminare(self, zaci_seminaru):
        for rocnik in self.__kolikaty:
            self.seminare.union(zaci_seminaru[rocnik])
    
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
        self.uloz_zaky(zaci_rocniku)
        self.uloz_seminare(zaci_seminaru)
        self.uloz_ucitele(ucitele_seminaru)
        self.uloz_id_seminaru_rocniku(seminare_rocniky)



def main():

    zaci_seminaru = nacti_zaky_seminaru("zapsani")
    zaci_rocniku = nacti_zaky_rocniku("zaci")
    id_vsech_seminaru = nacti_id_vsech_seminaru("seminare-fix-format.csv")
    id_vsech_ucitelu = nacti_id_vsech_ucitelu("seminare-fix-format.csv")
    seminare_rocniku = ktery_seminar_pro_ktery_rocnik("seminare-fix-format.csv")
    ucitele_seminaru = nacti_ucitele_seminaru("seminare-fix-format.csv")
    seminare_rocniky = ktery_seminar_pro_ktery_rocnik("seminare-fix-format.csv")
   
    # instance: jednotlive rocniky
    kvinta_sexta = Rocnik([5,6])
    breakpoint()
    kvinta_sexta.uloz_data_pro_rocnik(zaci_rocniku, zaci_seminaru,
                             ucitele_seminaru, seminare_rocniky)
    breakpoint()
    septima = Rocnik(7)
    oktava = Rocnik([8])


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