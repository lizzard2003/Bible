#jazelle and Lizdelarosa
#login and sing up created..
#still need API, database, ..

from flask import Flask, render_template, request, redirect, session

load_dotenv(find_dotenv())
app = Flask(__name__)
app.secret_key = "my_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'
db = SQLAlchemy(app)


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
        return redirect('/dashboard')
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
