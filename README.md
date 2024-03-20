
# Reportify - Simplifying Diagnostic Reports


## Overview
The Reportify Diagnostic Test Reporting System is a project developed by the "a² Team" for TinkerQuest'24, a hackathon hosted by IIT Roorkee. The system aims to provide users with intuitive and informative reports for diagnostic test results, enhancing their understanding and enabling better healthcare decisions.
## Features
- **Smart Report Generation:** Automatically generates comprehensive reports for diagnostic test results, including flagged tests, normal tests, and graphical representation of abnormalities.
- **Customized Cover Pages:** Reports are generated with cover pages, barcodes, and summaries for enhanced presentation.
- **Visualization:** Utilizes gray body diagrams to highlight flagged test results.
- **Test Definitions:** Provides detailed descriptions and use examples for each diagnostic test.
- **Ranges Representation:** Displays low-normal-high ranges for test parameters, aiding interpretation.
- **ML Model Integration:** Utilizes langchain.llms - Ollama for generating summaries and possible causes for abnormal test results.
- **User Dashboard:** Provides users with a personalized dashboard to view past test results and generate/print reports.
- **Interactive UI:** Developed with HTML, CSS, Tailwind CSS, and JavaScript for a seamless user experience.
- **Backend Storage:** Stores diagnostic reports data using MongoDB in the cloud (AWS), managed with PyMongo.
- **Gemini API Integration:** Utilizes Gemini API for fetching data on test summaries.
- **Barcode & QR Generation:** Includes barcode&QRgeneration for easy identification and tracking of reports.
## Demo

Check it out on our live website : https://reportifylanding.vercel.app/

Or watch a video here

https://github.com/AnandRajaM/tinkerquest2024/assets/142321494/b66bb259-1256-46ea-9949-ae29e5a36d7f


