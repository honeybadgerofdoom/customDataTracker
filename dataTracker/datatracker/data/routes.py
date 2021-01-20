import datetime
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, send_file
from datatracker import db
from datatracker.data.forms import DataForm, UpdateDataForm
from datatracker.models import User, DailyData, DataPoint
from flask_login import current_user, login_required
from datatracker.utils import visiblePoints, getDailyData, visIndicators, allNames, noteStatus, allGraphs, visibleGraphs, graphPointList, graphColorList

data = Blueprint('data', __name__)
DEBUG = True


@data.route('/')
@data.route('/data/visualize', methods=['GET', 'POST'])
@login_required
def visualize():
	page = request.args.get('page', 1, type=int)
	dataNum = DailyData.query.filter_by(user_id=current_user.id).count()
	return render_template('dataTemplates/visualize.html', title='visualize', dailyData=getDailyData(current_user),
		page=page, dataNum=dataNum, legend='Visualize', visGraphs=visibleGraphs(current_user))



@data.route('/graph0.html')
def graph0():
	theGraph = allGraphs(current_user)[0]
	points = list(map(str, graphPointList(theGraph)))
	colors = graphColorList(theGraph)
	return render_template('dataTemplates/graphs/graph0.html', theGraph=theGraph, points=points,
		colors=colors)

@data.route('/graph1.html')
def graph1():
	theGraph = allGraphs(current_user)[1]
	points = list(map(str, graphPointList(theGraph)))
	colors = graphColorList(theGraph)
	return render_template('dataTemplates/graphs/graph1.html', theGraph=theGraph, points=points,
		colors=colors)

@data.route('/graph2.html')
def graph2():
	theGraph = allGraphs(current_user)[2]
	points = list(map(str, graphPointList(theGraph)))
	colors = graphColorList(theGraph)
	return render_template('dataTemplates/graphs/graph2.html', theGraph=theGraph, points=points,
		colors=colors)

@data.route('/graph3.html')
def graph3():
	theGraph = allGraphs(current_user)[3]
	points = list(map(str, graphPointList(theGraph)))
	colors = graphColorList(theGraph)
	return render_template('dataTemplates/graphs/graph3.html', theGraph=theGraph, points=points,
		colors=colors)

@data.route('/graph4.html')
def graph4():
	theGraph = allGraphs(current_user)[4]
	points = list(map(str, graphPointList(theGraph)))
	colors = graphColorList(theGraph)
	return render_template('dataTemplates/graphs/graph4.html', theGraph=theGraph, points=points,
		colors=colors)

@data.route('/graph5.html')
def graph5():
	theGraph = allGraphs(current_user)[5]
	points = list(map(str, graphPointList(theGraph)))
	colors = graphColorList(theGraph)
	return render_template('dataTemplates/graphs/graph5.html', theGraph=theGraph, points=points,
		colors=colors)

@data.route('/graph6.html')
def graph6():
	theGraph = allGraphs(current_user)[6]
	points = list(map(str, graphPointList(theGraph)))
	colors = graphColorList(theGraph)
	return render_template('dataTemplates/graphs/graph6.html', theGraph=theGraph, points=points,
		colors=colors)

@data.route('/graph7.html')
def graph7():
	theGraph = allGraphs(current_user)[7]
	points = list(map(str, graphPointList(theGraph)))
	colors = graphColorList(theGraph)
	return render_template('dataTemplates/graphs/graph7.html', theGraph=theGraph, points=points,
		colors=colors)

@data.route('/graph8.html')
def graph8():
	theGraph = allGraphs(current_user)[8]
	points = list(map(str, graphPointList(theGraph)))
	colors = graphColorList(theGraph)
	return render_template('dataTemplates/graphs/graph8.html', theGraph=theGraph, points=points,
		colors=colors)


@data.route('/graph9.html')
def graph9():
	theGraph = allGraphs(current_user)[9]
	points = list(map(str, graphPointList(theGraph)))
	colors = graphColorList(theGraph)
	return render_template('dataTemplates/graphs/graph9.html', theGraph=theGraph, points=points,
		colors=colors)



@data.route('/data/input', methods=['GET', 'POST'])
@login_required
def inputData():
	form = DataForm()
	if form.validate_on_submit():

		vis = visIndicators(current_user)

		nlmh1 = form.lmh1.data if vis[0] else None
		nlmh2 = form.lmh2.data if vis[1] else None
		nlmh3 = form.lmh3.data if vis[2] else None
		nlmh4 = form.lmh4.data if vis[3] else None
		nlmh5 = form.lmh5.data if vis[4] else None
		nabogg1 = form.abogg1.data if vis[5] else None
		nabogg2 = form.abogg2.data if vis[6] else None
		nabogg3 = form.abogg3.data if vis[7] else None
		nabogg4 = form.abogg4.data if vis[8] else None
		nabogg5 = form.abogg5.data if vis[9] else None
		nyn1 = form.yn1.data if vis[10] else None
		nyn2 = form.yn2.data if vis[11] else None
		nyn3 = form.yn1.data if vis[12] else None
		nyn4 = form.yn2.data if vis[13] else None
		nyn5 = form.yn3.data if vis[14] else None
		nyn6 = form.yn1.data if vis[15] else None
		nyn7 = form.yn1.data if vis[16] else None
		nnum1 = form.num1.data if vis[17] else None
		nnum2 = form.num2.data if vis[18] else None
		nnum3 = form.num3.data if vis[19] else None
		nnum4 = form.num4.data if vis[20] else None
		nnum5 = form.num5.data if vis[21] else None
		nnum6 = form.num6.data if vis[22] else None
		nnum7 = form.num7.data if vis[23] else None
		nnotes = form.notes.data if vis[24] else None
		if nnotes == 'Today\'s notes...':
			nnotes = None

		newData = DailyData(date_recorded=form.date_recorded.data, lmh1=nlmh1, lmh2=nlmh2, lmh3=nlmh3, lmh4=nlmh4, lmh5=nlmh5,
			abogg1=nabogg1, abogg2=nabogg2, abogg3=nabogg3, abogg4=nabogg4, abogg5=nabogg5, yn1=nyn1, yn2=nyn2, yn3=nyn3,
			yn4=nyn4, yn5=nyn5, yn6=nyn6, yn7=nyn7,num1=nnum1, num2=nnum2, num3=nnum3, num4=nnum4, num5=nnum5, num6=nnum6,
			num7=nnum7, notes=nnotes, backrefDD=current_user)
		db.session.add(newData)
		db.session.commit()

		flash('Data Received', 'success')
		return redirect(url_for('data.visualize'))
	return render_template('dataTemplates/inputData.html', title='input', form=form,
		vis=visIndicators(current_user), names=allNames(current_user), legend='Input Data')



