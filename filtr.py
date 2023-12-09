# filtruje vsechna data podle trid 
# asi by to slo vyresit i elegantneji - tohle je provizorni...
from nacti_vstup import *
from barveni import *
def kvinta(kam_rocnik, rocnik_seminar, kam_seminar, seminare):
    zaci_kvinty = kam_rocnik[5] # mnozina zaku z rocniku
    kvinta_seminare = rocnik_seminar[5]
    ucitele_kvinta = dict()
    for ucitel in seminare.keys():
        seminare_ucitele = seminare[ucitel] 
        overlap = seminare_ucitele.intersection(kvinta_seminare)
        if len(overlap) > 0:
            ucitele_kvinta[ucitel] = overlap
    kam_kvintani = dict()
    for zak in zaci_kvinty:
        aktualni_seminare = kam_seminar[zak]
        kam_kvintani[zak] = aktualni_seminare
    return ucitele_kvinta, kvinta_seminare, zaci_kvinty


def main():
    ks = zaci_seminare("zapsani.csv")
    kt = zaci_tridy("zaci.csv")
    print(kt)
    print(ktery_seminar_pro_kterou_tridu("seminare.csv"))
    ucitele, seminare, id_seminaru = id_ucitelu("seminare.csv")
    print(seminare, id_seminaru)
    graf = udelej_graf(seminare, id_seminaru, ks)
    obarvi_graf_lip(graf, 4)
    return

if __name__ == "__main__":
    main()