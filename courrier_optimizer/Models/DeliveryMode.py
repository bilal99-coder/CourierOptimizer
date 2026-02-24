from enum import Enum

class DeliveryMode(Enum):
    """Delivery modes with their attributes"""

    # Each mode has: (name, speed_kmh, cost_per_km, co2_g_per_km)
    CAR = ("CAR", 50, 4, 120)
    BIKE = ("BIKE", 15, 0, 0)
    WALK = ("WALK", 5, 0, 0)

    # based on the table 1 of transport modes in the project description
    def __init__(self, mode_name: str, speed_kmh: int, cost_per_km: int, co2_g_per_km: int):
        self.mode_name = mode_name
        self.speed_kmh = speed_kmh
        self.cost_per_km = cost_per_km
        self.co2_g_per_km = co2_g_per_km

    def calculate_delivery_cost(self, distance_km: float) -> float:
        """Calculate cost for a given distance"""
        return self.cost_per_km * distance_km

    def calculate_co2_emissions(self, distance_km: float) -> float:
        """Calculate CO2 emissions in grams for a given distance"""
        return self.co2_g_per_km * distance_km

    def calculate_delivery_time(self, distance_km: float) -> float:
        """Calculate delivery time in hours for a given distance"""
        return distance_km / self.speed_kmh if self.speed_kmh > 0 else 0