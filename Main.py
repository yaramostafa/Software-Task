import json
import time
from database import SQLiteDataSink
from django_database import get_expression
from interpreter import *

def process_message(message, equation):

    message_obj = json.loads(message)
    attr_value = message_obj.get("value", "")  # Get returns default value if not found

    # Check if attr_value is numeric
    try:
        numeric_value = float(attr_value)
    except ValueError:
        numeric_value = None

    try:
        lexer = Lexer(equation)
    except Exception as e:
        raise Exception("Asset not linked to a KPI")

    parser = Parser(lexer)

    try:
        if "Regex" in equation:  # Handles regex equations
            interpreter = Interpreter(parser, attr_value)
        else:  # Handles arithmetic equations
            if numeric_value is None:
                raise ValueError(f"Non-numeric value '{attr_value}' cannot be used in arithmetic equations")
            parser.attr_value = numeric_value  # Pass numeric value to parser
            interpreter = Interpreter(parser, str(numeric_value))

        tree = parser.parse()
        if tree is None:  # Ensuring tree is valid
            raise Exception("Failed to parse equation: Invalid AST")

        result = interpreter.visit(tree)

        output_message = {
            "asset_id": message_obj["asset_id"],
            "attribute_id": "output_" + message_obj["attribute_id"],
            "timestamp": message_obj["timestamp"],
            "value": result
        }
        return output_message

    except Exception as e:
        raise Exception(f"Error processing message: {e}")


class FileReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.last_position = 0

    def read_new_records(self):
        """Read new records from the file starting from the last position."""
        with open(self.file_path, "r") as file:
            file.seek(self.last_position)
            records = file.readlines()
            self.last_position = file.tell()
        return [record.strip() for record in records if record.strip()]


class DataProcessor:
    def __init__(self, data_sink):
        self.data_sink = data_sink

    def process_records(self, records):
        """Processes a batch of records."""
        for record in records:
            try:
                # print("process_records",record)
                asset_id = json.loads(record.strip())['asset_id']
                output_message = process_message(record, get_expression(asset_id))
                self.data_sink.write_message(output_message)
                print(output_message)
            except Exception as e:
                print(f"Error processing record: {record}, Error: {e}")


def main():
    input_file = "djangoTask/data.txt"
    db_name = "processed_data.db" # DB to save the output on
    # config_file = "config.txt"

    # initialize dependencies
    data_sink = SQLiteDataSink(db_name)
    file_reader = FileReader(input_file)

    # Create the processor
    processor = DataProcessor(data_sink)

    try:
        while True:
            # Read new records every 5 seconds
            new_records = file_reader.read_new_records()
            processor.process_records(new_records)
            time.sleep(5)
    finally:
        data_sink.close()

if __name__ == "__main__":
    main()