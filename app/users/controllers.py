from flask import Blueprint, request, session, jsonify,make_response
from sqlalchemy.exc import IntegrityError
from app import db,requires_student_auth,requires_admin_auth
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import and_, or_
from calendar import monthrange
from app.mess.models import *
from app.users.models import *
from app.data.models import *
from datetime import *

mod_users = Blueprint('users', __name__, url_prefix='/api')

@mod_users.route('/login', methods=['GET'])
def check_login():
    if 'user_id' in session:
        if session['type'] == 'admin':
            admin = Admin.query.filter(Admin.id==session['user_id']).first()
            return jsonify(success=True, type=session['type'] , user=admin.to_dict())
        else:
            # date = datetime.now()
            student = Student.query.filter(Student.id == session['user_id']).first()
            # date = date.strftime("%Y-%m-%d")
            # mess_details = Data.query.filter(and_(Data.student_id==session['user_id'],Data.date==date)).all()
            # data=[]
            # print(mess_details)
            # breakfast=""
            # lunch=""
            # dinner=""
            # for i in mess_details:
            #     if i.meal_id==1:
            #         num = Mess.query.filter(Mess.id == i.mess_id).all()
            #         print("hello")
            #         breakfast = num[0].name
            #     if i.meal_id==2:
            #         num = Mess.query.filter(Mess.id == i.mess_id).all()
            #         lunch = num[0].name
            #     if i.meal_id==3:
            #         num = Mess.query.filter(Mess.id == i.mess_id).all()
            #         dinner = num[0].name
            #     details={'breakfast':breakfast,'lunch':lunch,'dinner':dinner}
            # return jsonify(success=True, type=session['type'] , user=student.to_dict(),details=details)
            return jsonify(success=True, type=session['type'] , user=student.to_dict())

    return jsonify(success=False,message="Not logged in",type="info")


@mod_users.route('/login', methods=['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args,type="warning")

    admin = Admin.query.filter(Admin.email == email).first()
    if admin is not None and admin.check_password(password):
        session['user_id'] = admin.id
        session['type'] = 'admin'

        return jsonify(success=True, type='admin' , user = admin.to_dict())

    student = Student.query.filter(Student.email == email).first()
    if student is not None and student.check_password(password):
        session['user_id'] = student.id
        if student.admin == True:
            session['type'] = 'student_admin'
            return jsonify(success=True, type='student_admin' , user = student.to_dict())

        else:
            session['type'] = 'student'
            return jsonify(success=True, type='student' , user = student.to_dict())

    return jsonify(success=False, message="Invalid Credentials",type="warning")

@mod_users.route('/logout', methods=['POST'])
def logout():
    if "user_id" in session:
        session.pop('user_id')
        session.pop('type')
    return jsonify(success=True)

@mod_users.route('/register', methods=['POST'])
def create_student():
    try:
        name = request.form['name']
        rollno = request.form['rollno']
        email = request.form['email']
        password = request.form['password']
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args,type="warning")

    if(name==''):
        return jsonify(success=False, message="Please enter your name",type="warning")
    if(rollno==''):
        return jsonify(success=False, message="Please enter your rollno",type="warning")
    if(password==''):
        return jsonify(success=False, message="Please enter password",type="warning")

    if '@' not in email:
        return jsonify(success=False, message="Please enter a valid email",type="warning")

    u = Student(name, rollno, email, password)
    db.session.add(u)
    try:
        db.session.commit()
    except IntegrityError as e:
        return jsonify(success=False, message="This email or rollno is already registered",type="warning")
    return jsonify(success=True, message="Successfully registered",type="success")

@mod_users.route('/active_students', methods=['GET'])
@requires_admin_auth
def active_students():
    a = Student.query.filter(Student.active == True).all()
    users = []
    for num in a:
        fun = num.to_dict()
        users.append(fun)
    return jsonify(success=True,users = users)

@mod_users.route('/inactive_students', methods=['GET'])
@requires_admin_auth
def inactive_students():
    a = Student.query.filter(Student.active == False).all()
    users = []
    for num in a:
        fun = num.to_dict()
        users.append(fun)
    return jsonify(success=True,users = users)

@mod_users.route('/view_student', methods=['GET'])
@requires_admin_auth
def view_student():
    try:
        rollno = request.args.get('rollno')
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args,type="warning")

    stu = Student.query.filter(Student.rollno == rollno).all()
    if len(stu)==0:
        return jsonify(success=False,message="student with %s does not exist" %(rollno),type="warning")
    else:
        stu=stu[0]
        student = stu.to_dict()
        return jsonify(student = student)

