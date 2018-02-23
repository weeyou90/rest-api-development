#/usr/bin/python

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
	DATABASE=os.path.join(app.root_path, 'flaskr.db'),
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
def index():
    """Returns a list of implemented endpoints."""
    return make_json_response(ENDPOINT_LIST)


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
@app.route("/users/register")
def users_register():
    #Register a user
    #if success
    if (1 == 1):
	return make_json_response(None), 201
    return make_json_response(None,False)

@app.route("/users/authenticate")
def users_authenticate():
    if (1 == 1):
    #validate access, return token
        return make_json_response(None)
    return make_json_response(None,False)

@app.route("/users/expire")
def users_expire():
	#expire a token
	if (1==1):
		return make_json_response(None)	
	return make_json_response(None,False)

@app.route("/users")
def users(): 
	if (1==1):
		return make_json_response(None)
	return make_json_response(None, False)
    

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
    cursor = db.execute('SELECT * FROM diary_entries')  
    print (cursor.fetchall())
   	
    return make_json_response(diary_entries)


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

    # Run the application
    app.run(debug=False, port=8080, host="0.0.0.0")
