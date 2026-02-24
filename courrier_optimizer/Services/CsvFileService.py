import csv
import os
from dataclasses import asdict
from DTO.Input import Input
from Models.Priority import Priority


class FileService:
    def __init__(self):
        pass

    def load_inputs(self, file_path: str, default_mode: str = "CAR") -> list[Input]:
        """load inputs from csv files and return a list of inputs.
        Supports both comma and semicolon delimiters.
        courrier_delivery_mode column is optional; falls back to default_mode."""
        objects = []
        # Detect delimiter by sniffing the first line
        with open(file_path, encoding="utf-8-sig", errors="ignore") as f:
            first_line = f.readline()
        delimiter = ";" if ";" in first_line else ","

        with open(
            file=file_path, newline="", encoding="utf-8-sig", errors="ignore"
        ) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=delimiter)
            for row in reader:
                try:
                    input_from_csv = Input(
                        customer=row["customer"],
                        weight_kg=row["weight_kg"],
                        latitude=row["latitude"],
                        priority=row["priority"],
                        longitude=row["longitude"],
                        courrier_delivery_mode=row.get("courrier_delivery_mode", default_mode),
                    )
                    objects.append(input_from_csv)
                except (KeyError, ValueError) as e:
                    import logging
                    logging.warning(f"Skipping invalid row {dict(row)}: {e}")
        return objects

    def write_rejected_inputs(self, file_path: str, data: list[Input], mode: str):
        """Write rejected inputs and add header only if file is new/empty."""
        rows = []
        for record in data:
            row = asdict(record)
            # Store enum as its value for cleaner CSV output.
            if isinstance(row.get("priority"), Priority):
                row["priority"] = row["priority"].value
            rows.append(row)
        headers = ["customer", "latitude", "longitude", "priority", "weight_kg"]

        file_exists = os.path.exists(file_path)
        should_write_header = (mode == "w") or not (
            file_exists and os.path.getsize(file_path) > 0
        )

        with open(
            file=file_path, newline="", encoding="utf-8", errors="ignore", mode=mode
        ) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers, extrasaction="ignore")
            if should_write_header:
                writer.writeheader()
            writer.writerows(rows)

    def write_route(self, file_path: str, deliveries, depot_point, mode_enum):
        """Write route.csv with ordered stops, distance from previous stop,
        cumulative distance, ETA, cost, and CO2."""
        import logging
        from datetime import datetime, timedelta

        headers = [
            "stop", "customer", "latitude", "longitude", "priority",
            "distance_from_prev_km", "cumulative_distance_km",
            "eta", "cost_nok", "co2_g",
        ]
        rows = []
        cumulative = 0.0
        eta_time = datetime.now().replace(second=0, microsecond=0)
        prev_point = depot_point

        for i, delivery in enumerate(deliveries, start=1):
            seg_dist = delivery.distance  # distance from depot; we recompute leg below
            # Recompute distance from previous stop for sequential legs
            from Services.DeliveryService import DeliveryService
            seg_dist = DeliveryService().calculate_distance_between_two_points(prev_point, delivery.end_point)
            cumulative += seg_dist
            travel_hours = mode_enum.calculate_delivery_time(seg_dist)
            eta_time += timedelta(hours=travel_hours)
            cost = mode_enum.calculate_delivery_cost(seg_dist)
            co2 = mode_enum.calculate_co2_emissions(seg_dist)
            rows.append({
                "stop": i,
                "customer": delivery.customer.customer_number if delivery.customer else "",
                "latitude": delivery.end_point.latitude,
                "longitude": delivery.end_point.longitude,
                "priority": delivery.urgency,
                "distance_from_prev_km": round(seg_dist, 3),
                "cumulative_distance_km": round(cumulative, 3),
                "eta": eta_time.strftime("%H:%M"),
                "cost_nok": round(cost, 2),
                "co2_g": round(co2, 1),
            })
            prev_point = delivery.end_point

        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
        logging.info(f"route.csv written to {file_path} ({len(rows)} stops)")