@mod_users.route('/view_registration', methods=['GET'])
@requires_admin_auth
def view_registration():
    try:
        rollno = request.args.get('rollno')
        year = request.args.get('year')
        month = request.args.get('month')
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args,type="warning")


    rollno = int(rollno)
    year = int(year)
    month = int(month)

    stu = Student.query.filter(Student.rollno == rollno).all()
    if len(stu) == 0:
        return jsonify(success=False, message="Student Doesnt exists",type="warning")
    stu = stu[0]

    if month < 10:
        data = Data.query.filter(and_(Data.date.like(str(year)+"-0"+str(month)+"%")),Data.student_id == stu.id).all()
    else:
        data = Data.query.filter(and_(Data.date.like(str(year)+"-"+str(month)+"%")),Data.student_id == stu.id).all()

    if len(data)>0:
        start_date = (data[0].date).split('-')
        finish_date = (data[len(data)-1].date).split('-')
        start_day = datetime(int(start_date[0]),int(start_date[1]),int(start_date[2])).weekday()
        finish_day = datetime(int(finish_date[0]),int(finish_date[1]),int(finish_date[2])).weekday()
        first_day = datetime(year,month,1).weekday()
        no_ofdays = monthrange(year,month)[1]

    else:
        start_date = -1
        finish_date = -1
        first_day = datetime(year,month,1).weekday()
        no_ofdays = monthrange(year,month)[1]


    view = []
    week = []
    for i in range(first_day):
        week.append({})

    if start_date == -1:
        for i in range(no_ofdays):
            week.append({"month_day":i+1})
            if len(week) == 7:
                view.append(week)
                week = []

    else:
        for i in range(int(start_date[2])-1):
            week.append({"month_day":i+1})
            if len(week) == 7:
                view.append(week)
                week = []
        mess = Mess.query.all()
        mess_obj = []
        for m in mess:
            mess_obj.append(m.name)

        for i in range(int(finish_date[2])-int(start_date[2])+1):
            obj = {
            "month_day":int(start_date[2])+i,
            "break_fast":mess_obj[data[i*3+0].mess_id-1],
            "break_fast_cancelled" : data[i*3+0].cancelled,
            "lunch":mess_obj[data[i*3+1].mess_id-1],
            "lunch_cancelled" : data[i*3+1].cancelled,
            "dinner":mess_obj[data[i*3+2].mess_id-1],
            "dinner_cancelled" : data[i*3+2].cancelled,
            }
            week.append(obj)
            if(len(week)) == 7:
                view.append(week)
                week = []

        for i in range(no_ofdays  - int(finish_date[2])):
            week.append({"month_day":int(finish_date[2])+i+1})
            if len(week) == 7:
                view.append(week)
                week = []
    if len(week) != 0:
        for i in range(8):
            week.append({})
            if(len(week) == 7):
                view.append(week)
                week = []

    return jsonify(success=True,registration = view)

