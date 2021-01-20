from flask import render_template, url_for, flash, redirect, request, Blueprint
from datatracker import db, bcrypt
from datatracker.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, TrackingPointForm, updatePointNameForm, GraphForm, UpdateGraphForm
from datatracker.models import User, DataPoint, DailyData, Graph
from flask_login import login_user, current_user, logout_user, login_required
from datatracker.utils import visiblePoints, send_reset_email, getDailyData, findNextOpenData, noteStatus, allNames, visIndicators, findGraphs, findNextOpenGraph

users = Blueprint('users', __name__)
DEBUG = False


# @users.route('/')
@users.route('/login', methods=['GET', 'POST'])
def login ():
	if current_user.is_authenticated:
		return redirect(url_for('data.visualize'))
	form=LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('data.visualize'))
		else:	
			flash('Login unsuccessful, please check email and password', 'danger')
	return render_template('login.html', title='Log In', form=form, legend='Log In')



@users.route('/register', methods=['GET', 'POST'])
def register():
	if(DEBUG):
		print('|register|')
	if current_user.is_authenticated:
		return redirect(url_for('data.visualize'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)

		for i in range(25):
			if i < 5:
				newPt = DataPoint(index=i, visible=False, dataType='lmh', name='N/A', backrefDP=user)
			elif i < 10:
				newPt = DataPoint(index=i, visible=False, dataType='abogg', name='N/A', backrefDP=user)
			elif i < 17:
				newPt = DataPoint(index=i, visible=False, dataType='yn', name='N/A', backrefDP=user)
			elif i < 24:
				newPt = DataPoint(index=i, visible=False, dataType='num', name='N/A', backrefDP=user)
			else:
				newPt = DataPoint(index=i, visible=False, dataType='notes', name='notes', backrefDP=user)
			db.session.add(newPt)

		for i in range(10):
			newGr = Graph(index=i, visible=False, name='N/A', date_recorded=False, dateColor=None,
				lmh1=False, cl1=None, lmh2=False, cl2=None, lmh3=False, cl3=None, lmh4=False, cl4=None,
					lmh5=False, cl5=None,
				abogg1=False, ca1=None, abogg2=False, ca2=None, abogg3=False, ca3=None, abogg4=False, ca4=None,
					abogg5=False, ca5=None,
				yn1=False, cy1=None, yn2=False, cy2=None, yn3=False, cy3=None, yn4=False, cy4=None, yn5=False,
					cy5=None, yn6=False, cy6=None, yn7=False, cy7=None,
				num1=False, cn1=None, num2=False, cn2=None, num3=False, cn3=None, num4=False, cn4=None,
					num5=False, cn5=None, num6=False, cn6=None, num7=False, cn7=None,
				backrefGraph=user)
			db.session.add(newGr)

		db.session.commit()

		flash(f'Your account has been created! You can now log in.', 'success')
		return redirect(url_for('users.login'))
	return render_template('register.html', title='register', form=form, legend='Register')



@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('users.login'))



