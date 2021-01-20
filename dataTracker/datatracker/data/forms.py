
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, DecimalField, TextAreaField, StringField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, NumberRange, InputRequired, ValidationError, Length
from wtforms_components import DateRange
from datatracker.models import User
from flask_login import current_user
from datetime import date


class DataForm(FlaskForm):

	lmhList = ['High', 'Mid', 'Low']
	aboggList = ['Great', 'Good', 'Okay', 'Bad', 'Awful']
	ynList = ['Yes', 'No']

	date_recorded = DateField('Date', format="%Y-%m-%d", default=date.today)

	lmh1 = SelectField(u'lmh1', choices=lmhList, default='Mid')
	lmh2 = SelectField(u'lmh2', choices=lmhList, default='Mid')
	lmh3 = SelectField(u'lmh3', choices=lmhList, default='Mid')
	lmh4 = SelectField(u'lmh4', choices=lmhList, default='Mid')
	lmh5 = SelectField(u'lmh5', choices=lmhList, default='Mid')

	abogg1 = SelectField(u'abogg1', choices=aboggList, default='Okay')
	abogg2 = SelectField(u'abogg2', choices=aboggList, default='Okay')
	abogg3 = SelectField(u'abogg3', choices=aboggList, default='Okay')
	abogg4 = SelectField(u'abogg4', choices=aboggList, default='Okay')
	abogg5 = SelectField(u'abogg5', choices=aboggList, default='Okay')

	yn1 = SelectField(u'yn1', choices=ynList, default='No')
	yn2 = SelectField(u'yn2', choices=ynList, default='No')
	yn3 = SelectField(u'yn3', choices=ynList, default='No')
	yn4 = SelectField(u'yn4', choices=ynList, default='No')
	yn5 = SelectField(u'yn5', choices=ynList, default='No')
	yn6 = SelectField(u'yn6', choices=ynList, default='No')
	yn7 = SelectField(u'yn7', choices=ynList, default='No')

	num1 = DecimalField('num1', default=0)
	num2 = DecimalField('num2', default=0)
	num3 = DecimalField('num3', default=0)
	num4 = DecimalField('num4', default=0)
	num5 = DecimalField('num5', default=0)
	num6 = DecimalField('num6', default=0)
	num7 = DecimalField('num7', default=0)

	notes = TextAreaField('Notes', default='Today\'s notes...')

	submit = SubmitField('Record Data')

	def validate_date_recorded(self, date_recorded):
		if date_recorded.data is None:
			raise ValidationError()
		if date_recorded.data > date.today():
			raise ValidationError('You can\'t record data for the future.')
		elif date_recorded.data < date(2000,1,1):
			raise ValidationError('The earliest date you can record data for is 01/01/2000')
		targetDate = date_recorded.data.strftime('%Y-%m-%d')
		userData = User.query.get(current_user.id).user_data
		for x in userData:
			if targetDate == x.date_recorded.strftime('%Y-%m-%d'):
				raise ValidationError('You already recorded data for this day. You may update this data from the data list.')

class UpdateDataForm(FlaskForm):

	lmhList = ['High', 'Mid', 'Low']
	aboggList = ['Great', 'Good', 'Okay', 'Bad', 'Awful']
	ynList = ['Yes', 'No']

	lmh1 = SelectField(u'lmh1', choices=lmhList, default='Mid')
	lmh2 = SelectField(u'lmh2', choices=lmhList, default='Mid')
	lmh3 = SelectField(u'lmh3', choices=lmhList, default='Mid')
	lmh4 = SelectField(u'lmh4', choices=lmhList, default='Mid')
	lmh5 = SelectField(u'lmh5', choices=lmhList, default='Mid')

	abogg1 = SelectField(u'abogg1', choices=aboggList, default='Okay')
	abogg2 = SelectField(u'abogg2', choices=aboggList, default='Okay')
	abogg3 = SelectField(u'abogg3', choices=aboggList, default='Okay')
	abogg4 = SelectField(u'abogg4', choices=aboggList, default='Okay')
	abogg5 = SelectField(u'abogg5', choices=aboggList, default='Okay')

	yn1 = SelectField(u'yn1', choices=ynList, default='No')
	yn2 = SelectField(u'yn2', choices=ynList, default='No')
	yn3 = SelectField(u'yn3', choices=ynList, default='No')
	yn4 = SelectField(u'yn4', choices=ynList, default='No')
	yn5 = SelectField(u'yn5', choices=ynList, default='No')
	yn6 = SelectField(u'yn6', choices=ynList, default='No')
	yn7 = SelectField(u'yn7', choices=ynList, default='No')

	num1 = DecimalField('num1', default=0)
	num2 = DecimalField('num2', default=0)
	num3 = DecimalField('num3', default=0)
	num4 = DecimalField('num4', default=0)
	num5 = DecimalField('num5', default=0)
	num6 = DecimalField('num6', default=0)
	num7 = DecimalField('num7', default=0)

	notes = TextAreaField('Notes', default='Today\'s notes...')

	submit = SubmitField('Update Data')

