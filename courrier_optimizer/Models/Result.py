from DTO.Input import input
class Result:
    def __init__(self, start_time: str, end_time: str, prameters: dict, skipped_rows: list[input], final_totals: dict):
        self.start_time = start_time
        self.end_time = end_time
        self.prameters = prameters
        self.skipped_rows = skipped_rows
        self.final_totals = final_totals