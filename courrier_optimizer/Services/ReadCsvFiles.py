class ReadCsvFiles():
    def __init__(self, file_path:str):
        self.file_path = file_path

    def readCsv(file_path:str):
        with open(file=file_path, mode="r", encoding="utf-8") as csv_file:
            csv_file.close()