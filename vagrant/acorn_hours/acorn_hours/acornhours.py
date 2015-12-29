from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from databasesetup import Base, User, ServiceType, Event
from flask import session as login_session
import random
import string
#from oauth2client.client import flow_from_clientsecrets
#from oauth2client.client import FlowExchangeError
#import httplib2
#import json
from flask import make_response
import requests
from datetime import date, datetime, time



app = Flask(__name__)

#CLIENT_ID = json.loads(
	#open('client_secrets.json', 'r').read())['web']['client_id']
#APPLICATION_NAME = "Acorn Hours"


# Connect to Database and create database session
engine = create_engine('sqlite:///serviceevents.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/ServiceTypes/')
def showTypes():
	types = session.query(ServiceType).all()
	return render_template('servicetypes.html', types=types)

@app.route('/ServiceTypes/new/', methods=['GET', 'POST'])
def newType():
	if request.method == 'POST':
		addtype= ServiceType(name=request.form['name'], description=request.form['description'])
		session.add(addtype)
		session.commit()
		return redirect(url_for('showTypes'))
	else:
		return render_template('newtype.html')

@app.route('/ServiceTypes/<int:servicetype_id>/delete/', methods=['GET', 'POST'])
def deleteType(servicetype_id):
	dtype = session.query(ServiceType).filter_by(id=servicetype_id).one()
	if request.method == 'POST':
		session.delete(dtype)
		session.commit()
		return redirect(url_for('showTypes'))
	else:
		return render_template('deletetype.html', dtype=dtype)

@app.route('/ServiceTypes/<int:servicetype_id>/edit/', methods=['GET', 'POST'])
def editType(servicetype_id):
	etype = session.query(ServiceType).filter_by(id=servicetype_id).one()
	if request.method == 'POST':
		if request.form['name']:
			etype.name = request.form['name']
		if request.form['description']:
			etype.description = request.form['description']
		session.add(etype)
		session.commit()
		return redirect(url_for('showTypes'))
	else:
		return render_template('edittype.html', etype=etype)

@app.route('/ServiceTypes/<int:servicetype_id>/new', methods=['GET', 'POST'])
def newEvent(servicetype_id):
	type = session.query(ServiceType).filter_by(id=servicetype_id).one()
	if request.method == 'POST':
		
		edate= request.form['edate']
		fixdate=datetime.strptime(edate, "%Y-%m-%d").date()
		etime=request.form['etime']
		fixtime=datetime.strptime(etime, "%H:%M").time()
		aevent= Event(name=request.form['name'], date=fixdate, time=fixtime, description=request.form['description'], address=request.form['address'], type_id=type.id)
		session.add(aevent)
		session.commit()
		return redirect(url_for('showEvents', servicetype_id=servicetype_id))
	else:
		return render_template('newevent.html', type=type)

@app.route('/ServiceTypes/<int:servicetype_id>/events/<int:event_id>/delete/', methods=['GET', 'POST'])
def deleteEvent(servicetype_id, event_id):
	dtype = session.query(ServiceType).filter_by(id=servicetype_id).one()
	devent= session.query(Event).filter_by(id=event_id).one()
	if request.method == 'POST':
		session.delete(devent)
		session.commit()
		return redirect(url_for('showEvents', servicetype_id=servicetype_id))
	else:
		return render_template('deleteevent.html', devent=devent, dtype= dtype)

@app.route('/ServiceTypes/<int:servicetype_id>/events/<int:event_id>/edit/', methods=['GET', 'POST'])
def editEvent(servicetype_id, event_id):
	etype = session.query(ServiceType).filter_by(id=servicetype_id).one()
	eevent= session.query(Event).filter_by(id=event_id).one()
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
		return redirect(url_for('showEvents', servicetype_id=servicetype_id))
	else:
		return render_template('editevent.html', etype=etype, eevent=eevent)


@app.route('/ServiceTypes/<int:servicetype_id>/')
def showEvents(servicetype_id):
	type = session.query(ServiceType).filter_by(id=servicetype_id).one()
	events= session.query(Event).filter_by(type_id=servicetype_id).all()
	return render_template('events.html', type=type, events=events)


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)