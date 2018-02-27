#/usr/bin/python

# from flask_cors import CORS
# from app import app, db 
from werkzeug import generate_password_hash, check_password_hash
from flask import Flask,request,session,abort,jsonify,redirect,render_template, escape, make_response, url_for, flash
# from flask_sqlalchemy import SQLAlchemy
import json
import os
from uuid import uuid4
import datetime
from forms import SignupForm, LoginForm, NewEntryForm


from flask import Flask, request, session, g
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
    DATABASE=('/src/service/flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# Enable cross origin sharing for all endpoints
CORS(app)

# Remember to update this list
ENDPOINT_LIST = ['/', '/meta/heartbeat', '/meta/members', '/users/register', '/users/authenticate', '/users/expire', '/users/', '/meta/short_answer_questions', '/diary', '/diary/create', '/diary/delete', '/diary/permissions','/diary/new_entry'] 

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
    if 'user_name' not in session:
        session['user_name'] = None
        session['token'] = None
    # if request.method =="POST":
    #     token = session.pop('_csrf_token',None)
    #     if not token or token != request.form.get('_csrf_token'):
    #         abort(403)
    

def is_logged_in(token):
# TBD: check if token is issued
    return True

# =======================================================
#                        M E T A
# =======================================================
@app.route("/")
def index():
    db=get_db()
    cursor2 = db.execute('Select * from diary_entries where public=1')
    posts = cursor2.fetchall()
    
    if session['token']:
        db=get_db()
        session_user_name = session['user_name']
        cursor = db.execute('SELECT * FROM users where name =(?)' ,[session_user_name])  
        cursor2 = db.execute('Select * from diary_entries where author=(?)', [session_user_name])
        user_posts = cursor2.fetchall()
        user = cursor.fetchone()
        make_json_response(session_user_name)
        return render_template('index.html', users=user, posts=posts, user_posts=user_posts )

    
    # return render_template('index.html', posts=posts )
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


    
# @verify_required_params(['email', 'password', 'name'])
# @validate_email_format

# ====================================================
#                 U S E R
# ====================================================
@app.route("/users/register", methods=['POST'])
def users_register():
    if not request.is_json:
        return make_json_response("Invalid request", False) 
    if request.method == 'POST':
        post_data = request.get_json() or {}
        username = post_data.get("username")
        password = post_data.get("password")
        fullname = post_data.get("fullname")
        age = post_data.get("age")

        db=get_db()
        submitted_name = username
        cursor = db.execute('SELECT * FROM users where name = (?)' , [submitted_name])
        a = cursor.fetchone()
        if a is None: 
            db=get_db()
            pw = generate_password_hash(password)
            db.execute('insert into users (id, name,password,fullname,age, token) values (null, ?,?,?,?, ?)', [username, pw, fullname ,age, '123'])
            #take note of token
            db.commit()
        else:
            data = {
                'status': False,
                'error': 'User already exists!'
            }
            return make_json_response(data)

        # User created response
        return make_json_response({'status': True}, status=201)

    else:
        print("Detect no posting data")

@app.route("/users/authenticate", methods=('GET','POST'))
def users_authenticate():
    if session['token']:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        db=get_db()
        form_name = form.name.data
        cursor = db.execute('SELECT * FROM users where name = ?', [form_name])  
        user = cursor.fetchone()
        #check_correct_password = check_password_hash(user['password', form.password.data) #double check pls! 
        if user is not None and check_password_hash(user['password'], form.password.data) is True:
            session['token'] = uuid4()
            session['user_name'] = user['name']
            flash('Thanks for logging in')
            return redirect(url_for('index'))
        else:
            flash('Sorry! no user exists with this username and password')
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

    #   return make_json_response(None) 
    # return make_json_response(None,False)

@app.route("/users")
def users():
    if session['token']:
        db=get_db()
        cursor = db.execute('SELECT * FROM users where name = (?)', [session['user_name']])  
        users = cursor.fetchone()
        # users = User.query.filter_by(name=session['user_name']).first()
        # if request.method =="POST":
        #   return make_json_response(users, True, 200)

        return render_template('info.html', users=users) 
    else:
        # if request.json and 'token' in request.json:
        #   error = [{"error":"Invalid authentication token"}]
        #   return make_json_response(error, False) 
        
        return render_template('unauthorised.html')
        
# @app.errorhandler(404)
# def not_found(error):
#   return make_json_response(jsonify({'eorror':'Not Found'}), 404)

# =====================================================
#                    D I A R Y
# =====================================================

@app.route("/diary", methods = ['GET'])
def diary(): 
    ## show authenticated user's diary
    # if session['token']:
    #     ## double check user's session
    #     # db=get_db()
    #     #cursor = db.execute('SELECT * FROM users where name = (?)', [session['user_name']])  
    #     # users = cursor.fetchone()
    #     # if users is not None:
    #     db=get_db()
    #     cursor = db.execute('SELECT * FROM diary_entries where author = (?)', [session['user_name']])  
    #     user_posts = cursor.fetchall()
    #     print(user_posts.text)
    #     return render_template("index.html",  user_posts=user_posts)

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
    

    cursor = db.execute('SELECT * FROM diary_entries where public=1')  
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
    diary_id = 1 if not a else 1 + int(a['id'])

    #insert diary entry

    # cur.execute('insert into members')
    db.execute('insert into diary_entries (id,title,author,publish_date,public,text) values (?,?,?,?,?,?)', [diary_id, title, session['user_name'], datetime.now() , public, text])

    db.commit()
    db.close()


    return make_json_response(diary_id,True,201)

@app.route("/diary/newEntry", methods=('GET','POST'))
def new_entry():
    form = NewEntryForm()
    if session['token']:
        if form.validate_on_submit():
            #====code to insert diary====
            db=get_db()
            #insert diary entry
            db.execute('insert into diary_entries (id,title,author,publish_date,public,text) values (null,?,?,?,?,?)', [form.title.data,session['user_name'], datetime.now() , form.public.data, form.text.data])
            db.commit()
            db.close()
            flash("Created new diaries")
            return redirect(url_for('index'))
        else:
            # flash("Sorry! Can't post now")
            # return make_json_response("Invalid inputs",False)
            return render_template('newEntry.html', form=form)

    return render_template('newEntry.html', form=form)



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
    app.run(debug=True, threaded=True, port=8080, host="0.0.0.0")
