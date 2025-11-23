import os
from dotenv import load_dotenv
from Services.ReadCsvFile import FileService
from Utils.Validate import Validate


def main():
    # Load environment variables from .env file.
    load_dotenv()

    """START BY GREETING THE USER AND ASK FOR THE USER NAME"""
    greeting = os.getenv(
        "GREETING_MESSAGE_AND_ASK_ABOUT_NAME", "Good day, what is your name?"
    )
    name_of_user = input(greeting + " ")

    if name_of_user:
        print(f"Hello, {name_of_user}!")
    else:
        print(f"Your name is automatically set to {os.getenv("DEFAULT_USER")}")
        name_of_user = os.getenv("DEFAULT_USER")

    """ASK ABOUT THE START DEPOT"""
    ask_about_start__stop_depot = os.getenv(
        "ASK_ABOUT_START_DEPOT",
        "Please provide the start & stop depot coordinates (or press Enter for default)",
    )
    fixed_depot = input(
        ask_about_start__stop_depot.format(name_of_user=name_of_user) + " "
    )
    if fixed_depot == "":
        fixed_depot = os.getenv("DEFAULT_START_STOP_DEPOT")
        print(f"Your start and stop depot is set to: {fixed_depot} ")
    elif fixed_depot:
        print(f"Your start and stop depot is set to: {fixed_depot} ")

    start_depot = stop_depot = fixed_depot

    """Ask about the input csv file"""
    input_csv_file_path = input(
        "Could you please provide us with the file path to your input.csv file. (or press Enter for default)"
    )

    """if the user did not provided a file path to input csv file then use the default path"""
    if not input_csv_file_path:
        print("The file path used is the default file path")  # fix
        input_csv_file_path = "input.csv"

    """check if the file path provided by the user is valid. Give the user maximum 3 tries to give a valid path"""
    tries = 1
    while not os.path.isfile(input_csv_file_path) & tries < 3:
        input_csv_file_path = input(
            "The file provided by you is not valid. Try again {tries}/3:"
        )

    file_service = FileService()
    inputs_from_csv = file_service.load_inputs("input.csv")

    validate = Validate
    rejected_inputs = []
    for record in inputs_from_csv:
        print(type(record))
        if validate.validate_inputDTO(record):
            print("OK")
        else:
            print("Not OK!")
            print(record)
            rejected_inputs.append(record)

    file_service.write_rejected_inputs(file_path="rejected.csv", data=rejected_inputs)


if __name__ == "__main__":
    main()