@mod_users.route('/student_view_registration', methods=['GET'])
@requires_student_auth
def student_view_registration():
    try:
        student_id = session['user_id']
        year = request.args.get('year')
        month = request.args.get('month')
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args,type="warning")


    student_id = int(student_id)
    year = int(year)
    month = int(month)

    stu = Student.query.filter(Student.id == student_id).all()
    if len(stu) == 0:
        return jsonify(success=False, message="Student Doesnt exists",type="warning")
    stu = stu[0]

    if month < 10:
        data = Data.query.filter(and_(Data.date.like(str(year)+"-0"+str(month)+"%")),Data.student_id == stu.id).all()
    else:
        data = Data.query.filter(and_(Data.date.like(str(year)+"-"+str(month)+"%")),Data.student_id == stu.id).all()

    if len(data)>0:
        start_date = (data[0].date).split('-')
        finish_date = (data[len(data)-1].date).split('-')
        start_day = datetime(int(start_date[0]),int(start_date[1]),int(start_date[2])).weekday()
        finish_day = datetime(int(finish_date[0]),int(finish_date[1]),int(finish_date[2])).weekday()
        first_day = datetime(year,month,1).weekday()
        no_ofdays = monthrange(year,month)[1]

    else:
        start_date = -1
        finish_date = -1
        first_day = datetime(year,month,1).weekday()
        no_ofdays = monthrange(year,month)[1]


    view = []
    week = []
    for i in range(first_day):
        week.append({})

    if start_date == -1:
        for i in range(no_ofdays):
            week.append({"month_day":i+1})
            if len(week) == 7:
                view.append(week)
                week = []

    else:
        for i in range(int(start_date[2])-1):
            week.append({"month_day":i+1})
            if len(week) == 7:
                view.append(week)
                week = []

        mess = Mess.query.all()
        mess_obj = []
        for m in mess:
            mess_obj.append(m.name)

        for i in range(int(finish_date[2])-int(start_date[2])+1):
            obj = {
            "month_day":int(start_date[2])+i,
            "break_fast":mess_obj[data[i*3+0].mess_id-1],
            "break_fast_cancelled" : data[i*3+0].cancelled,
            "lunch":mess_obj[data[i*3+1].mess_id-1],
            "lunch_cancelled" : data[i*3+1].cancelled,
            "dinner":mess_obj[data[i*3+2].mess_id-1],
            "dinner_cancelled" : data[i*3+2].cancelled,
            }
            week.append(obj)
            if(len(week)) == 7:
                view.append(week)
                week = []

        for i in range(no_ofdays  - int(finish_date[2])):
            week.append({"month_day":int(finish_date[2])+i+1})
            if len(week) == 7:
                view.append(week)
                week = []
    if len(week) != 0:
        for i in range(8):
            week.append({})
            if(len(week) == 7):
                view.append(week)
                week = []

    return jsonify(registration = view)

@mod_users.route('/edit_student_details', methods=['POST'])
def edit_student():
    try:
        rollno = request.form['rollno']
        new_name = request.form['name']
        new_email = request.form['email']

    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args,type="warning")


    stu = Student.query.filter(Student.rollno == rollno).all()
    if len(stu)==0:
        return jsonify(success=False,message="student with %s does not exist" %(rollno),type="warning")
    stu = stu[0]
    try:
        stu.name = new_name
        stu.email = new_email
        db.session.commit()
        return jsonify(success = True,message = "successfully edited",type="success")
    except Exception as e:
        return jsonify(success =False,message = "Details not updated",type="warning")

@mod_users.route('/reset_password', methods=['POST'])
@requires_admin_auth
def reset_password():
    try:
        rollno = request.form['rollno']
        new_pass = request.form['password']
    except KeyError as e:
         return jsonify(success=False, message="%s not sent in the request" % e.args,type="warning")
    num = Student.query.filter(Student.rollno == rollno).all()
    if len(num)==0:
        return jsonify(success=False,message ="Student with this roll number is not registered",type="warning")
    num[0].password = generate_password_hash(new_pass)
    try:
        db.session.commit()
        return jsonify(success=True,message ="Password has been successfully updated",type="success")
    except:
        jsonify(success=False,message = "Failed to reset the password",type="warning")

