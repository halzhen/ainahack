"""
Aplicació web amb Streamlit per a l'usuari.
Un cop es penja el fitxer pdf, es processa per a classificar el tràmit i extreure la informació més important
"""

import streamlit as st
from doc_ai import *
from model_roberta import *
from model_salamandra import *
from mongodb_functions import *

st.markdown(
    """
    <style>
    /* Target the main Streamlit app container */
    div.stApp {
        background: white;
        height: 100vh;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.subheader('Gestor de tràmits de la ciutadania')
camps_jus={'Òrgan judicial':('Partit judicial',1),
'Partit judicial':("Certifico que les dades que es consignen més avall sobre la designació d'un/a pèrit/a per fer la prova",1),
'Procediment judicial (denominació, número i secció)':("Àmbit jurisdiccional d'actuació",1),
'Data de nomenament del/de la pèrit/a':('Data de lliurament del dictamen',2),
'Cognoms i nom del/de la pèrit/a designat/ada':('Data de lliurament del dictamen',2),
'Data de lliurament del dictamen':('Dictamen redactat en català',1),
'Data':('NIF',1)
          }

uploaded_file = st.file_uploader("Insertar document:", type=["docx", "pdf", "jpg", "jpeg", "png"])
if uploaded_file is not None:
    text=get_processed_text('documents/'+uploaded_file.name)
    categoria=classificacio_tramit(text)
    if categoria in ['justicia','interior','salut']:
        st.text("L'organisme encarregat del tràmit es : "+categoria)
        #st.text(text)
        #parametros_revisar=camps_buits(text,camps_jus)
        #st.text(parametros_revisar)
        st.text("Resultat d'avaluació dels camps:")
        text_dictio=crear_diccionari(text,categoria)
        st.write(text_dictio)
        pujar_document("Marc",uploaded_file.name,categoria,text_dictio)
    else:
        st.error("No s'ha pogut determinar el organisme encarregat del tràmit")
