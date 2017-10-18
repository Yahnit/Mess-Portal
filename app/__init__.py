# Import flask and template operators
from flask import Flask, render_template, session, jsonify

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

from functools import wraps

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 200

def requires_student_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'type' not in session:
            return jsonify(type="error",message="Unauthorized!, Requires Student Login", success=False)
        if session['type'] != 'student' and session['type'] != 'student_admin':
            return jsonify(type="error",message="Unauthorized!, Requires Student Login", success=False)
        return f(*args, **kwargs)
    return decorated

def requires_admin_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'type' not in session:
            return jsonify(type="error",message="Unauthorized!, Requires Admin Login", success=False)
        if session['type'] != 'admin' and session['type'] != 'student_admin':
            return jsonify(type="error",message="Unauthorized!, Requires Admin Login", success=False)
        return f(*args, **kwargs)
    return decorated

# Import a module / component using its blueprint handler variable (mod_auth)
from app.users.controllers import mod_users
from app.data.controllers import mod_data
from app.mess.controllers import mod_mess

# Register blueprint(s)
app.register_blueprint(mod_users)
app.register_blueprint(mod_data)
app.register_blueprint(mod_mess)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
