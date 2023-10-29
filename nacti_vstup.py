def nacti_zaky(soubor):
    # nacita vstupni soubor zaci.csv
    with open(soubor, encoding='utf-8-sig') as infile:
        lines = infile.readlines()
        zaci = []
    for x in lines:
        radek = x.rstrip("\n")
        radek = radek.replace("'","")
        radek = radek.split(";")
        id, jmeno, trida, uzivjmeno = radek
        zaci.append(id, trida)
    print(zaci)
    return

def nacti_zapsane(soubor):
    # nacita vstupni soubor zapsani
    # vystupem je pole poli, kde je vzdy zak a jeho seminar
    with open(soubor, encoding='utf-8-sig') as infile:
        lines = infile.readlines()
        zapsani = []
    for x in lines:
        radek = x.rstrip("\n")
        radek = radek.replace("'","")
        radek = radek.split(";")
        zak = int(radek[1])
        seminar = int(radek[2])
        zapsani.append([zak, seminar])
    #print(zapsani)
    return zapsani

def zak_trida(soubor):
    # nacita soubor zaci
    #do jakych trid chodi zaci
    # vystup: dict, trida : mnozina jejich zaku
    with open(soubor, encoding='utf-8-sig') as infile:
        lines = infile.readlines()
        tridy = dict()
    for x in lines:
        radek = x.rstrip("\n")
        radek = radek.replace("'","")
        radek = radek.split(";")
        trida = radek[2].replace(" ", "") # odstranim mezery z nazvu tridy
        zak = int(radek[0]) # resp id zaka
        if trida in tridy:
            tridy[trida].add(zak) # prida do mnoziny noveho zaka
        else:
            tridy[trida] =set() # vytvori novou prazdnou mnozinu
            tridy[trida].add(zak) # prida do mnoziny rovnou prvniho zaka
    return tridy
        



def main():
    nacti_zapsane("zapsani")
    print(zak_trida("zaci"))
    return

if __name__ == "__main__":
    main()