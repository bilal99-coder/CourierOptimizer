import os
from dotenv import load_dotenv
from Services.ReadCsvFile import ReadCsvFile
from Utils.Validate import Validate


def main():
    # Load environment variables from .env file.
    load_dotenv()

    greeting = os.getenv("GREETING_MESSAGE_AND_ASK_ABOUT_NAME", "Good day, what is your name?")
    name_of_user = input(greeting + " ")
    print(f"Hello, {name_of_user}!")

    ask_about_start_depot = os.getenv(
        "ASK_ABOUT_START_DEPOT",
        "Nice to meet you {name_of_user}! Please provide the start depot coordinates (or press Enter for default)",
    )
    start_depot = input(ask_about_start_depot.format(name_of_user=name_of_user) + " ")

    if not start_depot:
        end_depot = input("Could you please provide us with the stop depot cordinates? Please click Enter if you want to use the default stop point")
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