## Screenshots
![App Screenshot](https://github.com/AnandRajaM/tinkerquest2024/blob/main/images/website_landing.png)
![App Screenshot](https://github.com/AnandRajaM/tinkerquest2024/blob/main/images/coverpage.png)
![App Screenshot](https://github.com/AnandRajaM/tinkerquest2024/blob/main/images/summary.png)
![App Screenshot](https://github.com/AnandRajaM/tinkerquest2024/blob/main/images/rbc.png)
![App Screenshot](https://github.com/AnandRajaM/tinkerquest2024/blob/main/images/report_page.png)
![App Screenshot](https://github.com/AnandRajaM/tinkerquest2024/blob/main/images/value.png)

## Brief on the working 
- **Data Retrieval:** The program begins by retrieving data from the MongoDB cloud database hosted on AWS. Using the customer/patient name and booking date as search parameters, it identifies all diagnostic tests conducted on that particular date.

- **Diagnostic Test Classification:** The retrieved diagnostic tests are classified into two main types:
  - Tests with Multiple Sub-tests: Examples include Kidney Function Test (KFT) with sub-tests like Blood Urea, Creatinine, etc.
  - Multi Value Tests: Tests like RBC count, Urine Routine, etc., which includes multiple values.
   
- **Report Generation:**
  - Multiple Sub-tests: For tests with multiple sub-tests, the program generates detailed reports for each sub-test, providing a comprehensive overview of the individual parameters measured. The program creates easily readable reports with graphical representations. A horizontal bar with green & red areas indicating normal, high, and low values. The user's test result is positioned on the bar for quick interpretation.
  - Multi Value Tests: For these tests , the program generates a table like report containing Test Description , Values , Units and referene range for differnt  parameters such as rbc , wbc , platelets etc. Along with this , each "Multi Value report" also has a note & advice section at the end , which can be added by the respective medical proffesional.

- **Summary Page Creation:** The program generates a summary page consolidating all test results. Tests are categorized as highlighted (indicating abnormal values) or non-highlighted (normal values).
Highlighted tests are visually linked to a gray body diagram, with lines drawn to the respective organ or body part affected by the abnormal result. For instance, if a Kidney Function Test result is abnormal, a line is drawn to the kidney region on the gray body image.

** Cover Page Generation:** Each report is accompanied by a customized cover page, providing patient-specific details and enhancing the presentation of the diagnostic report.

## Technologies Used

### Frontend
- HTML
- CSS
- Tailwind CSS
- JavaScript
- Flask (for backend communication)

### Backend
- MongoDB (AWS)
- PyMongo
- LangChain.llms - Ollama (Machine Learning Model)

### Report Generation
- Google.generativeai
- ReportLab
- PyPDF2 
- Barcode (EAN13)

## Machine Learning Model
Our Smart Diagnostic Report Generator incorporates the LangChain.llms - Ollama machine learning model to enhance the interpretability of diagnostic test results. This model plays a crucial role in providing simple summaries of specific tests, assisting users in understanding their results more comprehensively.
### LangChain.llms - Ollama
LangChain.llms - Ollama is a state-of-the-art language model trained on a large corpus of medical texts and healthcare literature. Leveraging the power of large language models (LLMs) like GPT-3, LangChain.llms - Ollama is fine-tuned specifically for medical applications, making it adept at understanding and generating medical text.

### Functionality
**Summarization:** Given a specific input query related to a diagnostic test (e.g., "{test} high"), LangChain.llms - Ollama generates a concise summary of the test along with potential causes for abnormal results. This summarization capability aids users in interpreting their test results effectively.
## Sample Dataset
```{
  "_id": {
    "$oid": "65436af849afd751c456ccb9"
  },
  "booking_id": 6064579,
  "customer_name": "Sarika Singh",
  "collection_date": "2023-11-02 00:00:00 UTC",
  "booking_date": "2023-11-01 00:00:00 UTC",
  "lead_id": 8032545,
  "uhid": 5190833,
  "useruuid": {
    "$binary": {
      "base64": "iEP/haC/QFmbRttS0953BQ==",
      "subType": "04"
    }
  },
  "test_id": 5667,
  "test_code": "BC063",
  "test_name": "Thyroid Profile Total",
  "test_values": [
    {
      "test_method": "",
      "test_parameter_id": 7050768,
      "parameter_name": "TRIIODOTHYRONINE ( T3 )",
      "parameter_value": "96.23",
      "is_highlighted": false,
      "lower_bound": "35",
      "display_value": "35 - 193",
      "upper_bound": "193",
      "impression": "N",
      "unit": "ng/dL",
      "other_male_id": "44"
    },
    {
      "test_method": "",
      "test_parameter_id": 7050769,
      "parameter_name": "TOTAL THYROXINE ( T4 )",
      "parameter_value": "6.49",
      "is_highlighted": false,
      "lower_bound": "4.87",
      "display_value": "4.87 - 11.72",
      "upper_bound": "11.72",
      "impression": "N",
      "unit": "µg/dL",
      "other_male_id": "4"
    },
    {
      "test_method": "CMIA",
      "test_parameter_id": 7052387,
      "parameter_name": "THYROID STIMULATING HORMONE  (Ultrasensitive)",
      "parameter_value": "4.4928",
      "is_highlighted": false,
      "lower_bound": "0.35",
      "display_value": "0.35 - 4.94",
      "upper_bound": "4.94",
      "impression": "N",
      "unit": "uIU/mL",
      "other_male_id": "41"
    }
  ],
  "created_at": "2023-11-02 09:25:12.613 UTC",
  "updated_at": "2023-11-02 09:25:12.613 UTC",
  "__hevo_id": "3be12f5b27fbe5cd9c2b58bdab8af2f317f32cd2bffff51ba3c765223fb9b5b2",
  "__hevo__ingested_at": {
    "$numberLong": "1698917364978"
  },
  "__hevo__loaded_at": {
    "$numberLong": "1698921148662"
  },
  "__hevo__marked_deleted": false,
  "__hevo__source_modified_at": {
    "$numberLong": "1698917112000"
  }
}
```
## Getting Started
-  1:  Clone the repository: git clone https://github.com/AnandRajaM/tinkerquest2024.git
- 2:  Install dependencies: pip install -r requirements.txt
- 3:  Set up MongoDB with your prefered dataset
- 4:  Run the Flask application: python app.py
- 5:  Access the application at http://localhost:5000
## Authors

- Anand Raja Mohan [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/anandrajam/) [![github](https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/AnandRajaM)

- Atharv Rastogi [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/atharv-rastogi-b9612a278/) [![github](https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Atharv714)

- Atul Akela [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/atulakella/) [![github](https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/atulakella)

- Aabir [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com) [![github](https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/aabir-2004)
