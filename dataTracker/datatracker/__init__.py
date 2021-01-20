from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
from flask_mail import Mail
from datatracker.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
bootStrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()



#this function returns a list of the visibility indicators for a user
def visIndicators(user):
	dPoints = user.query.get(user.id).user_points
	vis = []
	for x in dPoints:
		vis.append(x.visible)
	return vis


def getDailyData(user):
	page = request.args.get('page', 1, type=int)
	dailyData = DailyData.query.filter_by(user_id=user.id)\
		.order_by(DailyData.date_recorded.desc()).paginate(page=page, per_page=14)
	return dailyData


#this function determines if notes are on/off, return boolean True if on
def noteStatus(user):
	vis = visIndicators(user)
	noteIndicator = vis[24]
	return noteIndicator


def visiblePoints(user):
	dPoints = user.query.get(user.id).user_points
	visPoints = []
	for x in dPoints:
		if x.visible:
			visPoints.append(x)
	return visPoints


def getGraphData(user):
	graphs = user.query.get(user.id).user_graphs
	return graphs



def allNames(user):
	dPoints = user.query.get(user.id).user_points
	names = []
	for x in dPoints:
		names.append(x.name)
	return names



#this function returns a list of visible points for a graph
def graphPoints(user):
	graphs = user.query.get(user.id).user_graphs
	masterList = []

	for x in graphs:
		pointList = []

		pointList.append(x.lmh1)
		pointList.append(x.lmh2)
		pointList.append(x.lmh3)
		pointList.append(x.lmh4)
		pointList.append(x.lmh5)

		pointList.append(x.abogg1)
		pointList.append(x.abogg2)
		pointList.append(x.abogg3)
		pointList.append(x.abogg4)
		pointList.append(x.abogg5)

		pointList.append(x.yn1)
		pointList.append(x.yn2)
		pointList.append(x.yn3)
		pointList.append(x.yn4)
		pointList.append(x.yn5)
		pointList.append(x.yn6)
		pointList.append(x.yn7)

		pointList.append(x.num1)
		pointList.append(x.num2)
		pointList.append(x.num3)
		pointList.append(x.num4)
		pointList.append(x.num5)
		pointList.append(x.num6)
		pointList.append(x.num7)

		masterList.append(pointList)

	return masterList


#this function returns a list of visible booleans for a graph
def graphPointList(graph):
	graphList = []

	graphList.append(graph.lmh1)
	graphList.append(graph.lmh2)
	graphList.append(graph.lmh3)
	graphList.append(graph.lmh4)
	graphList.append(graph.lmh5)

	graphList.append(graph.abogg1)
	graphList.append(graph.abogg2)
	graphList.append(graph.abogg3)
	graphList.append(graph.abogg4)
	graphList.append(graph.abogg5)

	graphList.append(graph.yn1)
	graphList.append(graph.yn2)
	graphList.append(graph.yn3)
	graphList.append(graph.yn4)
	graphList.append(graph.yn5)
	graphList.append(graph.yn6)
	graphList.append(graph.yn7)

	graphList.append(graph.num1)
	graphList.append(graph.num2)
	graphList.append(graph.num3)
	graphList.append(graph.num4)
	graphList.append(graph.num5)
	graphList.append(graph.num6)
	graphList.append(graph.num7)

	return graphList


#this function returns a list of colors for a graph
def graphColorList(graph):
	graphList = []

	graphList.append(graph.cl1)
	graphList.append(graph.cl2)
	graphList.append(graph.cl3)
	graphList.append(graph.cl4)
	graphList.append(graph.cl5)

	graphList.append(graph.ca1)
	graphList.append(graph.ca2)
	graphList.append(graph.ca3)
	graphList.append(graph.ca4)
	graphList.append(graph.ca5)

	graphList.append(graph.cy1)
	graphList.append(graph.cy2)
	graphList.append(graph.cy3)
	graphList.append(graph.cy4)
	graphList.append(graph.cy5)
	graphList.append(graph.cy6)
	graphList.append(graph.cy7)

	graphList.append(graph.cn1)
	graphList.append(graph.cn2)
	graphList.append(graph.cn3)
	graphList.append(graph.cn4)
	graphList.append(graph.cn5)
	graphList.append(graph.cn6)
	graphList.append(graph.cn7)

	return graphList


#this function returns a list of all user graphs
def allGraphs(user):
	theGraphs = user.query.get(user.id).user_graphs
	graphList = []
	for x in theGraphs:
		graphList.append(x)
	return graphList



#this function returns a dictionary mapping color names
def colorMapper(color):
	allColors = {
		'None' : 'N/A',
		'#000000' : 'Black', 
		'#00ffff' : 'Aqua', 
		'#8a2be2' : 'Blue Violet', 
		'#7fff00' : 'Chartreuse', 
		'#006400' : 'Dark Green', 
		'#e9967a' : 'Dark Salmon', 
		'#00ced1' : 'Dark Turquoise', 
		'#b22222' : 'Fire Brick', 
		'#ff00ff' : 'Fuchsia', 
		'#ffd700' : 'Gold', 
		'#ff69b4' : 'Hot Pink', 
		'#da70d6' : 'Orchid', 
		'#800080' : 'Purple', 
		'#ee82ee' : 'Violet'
		}
	mappedColor = allColors[color]
	return mappedColor


def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)


	app.jinja_env.globals.update(getDailyData=getDailyData)
	app.jinja_env.globals.update(noteStatus=noteStatus)
	app.jinja_env.globals.update(visiblePoints=visiblePoints)
	app.jinja_env.globals.update(getGraphData=getGraphData)
	app.jinja_env.globals.update(colorMapper=colorMapper)
	app.jinja_env.globals.update(visIndicators=visIndicators)
	app.jinja_env.globals.update(allNames=allNames)
	app.jinja_env.globals.update(allGraphs=allGraphs)
	app.jinja_env.globals.update(graphPoints=graphPoints)
	app.jinja_env.globals.update(graphPointList=graphPointList)
	app.jinja_env.globals.update(graphColorList=graphColorList)


	db.init_app(app)
	bcrypt.init_app(app)
	bootStrap.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	from datatracker.users.routes import users
	from datatracker.data.routes import data
	from datatracker.errors.handlers import errors
	app.register_blueprint(users)
	app.register_blueprint(data)
	app.register_blueprint(errors)

	return app

from datatracker.models import DailyData
