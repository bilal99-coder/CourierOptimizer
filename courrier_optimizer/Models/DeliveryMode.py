class DeliveryMode():
    def __init__(self, speed:float, cost:float, co2: float):
        self.speed = speed
        self.cost = cost
        self.co2 = co2

    def get_walking_mode():
        return DeliveryMode(5, 0, 0)
    def get_car_mode():
        return DeliveryMode(50, 4, 120)
    def get_bycycle_mode():
        return DeliveryMode(15, 0, 0)