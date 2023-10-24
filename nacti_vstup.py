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
    # nacita vstupni soubor zapsani.csv
    with open(soubor, encoding='utf-8-sig') as infile:
        lines = infile.readlines()
        zapsani = []
    for x in lines:
        radek = x.rstrip("\n")
        radek = radek.replace("'","")
        radek = radek.split(";")
        id, jmeno, trida, uzivjmeno = radek
        zaci.append(id, trida)
    print(zaci)
    return


def main():
    nacti_zaky("zaci")
    return

if __name__ == "__main__":
    main()