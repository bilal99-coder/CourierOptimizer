from Models.Delivery import Delivery
from Models.Customer import Customer
from Models.Person import Person
from DTO.InputDTO import inputDTO
class DeliveryService:
    def sort_by_urgency(deliveries:list[Delivery]):
        deliveries.sort(key= lambda delivery : delivery.urgency)

    """CALCULATE USING THE HAVERSINE FORMULA"""
    def calculate_distance_between_two_points():
        pass

    def create_delivery_from_input(input:inputDTO, fixed_depot:str):
        delivery = Delivery()
        new_person = Person(id=#generateid, created = , last_updated=, first_name=input.customer, last_name="random_last_name")
        new_customer = Customer(id= #generateid, created=, last_updated=, credit_card_number=, person=new_person)
        delivery.customer = new_customer
        delivery.courrier = get_available_corrier()
        delivery.start_point = fixed_depot
        delivery.end_point = f"{input.latitude} , {input.longitude}"
        delivery.urgency = map_from_priority_to_urgency(input.priority)
        delivery.price = calculate_price()
        delivery.id = #generate id()
        delivery.weight_kg = input.weight_kg
        #delivery.delivered = true or false
        delivery.last_updated=
