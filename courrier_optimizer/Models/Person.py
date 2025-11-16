from Models.BaseEntity import BaseEntity
class Person(BaseEntity):
    def __init__(self, id, created, last_updated, first_name: str, last_name: str):
        super().__init__(self, id, created, last_updated, first_name, last_name)
        self.first_name = first_name
        self.last_name = last_name