#########################################################################
# when you download the csv files from the meteoapex page, you create a #
# .txt file in the same format of the lcst files                        #
#########################################################################

import csv

csv_file_path = '/path/to/your/folder/file.csv' #input
txt_file_path = '/path/to/your/folder/file.txt' #output

with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)

    with open(txt_file_path, mode='w', encoding='utf-8') as txt_file:
        for row in csv_reader:
            txt_file.write(','.join(row) + '\n')

print(f"CSV file successfully converted.")
