from Models.BaseEntity import BaseEntity
from Models.Person import Person

class Customer(BaseEntity):
    def __init__(self, id, created, last_updated, credit_card_number: str, customer_number:str, person: Person):
        super().__init__(id, created, last_updated)
        self.credit_card_number = credit_card_number
        self.customer_number = customer_number

        self.person = person

    def get_name(self) -> str | None:
        if (self.person != None):
            return f"{self.person.first_name} {self.person.last_name}"
        return None