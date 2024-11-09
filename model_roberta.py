"""
Utilitzem el model roberta-base-ca-cased-sts de Hugging Face per a classificar el tràmit.
"""

from transformers import pipeline, AutoTokenizer
from scipy.special import logit
from doc_ai import get_processed_text
import pandas as pd
templates={}
for ambito_template in ['interior','salut','justicia']:
    with open('processed_templates/template_'+ambito_template+'.txt','r',encoding='utf8') as f:
        templates[ambito_template]=f.read()
    f.close()
model = 'projecte-aina/roberta-base-ca-cased-sts'
tokenizer = AutoTokenizer.from_pretrained(model)
pipe = pipeline('text-classification', model=model, tokenizer=tokenizer)

def prepare(sentence_pair):
    sentence_pairs_prep = []
    sentence_pairs_prep.append(f"{tokenizer.cls_token} {sentence_pair[0]}{tokenizer.sep_token}{tokenizer.sep_token} {sentence_pair[1]}{tokenizer.sep_token}")
    return sentence_pairs_prep

def classificacio_tramit(text):
    maxim=0.92
    categoria='No categoria'
    for key in list(templates.keys()):
        predictions = pipe(prepare((text[:700], templates[key][:700])), add_special_tokens=False)
        score=predictions[0]['score']
        if score>maxim:
            categoria=key
            maxim=score
    return categoria