@mod_users.route('/add-student-admin', methods=['POST'])
@requires_admin_auth
def addStudentAdmin():
    try:
        rollno = request.form['rollno']
    except KeyError as e:
         return jsonify(success=False, message="%s not sent in the request" % e.args,type="warning")

    stu = Student.query.filter(Student.rollno == rollno).all()
    if len(stu)==0:
        return jsonify(success=False,message ="Student with this roll number is not registered",type="warning")
    stu[0].admin = True

    try:
        db.session.commit()
        return jsonify(success=True,message = "Successfully added student admin",type="success")
    except:
        jsonify(success=False,message = "Failed to add Student Admin",type="warning")

@mod_users.route('/view_bill_student', methods=['GET'])
@requires_admin_auth
def view_bill_student():
    try:
         rollno = request.args.get('rollno')

    except KeyError as e:
         return jsonify(success=False, message="%s not sent in the request" % e.args,type="warning")

    stu = Student.query.filter(Student.rollno==rollno).all()
    if not stu:
        return jsonify(success=False,message="Student is not registered",type="warning")

    stu = stu[0]

    yesterday = date.today()-timedelta(1)
    yesterday = yesterday.strftime("%Y-%m-%d")
    data = Data.query.filter(and_(Data.student_id==stu.id,Data.date<=yesterday,Data.date>=stu.updated_date,Data.cancelled==False)).all()

    cur_month = int(((stu.updated_date).split('-'))[1])

    for i in data:
        a = i.date.split('-')
        x = datetime(int(a[0]),int(a[1]),int(a[2])).weekday()
        if cur_month == int(a[1]):
            COST = Cost.query.filter(and_(Cost.meal_id==i.meal_id,Cost.mess_id==i.mess_id,Cost.day_id==x)).all()
            stu.bill =stu.bill+COST[0].cost
        else:
            bill = Bill(stu.id,True,cur_month,stu.bill)
            db.session.add(bill)
            db.session.commit()
            cur_month = int(a[1])
            COST = Cost.query.filter(and_(Cost.meal_id==i.meal_id,Cost.mess_id==i.mess_id,Cost.day_id==x)).first()
            stu.bill = COST.cost

    stu.updated_date = date.today().strftime("%Y-%m-%d")
    db.session.commit()

    bill = Bill.query.filter(and_(Bill.bill_id==stu.id,Bill.isStudent==True)).all()
    B = []
    for i in bill:
        obj = {
            "month" : i.month,
            "cost" : i.cost,
            }
        B.append(obj)

    return jsonify(success=True,bill=B)

@mod_users.route('/student_view_bill_student', methods=['GET'])
@requires_student_auth
def student_view_bill_student():
    try:
        student_id = session['user_id']

    except KeyError as e:
         return jsonify(success=False, message="%s not sent in the request" % e.args,type="warning")

    stu = Student.query.filter(Student.id==student_id).all()
    if not stu:
        return jsonify(success=False,message="Student is not registered",type="warning")

    stu = stu[0]

    yesterday = date.today()-timedelta(1)
    yesterday = yesterday.strftime("%Y-%m-%d")
    data = Data.query.filter(and_(Data.student_id==stu.id,Data.date<=yesterday,Data.date>=stu.updated_date,Data.cancelled==False)).all()

    cur_month = int(((stu.updated_date).split('-'))[1])

    for i in data:
        a = i.date.split('-')
        x = datetime(int(a[0]),int(a[1]),int(a[2])).weekday()
        if cur_month == int(a[1]):
            COST = Cost.query.filter(and_(Cost.meal_id==i.meal_id,Cost.mess_id==i.mess_id,Cost.day_id==x)).all()
            stu.bill =stu.bill+COST[0].cost
        else:
            bill = Bill(stu.id,True,cur_month,stu.bill)
            db.session.add(bill)
            db.session.commit()
            cur_month = int(a[1])
            COST = Cost.query.filter(and_(Cost.meal_id==i.meal_id,Cost.mess_id==i.mess_id,Cost.day_id==x)).first()
            stu.bill = COST.cost

    stu.updated_date = date.today().strftime("%Y-%m-%d")
    db.session.commit()

    bill = Bill.query.filter(and_(Bill.bill_id==stu.id,Bill.isStudent==True)).all()
    B = []
    for i in bill:
        obj = {
            "month" : i.month,
            "cost" : i.cost,
            }
        B.append(obj)

    return jsonify(success=True,bill=B)


