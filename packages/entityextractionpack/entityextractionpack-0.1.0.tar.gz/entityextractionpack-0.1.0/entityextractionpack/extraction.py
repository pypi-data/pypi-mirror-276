# import google.generativeai as genai
# from langchain.document_loaders import PyPDFLoader
# from langchain_community.document_loaders import PyPDFLoader
import os

import google.generativeai as genai
from langchain_community.document_loaders import PyPDFLoader

def setup_environment(pdf1_path, pdf2_path):
    loader1 = PyPDFLoader(pdf1_path)
    pages1 = loader1.load()

    loader2 = PyPDFLoader(pdf2_path)
    pages2 = loader2.load()

    # Replace with your actual Gemini API key
    gemini_api_key = "AIzaSyDMqmQEpgoG9n03UZ0OhMjgai0b5etks3w"

    # Configure Gemini API
    genai.configure(api_key=gemini_api_key)

    # Set up the model
    generation_config = {
      "temperature": 0.9,
      "top_p": 1,
      "top_k": 1,
      "max_output_tokens": 2048,
    }

    safety_settings = [
      {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
      {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
      {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
      {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)

    convo = model.start_chat(history=[])
    
    return pages1, pages2, convo

# Function for Cell3
def extract_entities(pages1, pages2, convo):
    import pandas as pd
    
    # Store extracted entities from both PDFs
    all_entities = {'pdf1': {}, 'pdf2': {}}

    # Extract entities from the first PDF
    for page in pages1:
        page_content = page.page_content

        for block in page_content.split("\n\n"):
            response = convo.send_message(f"Extract entities (Booking No, Address, Order No, Vessel name, OBOL number, Depart date, Cutoff date, Destination port, etc.) from this text:\n{block}")
            extracted_entities = response.text.split("\n")
            for entity in extracted_entities:
                try:
                    entity_type, entity_value = entity.split(":", 1)
                    all_entities['pdf1'][entity_type.strip()] = entity_value.strip()
                except ValueError:
                    pass

    # Extract entities from the second PDF
    for page in pages2:
        page_content = page.page_content

        for block in page_content.split("\n\n"):
            response = convo.send_message(f"Extract entities (Sea waybill no, Voyage no, Booking Ref, Port of Discharge, Date of issue, Onboard date, SCAC code etc.) from this text:\n{block}")
            extracted_entities = response.text.split("\n")
            for entity in extracted_entities:
                try:
                    entity_type, entity_value = entity.split(":", 1)
                    all_entities['pdf2'][entity_type.strip()] = entity_value.strip()
                except ValueError:
                    pass

    return all_entities