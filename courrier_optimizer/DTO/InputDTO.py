from dataclasses import dataclass
from Models.Priority import Priority
@dataclass
class inputDTO:
    customer: str #customer_name
    latitude: float
    longitude: float
    priority: Priority
    weight_kg: float