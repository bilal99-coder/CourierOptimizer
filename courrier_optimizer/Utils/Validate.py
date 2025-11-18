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
    def validate_weight(input) -> bool:
        try:
            float(input)
            if (input <= 0):
                return False
        except:
            return False


def validate_delivery():



