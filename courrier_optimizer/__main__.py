import os
from dotenv import load_dotenv
from Services.ReadCsvFile import ReadCsvFile
from Utils.Validate import Validate


def main():
    # Load environment variables from .env file.
    load_dotenv()

    """START BY GREETING THE USER AND ASK FOR THE USER NAME"""
    greeting = os.getenv("GREETING_MESSAGE_AND_ASK_ABOUT_NAME", "Good day, what is your name?")
    name_of_user = input(greeting + " ")

    if name_of_user:
        print(f"Hello, {name_of_user}!")
    else:
        name_of_user = os.getenv("DEFAULT_USER")

    """ASK ABOUT THE START DEPOT"""
    ask_about_start__stop_depot = os.getenv(
        "ASK_ABOUT_START_DEPOT",
        "Please provide the start & stop depot coordinates (or press Enter for default)",
    )
    fixed_depot = input(ask_about_start__stop_depot.format(name_of_user=name_of_user) + " ")
    if fixed_depot == "":
        fixed_depot = os.getenv("DEFAULT_START_STOP_DEPOT")
        print(f"Your start and stop depot is set to: {fixed_depot} " )
    elif fixed_depot:
        print(f"Your start and stop depot is set to: {fixed_depot} " )

    start_depot = stop_depot = fixed_depot

    csv_file = ReadCsvFile("input1.csv")
    inputs_from_input_csv = csv_file.readCsv()


    validate = Validate
    for record in inputs_from_input_csv:
        if validate.validate_name(record.customer):
            print("OK")
        else:
            print("Not Ok")
        print(record)


if __name__ == '__main__':
    main()
