from Services.DatabaseService import get_database
from Models.Courrier import Courrier
class CourrierService:
    """SERVICE FOR HANDLING COURIER RELATED OPERATIONS"""
    def find_available_courrier(self) -> Courrier | None:
        """CHECK IF THERE IS AN AVAILABLE COURIER, IF NOT RETURN NONE"""
        db = get_database()
        courriers = db.get_all_courriers()
        for courrier in courriers:
            if courrier.is_available:
                return courrier
        return None