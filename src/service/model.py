from app import app, db
from flask import jsonify
from flask.ext.bcrypt import Bcrypt

class User(db.Model):
	__tablename__ = 'uses'

	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(32), index=True)
	email = db.Column(db.String(128))
	password_hash = db.Column(db.String(128))

	def hash_password(self, password):
		return bcrypt.generate_password_hash(password)

	def check_password(self, password):
		return bcrypt.check_password_hash(self.password, password)

	def __init__(self, username, email, password):
		self.username = username.lower()
		self.email = email.lower()
		self.password_hash = self.hash_password(password)

	def __repr__(self):
		return '<username {}>'.format(self.username)
