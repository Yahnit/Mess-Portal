from flask_sqlalchemy import SQLAlchemy
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    rollno = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    updated_date = db.Column(db.String(80))
    bill = db.Column(db.Integer)
    admin = db.Column(db.Boolean)
    default_mess = db.Column(db.Integer)

    def __init__(self, name, rollno, email, password):
        self.name = name
        self.rollno = rollno
        self.email = email
        self.password = generate_password_hash(password)
        self.active = False
        self.bill = 0
        self.admin = False
        self.updated_date = datetime.now().strftime("%Y-%m-%d")

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id' : self.id,
            'rollno' : self.rollno,
            'name': self.name,
            'email': self.email,
            'admin': self.admin,
            'active': self.active,
            'bill' : self.bill,
            'updated_date' : self.updated_date,
        }

    def __repr__(self):
        return "Student Rollno :%d Name :%s" % (self.rollno, self.name)

class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id' : self.id,
            'name': self.name,
            'email': self.email,
        }

    def __repr__(self):
        return "Admin Name :%s" % self.name
