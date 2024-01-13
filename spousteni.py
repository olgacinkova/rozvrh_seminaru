from nacti_vstup import *
from barveni import *

class Rocnik:
    def __init__(self, kolikaty: [int]): # kvuli spojeni kvinty a sexty
        self.__kolikaty = kolikaty # kolikaty je to rocnik
        self.zaci = None
        self.seminare = None
        self.ucitele = None

def main():

    zaci_seminaru = nacti_zaky_seminaru("zapsani")
    zaci_rocniku = nacti_zaky_rocniku("zaci")
    id_vsech_seminaru = nacti_id_vsech_seminaru("seminare.csv")
    id_vsech_ucitelu = nacti_id_vsech_ucitelu("seminare.csv")
    seminare_rocniku = ktery_seminar_pro_ktery_rocnik("seminare.csv")
    ucitele_seminaru = nacti_id_ucitelu("seminare.csv")
    
    # rozšťouchat do objektu
    kvinta_sexta = Rocnik([5, 6]) 
    # kvinta a sexta muzou byt jako jedna instance, protoze s nimi manipuluji vzdy zaroven
    septima = Rocnik([7])
    oktava = Rocnik([8])
    septima.zaci = zaci_rocniku[7]
    graf = udelej_graf(zaci_seminaru)
    obarvi_graf(graf)
    obarvi_graf_lip(graf, 7)
    print(seskup_seminare_do_bloku(graf))
    return

if __name__ == "__main__":
    main()