@mod_users.route('/post_complaint', methods=['POST'])
def post_complaint():
    try:
        message = request.form['message']

    except KeyError as e:
         return jsonify(success=False, message="%s not sent in the request" % e.args,type="warning")

    student_id = session['user_id']

    complaint = Complaint(student_id,message)

    try:
        db.session.add(complaint)
        db.session.commit()
        return jsonify(success=True,message="Successfully posted Complaint",type="warning")

    except:
         return jsonify(success=False, message="Could not post the complaint",type="warning")

@mod_users.route('/complaints', methods=['GET'])
@requires_admin_auth
def complaints():
    unresolved = []
    complaint = Complaint.query.filter(Complaint.status=="unresolved").all()
    for comp in complaint:
        rollno = (Student.query.filter(Student.id==comp.student_id).first()).rollno
        obj = {
            "id" : comp.id,
            "rollno" : rollno,
            "date" : comp.date,
            "message" : comp.message,
            "status" : comp.status,
        }
        unresolved.append(obj)

    resolved = []
    complaint = Complaint.query.filter(Complaint.status=="resolved").all()
    for comp in complaint:
        rollno = (Student.query.filter(Student.id==comp.student_id).first()).rollno
        obj = {
            "id" : comp.id,
            "rollno" : rollno,
            "date" : comp.date,
            "message" : comp.message,
            "status" : comp.status,
        }
        resolved.append(obj)

    return jsonify(success=True, unresolved=unresolved, resolved=resolved)

@mod_users.route('/complaint-resolved', methods=['POST'])
@requires_admin_auth
def complaintResolved():
    try:
        complaint_id = request.form['complaint_id']

    except KeyError as e:
         return jsonify(success=False, message="%s not sent in the request" % e.args,type="warning")

    complaint = Complaint.query.filter(Complaint.id == complaint_id).first()
    complaint.status = "resolved";

    db.session.commit()
    return jsonify(success=True, message="Successfully Resolved",type="success")

@mod_users.route('/view-complaints', methods=['GET'])
@requires_student_auth
def viewComplaints():
    student_id = session['user_id']

    complaints = Complaint.query.filter(and_(Complaint.student_id==student_id,Complaint.status=="unresolved")).all()
    unresolved = []
    for comp in complaints:
        obj = {
            "id" : comp.id,
            "date" : comp.date,
            "message" : comp.message,
            "status" : comp.status,
        }
        unresolved.append(obj)

    complaints = Complaint.query.filter(and_(Complaint.student_id==student_id,Complaint.status=="resolved")).all()
    resolved = []
    for comp in complaints:
        obj = {
            "id" : comp.id,
            "date" : comp.date,
            "message" : comp.message,
            "status" : comp.status,
        }
        resolved.append(obj)
    return jsonify(success=True, unresolved=unresolved, resolved=resolved)

@mod_users.route('/student_defaultmess', methods=['GET'])
@requires_student_auth
def student_default():
    try:
        student_id = session['user_id']
    except KeyError as e:
         return jsonify(success=False, message="%s not sent in the request" % e.args,type="warning")
    student_data = Student.query.filter(Student.id==student_id).all()
    if not student_data:
        return jsonify(success=False,message = "Unable to fetch the default mess",type="warning")
    return jsonify(default_mess=student_data[0].default_mess)
