from dataclasses import dataclass
from Models.Priority import Priority


@dataclass
class inputDTO:
    customer: str  # customer_name
    latitude: float
    longitude: float
    priority: Priority
    weight_kg: float

    def __str__(self):
        return (
            "customer: "
            + self.customer
            + "; latitude: "
            + self.latitude
            + "; longitude: "
            + self.longitude
            + "; priority: "
            + self.priority.value
            + "; weight: "
            + self.weight_kg
            + " kg."
        )
