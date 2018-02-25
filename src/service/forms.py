from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField,IntegerField
from wtforms.validators import Email, Length, EqualTo, DataRequired


class LoginForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])


class SignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('Password', [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    # email = StringField('Email', validators=[DataRequired(), Length(min=5, max=35), Email()])
    fullname = StringField('Fullname', validators=[DataRequired(), Length(min=2, max=30)])
    age = IntegerField('Age', validators=[DataRequired()])


class NewEntryForm(FlaskForm):
    token = StringField('token')
    title = StringField('title', validators=[DataRequired(), Length(min=2, max=30)])
    public = IntegerField('public', validators=[DataRequired()])
    text = StringField('text', validators=[DataRequired()])

