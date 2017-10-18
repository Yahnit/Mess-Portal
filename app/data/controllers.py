from flask import Blueprint, request, session, jsonify,make_response
from sqlalchemy.exc import IntegrityError
from app import db,requires_student_auth,requires_admin_auth
from app.users.models import *
from app.data.models import *
from app.mess.models import *
from datetime import date, timedelta,datetime
from sqlalchemy import *
from calendar import *

mod_data = Blueprint('data', __name__, url_prefix='/api')

@mod_data.route('/activate_student', methods=['POST'])
@requires_admin_auth
def activate_student():
    try:
        student_roll = request.form['student_roll']
        default_mess = request.form['default_mess']
        register_from = request.form['register_from']
        register_till = request.form['register_till']

    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args,type="warning")

    register_from = register_from.split('-')
    register_from_year = register_from[0]
    register_from_month = register_from[1]
    register_from_day = register_from[2]

    register_till = register_till.split('-')
    register_till_year = register_till[0]
    register_till_month = register_till[1]
    register_till_day = register_till[2]

    student = Student.query.filter(Student.rollno == student_roll).all()
    if len(student) == 0:
        return jsonify(success=False, message="Failed to activate student",type="warning")
    student = student[0];

    mess = Mess.query.filter(Mess.name == default_mess).first()
    mess_id = mess.id
    if not student.active:
        student_id = student.id

        d1 = date(int(register_from_year),int(register_from_month),int(register_from_day))
        d2 = date(int(register_till_year),int(register_till_month),int(register_till_day))

        delta = d2 - d1

        for i in range(delta.days + 1):
            for j in range(1,4):
                stu = Data(student_id,d1+timedelta(days=i),j,mess_id,mess_id,0)
                db.session.add(stu)

        try:
            student.active = True
            student.updated_date = datetime.now().strftime("%Y-%m-%d")
            student.default_mess = mess.name
            db.session.commit()

        except IntegrityError as e:
            return jsonify(success=False, message="Failed to activate student",type="warning")

    return jsonify(success=True,message="Successfully activated Student")

@mod_data.route('/deactivate_student', methods=['POST'])
@requires_admin_auth
def deactive_students():
    print("in deactive")
    try:
        rollno = request.form['rollno']
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args,type="warning")


    stu = Student.query.filter(Student.rollno == rollno).all()
    if len(stu)==0:
        return jsonify(success=False, message="student with %s does not exist" %(rollno),type="warning")
    stu = stu[0]

    data = Data.query.filter(Data.student_id == stu.id)
    for i in data:
        db.session.delete(i)

    try:
        stu.active = False
        db.session.commit()
        return jsonify(success=True,message="Successfully deactived the student",type="success")

    except IntegrityError as e:
        return jsonify(success=False, message="Failed to activate student",type="warning")

@mod_data.route('/cancel_meals', methods=['GET'])
@requires_student_auth
def cancel_meals():
    try:
        student_id = session['user_id']
        start_day = request.args.get('start_day')
        end_day = request.args.get('end_day')
        meal_id = request.args.get('meal_id')

    except KeyError as e:
         return jsonify(success=False, message="%s not sent in the request" % e.args,type="warning")
    start_temp = start_day
    start_day = start_day.split('-')
    end_temp = end_day
    end_day = end_day.split('-')
    today = datetime.now().strftime("%Y-%m-%d")
    today = today.split('-')
    startof = date(int(start_day[0]),int(start_day[1]),int(start_day[2]))
    breakfast = startof-timedelta(1)
    breakfast = breakfast.strftime("%Y-%m-%d")
    breakfast = breakfast.split('-')
    lunch = startof
    lunch = lunch.strftime("%Y-%m-%d")
    lunch = lunch.split('-')
    dinner = startof
    dinner = dinner.strftime("%Y-%m-%d")
    dinner = dinner.split('-')
    d1 = date(int(end_day[0]),int(end_day[1]),int(end_day[2]))
    d0 = date(int(start_day[0]),int(start_day[1]),int(start_day[2]))
    d2 = date(int(today[0]),int(today[1]),int(today[2]))
    if (d1-d0).days<0 or (d0-d2).days<0:
        return jsonify(success=False,message="invalid date,please selected a valid date",type="warning")
    if int(meal_id)==1 and (datetime(int(breakfast[0]),int(breakfast[1]),int(breakfast[2]),19,0,0)-datetime.now()).total_seconds()<0:
        return jsonify(success=False,message="please check the rules of cancellation",type="warning")
    if int(meal_id)==2 and (datetime(int(lunch[0]),int(lunch[1]),int(lunch[2]),7,0,0)-datetime.now()).total_seconds()<0:
        return jsonify(success=False,message="please check the rules of cancellation",type="warning")
    if int(meal_id)==3 and (datetime(int(dinner[0]),int(dinner[1]),int(dinner[2]),15,0,0)-today_now).total_seconds()<0:
        return jsonify(success=False,message="please check the rules of cancellation",type="warning")
    num = Student.query.filter(and_(Student.id==student_id,Student.active == True)).all()
    if len(num)==0:
        return jsonify(success=False,message = "Student with given rollnumber does not exist",type="warning")
    data = Data.query.filter(and_(Data.date>=start_temp,Data.date<=end_temp,Data.student_id==num[0].id,Data.meal_id==meal_id)).all()
    for i in data:
        i.cancelled = True
    try:
        db.session.commit()
        return jsonify(success=True,message = "successfully cancelled meals",type="success")
    except:
        return jsonify(success=False,message = "error,unable to cancel meals",type="success")

