import csv

def modify_id_column(input_file, output_file):
    # Read the input CSV and store the data in a list of dictionaries
    data = []
    with open(input_file, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            data.append(row)

    # Modify the 'id' column
    for i, row in enumerate(data, start=1):
        row['id'] = str(i)

    # Write the modified data to a new CSV file
    with open(output_file, 'w', newline='') as modified_csv:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(modified_csv, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Example usage:
input_file = 'seminare.csv'
output_file = 'seminare.csv'
modify_id_column(input_file, output_file)
