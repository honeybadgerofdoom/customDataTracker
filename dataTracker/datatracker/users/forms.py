from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange, InputRequired
from datatracker.models import User
from datatracker.utils import findNextOpenData, usedNames, findGraphs


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username is taken. Please choose a different username.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('That email is taken. Please choose a different email.')



class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')



class UpdateAccountForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('That username is taken. Please choose a different username.')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('That email is taken. Please choose a different email.')



class RequestResetForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Request Password Reset')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('There is no account with that email, please register first.')



class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Reset Password')



class TrackingPointForm(FlaskForm):
	dataType = SelectField(u'Type', choices=[ 'Numeric',  'Yes/No', 'Low/Mid/High', 'Awful/Bad/Okay/Good/Great'])
	name = StringField('Name:', validators=[InputRequired(), Length(max=30)])
	submit = SubmitField('Create Data')

	def validate_dataType(self, dataType):
		if findNextOpenData(current_user, dataType.data) == -1:
			raise ValidationError('You cannot create any more of that data type')

	def validate_name(self, name):
		namesList = usedNames(current_user)
		for x in namesList:
			if x == name.data:
				raise ValidationError('You already have a tracking point with that name')



class updatePointNameForm(FlaskForm):
	name = StringField('Name:', validators=[InputRequired(), Length(max=30)])
	submit = SubmitField('Change Name')

	def validate_name(self, name):
		namesList = usedNames(current_user)
		for x in namesList:
			if x == name.data:
				raise ValidationError('You already have a tracking point with that name')




class GraphForm(FlaskForm):

	colorList = [(None, 'Choose a Color...'), 
		('#000000', 'Black'), 
		('#00ffff', 'Aqua'), 
		('#8a2be2', 'Blue Violet'), 
		('#7fff00', 'Chartreuse'), 
		('#006400', 'Dark Green'), 
		('#e9967a', 'Dark Salmon'), 
		('#00ced1', 'Dark Turquoise'), 
		('#b22222', 'Fire Brick'), 
		('#ff00ff', 'Fuchsia'), 
		('#ffd700', 'Gold'), 
		('#ff69b4', 'Hot Pink'), 
		('#da70d6', 'Orchid'), 
		('#800080', 'Purple'), 
		('#ee82ee', 'Violet')]

	name = StringField('Name', validators=[InputRequired(), Length(max=30)])

	# date_recorded = BooleanField('Date', default=False)
	# dateColor = SelectField(u'Date Color', choices=colorList, default=None)

	lmh1 = BooleanField('lmh1', default=False)
	cl1 = SelectField(u'cl1', choices=colorList, default='None')
	lmh2 = BooleanField('lmh2', default=False)
	cl2 = SelectField(u'cl2', choices=colorList, default='None')
	lmh3 = BooleanField('lmh3', default=False)
	cl3 = SelectField(u'cl3', choices=colorList, default='None')
	lmh4 = BooleanField('lmh4', default=False)
	cl4 = SelectField(u'cl4', choices=colorList, default='None')
	lmh5 = BooleanField('lmh5', default=False)
	cl5 = SelectField(u'cl5', choices=colorList, default='None')

	abogg1 = BooleanField('abogg1', default=False)
	ca1 = SelectField(u'ca1', choices=colorList, default='None')
	abogg2 = BooleanField('abogg2', default=False)
	ca2 = SelectField(u'ca2', choices=colorList, default='None')
	abogg3 = BooleanField('abogg3', default=False)
	ca3 = SelectField(u'ca3', choices=colorList, default='None')
	abogg4 = BooleanField('abogg4', default=False)
	ca4 = SelectField(u'ca4', choices=colorList, default='None')
	abogg5 = BooleanField('abogg5', default=False)
	ca5 = SelectField(u'ca5', choices=colorList, default='None')

	yn1 = BooleanField('yn1', default=False)
	cy1 = SelectField(u'cy1', choices=colorList, default='None')
	yn2 = BooleanField('yn2', default=False)
	cy2 = SelectField(u'cy2', choices=colorList, default='None')
	yn3 = BooleanField('yn3', default=False)
	cy3 = SelectField(u'cy3', choices=colorList, default='None')
	yn4 = BooleanField('yn4', default=False)
	cy4 = SelectField(u'cy4', choices=colorList, default='None')
	yn5 = BooleanField('yn5', default=False)
	cy5 = SelectField(u'cy5', choices=colorList, default='None')
	yn6 = BooleanField('yn6', default=False)
	cy6 = SelectField(u'cy6', choices=colorList, default='None')
	yn7 = BooleanField('yn7', default=False)
	cy7 = SelectField(u'cy7', choices=colorList, default='None')

	num1 = BooleanField('num1', default=False)
	cn1 = SelectField(u'cn1', choices=colorList, default='None')
	num2 = BooleanField('num2', default=False)
	cn2 = SelectField(u'cn2', choices=colorList, default='None')
	num3 = BooleanField('num3', default=False)
	cn3 = SelectField(u'cn3', choices=colorList, default='None')
	num4 = BooleanField('num4', default=False)
	cn4 = SelectField(u'cn4', choices=colorList, default='None')
	num5 = BooleanField('num5', default=False)
	cn5 = SelectField(u'cn5', choices=colorList, default='None')
	num6 = BooleanField('num6', default=False)
	cn6 = SelectField(u'cn6', choices=colorList, default='None')
	num7 = BooleanField('num7', default=False)
	cn7 = SelectField(u'cn7', choices=colorList, default='None')

	submit = SubmitField('Create Graph')

	def validate_name(self, name):
		graphNames = findGraphs(current_user)
		for x in graphNames:
			if x == name.data and name.data != 'N/A':
				raise ValidationError('You already have a graph with that name')

	def validate_index(self):
		if findNextOpenData(current_user) == -1:
			raise ValidationError('You cannot create any more graphs')





