#!/usr/bin/python

from flask import Flask
from flask_cors import CORS
from flask import request
import sys
import json
import os

app = Flask(__name__)
# Enable cross origin sharing for all endpoints
CORS(app)

# Remember to update this list
ENDPOINT_LIST = ['/', '/meta/heartbeat', '/meta/members', '/users/register', '/users/authenticate', '/users/expire', '/users/', '/meta/short_answer_questions', '/diary', '/diary/create', '/diary/delete', '/diary/permissions'] 


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

# =======================================================
#                     C O M M O N
# =======================================================

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
@app.route("/diary")
def diary():
	return make_json_response(None)

@app.route("/diary/create", methods=['POST'])
def diary_create():

	try:
		data = request.get_json()
		print data
		print data['token']
		if (is_logged_in(data['token'])):
			return make_json_response(None,True,201)
		return make_json_response("Invalid authentication token",False)
	except:
		return make_json_response("Invalid authentication token",False)


@app.route("/diary/delete")
def diary_delete():
	return make_json_response(None)

@app.route("/diary/permissions")
def diary_permissions():
	return make_json_response(None)


# working
if __name__ == '__main__':
    # Change the working directory to the script directory
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    # Run the application
    app.run(debug=False, port=8080, host="0.0.0.0")
