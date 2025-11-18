from Models.BaseEntity import BaseEntity
from Services.ReadCsvFile import ReadCsvFile
from datetime import datetime

def main():
    csv_file = ReadCsvFile("input.csv")
    csv_file.readCsv()

if __name__ == '__main__':
    main()
