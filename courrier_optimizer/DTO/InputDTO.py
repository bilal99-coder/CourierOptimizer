from dataclasses import dataclass
from Models.Priority import Priority
@dataclass
class inputDTO:
    customer: str
    latitude: float
    longitude: float
    priority: Priority
    weight_kg: float