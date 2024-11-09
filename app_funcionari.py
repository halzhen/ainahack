"""
Aplicació web amb Streamlit per a l'administratiu.
Es selecciona el pdf a revisar, que es renderitza i es mostra el processament fet amb IA.
També hi ha la funció per escoltar en audio amb el text processat.
"""

import streamlit as st
from mongodb_functions import *
from model_tts import *
import base64
st.subheader('Plataforma de classificació de tràmits')
filenames=get_all_doc_names()

filename = st.selectbox(
    "Tria un fitxer:",
    filenames,
)

with open('documents/'+filename, "rb") as f:
    base64_pdf = base64.b64encode(f.read()).decode("utf-8")

pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="500" height="600" type="application/pdf"></iframe>'
st.sidebar.markdown(pdf_display, unsafe_allow_html=True)

st.text('Informació del document '+filename+':')
doc=search_document(filename)
st.text('Data Publicació:'+doc['Data'])
st.text('Usuari:'+doc['Usuari'])
st.text('Departament:'+doc['Categoria'])
st.text('Contingut:\n')
st.write(doc['Contingut'])
audiotext=''
for key in doc['Contingut'].keys():
    audiotext=audiotext+'El camp '+key+" es "+doc['Contingut'][key]+'.\n'
audioname=genera_audio(filename,audiotext)
st.audio(audioname, format="audio/wav")