from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp

from albumy.models import User

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Length(1, 254), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Log in')

class RegisterForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
	email = StringField('Email', validators=[DataRequired(), Length(1, 254), Email()])
	username = StringField('Username', validators=[DataRequired(), Length(1, 20), Regexp('^[a-zA-Z0-9]*$', message='The username should contain only words and numbers')])
	password = PasswordField('Password', validators=[DataRequired(), Length(8, 128), EqualTo('password2')])
	password2 = PasswordField('Confirm password', validators=[DataRequired()])
	submit = SubmitField()

	def validate_email(self, field):
		if User.query.filter_by(email=field.data.lower()).first():
			return ValidationError('The email is already in use.')

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			return ValidationError('The username is already in use.')

class ForgetPasswordForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Length(1, 254), Email()])
	submit = SubmitField()

class ResetPasswordForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Length(1, 254), Email()])
	password = PasswordField('Password', validators=[DataRequired(), Length(8, 128), EqualTo('password2')])
	password2 = PasswordField('Comfirmed password', validators=[DataRequired()])
	submit = SubmitField()
