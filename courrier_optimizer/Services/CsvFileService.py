import csv
import os
from dataclasses import asdict
from DTO.InputDTO import inputDTO
from Models.Priority import Priority


class FileService:
    def __init__(self):
        pass

    def load_inputs(self, file_path: str) -> list[inputDTO]:
        objects = []
        with open(file=file_path, newline="", encoding="utf-8", errors="ignore") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                input = inputDTO(
                    customer=row["customer"],
                    weight_kg=row["weight_kg"],
                    latitude=row["latitude"],
                    priority=Priority.HIGH,
                    longitude=row["longitude"],
                )
                objects.append(input)
        return objects

    def write_rejected_inputs(self, file_path: str, data: list[inputDTO], mode: str):
        """Write rejected inputs and add header only if file is new/empty."""
        rows = [asdict(record) for record in data]
        headers = ["customer", "latitude", "longitude", "priority", "weight_kg"]

        file_exists = os.path.exists(file_path)
        should_write_header = (mode == "w") or not (file_exists and os.path.getsize(file_path) > 0)

        with open(file=file_path, newline="", encoding="utf-8", errors="ignore", mode=mode) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            if should_write_header:
                writer.writeheader()
            writer.writerows(rows)
