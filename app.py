<<<<<<< HEAD
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
=======
#jazelle and Lizdelarosa
#login and sing up created..
#still need API, database, ..

from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "my_secret_key"
 
users = {}

@app.route('/')
def home():
    return redirect('/login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
#here is so the user can make their OWN user name y password 
#sign up html the only affected from this update!
        if username in users:
            error = "Oops username already exists.."
            return render_template('signup.html', error=error)
        
        users[username] = password
    
        session['username'] = username
        return redirect('/dashboard')
    else:
        return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
#wrong pass word or email.. retry 
        if username not in users or users[username] != password:
            error = "Sorry, Incorrect username or password."
            return render_template('login.html', error=error)
        session['username'] = username
        return redirect('/dashboard')
    else:
        return render_template('login.html')

@app.route('/dashboard')
def dashboard():
#render bk to dashboard..
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect('/login')

@app.route('/logout')
def logout():
#logout option after logged on on dashboard page
    session.pop('username', None)
    return redirect('/login')
>>>>>>> origin/main
