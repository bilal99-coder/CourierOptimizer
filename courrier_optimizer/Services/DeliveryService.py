from Models.Delivery import Delivery
class DeliveryService:
    def sort_by_urgency(deliveries:list[Delivery]):
        deliveries.sort(key= lambda delivery : delivery.urgency)

    """CALCULATE USING THE HAVERSINE FORMULA"""
    def calculate_distance_between_two_points():
        pass