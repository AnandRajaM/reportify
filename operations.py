'''import barcode
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
'''
from openai import OpenAI
import math
from reportlab.graphics.shapes import Line, Polygon


client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key='api-key',
)


def get_data(test_name):  
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Give me a summary of this test in 50 words only : "+test_name}]
    )
    return response.choices[0].message.content.strip()


def get_data_cause(test_name, high_low_normal): 
    if high_low_normal == "normal":
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Give me 3 causes for {test_name} {high_low_normal} result in a Python list. Each cause should be 15 words or less."}]
        )
        return response.choices[0].message.content.strip().split('\n')

    else:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Give me 3 causes for {test_name} {high_low_normal} result in a Python list. Each cause should be 15 words or less."}]
        )
        return response.choices[0].message.content.strip().split('\n')

def get_data_cause_para(test_name, high_low): 
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Give me a general paragraph about {test_name} {high_low} result in 50 words."}]
    )
    return response.choices[0].message.content.strip()


def get_data_consider(test_name,high_low):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"What are the recommended next steps for {test_name} {high_low} results? Please provide concise guidance within 30 words or less and do not provide causes."}]
    )
    return response.choices[0].message.content.strip()
