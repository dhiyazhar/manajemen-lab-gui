import csv
from datetime import datetime 

file_path = "./data/penggunaan_lab.csv"

with open(file_path, 'r', encoding='utf-8') as file: 
    reader = csv.DictReader(file)
    
    max_width = {col: len(col) for col in reader.fieldnames}

    print(max_width)
    for row in reader:
        for col in reader.fieldnames:
            if col == 'Tanggal':
                tanggal_str = datetime.strptime(row['Tanggal'], '%Y-%m-%d').strftime('%d-%m-%Y')
                max_width[col] = max(max_width[col], len(tanggal_str))

            else:
                max_width[col] = max(max_width[col], len(str(row[col])))