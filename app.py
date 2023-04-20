from os import getenv
from dotenv import find_dotenv, load_dotenv
import flask
from flask import Flask

import requests
import random

load_dotenv (find_dotenv())


app = Flask(__name__)
api= "f89bb43fa16f2aad9148c3e7c5d7c31a"
POSSIBLE_BIBLES = [55, 10368]


app.secret_key= "secret"

BIBLE_URL= "https://api.scripture.api.bible/v1/bibles"

app.route('/main')
def main():
    random_verse= random.choice(POSSIBLE_BIBLES)
    response =requests.get(BIBLE_URL+(str(random_verse)+"?"),
    params={
        
        "api_key" : BIBLE_API
    })
    response.raise_for_status()
    bible_data={}
    id=response.json()["id"]
    name=response.json()["name"]
    type=response.json()["type"]
    

    bible_data= {}
    bible_data["id"]=id
    
    bible_data["name"] = name
    bible_data["type"]= type
   

    print (bible_data)
    return flask.jsonify(bible_data)
app.run(debug=True)