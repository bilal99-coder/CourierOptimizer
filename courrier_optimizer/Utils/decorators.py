import logging
from datetime import datetime

def timer_decorator(func):
    """A timing decorator to log start time, end time, parameters, skipped
    rows, and final totals. Print a one-screen summary at the end."""
    def wrapper(*args, **kwargs):
        logging.info(f"Running {func.__name__} with args: {args} and kwargs: {kwargs}")
        start_time = datetime.now()
        # Call the original function and capture its result
        result = func(*args, **kwargs)
        end_time = datetime.now()
        result_dict = result if isinstance(result, dict) else {}
        parameters = result_dict.get("parameters", {})
        skipped_rows = result_dict.get("skipped_rows", [])
        final_totals = result_dict.get("final_totals", {"total_deliveries": 0, "total_distance": 0})

        # Log the results (you can replace this with actual logging)
        logging.info(f"Start Time: {start_time}")
        logging.info(f"End Time: {end_time}")
        logging.info(f"Parameters: {parameters}")
        logging.info(f"Skipped Rows: {skipped_rows}")
        logging.info(f"Final Totals: {final_totals}")

        # Print a one-screen summary
        print("\nSummary:")
        print(f"Start Time: {start_time}")
        print(f"End Time: {end_time}")
        print(f"Parameters: {parameters}")
        print(f"Skipped Rows: {skipped_rows}")
        print(f"Final Totals: {final_totals}")

        logging.info(f"Finished {func.__name__} in {(end_time - start_time).total_seconds()} seconds")

        return result

    return wrapper