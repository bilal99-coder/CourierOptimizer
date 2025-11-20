from Models.Delivery import Delivery
from Models.Priority import Priority
from enum import Enum, EnumMeta
import re

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

    """
    Validate delivery priority against the Priority Enum.
    Returns True if the value is valid, False otherwise.
    """
    def validate_match_enum(a: EnumMeta, value_to_check: str) -> bool:
        """checks if a raw value matches any value of the enum class a"""
        try:
            a(value_to_check)
            return True
        except ValueError:
            return False

    """Name can have only printibale chars. It cannot contain numbers or special charachters. It can be a one name or two names with space in the midle. Second name is oprional"""
    def validate_name(customer_name:str) -> bool:
        return re.fullmatch('[A-Za-z]{2,25}( [A-Za-z]{2,25})?', customer_name)

    def validate_delivery(self, delivery:Delivery) -> bool:
        return Validate.validate_is_none_negative(delivery.weight_kg) & Validate.validate_name(delivery.customer.get_name())


