# # from app import app, db
# from flask import jsonify
# from flask.ext.bcrypt import Bcrypt

# class User(db.Model):
# 	__tablename__ = 'uses'

# 	id = db.Column(db.Integer, primary_key = True)
# 	username = db.Column(db.String(32), index=True)
# 	email = db.Column(db.String(128))
# 	password_hash = db.Column(db.String(128))

# 	def hash_password(self, password):
# 		return bcrypt.generate_password_hash(password)

# 	def check_password(self, password):
# 		return bcrypt.check_password_hash(self.password, password)

# 	def __init__(self, username, email, password):
# 		self.username = username.lower()
# 		self.email = email.lower()
# 		self.password_hash = self.hash_password(password)

# 	def __repr__(self):
# 		return '<username {}>'.format(self.username)


import bcrypt
import uuid
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedSerializer, SignatureExpired, BadSignature
from sqlalchemy.sql.functions import now

# from include.Config import SIGNATURE_EXPIRED, BAD_SIGNATURE

db = SQLAlchemy()


# class Room(db.Model):
#     __tablename__ = 'rooms'
#     id = db.Column('id', db.Integer, primary_key=True)
#     name = db.Column('name', db.VARCHAR(250), unique=True)
#     password_hash = db.Column('password_hash', db.TEXT)
#     created_at = db.Column('created_at', db.TIMESTAMP)
#     updated_at = db.Column('updated_at', db.TIMESTAMP)
#     unique_id = db.Column('unique_id', db.VARCHAR(23), unique=True)

#     def __init__(self, name, password_hash, created_at, unique_id, updated_at):
#         self.name = name
#         self.password_hash = password_hash
#         self.created_at = created_at
#         self.unique_id = unique_id
#         self.updated_at = updated_at

#     def __repr__(self):
#         return '<Room %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.VARCHAR(250))
    password_hash = db.Column('password_hash', db.TEXT)
    fullname = db.Column('fullname', db.VARCHAR(250))
    age = db.Column('age', db.VARCHAR(23), unique=True)

    def __init__(self, username, fullname, password, age):
        self.username = username
        self.password_hash = self.__hash_pass(password)
        self.fullname = fullname
        self.age = age

    def as_dict(self):
        return {c.username: getattr(self, c.username) for c in self.__table__.columns}

    def __repr__(self):
        return '<User %r>' % self.username

    # def generate_auth_token(self):

    #     s = TimedSerializer(db.get_app().config['SECRET_KEY'])
    #     token = s.dumps({'id': self.id})
    #     s.loads(token, 3600)
    #     return token

    # @staticmethod
    # def verify_auth_token(token):
    #     s = TimedSerializer(db.get_app().config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token)
    #     except SignatureExpired:
    #         return SIGNATURE_EXPIRED
    #     except BadSignature:
    #         return BAD_SIGNATURE
    #     user_id = User.query.get(data['id']).id
    #     return user_id

    @staticmethod
    def __hash_pass(password, hashed_pass_or_salt=bcrypt.gensalt(14)):
        password_encoded = password.encode('utf-8')
        return bcrypt.hashpw(password_encoded, hashed_pass_or_salt)

    def check_password(self, password):
        pass_hash = self.__hash_pass(password, self.password_hash.encode('utf-8')).decode('utf-8')
        return pass_hash == self.password_hash


# class Task(db.Model):
#     __tablename__ = 'tasks'
#     id = db.Column('id', db.Integer, primary_key=True)
#     name = db.Column('name', db.VARCHAR(250))
#     created_at = db.Column('created_at', db.TIMESTAMP)
#     updated_at = db.Column('updated_at', db.TIMESTAMP)
#     done_at = db.Column('done_at', db.TIMESTAMP)
#     unique_id = db.Column('unique_id', db.VARCHAR(23), unique=True)
#     unique_room_id = db.Column('unique_room_id', db.VARCHAR(23))
#     next_user_unique_id = db.Column('next_user_unique_id', db.VARCHAR(23))
#     how_often = db.Column('how_often', db.INT)
#     is_till_end = db.Column('is_till_end', db.INT)
#     is_ended = db.Column('is_ended', db.INT)

#     def __init__(self, name, created_at, unique_id,
#                  updated_at, unique_room_id, done_at, is_till_end,
#                  is_ended, next_user_unique_id, how_often):
#         self.name = name
#         self.created_at = created_at
#         self.updated_at = updated_at
#         self.done_at = done_at
#         self.unique_id = unique_id
#         self.unique_room_id = unique_room_id
#         self.next_user_unique_id = next_user_unique_id
#         self.how_often = how_often
#         self.is_till_end = is_till_end
#         self.is_ended = is_ended

#     def __repr__(self):
#         return '<Task %r>' % self.name


# class TaskUser(db.Model):
#     __tablename__ = 'tasks_users'
#     id = db.Column('id', db.Integer, primary_key=True)
#     unique_user_id = db.Column('unique_user_id', db.VARCHAR(23))
#     unique_task_id = db.Column('unique_task_id', db.VARCHAR(23))

#     def __init__(self, unique_user_id, unique_task_id):
#         self.unique_task_id = unique_task_id
#         self.unique_user_id = unique_user_id

#     def __repr__(self):
#         return '<Task user uid %r>' % self.unique_user_id
