from nacti_vstup import *
from barveni import *

def main():

    zaci_seminaru = nacti_zaky_seminaru("zapsani.csv")
    print(zaci_seminaru.keys())
    
    zaci_rocniku = nacti_zaky_rocniku("zaci.csv")
    id_vsech_seminaru = nacti_id_vsech_seminaru("seminare.csv")
    id_vsech_ucitelu = nacti_id_vsech_ucitelu("seminare.csv")
    seminare_rocniku = ktery_seminar_pro_ktery_rocnik("seminare.csv")
    ucitele_seminaru = nacti_ucitele_seminaru("seminare.csv")
    seminare_rocniky = ktery_seminar_pro_ktery_rocnik("seminare.csv")
    # instance pro kazdy seminar schovane v listu vsechny_seminare

    vsechny_seminare = [Seminar(id) for id in id_vsech_seminaru]
    for e in vsechny_seminare:
        e.uloz_data_pro_seminar("zapsani.csv" , "seminare.csv", id_vsech_ucitelu)

        #print(vars(e)) # tisknu si hodnoty z instanci


    # instance: jednotlive rocniky
    kvinta_sexta = Rocnik([5,6])
    kvinta_sexta.uloz_data_pro_rocnik(zaci_rocniku, zaci_seminaru,
                            seminare_rocniky, vsechny_seminare, ucitele_seminaru)

    septima = Rocnik(7)
    septima.uloz_data_pro_rocnik(zaci_rocniku, zaci_seminaru, seminare_rocniky, vsechny_seminare, ucitele_seminaru)
    oktava = Rocnik([8])
    oktava.uloz_data_pro_rocnik(zaci_rocniku, zaci_seminaru,
                        seminare_rocniky, vsechny_seminare, ucitele_seminaru)
    breakpoint()
    # kvinta a sexta muzou byt jako jedna instance, protoze s nimi manipuluji vzdy zaroven



    """graf = udelej_graf(ucitele_seminaru, id_vsech_seminaru, zaci_seminaru)
    obarvi_graf(graf)
    obarvi_graf_lip(graf, 7)
    print(seskup_seminare_do_bloku(graf))"""
    # co kdyz misto postupneho barveni seradim kazdy seminar v barve podle majoritniho rocniku
    # a podle toho budu obsazovat bloky
    # zjistim, jake
    return


if __name__ == "__main__":
    main()