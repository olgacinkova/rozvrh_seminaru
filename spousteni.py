from nacti_vstup import *
from barveni import *
def main():

    # zalozit rocnikove objekty
    # Rocnik([5,6]), Rocnik(7), Rocnik(8)
    # dict: rocnik to objekt rocniku
    # 5 ->  Rocnik([5,6])
    # 6 ->  Rocnik([5,6])
    # 7 ->  Rocnik(7)
    # ...
    # poslat mapu do nacitacich fci
    zaci_seminare = nacti_zaky_seminare("zapsani")
    tridy = zaci_tridy("zaci")
    ktery_seminar_pro_ktery_rocnik("seminare.csv")
    ucitele, seminare, id_seminaru = id_ucitelu("seminare.csv")

    # rozšťouchat do objektu

    graf = udelej_graf(seminare, id_seminaru, zaci_seminare)
    obarvi_graf(graf)
    obarvi_graf_lip(graf, 7)
    print(seskup_seminare_do_bloku(graf))
    return

if __name__ == "__main__":
    main()