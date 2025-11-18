import csv

class ReadCsvFile():
    def __init__(self, file_path:str):
        self.file_path = file_path

    def readCsv(self):
        with open(file= self.file_path, newline='', encoding='utf-8', errors="ignore") as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in reader:
                print(', '.join(row))