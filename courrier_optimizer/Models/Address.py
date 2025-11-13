from Models import BaseEntity

class Address(BaseEntity):
    def __init__(self, id, created, last_updated, city:str, postcode:str, country:str, address_line1:str, address_line2:str, state:str):
        super().__init__(id, created, last_updated)
        self.city = city
        self.postcode = postcode
        self.country = country
        self.address_line1 = address_line1
        self.address_line2 = address_line2
        self.state = state
