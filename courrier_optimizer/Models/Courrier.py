from Models.BaseEntity import BaseEntity
class Courrier(BaseEntity):
    def __init__(self, id, created, last_updated, work_city: str):
        super().__init__(id, created, last_updated)
        self.work_city = work_city
