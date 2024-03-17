#Imports
from openai import OpenAI
import google.generativeai as genai
import pymongo
from pymongo import MongoClient



#Client creations & tokens
genai.configure(api_key = "<api-key>")
model = genai.GenerativeModel('gemini-pro')


#MongoDB connection & data fetching
def get_patient_docs(customer_name,booking_date):
    cluster = MongoClient("mongodb+srv://anandrm1999:hqC4zZnKxSs55SzJ@cluster0.eqwlhpf.mongodb.net/")
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
    response = model.generate_content("Give me a summary of this test in 30 words only : "+test_name)
    return response.text.strip()


def get_data_cause(test_name, high_low_normal): 
    response = model.generate_content(f"Generate 3 possible causes for {test_name} {high_low_normal} result . Each cause should be 10 words or less and should start with a index number.")
    return response.text.strip().split('\n')
    
def get_data_cause_para(test_name, high_low): 
    response = model.generate_content(f"Give me a general paragraph about {test_name} {high_low} result in only 30 words or less.")
    return response.text.strip()


def get_data_consider(test_name,high_low):
    response = model.generate_content(f"What are the recommended next steps for {test_name} {high_low} results? Please provide concise guidance within 50 words and do not provide causes.")
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
