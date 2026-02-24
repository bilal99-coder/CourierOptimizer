import os
import logging
from time import sleep
from dotenv import load_dotenv
from Services.CsvFileService import FileService
from Utils.Validate import Validate
from Services.DeliveryService import DeliveryService
from Utils.decorators import timer_decorator
from Models.DeliveryMode import DeliveryMode


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('./Output/run.log'), logging.StreamHandler()]
)


def ask_menu(prompt: str, options: dict) -> str:
    """Display a numbered menu and return the user's chosen key."""
    print(f"\n{prompt}")
    keys = list(options.keys())
    for i, key in enumerate(keys, 1):
        print(f"  {i}. {options[key]}")
    while True:
        raw = input("Enter choice number: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(keys):
            return keys[int(raw) - 1]
        print(f"  Please enter a number between 1 and {len(keys)}.")


@timer_decorator
def optimize():
    """Load environment variables from .env file."""
    load_dotenv()

    logging.info("Starting Courier Optimizer Application ...")
    sleep(1)

    # --- Greet user ---
    greeting = os.getenv("GREETING_MESSAGE_AND_ASK_ABOUT_NAME", "Good day, what is your name?")
    name_of_user = input(greeting + " ").strip()
    if not name_of_user:
        name_of_user = os.getenv("DEFAULT_USER", "Guest")
    print(f"Hello, {name_of_user}!")

    # --- Transport mode ---
    mode_key = ask_menu(
        "Select transport mode for this run:",
        {"CAR": "Car  (50 km/h, 4 NOK/km, 120 g CO2/km)",
         "BIKE": "Bicycle  (15 km/h, free, 0 CO2)",
         "WALK": "Walking  (5 km/h, free, 0 CO2)"},
    )
    chosen_mode: DeliveryMode = DeliveryMode[mode_key]
    print(f"Mode: {chosen_mode.mode_name}")

    # --- Optimization objective ---
    objective_key = ask_menu(
        "Select optimization objective:",
        {"fastest": "Fastest total time",
         "cheapest": "Lowest total cost",
         "greenest": "Lowest CO2 emissions"},
    )
    print(f"Objective: {objective_key}")

    # --- Depot ---
    ask_about_depot = os.getenv(
        "ASK_ABOUT_START_DEPOT",
        "Enter start/stop depot coordinates as lat,lon (or press Enter for default):",
    )
    fixed_depot_input = input(f"\n{ask_about_depot} ").strip()
    if not fixed_depot_input:
        fixed_depot_input = os.getenv("DEFAULT_START_STOP_DEPOT", "59.919623,10.735394")
    print(f"Depot: {fixed_depot_input}")

    # --- Input CSV ---
    input_csv_file_path = input(
        "\nEnter path to input CSV file (or press Enter for default): "
    ).strip()
    if not input_csv_file_path:
        input_csv_file_path = os.getenv("DEFAULT_INPUT_CSV_PATH", "Input/input.csv")
        print(f"Using default: {input_csv_file_path}")

    tries, total_tries = 1, int(os.getenv("GET_FILE_PATH_TOTAL_TRIES", "3"))
    while not os.path.isfile(input_csv_file_path) and tries <= total_tries:
        input_csv_file_path = input(f"File not found. Try again ({tries}/{total_tries}): ").strip()
        tries += 1
    if not os.path.isfile(input_csv_file_path):
        input_csv_file_path = os.getenv("DEFAULT_INPUT_CSV_PATH", "Input/input.csv")
        print(f"Falling back to default: {input_csv_file_path}")

    # --- Load & validate ---
    file_service = FileService()
    inputs_from_csv = file_service.load_inputs(input_csv_file_path, default_mode=mode_key)

    validate = Validate()
    delivery_service = DeliveryService()
    rejected_inputs, valid_inputs = [], []
    for record in inputs_from_csv:
        # Override mode from global selection
        record.courrier_delivery_mode = mode_key
        if validate.validate_inputDTO(record):
            valid_inputs.append(record)
        else:
            logging.warning(f"Rejected row: {record}")
            rejected_inputs.append(record)

    logging.info(f"Loaded {len(valid_inputs)} valid, {len(rejected_inputs)} rejected rows.")

    # Write rejected rows
    file_service.write_rejected_inputs(
        file_path=os.getenv("DEFAULT_OUTPUT_CSV_PATH", "Output/rejected.csv"),
        data=rejected_inputs,
        mode="w",
    )

    # --- Build delivery objects ---
    from Models.Point import Point as PointModel
    from Models.Courrier import Courrier
    from Services.DatabaseService import get_database
    from datetime import datetime as dt

    depot_coords = fixed_depot_input.replace(" ", "")
    try:
        depot_lat, depot_lon = map(float, depot_coords.split(","))
    except ValueError:
        logging.warning("Invalid depot format; using default.")
        depot_lat, depot_lon = 59.919623, 10.735394
    depot_point = PointModel("DEPOT", depot_lat, depot_lon)

    db = get_database()
    if not db.get_all_courriers():
        db.add_courrier(Courrier(id=1, created=dt.now(), last_updated=dt.now(),
                                work_city="Oslo", is_available=True))

    valid_deliveries = delivery_service.load_deliveries_from_input(valid_inputs, depot_point)

    # --- Optimize ---
    sorted_deliveries = delivery_service.optimize_deliveries_route(valid_deliveries, objective=objective_key)

    # --- Write route.csv ---
    route_path = os.getenv("DEFAULT_ROUTE_CSV_PATH", "Output/route.csv")
    file_service.write_route(route_path, sorted_deliveries, depot_point, chosen_mode)

    # --- Compute totals ---
    totals = delivery_service.calculate_totals(sorted_deliveries)

    # --- Console summary (printed by decorator too, but we print a richer version here) ---
    print("\n" + "=" * 50)
    print(f"  COURIER OPTIMIZER — RESULTS")
    print("=" * 50)
    print(f"  Mode:       {chosen_mode.mode_name}  ({chosen_mode.speed_kmh} km/h, "
          f"{chosen_mode.cost_per_km} NOK/km, {chosen_mode.co2_g_per_km} g CO2/km)")
    print(f"  Objective:  {objective_key}")
    print(f"  Deliveries: {totals['total_deliveries']}")
    print(f"  Distance:   {totals['total_distance_km']} km")
    print(f"  Time:       {totals['total_time_h']} h")
    print(f"  Cost:       {totals['total_cost_nok']} NOK")
    print(f"  CO2:        {totals['total_co2_g']} g")
    print(f"  Rejected:   {len(rejected_inputs)} rows → Output/rejected.csv")
    print(f"  Route:      {route_path}")
    print("=" * 50)

    return {
        "skipped_rows": [str(r) for r in rejected_inputs],
        "final_totals": totals,
        "parameters": {
            "user": name_of_user,
            "depot": depot_coords,
            "mode": mode_key,
            "objective": objective_key,
            "input_file": input_csv_file_path,
        },
    }


# Entry point of the application
if __name__ == "__main__":
    optimize()
