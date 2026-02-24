from Models.BaseEntity import BaseEntity
from Models.Courrier import Courrier
from Models.Customer import Customer
from Models.DeliveryMode import DeliveryMode
from datetime import datetime
from Models.Point import Point

"""DELIVERY ENTITY REPRESENTING A DELIVERY IN THE SYSTEM"""
"""Get populated from inputDTO and used in the delivery optimization process"""
class Delivery(BaseEntity):

    def __init__(
        self,
        id,
        created,
        last_updated,
        start_point: Point,
        end_point: Point,
        price: float,
        last_price: float,
        delivered_at: datetime | None,
        courrier: Courrier,
        urgency: float,
        mode: DeliveryMode,
        customer: Customer,
        weight_kg: float,
        distance: float,
        is_delivered: bool,
    ):
        super().__init__(id, created, last_updated)
        self.start_point = start_point
        self.end_point = end_point
        self.price = price  # calculate_price()
        self.last_price = last_price  # calculate_last_price()
        self.delivered_at = delivered_at
        self.is_delivered = is_delivered
        self.courrier = courrier  # get_courrier()
        self.urgency = urgency  # map_from_priority_to_urgency()
        self.customer = customer
        self.mode = mode  # Car, Bicycle, or Walk
        self.weight_kg = weight_kg
        self.distance = distance  # calculate_distance_between_two_points()
