from flask import Blueprint, request, session, jsonify,make_response
from sqlalchemy.exc import IntegrityError
from app import db,requires_student_auth,requires_admin_auth
from app.users.models import *
from app.mess.models import *
from app.data.models import *
from datetime import datetime
from sqlalchemy import *
from datetime import *
from calendar import monthrange


mod_mess = Blueprint('mess', __name__, url_prefix='/api')

@mod_mess.route('/view_mess_students', methods = ['GET'])
@requires_admin_auth
def view_data():
    try:
        a = request.args.get('mess_name')
        meal_id = request.args.get('type')
        date = request.args.get('date')
        meal_id = int(meal_id)

    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args,type="warning")

    mess_data = Mess.query.filter(Mess.name == a).all()
    if not mess_data:
        return jsonify(success=False,message="Invalid Mess, Enter valid mess details",type="warning")

    num = Data.query.filter(and_(Data.meal_id == meal_id,Data.mess_id == mess_data[0].id,Data.date==date)).all()
    data = []
    array=[]
    for i in range(len(num)):
        req = Student.query.filter(num[i].student_id == Student.id).all()
        if len(req) != 0:
            fun = {
                "name" : req[0].name,
                "rollno" : req[0].rollno
                }
            data.append(fun)
        if (i+1)%10==0:
            array.append(data)
            data=[]
    if len(data)!=0:
        array.append(data)
    return jsonify(success=True,users = array)

@mod_mess.route('/view_monthly_students', methods = ['GET'])
@requires_admin_auth
def view_monthly():
    try:
        a = request.args.get('mess_name')
        month_id = request.args.get('month_id')
        month_id = int(month_id)

    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args,type="warning")

    mess_data = Mess.query.filter(Mess.name == a).all()
    if not mess_data:
        return jsonify(success=False,message="Invalid Mess, Enter valid mess details",type="warning")

    num = Monthly.query.filter(and_(Monthly.month_id == month_id,Monthly.mess_id == mess_data[0].id)).all()
    data = []
    array=[]
    for i in range(len(num)):
        req = Student.query.filter(num[i].student_id == Student.id).all()
        if len(req) != 0:
            fun = {
                "name" : req[0].name,
                "rollno" : req[0].rollno
                }
            data.append(fun)
        if (i+1)%10==0:
            array.append(data)
            data=[]
    if len(data)!=0:
        array.append(data)
    return jsonify(success=True,users = array)

@mod_mess.route('/view_mess_bill', methods=['GET'])
@requires_admin_auth
def view_mess_bill():
    try:
         name = request.args.get('name')

    except KeyError as e:
         return jsonify(success=False, message="%s not sent in the request" % e.args,type="warning")


    mess = Mess.query.filter(Mess.name == name).all()
    if not mess:
        return jsonify(success=False,message="Enter valid mess name",type="warning")

    mess = mess[0]
    yesterday = date.today()-timedelta(1)
    yesterday = yesterday.strftime("%Y-%m-%d")
    data = Data.query.filter(and_(Data.mess_id==mess.id, Data.date<=yesterday, Data.date>=mess.updated_date)).all()

    updated_month = int(((mess.updated_date).split('-'))[1])

    for i in data:
        a = i.date.split('-')
        x = datetime(int(a[0]),int(a[1]),int(a[2])).weekday()
        if updated_month == int(a[1]):
            COST = Cost.query.filter(and_(Cost.meal_id==i.meal_id,Cost.mess_id==i.mess_id,Cost.day_id==x)).first()
            mess.bill = mess.bill + COST.cost
        else:
            bill = Bill(mess.id,False,updated_month,mess.bill)
            db.session.add(bill)
            db.session.commit()
            updated_month = int(a[1])
            COST = Cost.query.filter(and_(Cost.meal_id==i.meal_id,Cost.mess_id==i.mess_id,Cost.day_id==x)).first()
            mess.bill = COST.cost

    mess.updated_date = date.today().strftime("%Y-%m-%d")
    db.session.commit()

    bill = Bill.query.filter(and_(Bill.bill_id==mess.id,Bill.isStudent==False)).all()

    B = []
    for i in bill:
        obj = {
            "month" : i.month,
            "cost" : i.cost,
            }
        B.append(obj)

    return jsonify(success=True,bill=B)

