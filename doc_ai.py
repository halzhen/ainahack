"""
La funció get_processed_text retorna el text d'un pdf amb el servei Document AI de Google Cloud 
"""

from google.cloud import documentai_v1 as documentai
from google.oauth2 import service_account
import io
import json

with open('document_ai_parameters.json', 'r') as f:
    params = json.load(f)
f.close()

PROJECT_ID = params['PROJECT_ID']         
LOCATION = "us"                          
PROCESSOR_ID = params['PROCESSOR_ID']       
KEY_PATH = "credencials.json"  

credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
client = documentai.DocumentProcessorServiceClient(credentials=credentials)
name = f"projects/{PROJECT_ID}/locations/{LOCATION}/processors/{PROCESSOR_ID}"

def get_processed_text(FILE_PATH):
    with io.open(FILE_PATH, "rb") as f:
        file_content = f.read()
    f.close()
    document = {"content": file_content, "mime_type": "application/pdf"}  
    request = documentai.ProcessRequest(name=name, raw_document=document)
    result = client.process_document(request=request)
    document = result.document
    return str(document.text)