@data.route('/data/<person_me>/<int:updateData_id>/update', methods=['GET', 'POST'])
@login_required
def updateData(person_me, updateData_id):
	datum = DailyData.query.get_or_404(updateData_id)
	if datum.backrefDD != current_user:
		abort(403)
	form = UpdateDataForm()
	if form.validate_on_submit():
		vis = visIndicators(current_user)
		x = DailyData.query.get(updateData_id)
		x.lmh1 = form.lmh1.data if vis[0] else x.lmh1
		x.lmh2 = form.lmh2.data if vis[1] else x.lmh2
		x.lmh3 = form.lmh3.data if vis[2] else x.lmh3
		x.lmh4 = form.lmh4.data if vis[3] else x.lmh4
		x.lmh5 = form.lmh5.data if vis[4] else x.lmh5
		x.abogg1 = form.abogg1.data if vis[5] else x.abogg1
		x.abogg2 = form.abogg2.data if vis[6] else x.abogg2
		x.abogg3 = form.abogg3.data if vis[7] else x.abogg3
		x.abogg4 = form.abogg4.data if vis[8] else x.abogg4
		x.abogg5 = form.abogg5.data if vis[9] else x.abogg5
		x.yn1 = form.yn1.data if vis[10] else x.yn1
		x.yn2 = form.yn2.data if vis[11] else x.yn2
		x.yn3 = form.yn3.data if vis[12] else x.yn3
		x.yn4 = form.yn4.data if vis[13] else x.yn4
		x.yn5 = form.yn5.data if vis[14] else x.yn5
		x.yn6 = form.yn6.data if vis[15] else x.yn6
		x.yn7 = form.yn7.data if vis[16] else x.yn7
		x.num1 = form.num1.data if vis[17] else x.num1
		x.num2 = form.num2.data if vis[18] else x.num2
		x.num3 = form.num3.data if vis[19] else x.num3
		x.num4 = form.num4.data if vis[20] else x.num4
		x.num5 = form.num5.data if vis[21] else x.num5
		x.num6 = form.num6.data if vis[22] else x.num6
		x.num7 = form.num7.data if vis[23] else x.num7
		if form.notes.data == 'Today\'s notes...':
			x.notes = None
		else:
			x.notes = form.notes.data if vis[24] else x.notes
		db.session.commit()
		flash('Data updated', 'success')
		return redirect(url_for('data.visualize'))
	elif request.method == 'GET':
		form.lmh1.data = datum.lmh1
		form.lmh2.data = datum.lmh2
		form.lmh3.data = datum.lmh3
		form.lmh4.data = datum.lmh4
		form.lmh5.data = datum.lmh5
		form.abogg1.data = datum.abogg1
		form.abogg2.data = datum.abogg2
		form.abogg3.data = datum.abogg3
		form.abogg4.data = datum.abogg4
		form.abogg5.data = datum.abogg5
		form.yn1.data = datum.yn1
		form.yn2.data = datum.yn2
		form.yn3.data = datum.yn3
		form.yn4.data = datum.yn4
		form.yn5.data = datum.yn5
		form.yn6.data = datum.yn6
		form.yn7.data = datum.yn7
		form.num1.data = datum.num1
		form.num2.data = datum.num2
		form.num3.data = datum.num3
		form.num4.data = datum.num4
		form.num5.data = datum.num5
		form.num6.data = datum.num6
		form.num7.data = datum.num7
		if datum.notes == 'Today\'s notes...':
			form.notes.data = 'Today\'s notes...'
		else:
			form.notes.data = datum.notes
	date = datum.date_recorded.strftime("%m/%d/%Y")
	return render_template('dataTemplates/updateData.html', title='Update Data', datum=datum, form=form,
		date=date, vis=visIndicators(current_user), names=allNames(current_user), legend='Update Data')



@data.route('/data/<int:data_id>')
@login_required
def datum(data_id):
	datum = DailyData.query.get_or_404(data_id)
	return render_template('dataTemplates/datum.html', datum=datum, vis=visIndicators(current_user),
		names=allNames(current_user), legend='Datum')



@data.route('/data/notes')
@login_required
def notes():
	page = request.args.get('page', 1, type=int)
	dataNum = DailyData.query.filter_by(user_id=current_user.id).count()
	return render_template('dataTemplates/notes.html', title='notes', page=page, dataNum=dataNum, legend='Notes')



@data.route('/data/<int:deleteData_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_data(deleteData_id):
	if(DEBUG):
		print('|delete_data|')
	datum = DailyData.query.get_or_404(deleteData_id)
	if datum.backrefDD != current_user:
		abort(403)
	db.session.delete(datum)
	db.session.commit()
	flash(f'deletion successful', 'success')
	return redirect(url_for('data.visualize'))
