from fce_pro_seminare_rocniky import *
from barveni import *
from seminare_rocniky import *
from tvorba_rozvrhu import *
from mergovani_grafu import *
from uloz_do_csv import *

#### zapsat do grafu jako hodnoty hran pozadavky ucitelu 
# zaspat si to jako atribut vrcholu

###### vyhodit sprachdiplomy

###### ma byt cca 9 bloku

###### pridat do barvici funkce do poradi vic bloku 

###### vyfiltrovat si seminare z druheho kola a pracovat jen s nimi (jsou v kolizich)

####### zacit s vlastni praci

#### instalace v uziv dokumentace: jak stahnu z githubu, co knihovny a pip
### v uvodu proc vubec barvim
###### najit si kolik stranek tam mam byt
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
    print(kvinta_sexta.obarveny_graf_colors)
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

    zmergovany_graf_dict, zmergovane_barvy = merge_weighted_graphs(septima.graf_dict, septima.graf_colors,
                                                              kvinta_sexta.obarveny_graf_dict, kvinta_sexta.obarveny_graf_colors)

    print(zmergovany_graf_dict)
    print(zmergovane_barvy)
    """vsichni.graf_dict = zmergovany_graf_dict
    vsichni.graf = nx.from_dict_of_dicts(zmergovany_graf_dict)
    vsichni.graf_colors = zmergovane_barvy
    print(vsichni.graf)
    print(vsichni.graf_colors)"""
    vsichni.graf_dict = zmergovany_graf_dict
    vsichni.graf = nx.from_dict_of_dicts(zmergovany_graf_dict)
    vsichni.graf_colors = zmergovane_barvy
    print(vsichni.graf_colors)
    vsichni.zobraz_obarveny_graf(
        *vsichni.obarvi_graf_lip(20, rozvrh.povolene_bloky_seminaru))

    # po obarveni pridavam jeste oktavu
    zmergovany_graf_dict, zmergovane_barvy = merge_weighted_graphs(oktava.graf_dict, oktava.graf_colors,
                                                              vsichni.obarveny_graf_dict, vsichni.obarveny_graf_colors)

    print(zmergovany_graf_dict)
    print(zmergovane_barvy)
    vsichni.graf_dict = zmergovany_graf_dict
    vsichni.graf = nx.from_dict_of_dicts(zmergovany_graf_dict)
    vsichni.graf_colors = zmergovane_barvy
    vsichni.zobraz_obarveny_graf(
        *vsichni.obarvi_graf_lip(20, rozvrh.povolene_bloky_seminaru))
    
    print("posledni obarveni")
    print(vsichni.obarveny_graf_dict)
    print(vsichni.obarveny_graf_colors)

    uloz_do_csv(vsichni.obarveny_graf_colors, "vystup.csv")
    return


if __name__ == "__main__":
    main()
