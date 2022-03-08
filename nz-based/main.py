#!/../../cloud/bin/python3

from flask import Flask, render_template, request, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'some random key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.sqlite3'

db = SQLAlchemy(app)

@app.errorhandler(404)
def page_not_found(e):
    # return render_template('file.html'), 404
    return 'page not found'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/email_check', methods=['POST'])
def email_check():
    if request.method == 'POST':
        email = request.form.get('email')
        print(email)
        email_exists = Users.query.filter_by(email=email).first()
        if email_exists is not None:
            resp = jsonify('<span style="\'color:red;\'">Email already registered. Try to Login.</span>')
            resp.status_code = 200
            return resp

@app.route('/user-details/', methods=['POST', 'GET'])
def user_details():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password = generate_password_hash(password)
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        age = request.form.get('age')
        gender = request.form.get('gender')
        location = request.form.get('location')
        
        user = Users(email=email, password=password, firstname=firstname, lastname=lastname, \
            age=age, gender=gender, location=location)
        db.session.add(user)
        db.session.commit()
        session['username'] = email
        return render_template('welcome.html')
    else:
        return render_template('signup.html')

@app.route('/signup/', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        return render_template('signup.html')
    return render_template('signup.html')

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Users.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['username'] = email
            return render_template('welcome.html')
        else:
            flash('Invalid Credentials!')
            return render_template('index.html')
    return render_template('index.html')

@app.route('/logout/')
def logOut():
    session.pop('username', None)
    session['username'] = None
    return render_template('index.html')

if __name__ == '__main__':
    from models import Users, db
    db.create_all()
    app.run(debug=True)