@mod_data.route('/uncancel_meals', methods=['GET'])
@requires_student_auth
def uncancel_meals():
    try:
        student_id = session['user_id']
        start_day = request.args.get('start_day')
        end_day = request.args.get('end_day')
        meal_id = request.args.get('meal_id')

    except KeyError as e:
         return jsonify(success=False, message="%s not sent in the request" % e.args,type="warning")
    start_temp = start_day
    start_day = start_day.split('-')
    end_temp = end_day
    end_day = end_day.split('-')
    today = datetime.now().strftime("%Y-%m-%d")
    today = today.split('-')
    startof = date(int(start_day[0]),int(start_day[1]),int(start_day[2]))
    breakfast = startof-timedelta(1)
    breakfast = breakfast.strftime("%Y-%m-%d")
    breakfast = breakfast.split('-')
    lunch = startof
    lunch = lunch.strftime("%Y-%m-%d")
    lunch = lunch.split('-')
    dinner = startof
    dinner = dinner.strftime("%Y-%m-%d")
    dinner = dinner.split('-')
    d1 = date(int(end_day[0]),int(end_day[1]),int(end_day[2]))
    d0 = date(int(start_day[0]),int(start_day[1]),int(start_day[2]))
    d2 = date(int(today[0]),int(today[1]),int(today[2]))
    if (d1-d0).days<0 or (d0-d2).days<0:
        return jsonify(success=False,message="invalid date,please selected a valid date",type="warning")
    if int(meal_id)==1 and (datetime(int(breakfast[0]),int(breakfast[1]),int(breakfast[2]),19,0,0)-datetime.now()).total_seconds()<0:
        return jsonify(success=False,message="please check the rules of uncancellation",type="warning")
    if int(meal_id)==2 and (datetime(int(lunch[0]),int(lunch[1]),int(lunch[2]),7,0,0)-datetime.now()).total_seconds()<0:
        return jsonify(success=False,message="please check the rules of uncancellation",type="warning")
    if int(meal_id)==3 and (datetime(int(dinner[0]),int(dinner[1]),int(dinner[2]),15,0,0)-today_now).total_seconds()<0:
        return jsonify(success=False,message="please check the rules of uncancellation",type="warning")
    num = Student.query.filter(and_(Student.id==student_id,Student.active == True)).all()
    if len(num)==0:
        return jsonify(success=False,message = "Student with given rollnumber does not exist",type="warning")
    data = Data.query.filter(and_(Data.date>=start_temp,Data.date<=end_temp,Data.student_id==num[0].id,Data.meal_id==meal_id)).all()
    for i in data:
        i.cancelled = False
    try:
        db.session.commit()
        return jsonify(success=True,message = "successfully uncancelled meals",type="success")
    except:
        return jsonify(success=False,message = "error,not able to uncancel meals",type="warning")
