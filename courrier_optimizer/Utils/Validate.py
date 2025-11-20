from Models.Delivery import Delivery
from enum import Enum
class Validate():
    def __init__(self):
        pass

    """Checks if a number is a decimal number"""
    def validate_is_float(input) -> bool:
        try:
            float(input)
        except:
            return False

    """Weight should be positive and a number"""
    def validate_is_none_negative(input) -> bool:
        try:
            float(input)
            if (input <= 0):
                return False
        except:
            return False

    """Validate delivery priority. Priority can be oly high, medium or low"""
    def validate_match_enum(input:Enum, x:str) -> bool:
        pass


    def validate_delivery(self, delivery:Delivery) -> bool:
        return Validate.validate_is_none_negative(delivery.weight_kg)


