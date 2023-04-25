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


#class User(db.Model):
   # id = db.Column(db.Integer, primary_key=True)
   # username = db.Column(db.String(80), nullable=False)
    #message = db.Column(db.String(150), nullable=False)
    #likes = db.Column(db.Integer, default=0)
    #dislikes = db.Column(db.Integer, default=0)



@app.route('/')
def home():
    return redirect('/login')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            error = "Oops username already exists.."
            return render_template('signup.html', error=error)

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        session['username'] = username
        return redirect('/dashboard')
    else:
        return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = user.query.filter_by(username=username).first()

        if not User or user.password != password:
            error = "Sorry, Incorrect username or password."
            return render_template('login.html', error=error)

        session['username'] = username
        return redirect('/form')
    else:
        return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        comments = Comment.query.all()
        return render_template('dashboard.html', username=session['username'], comments=comments)
    else:
        return redirect('/login')


@app.route('/add_comment', methods=['POST'])
def add_comment():
    if 'username' in session:
        new_comment = Comment(username=session['username'], message=request.form['message'])
        db.session.add(new_comment)
        db.session.commit()
        return redirect('/dashboard')
    else:
        return redirect('/login')


@app.route('/like_comment', methods=['POST'])
def like_comment():
    if 'username' in session:
        comment_id = request.form['id']
        action = request.form['action']

        comment = Comment.query.get(comment_id)

        if action == 'like':
            comment.likes += 1
        else:
            comment.dislikes += 1

        db.session.commit()

        return redirect('/dashboard')
    else:
        return redirect('/login')


@app.route('/logout')
def logout():
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

app.run(debug=True, port=5003)