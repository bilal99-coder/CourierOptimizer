from __future__ import annotations
from Models.DeliveryMode import DeliveryMode
from Models.Priority import Priority
from enum import EnumMeta
from typing import TYPE_CHECKING
import re

if TYPE_CHECKING:
    from DTO.Input import Input


class Validate:
    def __init__(self):
        pass

    """Checks if a number is a decimal number"""
    def validate_is_float(self, input) -> bool:
        try:
            float(input)
            return True
        except:
            return False

    """Weight should be nonnegative (>= 0) and a valid number"""
    def validate_is_none_negative_number(self, input:str) -> bool:
        try:
            if float(input) < 0:
                return False
            return True
        except:
            return False

    """
    Validate delivery priority against the Priority Enum.
    Returns True if the value is valid, False otherwise.
    """

    def validate_match_enum(self, a: EnumMeta, value_to_check) -> bool:
        """checks if a raw value matches any value of the enum class a (by value or by name)"""
        try:
            if isinstance(value_to_check, a):
                return True
            a(value_to_check)
            return True
        except ValueError:
            try:
                a[value_to_check]
                return True
            except KeyError:
                return False

    """Name can have only printibale chars. It cannot contain numbers or special charachters. It can be a one name or two names with space in the midle. Second name is oprional"""

    def validate_name(self, customer_name: str) -> bool:
        return re.fullmatch("[A-Za-z]{2,25}( [A-Za-z]{2,25})?", customer_name) is not None

    def is_valid_gps_cordinate(self, latitude: str, longitude: str) -> bool:
        try:
            lat = float(latitude)
            lon = float(longitude)

            if (-90 <= lat <= 90) and (-180 <= lon <= 180):
                return True
            else:
                return False
        except ValueError:
            return False


    def validate_input_loaded_from_csv(self, record: Input) -> bool:
        """Validate the input loaded from csv file. It should have a valid customer name, valid GPS coordinates, valid priority and valid delivery mode. Weight should be a positive number."""
        return (
            self.validate_match_enum(DeliveryMode, record.courrier_delivery_mode)
            and self.validate_is_none_negative_number(record.weight_kg)
            and self.validate_name(record.customer)
            and self.validate_match_enum(Priority, record.priority)
            and self.is_valid_gps_cordinate(record.latitude, record.longitude)
        )

    def validate_inputDTO(self, record: Input) -> bool:
        """Alias for validate_input_loaded_from_csv used in main delivery loop."""
        return self.validate_input_loaded_from_csv(record)
