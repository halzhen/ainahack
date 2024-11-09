"""
Utilitzem el model salamandra-7b-instruct-aina-hack de Hugging Face per a extreure els camps més rellevants del pdf.
"""

import requests
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM,AutoModel
from model_roberta import *
model_name = "BSC-LT/salamandra-7b-instruct-aina-hack"
tokenizer = AutoTokenizer.from_pretrained(model_name)

with open('hf_token.txt','r') as f:
    hf_token=f.read()
f.close()

url='https://hijbc1ux6ie03ouo.us-east-1.aws.endpoints.huggingface.cloud'
headers = {
    "Accept" : "application/json",
    "Authorization": f"Bearer "+hf_token,
    "Content-Type": "application/json"
}

def retornar_resposta(text,system_prompt):
    message = [ { "role": "system", "content": system_prompt} ]
    message += [ { "role": "user", "content": text } ]
    prompt = tokenizer.apply_chat_template(
       message,
       tokenize=False,
       add_generation_prompt=True,
    )

    payload = {
       "inputs": prompt,
       "parameters": {"temperature":1,"max_new_tokens":300}
    }
    api_url = url + "/generate"
    response = requests.post(api_url, headers=headers, json=payload)
    return response.json()['generated_text']

def crear_diccionari(text,categoria):
    if categoria=='justicia':
        camps={'Òrgan judicial':'El format te que tenir format similar a Jutjat n1 de Blanes',
               'Partit judicial':"El format te que tenir contenir el nom d'una ciutat",
               'Procediment judicial (denominació, número i secció)':'Es un alfanumèric similar a Procediment Monitori núm. 9243/2014 - Secció 1b',
               'Data de nomenament del/de la pèrit/a':'Format de data tipus 01/01/2000',
               'Cognoms i nom del/de la pèrit/a designat/ada':'El format ha de ser nom i cognos de persona amb la primera lletra en majúscules',
               'Data de lliurament del dictamen':'Format de data tipus 01/01/2000',
               'Data':'El format ha de ser similar a 01/01/2000'}
    elif categoria=='salut':
        camps={'Cognoms i nom de la persona assegurada':'Han de ser noms propis i entre una i tres paraules','CIP':'Es un conjunt alfanuméric','DNI/NIF/NIE':'Es un conjunt de números que acaba amb una lletra majúscula','Adreça':"Ha de ser un carrer amb número d'habitatge i porta, no una ciutat",'Població':'Ha de ser una ciutat i no una adreça , no pot tenir números'}
    elif categoria=='interior':
        camps={'Nom i cognoms':'Han de ser noms propis i entre una i tres paraules','NIF':'Es un conjunt alfanuméric','Telèfon':'Ha de ser un número de telèfon','Adreça':"Ha de ser un carrer amb número d'habitatge i porta, no una ciutat",'Correu electrònic':'Ha de ser una direcció de correu amb un caràcter @'}
    new_dictio={}
    for camp in list(camps.keys()):
        system_prompt="""Retorna el valor per el camp """+camp+""". """+camps[camp]+""". Busca el nom del camp i cerca el seu valor corresponent en les línies posteriors. Document:"""
        valor=retornar_resposta(text,system_prompt)
        valor=valor.split('\n')[0]
        new_dictio[camp]=valor
    return new_dictio