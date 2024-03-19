import csv
import json
def dashboard(username):
    data = []
    parameter_names = set()  # Store unique parameter names
    parameters_data = {}  # Initialize parameters_data dictionary
    with open('static/csv/health.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['customer_name'] == username:
                test_values = json.loads(row['test_values'])
                parameters_data[row['booking_id']] = test_values  # Store data by booking_id
                for parameter in test_values:
                    parameter_names.add(parameter['parameter_name'])
                data.append(row)

    return parameter_names, parameters_data, data

print(dashboard('Priyank Jain'))