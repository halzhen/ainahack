"""
Utilitzem el model matxa-tts-cat-multiaccent de Hugging Face per a passar el text a audio.
"""

import requests
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM,AutoModel

with open('hf_token.txt','r') as f:
    hf_token=f.read()
f.close()

url="https://p1b28cv1e843tih1.eu-west-1.aws.endpoints.huggingface.cloud/api/tts"
headers = {
   "Authorization": "Bearer "+hf_token,
}
def query(text):
    data = {"text": text, "voice": "quim", "accent": "balear"}
    return requests.post(url, headers=headers, json=data)

def genera_audio(filename,text):
    response = query(text)
    filename='audios/'+filename.replace('.pdf','')+".wav"
    with open(filename, "wb") as f:
        f.write(response.content)
    f.close()
    return filename