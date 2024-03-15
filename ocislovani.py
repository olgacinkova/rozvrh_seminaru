import csv
from typing import Collection


def modify_id_column(seminare_kolize, zapsani) -> None:
    id_table = dict()
    # pro soubor seminare_kolize
    with open(seminare_kolize, 'r') as csv_file:
        with open("ocislovane_seminare_kolize", 'w', newline='') as modified_csv:
            reader = csv.DictReader(csv_file, delimiter=";")
            writer = csv.DictWriter(
                modified_csv, fieldnames=reader.fieldnames, delimiter=";")
            writer.writeheader()
            for i, row in enumerate(reader, start=1):
                stare_id = row['id'].strip()
                id_table[stare_id] = i
                # ukladam do dictionary vzdy stare a k nemu korespondujici nove id
                row['id'] = str(i)
                writer.writerow(row)
                
    with open(zapsani, 'r') as csv_file:
        with open("ocislovane_zapsani.csv", 'w', newline='') as modified_csv:
            reader = csv.DictReader(csv_file, delimiter=";")
            writer = csv.DictWriter(
                modified_csv, fieldnames=reader.fieldnames, delimiter=";")
            writer.writeheader()
            for i, row in enumerate(reader, start=1):
                stare_id = row['seminar'].strip()
                aktualni_id = id_table.get(stare_id)
                if aktualni_id:
                    # kouknu do id table jako je nove id ke staremu
                    row['seminar'] = str(aktualni_id)
                    writer.writerow(row)


modify_id_column("seminare_kolize.csv", "zapsani.csv")
