#/usr/bin/python

from werkzeug import generate_password_hash, check_password_hash
from flask import Flask,request,session,abort,jsonify,redirect,render_template, escape, make_response, url_for, flash,g
from uuid import uuid4
from forms import SignupForm, LoginForm, NewEntryForm
from flask_cors import CORS
import sys
import json
import os
import sqlite3
from datetime import datetime


app = Flask(__name__
            # static_url_path='',
            # static_folder='/service/static',
            # template_folder='/service/templates'
            )
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=('/service/flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# Enable cross origin sharing for all endpoints
CORS(app)

# Remember to update this list
ENDPOINT_LIST = ['/', '/meta/heartbeat', '/meta/members', '/users/register', '/users/authenticate', '/users/expire', '/users/', '/meta/short_answer_questions', '/diary', '/diary/create', '/diary/delete', '/diary/permissions','/diary/new_entry'] 


app.config['SECRET_KEY'] = os.urandom(24)

#================================================================
#        D B    H E L P E R  F U N C TI O N S
#================================================================
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = dict_factory
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
        if data is not None:
            to_serialize['error'] = data
    response = app.response_class(
        response=json.dumps(to_serialize),
        status=code,
        mimetype='application/json'
    )
    return response

def is_logged_in(token):
    if token == 0:
        return False;    

    db = get_db()
    cursor = db.execute('SELECT * from users where token = ?',[token])
    a = cursor.fetchall()

    print (len(a))
    if len(a) == 1:
        return True
    if len(a) == 0:
        return False

    cursor = db.execute('UPDATE users SET token = ? WHERE token = ?', [0, token])
    db.commit()
    db.close()
    
    return False

# =======================================================
#                        M E T A
# =======================================================
@app.route("/")
def index():
   """Return list of endpoints"""
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

@app.route("/clear")
def clear():
    #test function to clear database of all users
    db=get_db()
    cursor = db.execute('DELETE from users')
    cursor = db.execute('DELETE from diary_entries')
    db.commit()
    db.close()

    return make_json_response(cursor.rowcount) 


# ====================================================
#                 U S E R
# ====================================================
@app.route("/users/register", methods=['POST'])
def users_register():
#username, password, fullname, age
    try:
    #check for correct inputs
        data = request.get_json()
        username = data['username']
        password = data['password']
        fullname = data['fullname']
        age = data['age']
    except:
        #print request.data
        return make_json_response("Invalid inputs",False)
    
    db=get_db()

    #check if username exists
    cursor = db.execute('SELECT * FROM users where name = (?)' , [username])
    a = cursor.fetchone()
    if a is not None:
        return make_json_response("User already exists!", False)
    #hash and salt pw
    hashedpw = generate_password_hash(password)
    cursor = db.execute('insert into users (id, name,password,fullname,age, token) values (null, ?,?,?,?, ?)', [username, hashedpw, fullname, age, '0'])
    db.commit()
    db.close()
   
    if ( cursor.rowcount == 1): #if insert successful
        return make_json_response(None, True,201)
    return make_json_response("Unknown Error, Registration Failed", False)

@app.route("/users/authenticate", methods=['POST'])
def users_authenticate():
#username, password
    try:
    #check for correct inputs
        data = request.get_json()
        username = data['username']
        password = data['password']
    except:
        #print request.data
        return make_json_response("Invalid inputs",False)

    db=get_db()
    cursor = db.execute('SELECT * FROM users where name = ?', [username])  
    user = cursor.fetchone()

    #check if user is not none and hashed+salted input = stored password
    if user is not None and check_password_hash(user['password'], password) is True:
        #Issues a token

        #TOKEN FOR TEST
        #token = "6bf00d02-dffc-4849-a635-a21b08500d61"
        token = str(uuid4())
        cursor = db.execute('UPDATE users SET token = ? WHERE name = ?', [token, username])
        db.commit()
        db.close()
        #if token issued successfully
        if ( cursor.rowcount == 1):
            a = {}
            a['token'] = token
            return make_json_response(a,200)
    #login failed
    return make_json_response(None,False)

@app.route("/users/expire", methods=['POST'])
def users_expire():
#token
    try:
    #check for correct inputs
        data = request.get_json()
        token = data['token']
    except:
        #print request.data
        return make_json_response("Invalid inputs",False)
 
    #expire a token
    db=get_db()
    cursor = db.execute('UPDATE users SET token = ? WHERE token = ?', [0, token])
    
    a = cursor.rowcount
    db.commit()
    db.close()
    if ( a==1 ): #if logged out
        return make_json_response(None, True)
    if (a==0): #cannot find token
        return make_json_response(None, False)
    return ("Something went wrong", False)

@app.route("/users", methods=['POST'])
def users():
    try:
    #check for correct inputs
        data = request.get_json()
        token = data['token']
    except:
        #print request.data
        return make_json_response("Invalid inputs",False)

    #check is logged in 
    if is_logged_in(token):
        db=get_db()
        #get user profile based on token if logged in
        cursor = db.execute('SELECT name, fullname, age FROM users where token = (?)', token)  
        user_information = cursor.fetchone()    
        return make_json_response(user_information, True)
    else:
        return make_json_response("Invalid authentication token.",False)
        
# @app.errorhandler(404)
# def not_found(error):
#   return make_json_response(jsonify({'eorror':'Not Found'}), 404)

# =====================================================
#                    D I A R Y
# =====================================================

@app.route("/diary", methods = ['GET','POST'])
def diary(): 

    #code to view diary
    db=get_db() 
    
    if request.method == 'GET':
        cursor = db.execute('SELECT * FROM diary_entries where public = 1')  
        a = cursor.fetchall()
        return make_json_response(a)

    if request.method == 'POST':
        try:
        #check for correct inputs
            data = request.get_json()
            token = data['token']
        except:
            #print request.data
            return make_json_response("Invalid inputs",False)
    
        if is_logged_in(token):
            #get username based on token
            cursor = db.execute('SELECT * FROM users where token = (?)', [token])  
            a = cursor.fetchone()
            #get diaries based on username
            cursor = db.execute('SELECT * FROM diary_entries where author = ?', [a['name']])
            a = cursor.fetchall()
            return make_json_response(a, True)
        else:
            return make_json_response("Invalid authentication token.",False)
 
       
    return make_json_response("Something went wrong", False)


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
    if not (is_logged_in(token)):
        return make_json_response("Invalid authentication token",False)
    
    db=get_db()
    cursor = db.execute('SELECT id FROM diary_entries where id = (select max(id) from diary_entries)')  
    a = cursor.fetchone()
    #set id as maxid+1
    diary_id = 1 if not a else 1 + int(a['id'])

    #insert diary entry
    cursor = db.execute('select * from users where token = (?)', [token])  
    a = cursor.fetchone()
    db.execute('insert into diary_entries (id,title,author,publish_date,public,text) values (?,?,?,?,?,?)', [diary_id, title, a["name"], datetime.now() , public, text])
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

    if not (is_logged_in(token)):
        return make_json_response("Invalid authentication token",False)
    
    #code to delete diary
    db=get_db()

    cursor = db.execute('select * from users where token = (?)', [token])  
    a = cursor.fetchone() 
    cursor = db.execute('delete from diary_entries where id = ? and author = ?',[diary_id, a['name']])
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

    if not (is_logged_in(token)):
        return make_json_response("Invalid authentication token",False)

    #code to update diary owned by user
    db=get_db()
   
    cursor = db.execute('select * from users where token = (?)', [token])  
    a = cursor.fetchone() 
  
    cursor = db.execute('update diary_entries set public = ? where id = ? and author = ?',[public, diary_id, a['name']])
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
app.run(debug=True, threaded=True, port=8080, host="0.0.0.0")
