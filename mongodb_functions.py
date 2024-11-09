"""
Funcions per a accedir a la base de dades MongoDB
"""

import pymongo
from datetime import datetime
import os

with open('mongo_uri.txt','r') as f:
    mongo_uri=f.read()
f.close()

myclient = pymongo.MongoClient(mongo_uri)

def get_all_doc_names():
    mydb = myclient["DB_AINA"]
    mycol = mydb["documents"]
    mydoc = mycol.find()
    filenames=[]
    for x in mydoc:
        filenames.append(x['Fitxer'])
    return filenames

def pujar_document(username,filename,categoria,diccionari):
    mydb = myclient["DB_AINA"]
    mycol = mydb["documents"]
    myquery = { "Fitxer": filename }
    mycol.delete_many(myquery)
    mydict = { "Data": str(datetime.now()).split('.')[0], 
              "Usuari": username,
              'Fitxer':filename,
              "Categoria":categoria,
              "Contingut":diccionari}
    x = mycol.insert_one(mydict)
    print(x)
    return x

def search_document(filename):
    mydb = myclient["DB_AINA"]
    mycol = mydb["documents"]
    myquery = { "Fitxer": filename }
    mydoc = mycol.find(myquery)
    for x in mydoc:
        return x
