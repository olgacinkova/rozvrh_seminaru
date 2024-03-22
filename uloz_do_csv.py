import csv
def uloz_do_csv(dictionary, filename):
    """
    Ukládá dictionary do csv - dva sloupce.

    Parametry:
        dictionary (dict): Dictionary, který chci zapsat do csv souboru.
        filename (str): Jméno souboru, do kterého chci dictionary uložit.
    """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        for key, value in dictionary.items(): # pary seminar:blok
            writer.writerow([key, value])