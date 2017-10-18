from flask_sqlalchemy import SQLAlchemy
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app.users.models import Student

class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer,db.ForeignKey('students.id'))
    date = db.Column(db.String(80))
    meal_id = db.Column(db.Integer,db.ForeignKey('meal.id'))
    mess_id = db.Column(db.Integer,db.ForeignKey('mess.id'))
    RFID = db.Column(db.Integer,db.ForeignKey('mess.id'))
    frequency = db.Column(db.Integer)
    cancelled = db.Column(db.Boolean)
    def __init__(self,student_id,date,meal_id,mess_id,RFID,frequency):
        self.student_id = student_id
        self.date = date
        self.meal_id = meal_id
        self.mess_id = mess_id
        self.RFID = RFID
        self.frequency = frequency
        self.cancelled = False
    def to_dict(self):
        return {
            'id'   : self.student_id,
            'data' : self.date,
            'meal_id' : self.meal_id,
            'mess_id' : self.mess_id,
            'RFID' : self.RFID,
            'frequency' : self.frequency,
        }

    def __repr__(self):
        return "Data Student_id: %d Mess_id: %d Date: %s Meal_id : %d" % (self.student_id,self.mess_id,self.date,self.meal_id)

class Complaint(db.Model):
    __tablename__ = 'complaint'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer,db.ForeignKey('students.id'))
    date = db.Column(db.String(80))
    message = db.Column(db.String(500))
    status = db.Column(db.String(100))

    def __init__(self, student_id, message):
        self.student_id = student_id
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.message = message
        self.status = "unresolved"

    def to_dict(self):
        return {
            'student_id' : self.student_id,
            'date': self.date,
            'message': self.message,
        }

    def __repr__(self):
        return "Student Id :%s Message : %s Status :" % (self.student_id,self.message)
