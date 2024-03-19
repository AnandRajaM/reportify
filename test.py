import pymongo
from pymongo import MongoClient



#Client creations & tokens


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


patient_docs, booking_id = get_patient_docs('N K Mohanty', "2023-11-01 00:00:00 UTC")
test_names = [(item[0],) for item in patient_docs]

print(test_names)


