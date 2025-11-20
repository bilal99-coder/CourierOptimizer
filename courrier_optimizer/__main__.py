from Services.ReadCsvFile import ReadCsvFile
from Utils.Validate import Validate
def main():
    csv_file = ReadCsvFile("input1.csv")
    inputs_from_input_csv = csv_file.readCsv()
    validate = Validate
    for input in inputs_from_input_csv:
        if validate.validate_name(input.customer):
            print("OK")
        else:
            print("Not Ok")
        print(input)

if __name__ == '__main__':
    main()
