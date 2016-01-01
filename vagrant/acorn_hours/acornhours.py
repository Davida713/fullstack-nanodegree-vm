from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from databasesetup import Base, User, ServiceType, Event
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from datetime import date, datetime, time





app = Flask(__name__)

CLIENT_ID = json.loads(
	open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Acorn Hours"


# Connect to Database and create database session
engine = create_engine('sqlite:///serviceevents.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/ServiceTypes/')
def showTypes():
	types = session.query(ServiceType).all()
	if 'username' not in login_session:
		return render_template('servicetypes.html', types=types)
	else:
		return render_template('servicetypes.html', types=types, username= login_session['username'], user_id=login_session['user_id'])

@app.route('/ServiceTypes/new/', methods=['GET', 'POST'])
def newType():
	if 'username' not in login_session:
			flash("You need to be logged on to create a type of service.")
			return redirect(url_for('showTypes'))
	if request.method == 'POST':
		addtype= ServiceType(name=request.form['name'], description=request.form['description'], owner= login_session['user_id'])
		session.add(addtype)
		session.commit()
		flash("New service type has been added")
		return redirect(url_for('showTypes'))
	else:
		return render_template('newtype.html',username= login_session['username'])

@app.route('/ServiceTypes/<int:servicetype_id>/delete/', methods=['GET', 'POST'])
def deleteType(servicetype_id):
	dtype = session.query(ServiceType).filter_by(id=servicetype_id).one()
	if 'username' not in login_session or dtype.owner != login_session['user_id']:
			flash("You need to be logged on to delete a type of service.")
			return redirect(url_for('showTypes'))
	else:
		if request.method == 'POST':
			session.delete(dtype)
			session.commit()
			flash("Item has been deleted")
			return redirect(url_for('showTypes'))
		else:
			return render_template('deletetype.html', dtype=dtype, username= login_session['username'])

@app.route('/ServiceTypes/<int:servicetype_id>/edit/', methods=['GET', 'POST'])
def editType(servicetype_id):
	etype = session.query(ServiceType).filter_by(id=servicetype_id).one()
	if 'username' not in login_session or etype.owner != login_session['user_id']:

		flash("You need to be logged on to delete a type of service.")
		return redirect(url_for('showTypes'))
	else:
		if request.method == 'POST':
			if request.form['name']:
				etype.name = request.form['name']
			if request.form['description']:
				etype.description = request.form['description']
			session.add(etype)
			session.commit()
			flash("You have edited %s" % etype.name)
			return redirect(url_for('showTypes'))
		else:
			return render_template('edittype.html', etype=etype, username= login_session['username'])

@app.route('/ServiceTypes/<int:servicetype_id>/new', methods=['GET', 'POST'])
def newEvent(servicetype_id):
	if 'username' not in login_session:
		flash("You need to be logged on to create an event.")
		return redirect(url_for('showEvents', servicetype_id=servicetype_id))
	else:
		type = session.query(ServiceType).filter_by(id=servicetype_id).one()
		if request.method == 'POST':
			
			edate= request.form['edate']
			fixdate=datetime.strptime(edate, "%Y-%m-%d").date()
			etime=request.form['etime']
			fixtime=datetime.strptime(etime, "%H:%M").time()
			aevent= Event(name=request.form['name'], date=fixdate, time=fixtime, description=request.form['description'], address=request.form['address'], type_id=type.id, owner= login_session['user_id'])
			session.add(aevent)
			session.commit()
			flash("You have added %s" % aevent.name)
			return redirect(url_for('showEvents', servicetype_id=servicetype_id))
		else:
			return render_template('newevent.html', type=type, username= login_session['username'])

@app.route('/ServiceTypes/<int:servicetype_id>/events/<int:event_id>/delete/', methods=['GET', 'POST'])
def deleteEvent(servicetype_id, event_id):
	dtype = session.query(ServiceType).filter_by(id=servicetype_id).one()
	devent= session.query(Event).filter_by(id=event_id).one()
	if 'username' not in login_session or devent.owner != login_session['user_id']:
		flash("You must be logged in as owner to delete an event.")
		return redirect(url_for('showEvents', servicetype_id=servicetype_id))
	else:
		if request.method == 'POST':
			session.delete(devent)
			session.commit()
			flash("You have deleted %s" % devent.name)
			return redirect(url_for('showEvents', servicetype_id=servicetype_id))
		else:
			return render_template('deleteevent.html', devent=devent, dtype= dtype, username= login_session['username'])

@app.route('/ServiceTypes/<int:servicetype_id>/events/<int:event_id>/edit/', methods=['GET', 'POST'])
def editEvent(servicetype_id, event_id):
	etype = session.query(ServiceType).filter_by(id=servicetype_id).one()
	eevent= session.query(Event).filter_by(id=event_id).one()
	if 'username' not in login_session or eevent.owner != login_session['user_id']:
		flash("You must be logged in as owner to edit an event.")
		return redirect(url_for('showEvents', servicetype_id=servicetype_id))
	else:
		if request.method == 'POST':
			etime=request.form['etime']
			if request.form['name']:
				eevent.name = request.form['name']
			if request.form['description']:
				eevent.description = request.form['description']
			if request.form['address']:
				eevent.address = request.form['address']
			if request.form['edate']:
				edate= request.form['edate']
				fixdate=datetime.strptime(edate, "%Y-%m-%d").date()
				eevent.date = fixdate
			if request.form['etime']:
				etime= request.form['etime']
				fixtime=datetime.strptime(etime, "%H:%M").time()
				eevent.time = fixtime

			session.add(eevent)
			session.commit()
			flash("You have edited %s" % eevent.name)
			return redirect(url_for('showEvents', servicetype_id=servicetype_id))
		else:
			return render_template('editevent.html', etype=etype, eevent=eevent, username= login_session['username'])


@app.route('/ServiceTypes/<int:servicetype_id>/')
def showEvents(servicetype_id):
	type = session.query(ServiceType).filter_by(id=servicetype_id).one()
	events= session.query(Event).filter_by(type_id=servicetype_id).all()
	if 'username' not in login_session:
		return render_template('events.html', type=type, events=events)
	else:
		return render_template('events.html', type=type, events=events, username= login_session['username'], user_id=login_session['user_id'])

@app.route('/ServiceTypes/<int:servicetype_id>/events/<int:event_id>/')
def singleEvent(servicetype_id, event_id ):
	type = session.query(ServiceType).filter_by(id=servicetype_id).one()
	event= session.query(Event).filter_by(id=event_id).one()
	if 'username' not in login_session:
		return render_template('singleevent.html', type=type, event=event)
	else:
		return render_template('singleevent.html', type=type, event=event, username= login_session['username'])


@app.route('/login')
def showLogin():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits)
					for x in xrange(32))
	login_session['state'] = state
	# return "The current session state is %s" % login_session['state']
	if 'username' not in login_session:
		return render_template('login.html', STATE=state)
	else:
		return render_template('login.html', STATE=state, username= login_session['username'])


