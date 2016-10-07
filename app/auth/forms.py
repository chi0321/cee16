from flask.ext.wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from ..modles import User

class LoginForm(Form):
	email = StringField('Email',validators=[Required(),Length(1,64),Email()])
	password = PasswordField('Password',validators=[Required()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Log In')

class RegistrationForm(Form):
	email = StringField('Email',validators=[Required(),Length(1,64),Email()])
	username = StringField('Username',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
	'Username must have only letter,numbers,dots or underscores')])
	password = StringField('Password',validators=[Required(),EqualTo('password2',message='Password must match.')])
	password2 = StringField('Confirm Password',validators=[Required()])
	submit = SubmitField('Register')

	def validate_email(self,field):	
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')
	def validate_username(self,field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already registered.')
class ChangePasswordForm(Form):
	oldpassword = StringField('Old Password',validators=[Required(),Length(1,64)])
	newpassword = StringField('New Password',validators=[Required(),Length(1,64)])
	newpassword2 = StringField('Confirm Password',validators=[Required(),EqualTo('newpassword',message='Password must match.')])
	submit = SubmitField('Change')
