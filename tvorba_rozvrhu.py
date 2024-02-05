class Rozvrh:
    def __init__(self):
        self.bloky_ve_ktery_cas:dict = dict()
        self.kteri_ucitele_nemohou_kdy: dict = dict() # pro kazdeho ucitele mnozina bloku, kdy nemuze
