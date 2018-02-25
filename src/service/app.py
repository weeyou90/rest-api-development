#!/usr/bin/python

from flask_cors import CORS
# from app import app, db 
from werkzeug import generate_password_hash, check_password_hash
from flask import Flask,request,session,abort,jsonify,redirect,render_template, escape, make_response, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import json
import os
from uuid import uuid4
# from model import db
from forms import SignupForm, LoginForm
# from model import *

app = Flask(__name__)
# Enable cross origin sharing for all endpoints
CORS(app)

# Remember to update this list
ENDPOINT_LIST = ['/', '/meta/heartbeat', '/meta/members', '/users/register', '/users/authenticate', '/users/expire', '/users/', '/meta/short_answer_questions'] 

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///paste.db"
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    password = db.Column(db.String(120))
    ## remove email page
    # email = db.Column(db.String(240))
    fullname = db.Column(db.String(120))
    age = db.Column(db.Integer) 
    token = db.Column(db.VARCHAR(100), unique=True)

    def __init__(self, name, password, fullname, age):
        self.name = name
        self.set_password(password)
        # self.email = email
        self.fullname = fullname
        self.age = age
        self.token = str(uuid4())

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.name

def make_json_response(data, status=True, code=200):
    """Utility function to create the JSON responses."""
    
    to_serialize = {}
    if status:
        to_serialize['status'] = True
        if data is not None:
            to_serialize['result'] = data
    else:
        to_serialize['status'] = False
        to_serialize['error'] = data
    response = app.response_class(
        response=json.dumps(to_serialize),
        status=code,
        mimetype='application/json'
    )
    return response

@app.before_request
def check_user_status():
    ## need to change to token
    if 'user_name' not in session:
        # session['user_email'] = None
        session['user_name'] = None

@app.route('/', methods=('GET', 'POST'))
def index():
    if session['user_name']:
        user = User.query.filter_by(name=session['user_name']).first()
        return render_template('index.html', users=user)
    ## modify it for debug 
    return render_template('index.html')
    """Returns a list of implemented endpoints."""
    # return make_json_response(ENDPOINT_LIST)


@app.route("/meta/heartbeat")
def meta_heartbeat():
    """Returns true"""
    return make_json_response(None)


@app.route("/meta/members")
def meta_members():
    """Returns a list of team members"""
    with open("./team_members.txt") as f:
        team_members = f.read().strip().split("\n")
    return make_json_response(team_members)

@app.route("/meta/short_answer_questions")
def meta_short_answer_questions():
    """Returns short answer questions"""
    with open("./short_answer_questions.txt") as f:
        short_answer_questions = f.read().strip().split("\n")
    return make_json_response(short_answer_questions)


@app.route("/users/register", methods=('GET','POST'))
    
# @verify_required_params(['email', 'password', 'name'])
# @validate_email_format
def users_register():
    # if session['user_email']:
    #     flash('you are already signed up')
    #     return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        user_name = User.query.filter_by(name=form.name.data).first()
        if user_name is None:
            try:
                user = User(name=form.name.data, password=form.password.data,fullname= form.fullname.data, age= form.age.data)
                db.session.add(user)
                db.session.commit()
            except:
                print('Insert error')
            # session['user_name'] = form.email.data
            session['user_name'] = form.name.data
            flash('Thanks for registering. You are now logged in!')
            return redirect(url_for('index'))
        else:
            flash("A User with that name already exists. Choose another one!", 'error')
            render_template('signup.html', form=form)
    return render_template('signup.html', form=form)
    # # #Register a user
    # username = request.form('username')
    # password = request.form('password')
    # fullname = request.form('fullname')
    # age = request.form('age')

    # return render_template('welcome.html', username=username)
    # if username.count(' ') > 0:
    #     return render_template('signup.html', username)

    # try:
    #     if username is None or password is None or password1 is None or email is None:
    #         return make_json_response({'data':{'succeed':False, 'message':"Missing required parameters"}}, 400)
    #     if password != password1:
    #         return make_json_response({'data':{'succeed':False, 'message':"Password don't match"}}, 400)

    #     username = username.lower()
    #     email = email.lower()

    #     if User.query.filter_by(username=username).first() is not None:
    #         return make_json_response({'data':{'succeed':False, 'message':"Username exists"}}, 400)

    #     if User.query.filter_by(email=email).first() is not None:
    #         return make_json_response({'data':{'succeed':False, 'message':"Email exists"}}, 400)

    #     user = User(username=username, email=email, password=password)
    #     db.session.add(user)
    #     db.session.commit()
    # except Exception as e:
    #     return handle_invalid_response(e)

    # return make_json_response({'data':{'succeed':True, 'message':"Successfully signup"}}, 201)

    #if success
 #    if (1 == 1):
	# return make_json_response(None), 201
 #    return make_json_response(None,False)

@app.route("/users/authenticate", methods=('GET','POST'))
def users_authenticate():
    if session['user_name']:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user is not None and user.check_password(form.password.data):
            # session['user_email'] = form.email.data
            session['user_name'] = user.name
            flash('Thanks for logging in')
            return redirect(url_for('index'))
        else:
            flash('Sorry! no user exists with this email and password')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)
    #validate access, return token
    #     return make_json_response(None)
    # return make_json_response(None,False)


@app.route("/users/expire")
def users_expire():
	#expire a token
    session.clear()
    return redirect(url_for('index'))

    ## add time out feature
    # token = User.query.filter(User.hashed == hashed)

    # if token.count():
    #     token = token.first()

    #     if token.expired_at > datetime.datetime.now():
    #         return True

	# 	return make_json_response(None)	
	# return make_json_response(None,False)

@app.route("/users")
def users():
    # if session['user_name']:
    user = User.query.filter_by(name=session['user_name']).first()
    return render_template('info.html', user=user) 
	# if (1==1):
	# 	return make_json_response(None)
	# return make_json_response(None, False)


if __name__ == '__main__':
    # Change the working directory to the script directory
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    db.create_all()
    # Run the application
    ## set debug as True for auto reload
    app.run(debug=True, port=8081, host="0.0.0.0")
