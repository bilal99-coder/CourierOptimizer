from Models import BaseEntity, Courrier, Priority
from datetime import datetime

class Delivery(BaseEntity):
    def __init__(self, id, created, last_updated, start_point: str, end_point: str, price: float, last_price: float, delivered_at: datetime, courrier: Courrier, priority: Priority):
        super().__init__(id, created, last_updated)
        self.start_point = start_point
        self.end_point = end_point
        self.price = price #calculate_price()
        self.last_price = last_price #calculate_last_price()
        self.delivered_at = delivered_at
        self.courrier = courrier #get_courrier()
        self.priority = priority