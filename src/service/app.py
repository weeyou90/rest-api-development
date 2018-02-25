#/usr/bin/python

from werkzeug import generate_password_hash, check_password_hash
from flask import Flask,request,session,abort,jsonify,redirect,render_template, escape, make_response, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import os
from model import db
from forms import SignupForm, LoginForm
from datetime import datetime
import sys

app = Flask(__name__)
app.config.from_object(__name__)

# Enable cross origin sharing for all endpoints
CORS(app)

# Remember to update this list
ENDPOINT_LIST = ['/', '/meta/heartbeat', '/meta/members', '/users/register', '/users/authenticate', '/users/expire', '/users/', '/meta/short_answer_questions', '/diary', '/diary/create', '/diary/delete', '/diary/permissions'] 

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///paste.db"
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    password = db.Column(db.String(120))
    fullname = db.Column(db.String(120))
    age = db.Column(db.Integer)
    email = db.Column(db.String(240))

    def __init__(self, name, email, password, fullname, age):
        self.name = name
        self.email = email
        self.fullname = fullname
        self.age = age
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.name

class DiaryEntry(db.Model):
    __tablename__ = 'diary'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    author = db.Column(db.String(120))
    publish_date = db.Column(db.DateTime)
    public = db.Column(db.Boolean)
    text = db.Column(db.Text)

    def __init__(self, id, title, author, publish_date, public, text):
        id = id
        self.title = email
        self.author = fullname
        self.publish_date = age
        self.public = public
	self.text = text

'''
#================================================================
#        D B    H E L P E R  F U N C TI O N S
#================================================================
def connect_db():
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv

def get_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

def init_db():
	db = get_db()
	with app.open_resource('schema.sql', mode='r') as f:
		db.cursor().executescript(f.read())
	db.commit()

@app.cli.command('initdb')
def initdb_command():
	init_db()
	print('Initialised the database')

@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
'''

# =======================================================
#                     C O M M O N
# =======================================================
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

def is_logged_in(token):
# TBD: check if token is issued
	return True

# =======================================================
#                        M E T A
# =======================================================
@app.route("/")
@app.before_request
def check_user_status():
    if 'user_email' not in session:
        session['user_email'] = None
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

# ====================================================
#                 U S E R
# ====================================================
@app.route("/users/register", methods=('GET','POST'))    
# @verify_required_params(['email', 'password', 'name'])
# @validate_email_format
def users_register():
    if session['user_email']:
        flash('you are already signed up')
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        user_email = User.query.filter_by(email=form.email.data).first()
        if user_email is None:
            try:
                user = User(form.name.data, form.email.data, form.password.data, form.fullname.data, form.age.data)
                db.session.add(user)
                db.session.commit()
            except:
                print('Insert error')
            session['user_email'] = form.email.data
            session['user_name'] = form.name.data
            flash('Thanks for registering. You are now logged in!')
            return redirect(url_for('index'))
        else:
            flash("A User with that email already exists. Choose another one!", 'error')
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
    if session['user_email']:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            session['user_email'] = form.email.data
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

# =====================================================
#                    D I A R Y
# =====================================================

@app.route("/diary", methods = ['GET'])
def diary(): 
    diary_entries = [{
      "id": 1,
      "title": "My First Project",
      "author": "ashrugged",
      "publish_date": "2013-02-27T13:37:00+00:00",
      "public": 'true',
      "text": "If you don't know, the thing to do is not to get scared, but to learn."
    },
    {
      "id": 2,
      "title": "A New Lesson!",
      "author": "audrey123talks",
      "publish_date": "2013-02-29T13:37:00+00:00",
      "public": 'true',
      "text": "Check out my latest video!"
    }]

    #code to view diary
    db=get_db()	
    db.row_factory = dict_factory

    cursor = db.execute('SELECT * FROM diary_entries')  
    a = cursor.fetchall()
   	
    return make_json_response(a)


@app.route("/diary/create", methods=['POST'])
def diary_create():
#token, title, public, text
	try:
	#check for correct inputs
		data = request.get_json()
		token = data['token']
		title = data['title']
		public = data['public']
		text = data['text']
	except:
		#print request.data
		return make_json_response("Invalid inputs",False)

	#authenticate
	if not (is_logged_in(data['token'])):
		return make_json_response("Invalid authentication token",False)
	
	#====code to insert diary====
	db=get_db()
	
	#get max id (TBD: get max id of entry by logged in user)	
    	cursor = db.execute('SELECT id FROM diary_entries where id = (select max(id) from diary_entries)')  
	a = cursor.fetchone()
	#set id as maxid+1
	diary_id = 1 if not a else 1 + int(a[0])

	#insert diary entry
	db.execute('insert into diary_entries (id,title,author,publish_date,public,text) values (?,?,?,?,?,?)', [diary_id, title, datetime.now() ,"author", public, text])
	db.commit()

	return make_json_response(diary_id,True,201)


@app.route("/diary/delete", methods=['POST'])
def diary_delete():
	#token, id
	try:
	#check for correct inputs
		data = request.get_json()
		token = data['token']
		diary_id = data['id']
	except:
		print request.data
		return make_json_response("Invalid inputs",False)

	if not (is_logged_in(data['token'])):
		return make_json_response("Invalid authentication token",False)

	#code to delete diary (TBD: delete entry owned by user)
	db=get_db()
	cursor = db.execute('delete from diary_entries where id = ?',[diary_id])
	db.commit()
	
	if ( cursor.rowcount == 1): #if delete successful
		return make_json_response(None, True)
	return make_json_response("Cannot find diary entry", False)

@app.route("/diary/permissions", methods=['POST'])
def diary_permissions():
	#token, id, public
	try:
		data = request.get_json()
		token = data['token']
		diary_id = data['id']
		public = data['public']
	except:
		#print request.data
		return make_json_response("Invalid inputs",False)

	if not (is_logged_in(data['token'])):
		return make_json_response("Invalid authentication token",False)

	#code to update diary owned by user
	db=get_db()
	cursor = db.execute('update diary_entries set public = ? where id = ?',[public, diary_id])
	db.commit()
	
	if ( cursor.rowcount == 1): #if update successful
		return make_json_response(None, True)
	return make_json_response("Cannot find diary entry", False)

# working
if __name__ == '__main__':
    # Change the working directory to the script directory
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    db.create_all()
    # Run the application
    ## set debug as True for auto reload
    app.run(debug=True, port=8080, host="0.0.0.0")
