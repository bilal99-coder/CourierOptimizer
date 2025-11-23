import csv
from Models.Priority import Priority
from DTO.InputDTO import inputDTO
class FileService():
    def __init__(self):
        pass

    def load_inputs(self, file_path:str) -> list[input]:
        objects = []
        with open(file= file_path, newline='', encoding='utf-8', errors="ignore") as csvfile:
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

    def write_rejected_inputs(self, file_path:str, data:list[inputDTO]):
        with open(file=file_path, newline='', encoding='utf-8', errors="ignore", mode="w") as csvfile:
            headers = ['customer', 'latitude', 'longitude', 'priority', 'weight_kg']
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