@mod_data.route('/date_wise', methods=['GET'])
@requires_admin_auth
def datewise_reg():
    try:
        rollno = request.args.get('rollno')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        mess_id = request.args.get('mess_id')
        meal_id = request.args.get('meal_id')
    except KeyError as e:
         return jsonify(success=False, message="%s not sent in the request" % e.args,type="warning")
    startof = start_date.split('-')
    start_month = int(startof[1])
    student_id = Student.query.filter(Student.rollno == rollno).all()
    if len(student_id)==0:
        return jsonify(success=False,message="Invalid rollnumber",type="warning")
    student_id = student_id[0].id
    monthly_check = Monthly.query.filter(and_(Monthly.month_id==start_month,Monthly.student_id == student_id)).all()
    if len(monthly_check)!=0:
        return jsonify(success=False,message="The student's registration cannot be changed",type="warning")
    constraint = date(int(startof[0]),int(startof[1]),int(startof[2]))-timedelta(2)
    constraint = constraint.strftime("%Y-%m-%d")
    constraint = constraint.split('-')
    if (datetime(int(constraint[0]),int(constraint[1]),int(constraint[2]))-datetime.now()).total_seconds()<0:
        return jsonify(success=False, message="please check the rules of changing mess registration",type="warning")
    change_data = Data.query.filter(and_(Data.student_id == student_id,Data.meal_id == meal_id,Data.date<=end_date,Data.date>=start_date)).all()
    for i in change_data:
        i.mess_id = mess_id
        i.cancelled = False
    try:
        db.session.commit()
        return jsonify(success=True,message ="successfully changed the registration",type="success")
    except:
        return jsonify(success=False,message ="unable to change the registration",type="warning")

@mod_data.route('/month_wise', methods=['GET'])
#@requires_admin_auth
def monthwise_reg():
    try:
        rollno = request.args.get('rollno')
        month_id = request.args.get('month_id')
        year = request.args.get('year')
        mess_id = request.args.get('mess_id')
    except KeyError as e:
         return jsonify(success=False, message="%s not sent in the request" % e.args,type="warning")
    today = datetime.now().strftime("%Y-%m-%d")
    today = today.split('-')
    if int(today[1]) >= int(month_id) and int(year)<=int(today[0]):
        return jsonify(success=False, message="Invalid month",type="warning")
    constraint = date(int(year),int(month_id),1)-timedelta(2)
    constraint = constraint.strftime("%Y-%m-%d")
    constraint = constraint.split('-')
    if (datetime(int(constraint[0]),int(constraint[1]),int(constraint[2]))-datetime.now()).total_seconds()<0:
        return jsonify(success=False, message="please check the rules of changing mess registration",type="warning")
    student_id = Student.query.filter(Student.rollno == int(rollno)).all()
    if len(student_id)==0:
        return jsonify(success=False,message="Invalid rollnumber",type="warning")
    student_id = student_id[0].id
    start_day = date(int(year),int(month_id),1).strftime("%Y-%m-%d")
    end_day = date(int(year),int(month_id),monthrange(int(year),int(month_id))[1]).strftime("%Y-%m-%d")
    change_data = Data.query.filter(and_(Data.student_id == student_id,Data.date<=end_day,Data.date>=start_day)).all()
    if len(change_data)==0:
        return jsonify(success=False,message = "Invalid month",type="warning")
    if (len(change_data)/3)!=monthrange(int(year),int(month_id))[1]:
        return jsonify(success=False,message = "Student's registration cannot be changed",type="warning")
    for i in change_data:
        i.mess_id = mess_id
        i.cancelled = False
    db.session.add(Monthly(int(month_id),int(mess_id),student_id))
    try:
        db.session.commit()
        return jsonify(success=True,message ="successfully changed the registration",type="success")
    except:
        return jsonify(success=False,message ="unable to change the registration",type="warning")


@mod_data.route('/day_wise', methods=['GET'])
#@requires_admin_auth
def daywise_reg():
    try:
        rollno = request.args.get('rollno')
        day_id = request.args.get('day')
        mess_id = request.args.get('mess_id')
        meal_id = request.args.get('meal_id')
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args,type="warning")
    student_id = Student.query.filter(Student.rollno == int(rollno)).all()
    if len(student_id)==0:
        return jsonify(success=False,message="Invalid rollnumber",type="warning")
    student_id = student_id[0].id
    total_data = Data.query.filter(and_(Data.student_id == student_id,Data.meal_id == meal_id)).all()
    for i in total_data:
        act = i.date
        act = act.split('-')
        act = date(int(act[0]),int(act[1]),int(act[2])).weekday()
        if act == int(day_id):
            i.mess_id = int(mess_id)
            i.cancelled = False
    try:
        db.session.commit()
        return jsonify(success=True,message = "successfully changed the student registration",type="success")
    except:
        return jsonify(success=False,message ="unable to change the registration",type="warning")

