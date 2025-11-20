from Services.ReadCsvFile import ReadCsvFile

def main():
    csv_file = ReadCsvFile("input1.csv")
    csv_file.readCsv()

if __name__ == '__main__':
    main()