class UpdateGraphForm(FlaskForm):

	colorList = [(None, 'Choose a Color...'), 
		('#000000', 'Black'), 
		('#00ffff', 'Aqua'), 
		('#8a2be2', 'Blue Violet'), 
		('#7fff00', 'Chartreuse'), 
		('#006400', 'Dark Green'), 
		('#e9967a', 'Dark Salmon'), 
		('#00ced1', 'Dark Turquoise'), 
		('#b22222', 'Fire Brick'), 
		('#ff00ff', 'Fuchsia'), 
		('#ffd700', 'Gold'), 
		('#ff69b4', 'Hot Pink'), 
		('#da70d6', 'Orchid'), 
		('#800080', 'Purple'), 
		('#ee82ee', 'Violet')]

	name = StringField('Name', validators=[InputRequired(), Length(max=30)])

	# date_recorded = BooleanField('Date', default=False)
	# dateColor = SelectField(u'Date Color', choices=colorList, default=None)

	lmh1 = BooleanField('lmh1', default=False)
	cl1 = SelectField(u'cl1', choices=colorList, default='None')
	lmh2 = BooleanField('lmh2', default=False)
	cl2 = SelectField(u'cl2', choices=colorList, default='None')
	lmh3 = BooleanField('lmh3', default=False)
	cl3 = SelectField(u'cl3', choices=colorList, default='None')
	lmh4 = BooleanField('lmh4', default=False)
	cl4 = SelectField(u'cl4', choices=colorList, default='None')
	lmh5 = BooleanField('lmh5', default=False)
	cl5 = SelectField(u'cl5', choices=colorList, default='None')

	abogg1 = BooleanField('abogg1', default=False)
	ca1 = SelectField(u'ca1', choices=colorList, default='None')
	abogg2 = BooleanField('abogg2', default=False)
	ca2 = SelectField(u'ca2', choices=colorList, default='None')
	abogg3 = BooleanField('abogg3', default=False)
	ca3 = SelectField(u'ca3', choices=colorList, default='None')
	abogg4 = BooleanField('abogg4', default=False)
	ca4 = SelectField(u'ca4', choices=colorList, default='None')
	abogg5 = BooleanField('abogg5', default=False)
	ca5 = SelectField(u'ca5', choices=colorList, default='None')

	yn1 = BooleanField('yn1', default=False)
	cy1 = SelectField(u'cy1', choices=colorList, default='None')
	yn2 = BooleanField('yn2', default=False)
	cy2 = SelectField(u'cy2', choices=colorList, default='None')
	yn3 = BooleanField('yn3', default=False)
	cy3 = SelectField(u'cy3', choices=colorList, default='None')
	yn4 = BooleanField('yn4', default=False)
	cy4 = SelectField(u'cy4', choices=colorList, default='None')
	yn5 = BooleanField('yn5', default=False)
	cy5 = SelectField(u'cy5', choices=colorList, default='None')
	yn6 = BooleanField('yn6', default=False)
	cy6 = SelectField(u'cy6', choices=colorList, default='None')
	yn7 = BooleanField('yn7', default=False)
	cy7 = SelectField(u'cy7', choices=colorList, default='None')

	num1 = BooleanField('num1', default=False)
	cn1 = SelectField(u'cn1', choices=colorList, default='None')
	num2 = BooleanField('num2', default=False)
	cn2 = SelectField(u'cn2', choices=colorList, default='None')
	num3 = BooleanField('num3', default=False)
	cn3 = SelectField(u'cn3', choices=colorList, default='None')
	num4 = BooleanField('num4', default=False)
	cn4 = SelectField(u'cn4', choices=colorList, default='None')
	num5 = BooleanField('num5', default=False)
	cn5 = SelectField(u'cn5', choices=colorList, default='None')
	num6 = BooleanField('num6', default=False)
	cn6 = SelectField(u'cn6', choices=colorList, default='None')
	num7 = BooleanField('num7', default=False)
	cn7 = SelectField(u'cn7', choices=colorList, default='None')

	submit = SubmitField('Update Graph')
