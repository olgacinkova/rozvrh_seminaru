from fce_pro_seminare_rocniky import *
from barveni import *
from seminare_rocniky import *
from copy import *
from tvorba_rozvrhu import *


def main():
    zaci_seminaru = nacti_zaky_seminaru("zapsani.csv")
    zaci_rocniku = nacti_zaky_rocniku("zaci.csv")
    id_vsech_seminaru = nacti_id_vsech_seminaru("seminare.csv")
    id_vsech_ucitelu = nacti_id_vsech_ucitelu("seminare.csv")
    seminare_rocniku = ktery_seminar_pro_ktery_rocnik("seminare.csv")
    ucitele_seminaru = nacti_ucitele_seminaru("seminare.csv")
    seminare_rocniky = ktery_seminar_pro_ktery_rocnik("seminare.csv")
    # instance pro kazdy seminar schovane v listu vsechny_seminare

    vsechny_seminare = [Seminar(id) for id in id_vsech_seminaru]
    for e in vsechny_seminare:
        e.uloz_data_pro_seminar(
            "zapsani.csv", "seminare.csv", id_vsech_ucitelu)

    # instance: jednotlive rocniky
    # kvinta a sexta muzou byt jako jedna instance, protoze s nimi manipuluji vzdy zaroven
    kvinta_sexta = Rocnik([5, 6])
    kvinta_sexta.uloz_data_pro_rocnik(zaci_rocniku, zaci_seminaru,
                                      seminare_rocniky, vsechny_seminare, ucitele_seminaru)
    # kvinta_sexta.zobraz_graf()
    # kvinta_sexta.obarvi_graf_lip(6)
    # kvinta_sexta.zobraz_obarveny_graf(*kvinta_sexta.obarvi_graf_lip(6))

    septima = Rocnik(7)
    septima.uloz_data_pro_rocnik(
        zaci_rocniku, zaci_seminaru, seminare_rocniky, vsechny_seminare, ucitele_seminaru)
    # septima.zobraz_graf()
    # septima.obarvi_graf_lip(6)
    # septima.zobraz_obarveny_graf(*septima.obarvi_graf_lip(6))

    # breakpoint()
    oktava = Rocnik([8])
    oktava.uloz_data_pro_rocnik(zaci_rocniku, zaci_seminaru,
                                seminare_rocniky, vsechny_seminare, ucitele_seminaru)
    # oktava.zobraz_graf()
    # oktava.obarvi_graf_lip(10)
    # oktava.zobraz_obarveny_graf(*oktava.obarvi_graf_lip(10))

    # pozorovani:
    #   na 10 barev to jeste jde - cokoliv pod hazi errory

    rozvrh = Rozvrh()
    rozvrh.nacti_povolene_bloky_seminaru("seminare_kolize.csv")

    # rozsirovani grafu o jednotlive rocniky a jeho obarvovani
    # chovam se jako by to byl rocnik, ale je to slepeny graf rocniku
    vsichni = Rocnik(0)
    vsichni.graf = deepcopy(kvinta_sexta.graf)
    vsichni.zobraz_obarveny_graf(*vsichni.obarvi_graf_lip(6, rozvrh.povolene_bloky_seminaru))
    # vsichni.obarvi_graf_lip(6)
    # vsichni.zobraz_obarveny_graf()

    # do jiz obarveneho grafu, kde je zatim jen kvinta a sexta, pridam i septimu
    vsichni.graf = deepcopy(vsichni.obarveny_graf)
    breakpoint()
    vsichni.graf = nx.compose(vsichni.graf, septima.graf)
    vsichni.zobraz_obarveny_graf(*vsichni.obarvi_graf_lip(7, rozvrh.povolene_bloky_seminaru))
    # vsichni.obarvi_graf_lip(7)
    # vsichni.zobraz_obarveny_graf()

    # po obarveni pridavam jeste oktavu
    vsichni.graf = nx.compose(vsichni.graf, oktava.graf)
    vsichni.graf = deepcopy(vsichni.obarveny_graf)
    vsichni.zobraz_obarveny_graf(*vsichni.obarvi_graf_lip(10, rozvrh.povolene_bloky_seminaru))

    return


if __name__ == "__main__":
    main()
