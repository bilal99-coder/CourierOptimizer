from dataclasses import dataclass, field
from Models.Priority import Priority
from Models.DeliveryMode import DeliveryMode
from Utils.Validate import Validate


@dataclass
class Input:
    customer: str  # customer name
    latitude: str  # delivery latitude
    longitude: str  # delivery longitude
    priority: str  # High, Medium, Low
    weight_kg: str  # weight of the delivery in kg
    courrier_delivery_mode: str = field(default="CAR")  # optional; defaulted globally

    def __post_init__(self):
        if not Validate().validate_input_loaded_from_csv(self):
            raise ValueError("Invalid input data. Please check the values and try again.")

    def __str__(self):
        return (
            "customer: "
            + self.customer
            + "; delivery latitude: "
            + str(self.latitude)
            + "; delivery longitude: "
            + str(self.longitude)
            + "; priority: "
            + self.priority
            + "; weight: "
            + str(self.weight_kg)
            + " kg"
            + "; delivery mode: "
            + self.courrier_delivery_mode
        )