@mod_mess.route('/update_mess', methods=['POST'])
@requires_admin_auth
def update_mess():
    try:
        name = request.form['name']
        day_id = request.form['day_id']
        meal_id = request.form['meal_id']
        cost = request.form['cost']
        menu = request.form['menu']

    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args,type="warning")

    # Updating mess bill before changing cost
    mess = Mess.query.filter(Mess.name == name).all()
    if not mess:
        return jsonify(success=False,message="Enter valid mess name",type="warning")
    mess = mess[0]
    yesterday = date.today()-timedelta(1)
    yesterday = yesterday.strftime("%Y-%m-%d")
    data = Data.query.filter(and_(Data.mess_id==mess.id, Data.date<=yesterday, Data.date>=mess.updated_date)).all()

    updated_month = int(((mess.updated_date).split('-'))[1])

    for i in data:
        a = i.date.split('-')
        x = datetime(int(a[0]),int(a[1]),int(a[2])).weekday()
        if updated_month == int(a[1]):
            COST = Cost.query.filter(and_(Cost.meal_id==i.meal_id,Cost.mess_id==i.mess_id,Cost.day_id==x)).first()
            mess.bill = mess.bill + COST.cost
        else:
            bill = Bill(mess.id,False,updated_month,mess.bill)
            db.session.add(bill)
            db.session.commit()
            updated_month = int(a[1])
            COST = Cost.query.filter(and_(Cost.meal_id==i.meal_id,Cost.mess_id==i.mess_id,Cost.day_id==x)).first()
            mess.bill = COST.cost

    mess.updated_date = date.today().strftime("%Y-%m-%d")
    db.session.commit()


    # Updating students bill before changing cost
    students = Student.query.all()

    for stu in students:
        yesterday = date.today()-timedelta(1)
        yesterday = yesterday.strftime("%Y-%m-%d")
        data = Data.query.filter(and_(Data.student_id==stu.id,Data.date<=yesterday,Data.date>=stu.updated_date,Data.cancelled==False)).all()

        cur_month = int(((stu.updated_date).split('-'))[1])

        for i in data:
            a = i.date.split('-')
            x = datetime(int(a[0]),int(a[1]),int(a[2])).weekday()

            if updated_month == int(a[1]):
                COST = Cost.query.filter(and_(Cost.meal_id==i.meal_id,Cost.mess_id==i.mess_id,Cost.day_id==x)).all()
                stu.bill =stu.bill+COST[0].cost
            else:
                bill = Bill(stu.id,True,updated_month,stu.bill)
                db.session.add(bill)
                db.session.commit()
                updated_month = int(a[1])
                COST = Cost.query.filter(and_(Cost.meal_id==i.meal_id,Cost.mess_id==i.mess_id,Cost.day_id==x)).all()
                stu.bill = COST.cost

        stu.updated_date = date.today().strftime("%Y-%m-%d")
        db.session.commit()

    mess = Mess.query.filter(Mess.name == name).first()

    COST = Cost.query.filter(and_(Cost.day_id == day_id, Cost.meal_id == meal_id, Cost.mess_id == mess.id)).first()

    COST.cost = cost
    COST.menu = menu

    db.session.commit()
    return jsonify(success=True,message="successfully update Cost",type="success")

@mod_mess.route('/cancel_mess', methods=['GET'])
@requires_admin_auth
def cancel_mess():
    try:
        mess_name = request.args.get('mess_name')
        date = request.args.get('date')
        meal_id = request.args.get('type')
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args,type="warning")
    mess_id = Mess.query.filter(Mess.name == mess_name).all()
    if not mess_id:
        return jsonify(success=False,message="Enter a valid mess name",type="warning")
    mess_id = mess_id[0].id
    data = Data.query.filter(and_(Data.date == date,Data.meal_id == int(meal_id),Data.mess_id==int(mess_id))).all()
    for i in data:
        i.cancelled = True
    try:
        db.session.commit()
        return jsonify(success=True,message = "successfully cancelled mess",type="success")
    except:
        return jsonify(success=False,message = "Not able to cancel mess",type="warning")
