#!/usr/bin/python

from flask import Flask
from flask_cors import CORS
from app import app, db 
from flask import session, request, abort, jsonify, render_template, escape
import json
import os
from model import *

app = Flask(__name__)
# Enable cross origin sharing for all endpoints
CORS(app)

# Remember to update this list
ENDPOINT_LIST = ['/', '/meta/heartbeat', '/meta/members', '/users/register', '/users/authenticate', '/users/expire', '/users/', '/meta/short_answer_questions'] 

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

@app.route("/users/register", methods=['POST'])
# @verify_required_params(['email', 'password', 'name'])
# @validate_email_format
def users_register():
    #Register a user
    username = request.args.get('name')
    password = request.args.get('password')
    password1 = request.args.get('password1')
    email = request.args.get('email')

    try:
        if username is None or password is None or password1 is None or email is None:
            return make_json_response({'data':{'succeed':False, 'message':"Missing required parameters"}}, 400)
        if password != password1:
            return make_json_response({'data':{'succeed':False, 'message':"Password don't match"}}, 400)

        username = username.lower()
        email = email.lower()

        if User.query.filter_by(username=username).first() is not None:
            return make_json_response({'data':{'succeed':False, 'message':"Username exists"}}, 400)

        if User.query.filter_by(email=email).first() is not None:
            return make_json_response({'data':{'succeed':False, 'message':"Email exists"}}, 400)

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        return handle_invalid_response(e)

    return make_json_response({'data':{'succeed':True, 'message':"Successfully signup"}}, 201)

 #    #if success
 #    if (1 == 1):
	# return make_json_response(None), 201
 #    return make_json_response(None,False)

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


if __name__ == '__main__':
    # Change the working directory to the script directory
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    # Run the application
    app.run(debug=False, port=8080, host="0.0.0.0")
