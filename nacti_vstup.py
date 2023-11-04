import pandas as pd
def nacti_zaky(soubor):
    # nacita vstupni soubor zaci.csv
    df = pd.read_csv(soubor)
    id = list(df.id) # id zaku
    tridy = list(df.trida) # kam patri
    zaci = []
    for i in range(len(id)):
        zak = id.pop(0)
        trida = tridy.pop(0)
        zaci[zak] = trida
    return zaci

def zak_trida(soubor):
    # nacita soubor zaci
    #do jakych trid chodi zaci
    # vystup: dict, trida : mnozina jejich zaku
    df = pd.read_csv(soubor)
    id = list(df.id) # id zaku
    tridy = list(df.trida) # kam patri
    kam_trida = dict()
    for i in range(len(id)):
        trida = tridy.pop(0).replace(" ", "")
        zak = id. pop(0) #id zaka
        if trida in kam_trida:
            kam_trida[trida].add(zak) # prida do mnoziny noveho zaka
        else:
            kam_trida[trida] =set() # vytvori novou prazdnou mnozinu
            kam_trida[trida].add(zak) # prida do mnoziny rovnou prvniho zaka
    return kam_trida

def nacti_zapsane(soubor):
    # nacita vstupni soubor zapsani.csv
    # vystupem je dict, kde je vzdy zak a jeho seminare
    df = pd.read_csv(soubor)
    id = list(df.zak) # id zaka
    seminare = list(df.seminar) # kam patri
    kam_seminar = dict()
    for i in range(len(id)):
        zak = id.pop(0)
        seminar = seminare.pop(0)
        if zak in kam_seminar:
            kam_seminar[zak].add(seminar) # prida do mnoziny novy seminar
        else:
            kam_seminar[zak] =set() # vytvori novou prazdnou mnozinu
            kam_seminar[zak].add(seminar) 
    return kam_seminar

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

def udelej_graf(ucitele, seminare):
    pass

        
    

def main():
    print(nacti_zapsane("zapsani.csv"))
    #print(zak_trida("zaci.csv"))
    #print(ucitel_seminar("seminare.csv"))
    #print(id_ucitelu("seminare.csv"))
    return

if __name__ == "__main__":
    main()