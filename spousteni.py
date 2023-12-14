from nacti_vstup import *
from barveni import *
def main():
    ks = zaci_seminare("zapsani.csv")
    kt = zaci_tridy("zaci.csv")
    ktery_seminar_pro_ktery_rocnik("seminare.csv")
    ucitele, seminare, id_seminaru = id_ucitelu("seminare.csv")
    graf = udelej_graf(seminare, id_seminaru, ks)
    obarvi_graf_lip(graf, 4)
    print(seskup_seminare_do_bloku(graf))
    return

if __name__ == "__main__":
    main()