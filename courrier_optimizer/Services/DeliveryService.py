from Models.Delivery import Delivery
class DeliveryService:
    def sort_by_urgency(deliveries:list[Delivery]):
        deliveries.sort(key= lambda delivery : delivery.urgency)