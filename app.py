#jazelle and Lizdelarosa
#login and sing up created..
#still need API, database, ..

import json
from os import getenv
from dotenv import find_dotenv, load_dotenv
from flask import Flask, jsonify, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import requests


load_dotenv(find_dotenv())
app = Flask(__name__)
app.secret_key = "my_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String(150), nullable=False)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
 
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


@app.route("/search")
def search():
    query = request.args.get('query')
    if not query:
        return jsonify(error="Missing search query")
    each_entry.clear()
    results = search_scripture(query)
    
    
    return render_template("results.html", each_entry=each_entry, query=query)
@app.route("/form")
def form():
    return render_template("search.html")

each_entry = []

def search_scripture(query):
    url = f"https://api.scripture.api.bible/v1/bibles/de4e12af7f28f599-02/search?query={query}&sort=relevance"
    headers = {'api-key': getenv("BIBLE_API")}
    response = requests.request("GET", url, headers=headers)
    response_json = json.loads(response.text)
    bible_data = response_json['data']['verses']
    #each_entry = [] # create list that has a 3 Id bible and so on 
    for i in range(10):
        
        bibleId = bible_data[i]['bookId']
        chapterId = bible_data[i]['chapterId']
        text = bible_data[i]['text']
        each_entry.append({'bibleId': bibleId, 'chapterId': chapterId, 'text': text})

if __name__ == "__main__":
    app.run(debug=True, port=5003)