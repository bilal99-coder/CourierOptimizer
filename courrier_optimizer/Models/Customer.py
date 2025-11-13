from Models.BaseEntity import BaseEntity

class Customer(BaseEntity):
    def __init__(self, id, created, last_updated, credit_card_number: str, customer_number:str):
        super().__init__(id, created, last_updated)
        self.credit_card_number = credit_card_number
        self.customer_number = customer_number
