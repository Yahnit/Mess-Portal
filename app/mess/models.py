from flask_sqlalchemy import SQLAlchemy
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Mess(db.Model):
    __tablename__ = 'mess'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    updated_date = db.Column(db.String(80))
    bill = db.Column(db.Integer)

    def __init__(self,name):
        self.name = name
        self.updated_date = datetime.now().strftime("%Y-%m-%d")
        self.bill=0

    def to_dict(self):
        return {
            'name' : self.name,
            'updated_date' : self.updated_date,
            'bill' : self.bill,
        }
    def __repr__(self):
        return "Mess Name : %s Mess Bill: %d Updated Date : %s" % (self.name,self.bill,self.updated_date)

class Cost(db.Model):
    __tablename__ = 'cost'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mess_id = db.Column(db.Integer,db.ForeignKey('mess.id'))
    meal_id = db.Column(db.Integer,db.ForeignKey('meal.id'))
    cost = db.Column(db.Float)
    menu = db.Column(db.String(255))
    day_id = db.Column(db.Integer)

    def __init__(self,mess_id,meal_id,cost,menu,day_id):
        self.mess_id = mess_id
        self.meal_id = meal_id
        self.cost = cost
        self.menu = menu
        self.day_id = day_id

    def to_dict(self):
        return {
            'meal_id' : self.meal_id,
            'mess_id' : self.mess_id,
            'cost' : self.cost,
            'menu' : self.menu,
            'day_id': self.day_id
        }

    def __repr__(self):
        return "Cost : %f , Mess-id : %d , Meal-id : %d , Menu : %s Day_id : %d"  %(self.cost,self.mess_id,self.meal_id,self.menu,self.day_id)

class Bill(db.Model):
    __tablename__ = 'Bill'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bill_id = db.Column(db.Integer)
    isStudent = db.Column(db.Boolean)
    month = db.Column(db.Integer)
    cost = db.Column(db.Integer)

    def __init__(self,bill_id,isStudent,month,cost):
        self.bill_id = bill_id
        self.isStudent = isStudent
        self.month = month
        self.cost = cost

    def to_dict(self):
        return {
            'bill_id' : self.bill_id,
            'month' : self.month,
            'isStudent' : self.isStudent,
            'cost' : self.cost,
        }

    def __repr__(self):
        return "Bill Id %d Month %d cost: %d"  %(self.bill_id,self.month,self.cost)

class Meal(db.Model):
    __tablename__ = 'meal'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Integer)

    def __init__(self,name):
        self.name = name

    def to_dict(self):
        return {
            'name' : self.name
        }

    def __repr__(self):
        return "Meal name: %d"  %(self.name)

class Monthly(db.Model):
    __tablename__ = 'monthly'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    month_id = db.Column(db.Integer)
    mess_id = db.Column(db.Integer)
    student_id = db.Column(db.Integer)
    def __init__(self,month_id,mess_id,student_id):
        self.month_id = month_id
        self.mess_id = mess_id
        self.student_id = student_id
    def to_dict(self):
        return {
            'name' : self.name
        }
    def __repr__(self):
        return "Mess Id : %d Month_id : %d Student_id : %d" % (self.mess_id,self.month_id,self.student_id)
