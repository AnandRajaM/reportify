"""
Data fetching service - handles MongoDB queries and AI-powered insights
"""
import google.generativeai as genai
from pymongo import MongoClient
from typing import List, Tuple, Optional
from app.core.config import settings
from app.core.database import get_database


# Configure Gemini AI
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')


class DataFetchingService:
    """Service for fetching patient data and AI-generated insights"""
    
    def __init__(self):
        self.db = get_database()
    
    def get_patient_docs(self, customer_name: str, booking_date: str) -> Tuple[List, Optional[str]]:
        """
        Fetch patient documents from MongoDB
        
        Args:
            customer_name: Patient's name
            booking_date: Booking date
            
        Returns:
            Tuple of (patient_tests, booking_id)
        """
        collection = self.db[settings.COLLECTION_NAME]
        
        query = {
            "$and": [
                {"customer_name": customer_name},
                {"booking_date": booking_date},
            ]
        }
        
        result = collection.find(query)
        booking_id = None
        patient_tests = []
        
        for doc in result:
            booking_id = doc.get('booking_id')
            patient_tests.append((doc['test_name'], doc['test_values']))
        
        return patient_tests, booking_id
    
    @staticmethod
    def get_test_summary(test_name: str) -> str:
        """
        Get AI-generated summary for a medical test
        
        Args:
            test_name: Name of the medical test
            
        Returns:
            Summary text (30 words)
        """
        try:
            response = model.generate_content(
                f"Give me a summary of this test in 30 words only: {test_name}"
            )
            return response.text.strip()
        except Exception as e:
            return f"Summary unavailable for {test_name}"
    
    @staticmethod
    def get_test_causes(test_name: str, status: str) -> List[str]:
        """
        Get possible causes for abnormal test results
        
        Args:
            test_name: Name of the test
            status: 'high', 'low', or 'normal'
            
        Returns:
            List of possible causes
        """
        try:
            prompt = f"Generate 3 possible causes for {test_name} {status} result. " \
                    f"Each cause should be 10 words or less and should start with a index number."
            response = model.generate_content(prompt)
            return response.text.strip().split('\n')
        except Exception as e:
            return ["Unable to generate causes"]
    
    @staticmethod
    def get_cause_paragraph(test_name: str, status: str) -> str:
        """
        Get a paragraph explaining the test result status
        
        Args:
            test_name: Name of the test
            status: 'high' or 'low'
            
        Returns:
            Paragraph (30 words or less)
        """
        try:
            prompt = f"Give me a general paragraph about {test_name} {status} result in only 30 words or less."
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Information unavailable for {test_name} {status} result"
    
    @staticmethod
    def get_recommendations(test_name: str, status: str) -> str:
        """
        Get recommended next steps for abnormal results
        
        Args:
            test_name: Name of the test
            status: 'high' or 'low'
            
        Returns:
            Recommendations (50 words or less)
        """
        try:
            prompt = f"What are the recommended next steps for {test_name} {status} results? " \
                    f"Please provide concise guidance within 50 words and do not provide causes."
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return "Consult with your healthcare provider for personalized recommendations."
    
    @staticmethod
    def merge_test_lists(existing_list: List, new_list: List) -> List:
        """
        Merge test lists avoiding duplicates
        
        Args:
            existing_list: Current list of tests
            new_list: New tests to merge
            
        Returns:
            Merged list
        """
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


# Create service instance
data_service = DataFetchingService()
