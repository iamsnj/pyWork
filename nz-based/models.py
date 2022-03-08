from main import db

class Users(db.Model):
    email = db.Column(db.String(32), primary_key=True)
    password = db.Column(db.String(32))
    firstname = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    location = db.Column(db.String(32))
