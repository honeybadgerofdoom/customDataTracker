import os
import secrets
from flask import url_for, request
from flask_mail import Message
from datatracker import mail
from datatracker.models import User, DailyData
from flask_login import current_user


#FIXME Why does user.query work? Should be User.query....



#this function creates a dictionary of {user's name: database's name} pairs for data names
def nameMapper(user):
	uNames = []
	dNames = ['lmh1', 'lmh2', 'lmh3', 'lmh4', 'lmh5', 'abogg1', 'abogg2', 'abogg3', 'abogg4', 'abogg5',
		'yn1', 'yn2', 'yn3', 'yn4', 'yn5', 'yn6', 'yn7', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'num7', 'Notes']
	dPoints = User.query.get(user.id).user_points
	for x in dPoints:
		uNames.append(x.name)
	mappedNames = {}
	for key in uNames:
		for value in dNames:
			mappedNames[key] = value
			dNames.remove(value)
			break
	return mappedNames



#this function returns a lsit of all graphs a user has
def findGraphs(user):
	graphs = user.query.get(user.id).user_graphs
	graphNames = []
	for x in graphs:
		if x.name != 'N/A':
			graphNames.append(x.name)
	return graphNames



#this function returns a list of the names of all user points USED
def usedNames(user):
	dPoints = User.query.get(current_user.id).user_points
	namesList = []
	for x in dPoints:
		if x.visible:
			namesList.append(x.name)
	return namesList



#this function sends a password reset token to the user
def send_reset_email(user): 
	token = user.get_reset_token()
	msg = Message('Password Reset Request', sender='vocaldatatracker@gmail.com', recipients=[user.email])
	msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
	mail.send(msg)



#this function returns all DailyData associated with a user, paginated at 30/page
def getDailyData(user):
	page = request.args.get('page', 1, type=int)
	dailyData = DailyData.query.filter_by(user_id=user.id)\
		.order_by(DailyData.date_recorded.desc()).paginate(page=page, per_page=14)
	return dailyData



#this function returns the index of the next open graph slot, -1 in none available
def findNextOpenGraph(user):
	graphs = User.query.get(current_user.id).user_graphs
	visList = []
	for x in graphs:
		visList.append(x.visible)
	for i in range(10):
		if not visList[i]:
			return i
	return -1




#this function returns the index of the next open data slot of that type, -1 if none available
def findNextOpenData(user, dType):
	dPoints = User.query.get(current_user.id).user_points
	visList = []
	for x in dPoints:
		visList.append(x.visible)
	if dType == 'Low/Mid/High':
		for i in range(5):
			if not visList[i]:
				return i
	elif dType == 'Awful/Bad/Okay/Good/Great':
		for i in range(5, 10):
			if not visList[i]:
				return i
	elif dType == 'Yes/No':
		for i in range(10, 17):
			if not visList[i]:
				return i
	elif dType == 'Numeric':
		for i in range(17, 24):
			if not visList[i]:
				return i
	return -1



#this function returns a list of the visibility indicators for a user
def visIndicators(user):
	dPoints = user.query.get(user.id).user_points
	vis = []
	for x in dPoints:
		vis.append(x.visible)
	return vis



#this function determines if notes are on/off, return boolean True if on
def noteStatus(user):
	vis = visIndicators(user)
	noteIndicator = vis[24]
	return noteIndicator



#this function returns a list of all names
def allNames(user):
	dPoints = user.query.get(user.id).user_points
	names = []
	for x in dPoints:
		names.append(x.name)
	return names



def visiblePoints(user):
	dPoints = user.query.get(user.id).user_points
	visPoints = []
	for x in dPoints:
		if x.visible:
			visPoints.append(x)
	return visPoints


#this function returns a list of all user graphs
def allGraphs(user):
	theGraphs = user.query.get(user.id).user_graphs
	graphList = []
	for x in theGraphs:
		graphList.append(x)
	return graphList


#this function returns a list of visible indicators for user graphs
def visibleGraphs(user):
	theGraphs = user.query.get(user.id).user_graphs
	graphList = []
	for x in theGraphs:
		graphList.append(x.visible)
	return graphList



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

