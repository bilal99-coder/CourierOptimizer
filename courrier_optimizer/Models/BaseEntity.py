from datetime import datetime
from uuid import uuid4
class BaseEntity():
    def __init__(self, id:uuid4, created:datetime, last_updated:datetime):
        self.id = id
        self.last_updated = last_updated
        self.created = created
