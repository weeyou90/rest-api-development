#/usr/bin/python

# from flask_cors import CORS
# from app import app, db 
from werkzeug import generate_password_hash, check_password_hash
from flask import Flask,request,session,abort,jsonify,redirect,render_template, escape, make_response, url_for, flash
# from flask_sqlalchemy import SQLAlchemy
import json
import os
from uuid import uuid4
from forms import SignupForm, LoginForm


from flask import Flask, request, session, g
from flask_cors import CORS
import sys
import json
import os
import sqlite3
from datetime import datetime


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
	DATABASE=('flaskr.db'),
	SECRET_KEY='development key',
	USERNAME='admin',
	PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# Enable cross origin sharing for all endpoints
CORS(app)

# Remember to update this list
ENDPOINT_LIST = ['/', '/meta/heartbeat', '/meta/members', '/users/register', '/users/authenticate', '/users/expire', '/users/', '/meta/short_answer_questions', '/diary', '/diary/create', '/diary/delete', '/diary/permissions'] 

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
	with app.app_context():
		db = get_db()
		with app.open_resource('schema.sql', mode='r') as f:
			try:
				db.cursor().executescript(f.read())
			except sqlite3.OperationalError, msg:
				print msg
		db.commit()

@app.cli.command('initdb')
def initdb_command():
	init_db()
	print('Initialised the database')

@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()


app.config['SECRET_KEY'] = os.urandom(24)


class User():
  

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


    def set_password(self, password):
        self.password = generate_password_hash(password)

    # def check_password(self, password):
    #     return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.name

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

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


@app.before_request
def check_user_status():
    ## need to change to token
    if 'user_name' not in session:
        # session['user_email'] = None
        session['user_name'] = None


def is_logged_in(token):
# TBD: check if token is issued
	return True

# =======================================================
#                        M E T A
# =======================================================
@app.route("/")
def index():
    if session['user_name']:
		db=get_db()
		session_user_name = session['user_name']
		cursor = db.execute('SELECT * FROM users where name = session_user_name')  
		user = cursor.fetchone()
		make_json_response(user_name)
		return render_template('index.html', users=user)

        # user = User.query.filter_by(name=session['user_name']).first()
        
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


    
# @verify_required_params(['email', 'password', 'name'])
# @validate_email_format

# ====================================================
#                 U S E R
# ====================================================
@app.route("/users/register", methods=('GET','POST'))
def users_register():
	form = SignupForm()
	if form.validate_on_submit():
		db=get_db()
		cursor = db.execute('SELECT * FROM users where name = form.name.data')
		user_name = cursor.fetchone()
		make_json_response(user_name)
		diary_id = 1 if not a else 1 + int(a[0])
		if user_name is None:
			try:
				db.execute('insert into users (id,name,password,fullname,age) values (?,?,?,?,?)', [diary_id,form.name.data, form.password.data, form.fullname.data ,form.age.data])
				db.commit()
				db.close()
			except:
				print('Insert error')
			session['user_name'] = form.name.data
			flash('Thanks for registering. You are now logged in!')
			return redirect(url_for('index'))
		else:
			flash("A User with that name already exists. Choose another one!", 'error')
			render_template('signup.html', form=form)
	return render_template('signup.html', form=form)

@app.route("/users/authenticate", methods=('GET','POST'))
def users_authenticate():
	if session['user_name']:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		db=get_db()
		user_name = form.name.data
		cursor = db.execute('SELECT * FROM users where name = user_name')  
		user = cursor.fetchone()
		make_json_response(user)
		check_correct_password = check_password_hash(user.password, form.password.data) #double check pls! 
		if user is not None and check_correct_password:
			session['user_name'] = user.name
			flash('Thanks for logging in')
			return redirect(url_for('index'))
		else:
			flash('Sorry! no user exists with this email and password')
			return render_template('login.html', form=form)
	return render_template('login.html', form=form)

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
    if session['user_name']:
    	db=get_db()
    	cursor = db.execute('SELECT * FROM users where session = user_name')  
    	users = cursor.fetchall()
    	make_json_response(users)
        # users = User.query.filter_by(name=session['user_name']).first()
        return render_template('info.html', users=users) 
    else:
        return render_template('unauthorised.html')


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
    print a 
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

	# cur.execute('insert into members')
	db.execute('insert into diary_entries (id,title,author,publish_date,public,text) values (?,?,?,?,?,?)', [diary_id, title, datetime.now() ,"author", public, text])
	

	db.commit()
	db.close()


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
    # Run the application
    ## set debug as True for auto reload
    app.run(debug=True, port=8080, host="0.0.0.0")
