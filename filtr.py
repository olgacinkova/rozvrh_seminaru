# filtruje vsechna data podle trid 
# asi by to slo vyresit i elegantneji - tohle je provizorni...
from nacti_vstup import *
from barveni import *

def rocnik(cislo_rocniku, kam_rocnik, rocnik_seminar, kam_seminar, seminare):
    zaci_rocniku = kam_rocnik[cislo_rocniku] # mnozina zaku z rocniku
    rocnik_seminare = rocnik_seminar[cislo_rocniku] # jake seminare pro rocnik
    ucitele_rocniku = dict() # jaci ucitele pro rocnik
    for ucitel in seminare.keys():
        seminare_ucitele = seminare[ucitel] 
        overlap = seminare_ucitele.intersection(rocnik_seminare)
        if len(overlap) > 0:
            ucitele_rocniku[ucitel] = overlap
    kam_kvintani = dict()
    for zak in zaci_rocniku:
        aktualni_seminare = kam_seminar[zak]
        kam_kvintani[zak] = aktualni_seminare
    return ucitele_rocniku, rocnik_seminare, zaci_rocniku, kam_kvintani

def kvinta(kam_rocnik, rocnik_seminar, kam_seminar, seminare):
    zaci_kvinty = kam_rocnik[5] # mnozina zaku z rocniku
    kvinta_seminare = rocnik_seminar[5] # jake seminare pro rocnik
    ucitele_kvinta = dict() # jaci ucitele pro rocnik
    for ucitel in seminare.keys():
        seminare_ucitele = seminare[ucitel] 
        overlap = seminare_ucitele.intersection(kvinta_seminare)
        if len(overlap) > 0:
            ucitele_kvinta[ucitel] = overlap
    kam_kvintani = dict()
    for zak in zaci_kvinty:
        aktualni_seminare = kam_seminar[zak]
        kam_kvintani[zak] = aktualni_seminare
    return ucitele_kvinta, kvinta_seminare, zaci_kvinty, kam_kvintani


def main():
    ks = nacti_zaky_seminaru("zapsani.csv")
    kt = nacti_zaky_rocniku("zaci.csv")
    #kvinta = rocnik(cislo_rocniku, kam_rocnik, rocnik_seminar, kam_seminar, seminare)
    print(kt)
    print(ktery_seminar_pro_ktery_rocnik("seminare.csv"))
    ucitele, seminare, id_seminaru = nacti_id_ucitelu("seminare.csv")
    print(seminare, id_seminaru)
    graf = udelej_graf(seminare, id_seminaru, ks)
    obarvi_graf_lip(graf, 8)
    return

if __name__ == "__main__":
    main()