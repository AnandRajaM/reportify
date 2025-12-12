"""
Flask Web Routes
Traditional web application routes for the UI
"""
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import csv
import json
import os

web_bp = Blueprint('web', __name__)


def extract_parameter_names(filename: str, customer_name: str) -> set:
    """
    Extract unique parameter names for a customer from CSV
    
    Args:
        filename: CSV file path
        customer_name: Customer name
        
    Returns:
        Set of parameter names
    """
    parameter_names = set()
    
    if not os.path.exists(filename):
        return parameter_names
    
    with open(filename, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row.get('customer_name') == customer_name:
                test_values = json.loads(row.get('test_values', '[]'))
                for parameter in test_values:
                    parameter_names.add(parameter.get('parameter_name'))
    
    return parameter_names


@web_bp.route('/')
def index():
    """Home page"""
    return render_template("index.html")



@web_bp.route('/signin')
def signin():
    """Sign in page"""
    return render_template('signin.html')


@web_bp.route('/login', methods=['POST'])
def login():
    """Handle login form submission"""
    username = request.form.get('username')
    
    if not username:
        return 'Username required', 400
    
    # Read data from CSV file
    csv_path = 'static/csv/health.csv'
    
    if not os.path.exists(csv_path):
        return 'Data file not found', 500
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row.get('customer_name') == username:
                return redirect(url_for('web.dashboard', username=username))
    
    return 'Invalid username', 401


@web_bp.route('/dashboard/<username>')
def dashboard(username):
    """
    Dashboard page showing patient health data
    
    Args:
        username: Patient username
    """
    csv_path = 'static/csv/health.csv'
    parameter_names = extract_parameter_names(csv_path, username)
    
    return render_template(
        'dashboard.html', 
        username=username, 
        parameter_names=parameter_names
    )


@web_bp.route('/get_parameter_data')
def get_parameter_data():
    """
    API endpoint to get parameter data for a specific user
    
    Query params:
        parameter_name: Name of the parameter
        username: Patient username
    """
    parameter_name = request.args.get('parameter_name')
    username = request.args.get('username')
    
    if not parameter_name or not username:
        return jsonify({'error': 'Missing parameters'}), 400
    
    csv_path = 'static/csv/health.csv'
    
    if not os.path.exists(csv_path):
        return jsonify({'error': 'Data file not found'}), 500
    
    # Read data from CSV
    data = []
    with open(csv_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row.get('customer_name') == username:
                data.append(row)
    
    # Filter data based on parameter name
    parameter_data = [
        row for row in data 
        if row.get('parameter_name') == parameter_name
    ]
    
    return jsonify(parameter_data)
