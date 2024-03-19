from flask import Flask, render_template, request, redirect, url_for, jsonify
import csv
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    # Read data from CSV file
    with open('static/csv/health.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['customer_name'] == username:
                # Redirect to the dashboard with username as parameter
                return redirect(url_for('dashboard', username=username))
    return 'Invalid username'


from flask import json

# v.1.0
# @app.route('/dashboard/<username>')
# def dashboard(username):
#     data = []
#     parameter_names = set()  # Store unique parameter names
#     parameters_data = {}  # Initialize parameters_data dictionary
#     with open('static/csv/health.csv', 'r') as file:
#         csv_reader = csv.DictReader(file)
#         for row in csv_reader:
#             if row['customer_name'] == username:
#                 test_values = json.loads(row['test_values'])
#                 if 'booking_id' in row:  # Check if 'booking_id' exists in row
#                     parameters_data[row['booking_id']] = test_values  # Store data by booking_id
#                     for parameter in test_values:
#                         parameter_names.add(parameter['parameter_name'])
#                     data.append(row)

#     # Filter out undefined values from parameters_data dictionary
#     parameters_data_filtered = {k: v for k, v in parameters_data.items() if v is not None}

#     parameters_data_json = json.dumps(parameters_data_filtered)  # Convert filtered parameters_data to JSON string
#     return render_template('dashboard.html', username=username, parameter_names=parameter_names, parameters_data_json=parameters_data_json, data=data)

# v 2.0
def parse_csv(filename, selected_date, customer_name):
    parameter_names = set()
    with open(filename, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Check if the row matches the selected date and customer name
            if row['collection_date'] == selected_date and row['customer_name'] == customer_name:
                test_values = json.loads(row['test_values'])
                for parameter in test_values:
                    parameter_names.add(parameter['parameter_name'])
    return parameter_names

from flask import Flask, render_template
import csv
import json

# Function to parse CSV file and extract parameter names for a specific customer
def extract_parameter_names(filename, customer_name):
    parameter_names = set()
    with open(filename, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Check if the row matches the customer name
            if row['customer_name'] == customer_name:
                test_values = json.loads(row['test_values'])
                for parameter in test_values:
                    parameter_names.add(parameter['parameter_name'])
    return parameter_names

@app.route('/dashboard/<username>')
def dashboard(username):
    parameter_names = extract_parameter_names('static/csv/health.csv', username)
    return render_template('dashboard.html', username=username, parameter_names=parameter_names)






@app.route('/get_parameter_data')
def get_parameter_data():
    parameter_name = request.args.get('parameter_name')
    username = request.args.get('username')

    # Read data from the CSV file
    data = []
    with open('static/csv/health.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['customer_name'] == username:
                data.append(row)

    # Filter data based on parameter name
    parameter_data = [row for row in data if row['parameter_name'] == parameter_name]

    return jsonify(parameter_data)



if __name__ == '__main__':
    app.run(debug=True)
