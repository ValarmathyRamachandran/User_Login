from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient

app= Flask(__name__)
app.secret_key = 'secret_key'
client = MongoClient('mongodb://localhost:27017/')
db = client['user_database']
collection = db['users']


@app.route('/')
def home():
    if 'username' in session:
        return f"Logged in as {session['username']}"
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = collection.find_one({'username': username})
        if existing_user:
            return "Username already exists!"
        new_user = {'username': username, 'password': password}
        collection.insert_one(new_user)
        session['username'] = username
        return redirect('/')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = collection.find_one({'username': username})
        if user and user['password'] == password:
            session['username'] = username
            return redirect('/')
        return "Invalid username or password"
    return render_template('login.html')
