from fce_pro_seminare_rocniky import *
from barveni import *
from seminare_rocniky import *
from tvorba_rozvrhu import *
from spojovani_grafu import *
from uloz_do_csv import *
from networkx import greedy_color
# to importuju kvuli konci kodu
from collections import defaultdict
from ocislovani import modify_id_column


def pocty(barvy):
    pocitadlo = {}
    for barva in barvy:
        if barva in pocitadlo:
            pocitadlo[barva] += 1
        else:
            pocitadlo[barva] = 1
    print(pocitadlo)


def main():
    # správně očísluju vstupní tabulky
    modify_id_column("seminare_kolize.csv", "zapsani.csv")
    zaci_seminaru = nacti_zaky_seminaru("ocislovane_zapsani.csv")
    zaci_rocniku = nacti_zaky_rocniku("zaci.csv")
    id_vsech_seminaru = nacti_id_vsech_seminaru(
        "ocislovane_seminare_kolize.csv")
    id_vsech_ucitelu = nacti_id_vsech_ucitelu("ocislovane_seminare_kolize.csv")
    # print(f"id_vsech_ucitelu: {id_vsech_ucitelu}")
    ucitele_seminaru = nacti_ucitele_seminaru("ocislovane_seminare_kolize.csv")
    seminare_rocniky = ktery_seminar_pro_ktery_rocnik(
        "ocislovane_seminare_kolize.csv")

    # instance pro kazdy seminar schovane v listu vsechny_seminare
    rozvrh = Rozvrh()
    rozvrh.nacti_povolene_bloky_seminaru("ocislovane_seminare_kolize.csv")

    vsechny_seminare = [Seminar(id) for id in id_vsech_seminaru]
    for e in vsechny_seminare:
        e.uloz_data_pro_seminar(
            "ocislovane_zapsani.csv", "ocislovane_seminare_kolize.csv", id_vsech_ucitelu)

    # instance: jednotlive rocniky
    # kvinta a sexta muzou byt jako jedna instance, protoze s nimi manipuluji vzdy zaroven
    kvinta_sexta = Rocnik([5, 6])
    kvinta_sexta.uloz_data_pro_rocnik(zaci_rocniku, zaci_seminaru,
                                      seminare_rocniky, vsechny_seminare, ucitele_seminaru)
    kvinta_sexta.zobraz_graf()
    kvinta_sexta.zobraz_obarveny_graf(
        *kvinta_sexta.obarvi_graf_lip(2, rozvrh.povolene_bloky_seminaru))  # meli by se vejit do dvou bloku
    septima = Rocnik(7)

    septima.uloz_data_pro_rocnik(
        zaci_rocniku, zaci_seminaru, seminare_rocniky, vsechny_seminare, ucitele_seminaru)
    septima.zobraz_graf()

    oktava = Rocnik([8])
    oktava.uloz_data_pro_rocnik(zaci_rocniku, zaci_seminaru,
                                seminare_rocniky, vsechny_seminare, ucitele_seminaru)
    oktava.zobraz_graf()
    # rozsirovani grafu o jednotlive rocniky a jeho obarvovani
    # chovam se jako by to byl rocnik, ale je to slepeny graf rocniku
    vsichni = Rocnik(0)
    vsichni.poradi = septima.poradi
    zmergovany_graf_dict, zmergovane_barvy = merge_weighted_graphs(septima.graf_dict, septima.graf_colors,
                                                                   kvinta_sexta.obarveny_graf_dict, kvinta_sexta.obarveny_graf_colors)
    vsichni.graf_dict = zmergovany_graf_dict
    vsichni.graf = nx.from_dict_of_dicts(zmergovany_graf_dict)
    vsichni.graf_colors = zmergovane_barvy
    vsichni.zobraz_obarveny_graf(
        *vsichni.obarvi_graf_lip(7, rozvrh.povolene_bloky_seminaru))

    vsichni.poradi = oktava.poradi
    # po obarveni pridavam jeste oktavu
    zmergovany_graf_dict, zmergovane_barvy = merge_weighted_graphs(oktava.graf_dict, oktava.graf_colors,
                                                                   vsichni.obarveny_graf_dict, vsichni.obarveny_graf_colors)

    vsichni.graf_dict = zmergovany_graf_dict
    vsichni.graf = nx.from_dict_of_dicts(zmergovany_graf_dict)
    vsichni.graf_colors = zmergovane_barvy
    vsichni.zobraz_obarveny_graf(
        *vsichni.obarvi_graf_lip(7, rozvrh.povolene_bloky_seminaru))

    # kolik jsme pouzili barev - resp. na kolik je to bloku
    colors_set = set(vsichni.obarveny_graf_colors.values())
    pocty(vsichni.obarveny_graf_colors.values())
    pocet_barev = len(colors_set)
    print(f"pocet bloku je {pocet_barev}")
    uloz_do_csv(vsichni.obarveny_graf_colors, "vystup.csv")

    # nasledujici kod jen tiskne na terminal pro lepsi pochopeni
    # tiskne dictionary rozvrh_dict, kde je jako key vzdy blok a jako value mnozina seminare, ktere v danem bloku jsou
    color_dict = defaultdict(set)
    for id, color in vsichni.obarveny_graf_colors.items():
        color_dict[color].add(id)
    print(
        f"zde dictionary, kde je vzdy blok a mnozina jeho seminaru: {color_dict}")

    return


if __name__ == "__main__":
    main()
