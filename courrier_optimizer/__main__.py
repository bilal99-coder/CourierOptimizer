import os
from dotenv import load_dotenv
from Services.CsvFileService import FileService
from Utils.Validate import Validate
from Services.DeliveryService import DeliveryService

def main():
    """Load environment variables from .env file."""
    load_dotenv()

    """START BY GREETING THE USER AND ASK FOR THE USER NAME"""
    greeting = os.getenv(
        "GREETING_MESSAGE_AND_ASK_ABOUT_NAME", "Good day, what is your name?"
    )
    name_of_user = input(greeting + " ")

    if name_of_user:
        print(f"Hello, {name_of_user}!")
    else:
        print(f"Your name is automatically set to {os.getenv('DEFAULT_USER')}")
        name_of_user = os.getenv("DEFAULT_USER")

    """ASK ABOUT THE START DEPOT"""
    ask_about_start_stop_depot = os.getenv(
        "ASK_ABOUT_START_DEPOT",
        "Please provide the start & stop depot coordinates (or press Enter for default)",
    )

    """The start and stop depot are fixed to the same latitude and longitude"""

    fixed_depot = input(
        ask_about_start_stop_depot.format(name_of_user=name_of_user) + " "
    )
    if fixed_depot == "":
        fixed_depot = os.getenv("DEFAULT_START_STOP_DEPOT")
        print(f"Your start and stop depot is set to: {fixed_depot} ")
    elif fixed_depot:
        #validate fixed depot
        print(f"Your start and stop depot is set to: {fixed_depot} ")

    start_depot = stop_depot = fixed_depot

    """Ask about the input csv file"""
    input_csv_file_path = input(
        "Could you please provide us with the file path to your input csv file. (or press Enter for default) "
    )

    """if the user did not provided a file path to input csv file then use the default path"""
    if not input_csv_file_path:
        print(
            f"The file path used is set to the default file path: {os.getenv('DEFAULT_INPUT_CSV_PATH')} "
        )
        input_csv_file_path = os.getenv("DEFAULT_INPUT_CSV_PATH")

    """check if the file path provided by the user is valid. Give the user maximum 3 tries to give a valid path"""
    tries = 1
    total_tries = int(os.getenv("GET_FILE_PATH_TOTAL_TRIES", "3"))
    while (not os.path.isfile(input_csv_file_path)) and tries <= total_tries:
        input_csv_file_path = input(
            f"The file provided by you is not valid. Try again ({tries}/{total_tries}): "
        )
        tries += 1

    if not os.path.isfile(input_csv_file_path):
        print(
            f"All the attempts to get a valid path file were not successful. The input csv file will be set to default: {os.getenv('DEFAULT_INPUT_CSV_PATH')}"
        )
        input_csv_file_path = os.getenv("DEFAULT_INPUT_CSV_PATH")

    file_service = FileService()
    inputs_from_csv = file_service.load_inputs(input_csv_file_path)

    validate = Validate()
    delivery_service = DeliveryService()
    rejected_inputs = []
    valid_deliveries = []
    for record in inputs_from_csv:
        if validate.validate_inputDTO(record):
            print("OK")
            valid_deliveries.append(record)
        else:
            print("Not OK!")
            rejected_inputs.append(record)

    "write non valid input rows to rejected.csv"
    file_service.write_rejected_inputs(file_path=os.getenv("DEFAULT_OUTPUT_CSV_PATH"), data=rejected_inputs, mode="a")

    delivery_service.sort_by_urgency()



if __name__ == "__main__":
    main()
