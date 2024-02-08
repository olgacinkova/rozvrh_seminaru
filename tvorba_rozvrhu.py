import pandas as pd
import networkx as nx


class Rozvrh:
    def __init__(self):
        self.bloky_ve_ktery_cas: dict = {"po7": 1, "po9": 2, "ut7": 3, "ut9": 4,
                                         "st7": 8, "ct7": 5, "ct9": 6, "pa7": 7}
        # key = ktery den od ktere vyucovaci hodiny
        # value = id bloku
        # pro kazdeho ucitele mnozina bloku, kdy nemuze
        self.povolene_bloky_seminaru: dict = dict()

    def nacti_povolene_bloky_seminaru(self, soubor):
        # nacita ze souboru seminare_kolize.csv
        # udela dict, kde ke kazdemu seminari je seznam jeho povolenych bloku
        # načtu seznam seminářů jako dataframe
        df = pd.read_csv(soubor, delimiter=';')
        id = list(df.id)  # id seminářů
        # pro kazdy seminar v jakych blocich muze byt
        bloky = list(df.bloky)
        povolene_bloky = [set(map(int, item.split(','))) for item in bloky]
        # udelam z toho list setu integeru

        for seminar in id:
            self.povolene_bloky_seminaru[seminar] = povolene_bloky.pop(0)
        print(self.povolene_bloky_seminaru)