@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated', 'success')
		return redirect(url_for('users.account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	return render_template('userTemplates/account.html', title="Account", form=form, legend='Account')



@users.route('/addTrackingPoint', methods=['GET', 'POST'])
@login_required
def addTrackingPoint():
	form = TrackingPointForm()
	if form.validate_on_submit():
		dataIndex = findNextOpenData(current_user, form.dataType.data)
		userPoints = User.query.get(current_user.id).user_points
		for x in userPoints:
			if x.index == dataIndex:
				x.visible = True
				x.name = form.name.data
				db.session.commit()
				break
		flash('Data created', 'success')
		return redirect(url_for('data.inputData'))
	return render_template('userTemplates/addTrackingPoint.html', title='addTrackingPoint', form=form, legend='Add Tracking Point')



@users.route('/point/<int:point_id>', methods=['GET', 'POST'])
@login_required
def point(point_id):
	trackPoint = DataPoint.query.get_or_404(point_id)
	return render_template('userTemplates/point.html', trackPoint=trackPoint)



@users.route('/graph/<int:graph_id>', methods=['GET', 'POST'])
@login_required
def graph(graph_id):
	graphItem = Graph.query.get_or_404(graph_id)
	return render_template('userTemplates/graph.html', graphItem=graphItem, vis=visIndicators(current_user),
		names=allNames(current_user), legend='Graph')



@users.route('/createGraph', methods=['GET', 'POST'])
@login_required
def createGraph():
	form = GraphForm()
	if form.validate_on_submit():
		graphIndex = findNextOpenGraph(current_user)
		userGraphs = User.query.get(current_user.id).user_graphs
		for x in userGraphs:

			if x.index == graphIndex:

				x.visible = True
				x.name = form.name.data

				x.lmh1 = form.lmh1.data
				x.cl1 = form.cl1.data
				x.lmh2 = form.lmh2.data
				x.cl2 = form.cl2.data
				x.lmh3 = form.lmh3.data
				x.cl3 = form.cl3.data
				x.lmh4 = form.lmh4.data
				x.cl4 = form.cl4.data
				x.lmh5 = form.lmh5.data
				x.cl5 = form.cl5.data

				x.abogg1 = form.abogg1.data
				x.ca1 = form.ca1.data
				x.abogg2 = form.abogg2.data
				x.ca2 = form.ca2.data
				x.abogg3 = form.abogg3.data
				x.ca3 = form.ca3.data
				x.abogg4 = form.abogg4.data
				x.ca4 = form.ca4.data
				x.abogg5 = form.abogg5.data
				x.ca5 = form.ca5.data

				x.yn1 = form.yn1.data
				x.cy1 = form.cy1.data
				x.yn2 = form.yn2.data
				x.cy2 = form.cy2.data
				x.yn3 = form.yn3.data
				x.cy3 = form.cy3.data
				x.yn4 = form.yn4.data
				x.cy4 = form.cy4.data
				x.yn5 = form.yn5.data
				x.cy5 = form.cy5.data
				x.yn6 = form.yn6.data
				x.cy6 = form.cy6.data
				x.yn7 = form.yn7.data
				x.cy7 = form.cy7.data

				x.num1 = form.num1.data
				x.cn1 = form.cn1.data
				x.num2 = form.num2.data
				x.cn2 = form.cn2.data
				x.num3 = form.num3.data
				x.cn3 = form.cn3.data
				x.num4 = form.num4.data
				x.cn4 = form.cn4.data
				x.num5 = form.num5.data
				x.cn5 = form.cn5.data
				x.num6 = form.num6.data
				x.cn6 = form.cn6.data
				x.num7 = form.num7.data
				x.cn7 = form.cn7.data

			db.session.commit()

		flash('Graph Created!', 'success')
		return redirect(url_for('data.visualize'))

	return render_template('userTemplates/createGraph.html', title='ceateGraph', form=form,
		vis=visIndicators(current_user), names=allNames(current_user), legend='Create Graph')



@users.route('/point/addNotes', methods=['GET', 'POST'])
@login_required
def switchNotes():
	noteIndicator = noteStatus(current_user)
	userPoints = User.query.get(current_user.id).user_points
	for x in reversed(userPoints):
		if x.name == 'notes':
			x.visible = not noteIndicator
			db.session.commit()
			break
	return redirect(url_for('data.inputData'))



@users.route('/deleteGraph/<int:graph_id>', methods=['GET', 'POST'])
@login_required
def deleteGraph(graph_id):
	theGraph = Graph.query.get_or_404(graph_id)
	if theGraph.backrefGraph != current_user:
		abort(403)
	theGraph.visible = False
	#FINISH ME
	#Set all its fields to False/None
	db.session.commit()
	flash('Graph Deleted', "success")
	return redirect(url_for('data.visualize'))



@users.route('/deleteTrackingPoint/<int:point_id>', methods=['GET', 'POST'])
@login_required
def deleteTrackingPoint(point_id):
	trackPoint = DataPoint.query.get(point_id)
	theName = trackPoint.name
	#Iterate DailyData, set that spot to NULL for each row in table
	names = allNames(current_user)
	dailyData = User.query.get(current_user.id).user_data
	for x in dailyData:
		if names[0] == theName:
			x.lmh1 = None
		elif names[1] == theName:
			x.lmh2 = None
		elif names[2] == theName:
			x.lmh3 = None
		elif names[3] == theName:
			x.lmh4 = None
		elif names[4] == theName:
			x.lmh5 = None
		elif names[5] == theName:
			x.abogg1 = None
		elif names[6] == theName:
			x.abogg2 = None
		elif names[7] == theName:
			x.abogg3 = None
		elif names[8] == theName:
			x.abogg4 = None
		elif names[9] == theName:
			x.abogg5 = None
		elif names[10] == theName:
			x.yn1 = None
		elif names[11] == theName:
			x.yn2 = None
		elif names[12] == theName:
			x.yn3 = None
		elif names[13] == theName:
			x.yn4 = None
		elif names[14] == theName:
			x.yn5 = None
		elif names[15] == theName:
			x.yn6 = None
		elif names[16] == theName:
			x.yn7 = None
		elif names[17] == theName:
			x.num1 = None
		elif names[18] == theName:
			x.num2 = None
		elif names[19] == theName:
			x.num3 = None
		elif names[20] == theName:
			x.num4 = None
		elif names[21] == theName:
			x.num5 = None
		elif names[22] == theName:
			x.num6 = None
		elif names[23] == theName:
			x.num7 = None
	trackPoint.name = 'N/A'
	trackPoint.visible = False
	db.session.commit()
	flash('Tracking point deleted', 'success')
	return redirect(url_for('data.visualize'))



@users.route('/updateGraph/<int:graph_id>', methods=['GET', 'POST'])
@login_required
def updateGraph(graph_id):
	graphItem = Graph.query.get(graph_id)
	oldName = graphItem.name
	if graphItem.backrefGraph != current_user:
		abort(403)
	form = UpdateGraphForm()
	if form.validate_on_submit():

		#FIXME Find a way to do this in users/forms.py 
		graphNames = findGraphs(current_user)
		for x in graphNames:
			if x == form.name.data and oldName != form.name.data:
				flash(u'You already have a graph with that name, plase choose a different one', 'danger')
				return render_template('userTemplates/createGraph.html', title='Update Graph', form=form, vis=visIndicators(current_user),
				names=allNames(current_user), legend='Update Graph')

		graphItem.name = form.name.data

		graphItem.lmh1 = form.lmh1.data
		graphItem.cl1 = form.cl1.data
		graphItem.lmh2 = form.lmh2.data
		graphItem.cl2 = form.cl2.data
		graphItem.lmh3 = form.lmh3.data
		graphItem.cl3 = form.cl3.data
		graphItem.lmh4 = form.lmh4.data
		graphItem.cl4 = form.cl4.data
		graphItem.lmh5 = form.lmh5.data
		graphItem.cl5 = form.cl5.data

		graphItem.abogg1 = form.abogg1.data
		graphItem.ca1 = form.ca1.data
		graphItem.abogg2 = form.abogg2.data
		graphItem.ca2 = form.ca2.data
		graphItem.abogg3 = form.abogg3.data
		graphItem.ca3 = form.ca3.data
		graphItem.abogg4 = form.abogg4.data
		graphItem.ca4 = form.ca4.data
		graphItem.abogg5 = form.abogg5.data
		graphItem.ca5 = form.ca5.data

		graphItem.yn1 = form.yn1.data
		graphItem.cy1 = form.cy1.data
		graphItem.yn2 = form.yn2.data
		graphItem.cy2 = form.cy2.data
		graphItem.yn3 = form.yn3.data
		graphItem.cy3 = form.cy3.data
		graphItem.yn4 = form.yn4.data
		graphItem.cy4 = form.cy4.data
		graphItem.yn5 = form.yn5.data
		graphItem.cy5 = form.cy5.data
		graphItem.yn6 = form.yn6.data
		graphItem.cy6 = form.cy6.data
		graphItem.yn7 = form.yn7.data
		graphItem.cy7 = form.cy7.data

		graphItem.num1 = form.num1.data
		graphItem.cn1 = form.cn1.data
		graphItem.num2 = form.num2.data
		graphItem.cn2 = form.cn2.data
		graphItem.num3 = form.num3.data
		graphItem.cn3 = form.cn3.data
		graphItem.num4 = form.num4.data
		graphItem.cn4 = form.cn4.data
		graphItem.num5 = form.num5.data
		graphItem.cn5 = form.cn5.data
		graphItem.num6 = form.num6.data
		graphItem.cn6 = form.cn6.data
		graphItem.num7 = form.num7.data
		graphItem.cn7 = form.cn7.data

		db.session.commit()
		flash('Graph Updated!', 'success')
		return redirect(url_for('data.visualize'))

	elif request.method == 'GET':
		form.name.data = graphItem.name

		form.lmh1.data = graphItem.lmh1
		form.cl1.data = graphItem.cl1
		form.lmh2.data = graphItem.lmh2
		form.cl2.data = graphItem.cl2
		form.lmh3.data = graphItem.lmh3
		form.cl3.data = graphItem.cl3
		form.lmh4.data = graphItem.lmh4
		form.cl4.data = graphItem.cl4
		form.lmh5.data = graphItem.lmh5
		form.cl5.data = graphItem.cl5

		form.abogg1.data = graphItem.abogg1
		form.ca1.data = graphItem.ca1
		form.abogg2.data = graphItem.abogg2
		form.ca2.data = graphItem.ca2
		form.abogg3.data = graphItem.abogg3
		form.ca3.data = graphItem.ca3
		form.abogg4.data = graphItem.abogg4
		form.ca4.data = graphItem.ca4
		form.abogg5.data = graphItem.abogg5
		form.ca5.data = graphItem.ca5

		form.yn1.data = graphItem.yn1
		form.cy1.data = graphItem.cy1
		form.yn2.data = graphItem.yn2
		form.cy2.data = graphItem.cy2
		form.yn3.data = graphItem.yn3
		form.cy3.data = graphItem.cy3
		form.yn4.data = graphItem.yn4
		form.cy4.data = graphItem.cy4
		form.yn5.data = graphItem.yn5
		form.cy5.data = graphItem.cy5
		form.yn6.data = graphItem.yn6
		form.cy6.data = graphItem.cy6
		form.yn7.data = graphItem.yn7
		form.cy7.data = graphItem.cy7

		form.num1.data = graphItem.num1
		form.cn1.data = graphItem.cn1
		form.num2.data = graphItem.num2
		form.cn2.data = graphItem.cn2
		form.num3.data = graphItem.num3
		form.cn3.data = graphItem.cn3
		form.num4.data = graphItem.num4
		form.cn4.data = graphItem.cn4
		form.num5.data = graphItem.num5
		form.cn5.data = graphItem.cn5
		form.num6.data = graphItem.num6
		form.cn6.data = graphItem.cn6
		form.num7.data = graphItem.num7
		form.cn7.data = graphItem.cn7

	return render_template('userTemplates/createGraph.html', title='Update Graph', form=form, vis=visIndicators(current_user),
		names=allNames(current_user), legend='Update Graph')



@users.route('/changePointName/<int:point_id>', methods=['GET', 'POST'])
@login_required
def changeName(point_id):
	form = updatePointNameForm()
	point = DataPoint.query.get(point_id)
	if form.validate_on_submit():
		point.name = form.name.data
		db.session.commit()
		flash('Tracking point name updated', 'success')
		return redirect(url_for('data.visualize'))
	elif request.method == 'GET':
		form.name.data = point.name
	return render_template('userTemplates/updatePointName.html', title='updatePointName', form=form, legend='Change Name')



@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
	# if current_user.is_authenticated:
	# 	return redirect(url_for('users.account'))
	form = RequestResetForm()
	logout_user()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent with instructions to reset your password. Please check your spam folder if you do not see this email within a few minutes.', 'info')
		return redirect(url_for('users.login'))
	return render_template('userTemplates/reset_request.html', title='reset password', form=form, legend="Reset Password")



@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('users.account'))
	user = User.verify_reset_token(token)
	if not user:
		flash('That token is invalid or has expired', 'warning')
		return redirect(url_for('users.reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash(f'Your password has been updated.', 'success')
		return redirect(url_for('users.login'))
	return render_template('userTemplates/reset_token.html', title='reset password', form=form, legend='Reset Token')



@users.route('/user/<int:deleteUser_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_user(deleteUser_id):
	user = User.query.get_or_404(deleteUser_id)
	if user != current_user:
		abort(403)
	dailyData = user.user_data
	dataPoints = user.user_points
	graphs = user.user_graphs
	for x in dailyData:
		db.session.delete(x)
	for x in dataPoints:
		db.session.delete(x)
	for x in graphs:
		db.session.delete(x)
	db.session.commit() #Remove after this is solved

	db.session.delete(user)
	db.session.commit()
	flash(f'account deleted', 'success')
	return redirect(url_for('users.login'))

