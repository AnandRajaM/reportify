#Imports
from openai import OpenAI
from google import genai
import pymongo
from pymongo import MongoClient
import os
import json
import time

client = genai.Client( api_key="AIzaSyC-A4uUzz9_wy-0fuRAUt1u-TB3GW9wKC0")


#MongoDB connection & data fetching
def get_patient_docs(customer_name,booking_date):
    cluster = MongoClient("<mogodb-connection>")
    db = cluster['RedCliffe_Labs']
    collection = db['patient_details']
    # Construct query
    query = {
        "$and": [
            {"customer_name": customer_name},
            {"booking_date": booking_date},
        ]
    }
    # Find documents matching the query
    result = collection.find(query)
    booking_id = None
    patient_tests = []
    # Iterate over the result
    for doc in result:
        booking_id = doc['booking_id']
        patient_tests.append((doc['test_name'], doc['test_values']))
        
    return patient_tests,booking_id



#Medical data fetching
def get_data(test_name):  
    print("v1")
    time.sleep(10)
    response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Give me a summary of this test in 30 words only : "+test_name
)
    return response.text.strip()


def get_data_cause(test_name, high_low_normal): 
    time.sleep(10)
    response = client.models.generate_content(
    model="gemini-2.5-flash", contents=f"Generate 3 possible causes for {test_name} {high_low_normal} result . Each cause should be 10 words or less and should start with a index number.")
    return response.text.strip().split('\n')
    
def get_data_cause_para(test_name, high_low): 
    time.sleep(10)
    response = client.models.generate_content(
    model="gemini-2.5-flash", contents=f"Give me a general paragraph about {test_name} {high_low} result in only 30 words or less.")
    return response.text.strip()


def get_data_consider(test_name,high_low):
    time.sleep(10)
    response = client.models.generate_content(
    model="gemini-2.5-flash", contents=f"What are the recommended next steps for {test_name} {high_low} results? Please provide concise guidance within 50 words and do not provide causes.")
    return response.text.strip()


def merge_lists(existing_list, new_list):
    for new_item in new_list:
        found = False
        for existing_item in existing_list:
            if existing_item[0] == new_item[0]:
                existing_item[1].append(new_item[1])
                found = True
                break
        if not found:
            existing_list.append([new_item[0], [new_item[1]]])
        
    return existing_list

def useSampleData():
    print("v0")
    result = json.load(open('./reportGen/sampleData/sample1.json'))

    booking_id = result['booking_id']
    patient_tests = []

    patient_tests.append(
        (result['test_name'], result['test_values'])
    )

    return patient_tests, booking_id
