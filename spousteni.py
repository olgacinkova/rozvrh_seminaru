from fce_pro_seminare_rocniky import *
from barveni import *
from seminare_rocniky import *
from matplotlib import pyplot
from copy import *
from tvorba_rozvrhu import *
from mergovani_grafu import *


def main():
    zaci_seminaru = nacti_zaky_seminaru("zapsani.csv")
    zaci_rocniku = nacti_zaky_rocniku("zaci.csv")
    id_vsech_seminaru = nacti_id_vsech_seminaru("seminare.csv")
    id_vsech_ucitelu = nacti_id_vsech_ucitelu("seminare.csv")
    ucitele_seminaru = nacti_ucitele_seminaru("seminare.csv")
    seminare_rocniky = ktery_seminar_pro_ktery_rocnik("seminare.csv")
    # instance pro kazdy seminar schovane v listu vsechny_seminare
    rozvrh = Rozvrh()
    rozvrh.nacti_povolene_bloky_seminaru("seminare_kolize.csv")

    vsechny_seminare = [Seminar(id) for id in id_vsech_seminaru]
    for e in vsechny_seminare:
        e.uloz_data_pro_seminar(
            "zapsani.csv", "seminare.csv", id_vsech_ucitelu)

    # instance: jednotlive rocniky
    # kvinta a sexta muzou byt jako jedna instance, protoze s nimi manipuluji vzdy zaroven
    kvinta_sexta = Rocnik([5, 6])
    kvinta_sexta.uloz_data_pro_rocnik(zaci_rocniku, zaci_seminaru,
                                      seminare_rocniky, vsechny_seminare, ucitele_seminaru)
    kvinta_sexta.zobraz_graf()
    # kvinta_sexta.obarvi_graf_lip(6, rozvrh.povolene_bloky_seminaru)
    kvinta_sexta.zobraz_obarveny_graf(
        *kvinta_sexta.obarvi_graf_lip(6, rozvrh.povolene_bloky_seminaru))

    septima = Rocnik(7)
    septima.uloz_data_pro_rocnik(
        zaci_rocniku, zaci_seminaru, seminare_rocniky, vsechny_seminare, ucitele_seminaru)
    septima.zobraz_graf()
    # septima.obarvi_graf_lip(6, rozvrh.povolene_bloky_seminaru)
    septima.zobraz_obarveny_graf(
        *septima.obarvi_graf_lip(6, rozvrh.povolene_bloky_seminaru))

    # breakpoint()
    oktava = Rocnik([8])
    oktava.uloz_data_pro_rocnik(zaci_rocniku, zaci_seminaru,
                                seminare_rocniky, vsechny_seminare, ucitele_seminaru)
    oktava.zobraz_graf()
    # oktava.obarvi_graf_lip(10, rozvrh.povolene_bloky_seminaru)
    oktava.zobraz_obarveny_graf(
        *oktava.obarvi_graf_lip(10, rozvrh.povolene_bloky_seminaru))

    # pozorovani:
    #   na 10 barev to jeste jde - cokoliv pod hazi errory

    # rozsirovani grafu o jednotlive rocniky a jeho obarvovani
    # chovam se jako by to byl rocnik, ale je to slepeny graf rocniku
    vsichni = Rocnik(0)
    """vsichni.graf = deepcopy(kvinta_sexta.graf)
    print("dict")
    print(vsichni.graf_dict)
    print("colors")
    print(vsichni.graf_colors)
    vsichni.zobraz_obarveny_graf(
        *vsichni.obarvi_graf_lip(6, rozvrh.povolene_bloky_seminaru))"""

    # vsichni.obarvi_graf_lip(6)
    # vsichni.zobraz_obarveny_graf()

    # do jiz obarveneho grafu, kde je zatim jen kvinta a sexta, pridam i septimu
    # vsichni.graf = deepcopy(vsichni.obarveny_graf)
    # vsichni.graf = nx.compose(septima.graf, vsichni.obarveny_graf)
    # print("septima")
    # print(septima.graf_dict)
    # print(septima.graf_colors)
    # print("kvinta_sexta")
    # print(kvinta_sexta.obarveny_graf_dict)
    # print(kvinta_sexta.obarveny_graf_colors)

    zmergovany_graf, zmergovane_barvy = merge_weighted_graphs(septima.graf_dict, septima.graf_colors,
                                                              kvinta_sexta.obarveny_graf_dict, kvinta_sexta.obarveny_graf_colors)

    vsichni.obarveny_graf = nx.from_dict_of_dicts(zmergovany_graf)
    vsichni.obarveny_graf_colors = zmergovane_barvy
    # print(vsichni.obarveny_graf)
    # print(vsichni.obarveny_graf_colors)
    # for node, data in vsichni.obarveny_graf.nodes(data=True):
    # > data jsou daty prazdna, takze to nikam
    # > nic nepriradi
    # > barvy vracis z obarvi_graf_lip jako node_colors
    # > doufam, ze jsme se neseknul...
    # if 'color' in data:
    #    vsichni.graf.nodes[node]['color'] = data['color']

    vsichni.zobraz_graf()
    vsichni.obarvi_graf_lip(6, rozvrh.povolene_bloky_seminaru)
    vsichni.zobraz_obarveny_graf(
        *vsichni.obarvi_graf_lip(6, rozvrh.povolene_bloky_seminaru))
    # vsichni.obarvi_graf_lip(7)
    # vsichni.zobraz_obarveny_graf()

    # po obarveni pridavam jeste oktavu
    vsichni.graf = nx.compose(vsichni.graf, oktava.graf)
    for node, data in vsichni.obarveny_graf.nodes(data=True):
        if 'color' in data:
            vsichni.graf.nodes[node]['color'] = data['color']

    # vsichni.graf = deepcopy(vsichni.obarveny_graf)
    vsichni.zobraz_obarveny_graf(
        *vsichni.obarvi_graf_lip(10, rozvrh.povolene_bloky_seminaru))

    return


if __name__ == "__main__":
    main()