@mod_data.route('/student_date_wise', methods=['GET'])
@requires_student_auth
def student_datewise_reg():
    try:
        student_id = session['user_id']
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        mess_id = request.args.get('mess_id')
        meal_id = request.args.get('meal_id')
    except KeyError as e:
         return jsonify(success=False, message="%s not sent in the request" % e.args,type="warning")
    startof = start_date.split('-')
    start_month = int(startof[1])
    student_id = Student.query.filter(Student.id == student_id).all()
    if len(student_id)==0:
        return jsonify(success=False,message="Invalid rollnumber",type="warning")
    student_id = student_id[0].id
    monthly_check = Monthly.query.filter(and_(Monthly.month_id==start_month,Monthly.student_id == student_id)).all()
    if len(monthly_check)!=0:
        return jsonify(success=False,message="The student's registration cannot be changed",type="warning")
    constraint = date(int(startof[0]),int(startof[1]),int(startof[2]))-timedelta(2)
    constraint = constraint.strftime("%Y-%m-%d")
    constraint = constraint.split('-')
    if (datetime(int(constraint[0]),int(constraint[1]),int(constraint[2]))-datetime.now()).total_seconds()<0:
        return jsonify(success=False, message="please check the rules of changing mess registration",type="warning")
    change_data = Data.query.filter(and_(Data.student_id == student_id,Data.meal_id == meal_id,Data.date<=end_date,Data.date>=start_date)).all()
    for i in change_data:
        i.mess_id = mess_id
        i.cancelled = False
    try:
        db.session.commit()
        return jsonify(success=True,message ="successfully changed the registration",type="success")
    except:
        return jsonify(success=False,message ="unable to change the registration",type="warning")

@mod_data.route('/student_month_wise', methods=['GET'])
#@requires_admin_auth
def student_monthwise_reg():
    try:
        student_id = session['user_id']
        month_id = request.args.get('month_id')
        year = request.args.get('year')
        mess_id = request.args.get('mess_id')
    except KeyError as e:
         return jsonify(success=False, message="%s not sent in the request" % e.args,type="warning")
    today = datetime.now().strftime("%Y-%m-%d")
    today = today.split('-')
    if int(today[1]) >= int(month_id) and int(year)<=int(today[0]):
        return jsonify(success=False, message="Invalid month",type="warning")
    constraint = date(int(year),int(month_id),1)-timedelta(2)
    constraint = constraint.strftime("%Y-%m-%d")
    constraint = constraint.split('-')
    if (datetime(int(constraint[0]),int(constraint[1]),int(constraint[2]))-datetime.now()).total_seconds()<0:
        return jsonify(success=False, message="please check the rules of changing mess registration",type="warning")
    student_id = Student.query.filter(Student.id == student_id).all()
    if len(student_id)==0:
        return jsonify(success=False,message="Invalid rollnumber",type="warning")
    student_id = student_id[0].id
    # print(student_id)
    start_day = date(int(year),int(month_id),1).strftime("%Y-%m-%d")
    # print(start_day)
    # print("...")
    end_day = date(int(year),int(month_id),calendar.monthrange(int(year),int(month_id))[1]).strftime("%Y-%m-%d")
    # print(end_day)
    change_data = Data.query.filter(and_(Data.student_id == student_id,Data.date<=end_day,Data.date>=start_day)).all()
    if len(change_data)==0:
        return jsonify(success=False,message = "Invalid month",type="warning")
    if (len(change_data)/3)!=calendar.monthrange(int(year),int(month_id))[1]:
        return jsonify(success=False,message = "Student's registration cannot be changed",type="warning")
    for i in change_data:
        i.mess_id = mess_id
        i.cancelled = False
    db.session.add(Monthly(int(month_id),int(mess_id),student_id))
    try:
        db.session.commit()
        return jsonify(success=True,message ="successfully changed the registration",type="success")
    except:
        return jsonify(success=False,message ="unable to change the registration",type="warning")


@mod_data.route('/student_day_wise', methods=['GET'])
#@requires_admin_auth
def student_daywise_reg():
    try:
        student_id = session['user_id']
        day_id = request.args.get('day')
        mess_id = request.args.get('mess_id')
        meal_id = request.args.get('meal_id')
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args,type="warning")
    student_id = Student.query.filter(Student.id == student_id).all()
    if len(student_id)==0:
        return jsonify(success=False,message="Invalid rollnumber",type="warning")
    student_id = student_id[0].id
    total_data = Data.query.filter(and_(Data.student_id == student_id,Data.meal_id == meal_id)).all()
    for i in total_data:
        act = i.date
        act = act.split('-')
        act = date(int(act[0]),int(act[1]),int(act[2])).weekday()
        if act == int(day_id):
            i.mess_id = int(mess_id)
            i.cancelled = False
    try:
        db.session.commit()
        return jsonify(success=True,message = "successfully changed the student registration",type="success")
    except:
        return jsonify(success=False,message ="unable to change the registration",type="warning")
