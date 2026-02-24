from typing import List, Optional, Dict
from Models.Customer import Customer
from Models.Delivery import Delivery
from Models.Courrier import Courrier


class DatabaseService:
    """Simple in-memory database for storing customers, deliveries, and couriers"""

    def __init__(self):
        self._customers: Dict[int, Customer] = {}
        self._deliveries: Dict[int, Delivery] = {}
        self._courriers: Dict[int, Courrier] = {}
        self._customer_counter = 0
        self._delivery_counter = 0
        self._courrier_counter = 0

    # Customer operations
    def add_customer(self, customer: Customer) -> Customer:
        """Add a customer to the database"""
        if customer.id is None:
            self._customer_counter += 1
            customer.id = self._customer_counter
        self._customers[customer.id] = customer
        return customer

    def get_customer(self, customer_id: int) -> Optional[Customer]:
        """Get a customer by ID"""
        return self._customers.get(customer_id)

    def get_all_customers(self) -> List[Customer]:
        """Get all customers"""
        return list(self._customers.values())

    def update_customer(self, customer: Customer) -> Optional[Customer]:
        """Update a customer"""
        if customer.id in self._customers:
            self._customers[customer.id] = customer
            return customer
        return None

    def delete_customer(self, customer_id: int) -> bool:
        """Delete a customer by ID"""
        if customer_id in self._customers:
            del self._customers[customer_id]
            return True
        return False

    def find_customer_by_name(self, customer_name: str) -> Optional[Customer]:
        """Find a customer by customer name"""
        for customer in self._customers.values():
            if customer.get_name() == customer_name:
                return customer
        return None

    # Delivery operations
    def add_delivery(self, delivery: Delivery) -> Delivery:
        """Add a delivery to the database"""
        if delivery.id is None:
            self._delivery_counter += 1
            delivery.id = self._delivery_counter
        self._deliveries[delivery.id] = delivery
        return delivery

    def get_delivery(self, delivery_id: int) -> Optional[Delivery]:
        """Get a delivery by ID"""
        return self._deliveries.get(delivery_id)

    def get_all_deliveries(self) -> List[Delivery]:
        """Get all deliveries"""
        return list(self._deliveries.values())

    def update_delivery(self, delivery: Delivery) -> Optional[Delivery]:
        """Update a delivery"""
        if delivery.id in self._deliveries:
            self._deliveries[delivery.id] = delivery
            return delivery
        return None

    def delete_delivery(self, delivery_id: int) -> bool:
        """Delete a delivery by ID"""
        if delivery_id in self._deliveries:
            del self._deliveries[delivery_id]
            return True
        return False

    def get_deliveries_by_customer(self, customer_id: int) -> List[Delivery]:
        """Get all deliveries for a specific customer"""
        return [d for d in self._deliveries.values() if d.customer and d.customer.id == customer_id]

    def get_deliveries_by_courrier(self, courrier_id: int) -> List[Delivery]:
        """Get all deliveries for a specific courier"""
        return [d for d in self._deliveries.values() if d.courrier and d.courrier.id == courrier_id]

    # Courrier operations
    def add_courrier(self, courrier: Courrier) -> Courrier:
        """Add a courier to the database"""
        if courrier.id is None:
            self._courrier_counter += 1
            courrier.id = self._courrier_counter
        self._courriers[courrier.id] = courrier
        return courrier

    def get_courrier(self, courrier_id: int) -> Optional[Courrier]:
        """Get a courier by ID"""
        return self._courriers.get(courrier_id)

    def get_all_courriers(self) -> List[Courrier]:
        """Get all couriers"""
        return list(self._courriers.values())

    def update_courrier(self, courrier: Courrier) -> Optional[Courrier]:
        """Update a courier"""
        if courrier.id in self._courriers:
            self._courriers[courrier.id] = courrier
            return courrier
        return None

    def delete_courrier(self, courrier_id: int) -> bool:
        """Delete a courier by ID"""
        if courrier_id in self._courriers:
            del self._courriers[courrier_id]
            return True
        return False

    def get_courriers_by_city(self, city: str) -> List[Courrier]:
        """Get all couriers working in a specific city"""
        return [c for c in self._courriers.values() if c.work_city.lower() == city.lower()]

    # Utility operations
    def clear_all(self):
        """Clear all data from the database"""
        self._customers.clear()
        self._deliveries.clear()
        self._courriers.clear()
        self._customer_counter = 0
        self._delivery_counter = 0
        self._courrier_counter = 0

    def get_stats(self) -> Dict[str, int]:
        """Get database statistics"""
        return {
            "customers": len(self._customers),
            "deliveries": len(self._deliveries),
            "courriers": len(self._courriers)
        }


# Singleton instance
_db_instance = None

def get_database() -> DatabaseService:
    """Get the singleton database instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseService()
    return _db_instance
