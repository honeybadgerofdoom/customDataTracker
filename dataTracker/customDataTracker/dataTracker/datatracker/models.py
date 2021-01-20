
from datetime import date
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datatracker import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))



class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	user_points = db.relationship('DataPoint', backref='backrefDP', lazy=True)
	user_data = db.relationship('DailyData', backref='backrefDD', lazy=True)
	user_graphs = db.relationship('Graph', backref='backrefGraph', lazy=True)

	def get_reset_token(self, expires_sec=1800):
		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}')"



class DataPoint(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	index = db.Column(db.Integer, nullable=False)
	visible = db.Column(db.Boolean, nullable=False)
	dataType = db.Column(db.String(30), nullable=False)
	name = db.Column(db.String(30), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	def __repr__(self):
		return f"DataPoint('{self.id}, {self.name}', '{self.dataType}', '{self.index}', '{self.visible}')"



class DailyData(db.Model):

	id = db.Column(db.Integer, primary_key=True)

	date_recorded = db.Column(db.Date, nullable=False)

	lmh1 = db.Column(db.String, nullable=True)
	lmh2 = db.Column(db.String, nullable=True)
	lmh3 = db.Column(db.String, nullable=True)
	lmh4 = db.Column(db.String, nullable=True)
	lmh5 = db.Column(db.String, nullable=True)

	abogg1 = db.Column(db.String, nullable=True)
	abogg2 = db.Column(db.String, nullable=True)
	abogg3 = db.Column(db.String, nullable=True)
	abogg4 = db.Column(db.String, nullable=True)
	abogg5 = db.Column(db.String, nullable=True)

	yn1 = db.Column(db.String, nullable=True)
	yn2 = db.Column(db.String, nullable=True)
	yn3 = db.Column(db.String, nullable=True)
	yn4 = db.Column(db.String, nullable=True)
	yn5 = db.Column(db.String, nullable=True)
	yn6 = db.Column(db.String, nullable=True)
	yn7 = db.Column(db.String, nullable=True)

	num1 = db.Column(db.Float, nullable=True)
	num2 = db.Column(db.Float, nullable=True)
	num3 = db.Column(db.Float, nullable=True)
	num4 = db.Column(db.Float, nullable=True)
	num5 = db.Column(db.Float, nullable=True)
	num6 = db.Column(db.Float, nullable=True)
	num7 = db.Column(db.Float, nullable=True)

	notes = db.Column(db.Text, nullable=True)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f'''DailyData('{self.date_recorded}', 
'{self.lmh1}', '{self.lmh2}', '{self.lmh3}', '{self.lmh4}', '{self.lmh5}', , 
'{self.abogg1}', '{self.abogg2}', '{self.abogg3}', '{self.abogg4}', '{self.abogg5}', 
'{self.yn1}', '{self.yn2}', '{self.yn3}', '{self.yn4}', '{self.yn5}', '{self.yn6}', '{self.yn7}', 
'{self.num1}', '{self.num2}', '{self.num3}', '{self.num4}', '{self.num5}', '{self.num6}', '{self.num7}', 
'{self.notes}')'''


class Graph(db.Model):

	id = db.Column(db.Integer, primary_key=True)

	index = db.Column(db.Integer, nullable=False)
	visible = db.Column(db.Boolean, default=False)
	name = db.Column(db.String(30), default='N/A')

	date_recorded = db.Column(db.Boolean, default=False)
	dateColor = db.Column(db.String(15), default=None)

	lmh1 = db.Column(db.Boolean, default=False)
	cl1 = db.Column(db.String(15), default=None)
	lmh2 = db.Column(db.Boolean, default=False)
	cl2 = db.Column(db.String(15), default=None)
	lmh3 = db.Column(db.Boolean, default=False)
	cl3 = db.Column(db.String(15), default=None)
	lmh4 = db.Column(db.Boolean, default=False)
	cl4 = db.Column(db.String(15), default=None)
	lmh5 = db.Column(db.Boolean, default=False)
	cl5 = db.Column(db.String(15), default=None)

	abogg1 = db.Column(db.Boolean, default=False)
	ca1 = db.Column(db.String(15), default=None)
	abogg2 = db.Column(db.Boolean, default=False)
	ca2 = db.Column(db.String(15), default=None)
	abogg3 = db.Column(db.Boolean, default=False)
	ca3 = db.Column(db.String(15), default=None)
	abogg4 = db.Column(db.Boolean, default=False)
	ca4 = db.Column(db.String(15), default=None)
	abogg5 = db.Column(db.Boolean, default=False)
	ca5 = db.Column(db.String(15), default=None)

	yn1 = db.Column(db.Boolean, default=False)
	cy1 = db.Column(db.String(15), default=None)
	yn2 = db.Column(db.Boolean, default=False)
	cy2 = db.Column(db.String(15), default=None)
	yn3 = db.Column(db.Boolean, default=False)
	cy3 = db.Column(db.String(15), default=None)
	yn4 = db.Column(db.Boolean, default=False)
	cy4 = db.Column(db.String(15), default=None)
	yn5 = db.Column(db.Boolean, default=False)
	cy5 = db.Column(db.String(15), default=None)
	yn6 = db.Column(db.Boolean, default=False)
	cy6 = db.Column(db.String(15), default=None)
	yn7 = db.Column(db.Boolean, default=False)
	cy7 = db.Column(db.String(15), default=None)

	num1 = db.Column(db.Boolean, default=False)
	cn1 = db.Column(db.String(15), default=None)
	num2 = db.Column(db.Boolean, default=False)
	cn2 = db.Column(db.String(15), default=None)
	num3 = db.Column(db.Boolean, default=False)
	cn3 = db.Column(db.String(15), default=None)
	num4 = db.Column(db.Boolean, default=False)
	cn4 = db.Column(db.String(15), default=None)
	num5 = db.Column(db.Boolean, default=False)
	cn5 = db.Column(db.String(15), default=None)
	num6 = db.Column(db.Boolean, default=False)
	cn6 = db.Column(db.String(15), default=None)
	num7 = db.Column(db.Boolean, default=False)
	cn7 = db.Column(db.String(15), default=None)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f'''Graph('{self.visible}', '{self.name}', '{self.date_recorded}', '{self.dateColor}', 
'{self.lmh1}', '{self.cl1}', '{self.lmh2}', '{self.cl2}', '{self.lmh3}', '{self.cl3}', '{self.lmh4}', '{self.cl4}', '{self.lmh5}', '{self.cl5}', 
'{self.abogg1}', '{self.ca1}', '{self.abogg2}', '{self.ca2}', '{self.abogg3}', '{self.ca3}', '{self.abogg4}', '{self.ca4}', '{self.abogg5}', '{self.ca5}', 
'{self.yn1}', '{self.cy1}', '{self.yn2}', '{self.cy2}', '{self.yn3}', '{self.cy3}', '{self.yn4}', '{self.cy4}', '{self.yn5}', '{self.cy5}', '{self.yn6}', '{self.cy6}', '{self.yn7}', '{self.cy7}', 
'{self.num1}', '{self.cn1}', '{self.num2}', '{self.cn2}', '{self.num3}', '{self.cn3}', '{self.num4}', '{self.cn4}', '{self.num5}', '{self.cn5}', '{self.num6}', '{self.cn6}', '{self.num7}', '{self.cn7}')'''
