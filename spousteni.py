from nacti_vstup import *
from barveni import *
def main():
    ks = zaci_seminare("zapsani.csv")
    kt = zaci_tridy("zaci.csv")
    ucitele, seminare, id_seminaru = id_ucitelu("seminare.csv")
    print(seminare, id_seminaru)
    graf = udelej_graf(ucitele, 
                      seminare, id_seminaru, ks)
    obarvi_graf_lip(graf, 9)
    return

if __name__ == "__main__":
    main()