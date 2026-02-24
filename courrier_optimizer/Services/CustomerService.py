from Services.DatabaseService import get_database
from Models.Customer import Customer

class CustomerService:
    """SERVICE FOR HANDLING CUSTOMER RELATED OPERATIONS"""

    def getCustomer(self, customer_name: str) -> Customer | None:
        """CHECK IF CUSTOMER EXISTS IN THE DATABASE, IF NOT RETURN NONE"""
        db = get_database()
        return db.find_customer_by_name(customer_name)

    def add_customer(self, customer: Customer) -> Customer:
        """ADD A CUSTOMER TO THE DATABASE"""
        db = get_database()
        return db.add_customer(customer)