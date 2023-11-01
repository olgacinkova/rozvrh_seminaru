import pandas as pd
def nacti_zaky(soubor):
    # nacita vstupni soubor zaci.csv
    with open(soubor, encoding='utf-8-sig') as infile:
        lines = infile.readlines()
        zaci = []
    for x in lines:
        radek = x.rstrip("\n")
        radek = radek.replace("'","")
        radek = radek.split(",")
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
        lines.pop(0)
    for x in lines:
        radek = x.rstrip("\n")
        radek = radek.replace("'","")
        radek = radek.replace('"','')
        radek = radek.split(",")
        zak = int(radek[1])
        seminar = int(radek[2])
        zapsani.append([zak, seminar])
    #print(zapsani)
    return zapsani

def zak_trida(soubor):
    # nacita soubor zaci
    #do jakych trid chodi zaci
    # vystup: dict, trida : mnozina
    #  jejich zaku
    with open(soubor, encoding='utf-8-sig') as infile:
        lines = infile.readlines()
        tridy = dict()
        lines.pop(0)
    for x in lines:
        radek = x.rstrip("\n")
        radek = radek.replace("'","")
        radek = radek.replace('"','')
        radek = radek.split(",")
        trida = radek[2].replace(" ", "") # odstranim mezery z nazvu tridy
        zak = int(radek[0]) # resp id zaka
        if trida in tridy:
            tridy[trida].add(zak) # prida do mnoziny noveho zaka
        else:
            tridy[trida] =set() # vytvori novou prazdnou mnozinu
            tridy[trida].add(zak) # prida do mnoziny rovnou prvniho zaka
    return tridy

def ucitel_seminar(soubor):
    # dictionary s mnozinou seminaru pro kazdeho ucitele
    #`id`, `cislo`, `nazev`, `ucitel`, `hodin`, `anotace`, `pro5`, `pro6`, `pro7`, 
    # `pro8`, `aktivni`, `hnizdo`, `uzavreny`, `kapacita`, `rozsirujici`
    # nacita vstupni soubor zapsani
    # vystupem je pole poli, kde je vzdy zak a jeho seminar
    with open(soubor, encoding='utf-8-sig') as infile:
        lines = infile.readlines()
        seminare = []
        lines.pop(0)
    for x in lines:
        radek = x.rstrip("\n")
        radek = radek.replace("'","")
        radek = radek.replace('"','')
        radek = radek.split(",")
        ucitel = int(radek[3])
        seminar = int(radek[0])
        seminare.append([ucitel, seminar])
    #print(zapsani)
    return seminare

def id_ucitelu(soubor):
    df = pd.read_csv(soubor)
    j= df.ucitel #you can also use df['column_name']
    jmena = set()
    for jm in list(df.ucitel):
        for x in jm.split(","):
            x = x.replace(" ","")
            if x != 'bude upřesněno' or x != 'příp. M. Roháčková (podle úvazku)':
                jmena.add(x)
    print(jmena)
    ucitele = dict()
    i = 1
    for jm in jmena:
        ucitele[jm] = i
        i += 1
    print(ucitele)
    return ucitele


def main():
    #print(nacti_zapsane("zapsani.csv"))
    #print(zak_trida("zaci.csv"))
    #print(ucitel_seminar("seminare.csv"))
    print(id_ucitelu("seminare.csv"))
    return

if __name__ == "__main__":
    main()