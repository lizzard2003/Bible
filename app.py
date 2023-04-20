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

