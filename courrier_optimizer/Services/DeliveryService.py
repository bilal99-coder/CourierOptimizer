from datetime import datetime
import math
from Models.Delivery import Delivery
from Models.Customer import Customer
from Models.Priority import Priority
from DTO.Input import Input
from Utils.Generate import Generate
from Models.DeliveryMode import DeliveryMode
from Models.Person import Person
from Models.Point import Point
from Services.CustomerService import CustomerService
from Services.CourrierService import CourrierService
from Services.CsvFileService import FileService

class DeliveryService:

    """CALCULATE DISTANCE USING THE HAVERSINE FORMULA"""
    def calculate_distance_between_two_points(self, start_point: Point, end_point: Point):
        ratio = 6371  # earth radius in km
        # Convert degrees to radians
        lat1 = math.radians(start_point.latitude)
        lat2 = math.radians(end_point.latitude)
        lon1 = math.radians(start_point.longitude)
        lon2 = math.radians(end_point.longitude)
        distance = (
            2
            * ratio
            * math.asin(
                math.sqrt(
                    math.sin((lat2 - lat1) / 2) ** 2
                    + math.cos(lat1)
                    * math.cos(lat2)
                    * math.sin((lon2 - lon1) / 2) ** 2
                )
            )
        )
        return distance

    def create_delivery_from_input(self, input: Input, fixed_depot: Point) -> Delivery:
        datetime_now = datetime.now()
        new_delivery_id = Generate.generate_random_uui()

        """CHECK IF CUSTOMER EXISTS IN THE DATABASE, IF NOT CREATE A NEW CUSTOMER"""
        Customer_found = CustomerService().getCustomer(input.customer)
        if Customer_found is not None:
            customer = Customer_found
        else:
            new_customer = Customer(
                id=Generate.generate_random_uui(),
                created=datetime_now,
                last_updated=datetime_now,
                credit_card_number="",
                customer_number=input.customer,
                person=Person("", "", "", input.customer, "")
            )
            CustomerService().add_customer(new_customer)
            customer = new_customer

        """CHECK IF THERE IS AN AVAILABLE COURIER, IF NOT RAISE AN EXCEPTION"""
        courrier = CourrierService().find_available_courrier()
        if courrier is None:
            raise ValueError("No available courier found")

        # Calculate delivery point and distance
        delivery_point = Point("END_POINT", latitude=float(input.latitude), longitude=float(input.longitude))
        distance = self.calculate_distance_between_two_points(fixed_depot, delivery_point)

        # Create delivery with all required fields
        delivery = Delivery(
            id=new_delivery_id,
            created=datetime_now,
            last_updated=datetime_now,
            start_point=fixed_depot,
            end_point=delivery_point,
            price=0.0,  # Calculate based on your business logic
            last_price=0.0,
            delivered_at=None,
            courrier=courrier,
            urgency=self.map_from_priority_to_urgency(input.priority),  # map string to Priority enum
            mode=DeliveryMode[input.courrier_delivery_mode],  # Convert to DeliveryMode enum
            customer=customer,
            weight_kg=float(input.weight_kg),
            distance=distance,
            is_delivered=False
        )

        return delivery

    def map_from_priority_to_urgency(self, priority: str) -> float:
        """MAP PRIORITY TO URGENCY, HIGH = 0.6, MEDIUM = 1, LOW = 1.2"""
        p = priority.upper()
        if p == "HIGH":
            return 0.6
        elif p == "MEDIUM":
            return 1
        elif p == "LOW":
            return 1.2
        else:
            raise ValueError("Invalid priority value. Must be 'HIGH', 'MEDIUM', or 'LOW'.")


    def calculate_delivery_price(self, delivery: Delivery) -> float:
        """CALCULATE PRICE THE CUSTOMER SHOULD PAY BASED ON DISTANCE AND URGENCY"""
        """1 KM = 1NOK , URGENCY MULTIPLIER: HIGH = 1.5, MEDIUM = 1.2, LOW = 1"""
        """MODE MULTIPLIER: CAR = 1.5, BICYCLE = 1.2, WALK = 1"""
        urgency_multiplier = 1.0
        mode_multiplier = 1.0
        """The higher is the priority, the higher is the urgency multiplier, and the higher is the price of the delivery for the customer but the more likely the delivery will be delivered faster"""
        if delivery.urgency == 0.6: # HIGH URGENCY
            urgency_multiplier = 1.5 # HIGHER DELIVERTY PRICE FOR HIGH URGENCY
        elif delivery.urgency == 1: # MEDIUM URGENCY
            urgency_multiplier = 1.2 # MEDIUM DELIVERY PRICE FOR MEDIUM URGENCY
        elif delivery.urgency == 1.2: # LOW URGENCY
            urgency_multiplier = 1.0  # LOWER DELIVERY PRICE FOR LOW URGENCY

        """The car mode is the most expensive mode of delivery, then the bicycle mode, then the walk mode"""
        if delivery.mode.mode_name == "Car":
            mode_multiplier = 1.5 # HIGHER DELIVERY PRICE FOR CAR MODE
        elif delivery.mode.mode_name == "Bicycle":
            mode_multiplier = 1.2 # MEDIUM DELIVERY PRICE FOR BICYCLE MODE
        elif delivery.mode.mode_name == "Walk":
            mode_multiplier = 1.0 # LOWER DELIVERY PRICE FOR WALK MODE

        return delivery.distance * urgency_multiplier * mode_multiplier

    """Function for prioritizing delivieries order based on urgency"""
    """HIGH PRIORITY DELIVERIES SHOULD BE DELIVERED FIRST, THEN MEDIUM, THEN LOW PRIORITY"""
    """IF TWO DELIVERIES HAVE THE SAME URGENCY THEN THE ONE WITH THE SHORTER DISTANCE SHOULD BE DELIVERED FIRST"""
    """This function will be used in the optimization process to sort the deliveries based on their urgency and distance"""
    """The function will sort the deliveries in place and return the sorted list of deliveries"""
    """The more higer the urgency the earlier the delivery should be delivered"""
    """The shorter the distance the earlier the delivery should be delivered"""
    """The more higher the urgency the less is the cost of the delivery for optimalisation algorithm to prioritize high urgency deliveries over low urgency deliveries"""
    def optimize_deliveries_route(self, deliveries: list[Delivery], objective: str = "fastest") -> list[Delivery]:
        """Sort deliveries by the chosen objective, with urgency as primary weight.
        Objectives: 'fastest', 'cheapest', 'greenest'.
        urgency weight: High=0.6, Medium=1.0, Low=1.2 — lower = delivered earlier."""
        obj = objective.lower()
        if obj == "fastest":
            # Weighted by travel time (distance / speed), urgency first
            deliveries.sort(key=lambda d: (d.urgency, d.distance / d.mode.speed_kmh if d.mode.speed_kmh else float("inf")))
        elif obj == "cheapest":
            # Weighted by cost (cost_per_km * distance), urgency first
            deliveries.sort(key=lambda d: (d.urgency, d.mode.cost_per_km * d.distance))
        elif obj == "greenest":
            # Weighted by CO2 (co2_g_per_km * distance), urgency first
            deliveries.sort(key=lambda d: (d.urgency, d.mode.co2_g_per_km * d.distance))
        else:
            raise ValueError(f"Unknown objective '{objective}'. Choose: fastest, cheapest, greenest.")
        return deliveries


    def calculate_totals(self, deliveries: list[Delivery]) -> dict:
        """Return total distance, time, cost and CO2 across all deliveries."""
        total_distance = sum(d.distance for d in deliveries)
        total_time = sum(d.mode.calculate_delivery_time(d.distance) for d in deliveries)
        total_cost = sum(d.mode.calculate_delivery_cost(d.distance) for d in deliveries)
        total_co2 = sum(d.mode.calculate_co2_emissions(d.distance) for d in deliveries)
        return {
            "total_deliveries": len(deliveries),
            "total_distance_km": round(total_distance, 2),
            "total_time_h": round(total_time, 2),
            "total_cost_nok": round(total_cost, 2),
            "total_co2_g": round(total_co2, 1),
        }

    def load_deliveries_from_input(self, input_list: list[Input], fixed_depot: Point) -> list[Delivery]:
        deliveries = []
        for input in input_list:
            delivery = self.create_delivery_from_input(input, fixed_depot)
            deliveries.append(delivery)
        return deliveries

    def mark_delivery_as_delivered(self, delivery: Delivery):
        delivery.is_delivered = True
        delivery.delivered_at = datetime.now()

    def mark_delivery_as_not_delivered(self, delivery: Delivery):
        delivery.is_delivered = False
        delivery.delivered_at = None

    def load_deliveries_from_csv(self, file_path: str, fixed_depot: Point) -> list[Delivery]:
        file_service = FileService()
        input_list = file_service.load_inputs(file_path)
        deliveries = self.load_deliveries_from_input(input_list, fixed_depot)
        return deliveries

    def write_rejected_deliveries_to_csv(self, file_path: str, deliveries: list[Delivery], mode: str):
        file_service = FileService()
        rejected_inputs = []
        for delivery in deliveries:
            if not delivery.is_delivered:
                rejected_input = Input(
                    customer=delivery.customer.customer_number,
                    latitude=str(delivery.end_point.latitude),
                    longitude=str(delivery.end_point.longitude),
                    priority=Priority(delivery.urgency).name,
                    weight_kg=str(delivery.weight_kg),
                    courrier_delivery_mode=delivery.mode.mode_name
                )
                rejected_inputs.append(rejected_input)
        file_service.write_rejected_inputs(file_path, rejected_inputs, mode)


    def optimize_deliveries(self, deliveries: list[Delivery]) -> list[Delivery]:
        """OPTIMIZE DELIVERIES BASED ON URGENCY AND DISTANCE AND MODE OF TRANSPORTATION"""
        """Sort deliveries by urgency and then by distance"""
        deliveries.sort(key=lambda delivery: (delivery.urgency, delivery.distance))
        return deliveries