@app.route('/gconnect', methods=['POST'])
def gconnect():
	# Validate state token
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	# Obtain authorization code
	code = request.data

	try:
		# Upgrade the authorization code into a credentials object
		oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)
	except FlowExchangeError:
		response = make_response(
			json.dumps('Failed to upgrade the authorization code.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Check that the access token is valid.
	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
		   % access_token)
	h = httplib2.Http()
	result = json.loads(h.request(url, 'GET')[1])
	# If there was an error in the access token info, abort.
	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')), 500)
		response.headers['Content-Type'] = 'application/json'

	# Verify that the access token is used for the intended user.
	gplus_id = credentials.id_token['sub']
	if result['user_id'] != gplus_id:
		response = make_response(
			json.dumps("Token's user ID doesn't match given user ID."), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Verify that the access token is valid for this app.
	if result['issued_to'] != CLIENT_ID:
		response = make_response(
			json.dumps("Token's client ID does not match app's."), 401)
		print "Token's client ID does not match app's."
		response.headers['Content-Type'] = 'application/json'
		return response

	stored_credentials = login_session.get('credentials')
	stored_access_token = login_session.get('access_token')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_credentials is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps('Current user is already connected.'),200)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Store the access token in the session for later use.
	login_session['gplus_id'] = gplus_id
	login_session['credentials'] = credentials

	# Get user info
	userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
	params = {'access_token': credentials.access_token, 'alt': 'json'}
	answer = requests.get(userinfo_url, params=params)

	data = answer.json()

	login_session['username'] = data['name']
	login_session['email'] = data['email']

	login_session['provider'] = 'google'
	
	# see if user exists, if it doesn't make a new one
	
	user_id = getUserID(login_session['email']) 
	if not user_id:
		user_id = createUser(login_session)
	login_session['user_id'] = user_id


	output = ''
	output += '<h1>Welcome, '
	output += login_session['username']
	output += '!</h1>'
	flash("You are now logged in as %s!" % login_session['username'])
	print "done!"
	return output
	return redirect(url_for('showTypes'))

@app.route('/gdisconnect')
def gdisconnect():
	# Only disconnect a connected user.
	credentials = login_session.get('credentials')
	print credentials
	if credentials is None:
		response = make_response(
			json.dumps('Current user not connected.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	print "this is a access token from credentials"
	print credentials.access_token
	access_token = login_session["credentials"].access_token
	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]
	print "Right before if statement"
	if result['status'] == '200':
		login_session.pop('access_token', None)
		del login_session['gplus_id']
		del login_session['username']
		del login_session['email']
		response = make_response(json.dumps('Successfully disconnected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		flash("You are now logged out.")
		return redirect(url_for('showTypes'))
	else:
	
		response = make_response(json.dumps('Failed to revoke token for given user.', 400))
		response.headers['Content-Type'] = 'application/json'
		return response


def createUser(login_session):
	newUser = User(name=login_session['username'], email=login_session[
				   'email'])
	session.add(newUser)
	session.commit()
	user = session.query(User).filter_by(email=login_session['email']).one()
	return user.id


def getUserInfo(user_id):
	user = session.query(User).filter_by(id=user_id).one()
	return user


def getUserID(email):
	try:
		user = session.query(User).filter_by(email=email).one()
		return user.id
	except:
		return None

'''
@app.route('/clearSession')
def clearSession():
	login_session.clear()
	return "Session cleared"

'''

@app.route('/ServiceTypes/<int:servicetype_id>/events/<int:event_id>/JSON')
def singleEventJSON(servicetype_id, event_id):
	#type = session.query(ServiceType).filter_by(id=servicetype_id).one()
	event= session.query(Event).filter_by(id=event_id, type_id=servicetype_id).one()
	return jsonify(Event=event.serialize)


@app.route('/ServiceTypes/<int:servicetype_id>/events/JSON/')
def serviceEventsJSON(servicetype_id):
	events= session.query(Event).filter_by(type_id=servicetype_id).all()

	return jsonify(Events=[i.serialize for i in events])




@app.route('/ServiceTypes/JSON')
def serviceTypesJSON():
	types = session.query(ServiceType).all()
	return jsonify(types=[t.serialize for t in types])






if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)