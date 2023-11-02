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

def id_ucitelu(soubor):
    # bere na vstupu seznam seminaru s uciteli
    # ke kazdemu uciteli vymysli id cislo
    # vystup dict, kde je ke kazdemu uciteli 
    # mnozina seminaru, ktere uci
    df = pd.read_csv(soubor)
    s = list(df.id) # id seminaru
    j= list(df.ucitel) # jmena ucitelu
    jmena = set()
    for jm in j:
        for x in jm.split(","): # obcas je nekde vic ucitelu u jednoho seminare
            x = x.replace(" ","")
            jmena.add(x)
    ucitele = dict()
    i = 1
    for jm in jmena:
        ucitele[jm] = i
        i += 1
    print(ucitele)
    ## odstranim to, co tam dela neplechu, co je nejednoznacne
    #del ucitele['budeupřesněno']
    #del ucitele['příp.M.Roháčková(podleúvazku)']
    seminare = dict()
    for x in range(len(s)):
        seminar = s.pop(0)
        ucitel = j.pop(0)
        ucitel = ucitel.replace(' ','') 
        ucitel = ucitel.split(",") # blbne to, kdyz je ucitelu u jednoho seminare vic nez jeden
        print(ucitel)
        if type(ucitel) == list:
            for x in ucitel:
                id_ucitele = ucitele[x]
                if id_ucitele in seminare:
                    seminare[id_ucitele].add(seminar)
                else:
                    seminare[id_ucitele] = set()
                    seminare[id_ucitele].add(seminar)
        else:
            id_ucitele = ucitele[ucitel]
            if id_ucitele in seminare:
                seminare[id_ucitele].add(seminar)
            else:
                seminare[id_ucitele] = set()
                seminare[id_ucitele].add(seminar)

    return ucitele, seminare

        
    



def main():
    #print(nacti_zapsane("zapsani.csv"))
    #print(zak_trida("zaci.csv"))
    #print(ucitel_seminar("seminare.csv"))
    print(id_ucitelu("seminare.csv"))
    return

if __name__ == "__main__":
    main()