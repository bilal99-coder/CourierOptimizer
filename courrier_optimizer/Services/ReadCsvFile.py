import csv
from Models.Priority import Priority
from DTO.InputDTO import inputDTO
class ReadCsvFile():
    def __init__(self, file_path:str):
        self.file_path = file_path

    def readCsv(self) -> list[input]:
        objects = []
        with open(file= self.file_path, newline='', encoding='utf-8', errors="ignore") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                input = inputDTO(
                    customer=row['customer'],
                    weight_kg=row['weight_kg'],
                    latitude=row['latitude'],
                    priority=Priority.HIGH,
                    longitude=row['longitude']
                    )
                objects.append(input)
        return objects