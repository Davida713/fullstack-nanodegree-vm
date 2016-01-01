from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from databasesetup import Base, User, ServiceType, Event
import datetime


'''
This file is to be used along side the acornhours.py file.
To use, don't mess with the functions. Just uncomment their execution at the bottom and run.
You can populate the DB with dummy data and also test what is outputting from the console.
'''


# Connect to Database and create database session
engine = create_engine('sqlite:///serviceevents.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



def deleteCats():
	allcats = session.query(ServiceType).all()
	for cat in allcats:
		session.delete(cat)
	session.commit()


def deleteEvents():
	allevents = session.query(Event).all()
	for event in allevents:
		session.delete(event)
		session.commit()


######use these two to delete tables#######



def addCats():
	cat1 = ServiceType(name="Education", description="Help kids in schools.")
	session.add(cat1)
	session.commit()


	cat2 = ServiceType(name="Health", description="Help people eat better.")
	session.add(cat2)
	session.commit()


	cat3 = ServiceType(name="Family", description="Help people be better family members.")
	session.add(cat3)
	session.commit()

	cat4 = ServiceType(name="Elder Care", description="Help old people.")
	session.add(cat4)
	session.commit()



def addEvent(name, date, time, address, description, type_id):
	newevent = Event(name= name, date= date, time=time, address=address, description=description, type_id=type_id)
	session.add(newevent)
	session.commit()

def addEvents():
	#education
	addEvent('Reading Tutor', datetime.date(2016,02,05), datetime.time(1,30,00),'123 main', 'Teach kids to read.', 1)
	addEvent('Teacher Aid', datetime.date(2016,01,15), datetime.time(14,30,00),'234 teach st.', 'Help teachers fix up their classes.', 1)
	addEvent('Student Volleyball tournament', datetime.date(2016,01,25), datetime.time(9,30,00),'Stadium Ave.', 'We need people to organize a student volleyball tournament.', 1)
	#health
	addEvent('Diabetees Screening', datetime.date(2016,02,06), datetime.time(7,30,00),'123 main st', 'We need volunteers to screen people for diabetes.', 2)
	addEvent('Hospital Shadowing', datetime.date(2016,02,19), datetime.time(7,30,00),'Hospital Road', 'Students interereted in a health career should shadown a doctor.', 2)
	#family
	addEvent('Home Visits', datetime.date(2016,01,25), datetime.time(7,30,00),'123 main st.', 'Go into the homes of of people and check on them.', 3)
	addEvent('Day Care', datetime.date(2016,02,01), datetime.time(16,30,00),'123 main st.', 'Watch kids while parents at work.', 3)
	#eldercare
	addEvent('Reading to the elderly', datetime.date(2016,01,05), datetime.time(12,30,00),'123 main st.', 'Read to the elderly to make them feel nice.', 4)

	addEvent('Grocery store help', datetime.date(2016,01,25), datetime.time(4,30,00),'123 main st.', 'Take grannies to the store to help them get food.', 4)


def printEvents():

	events = session.query(Event).all()
	for event in events:
		print event.name
		print event.date
		print event.time
		print event.address
		print event.description
		print event.type_id
		print event.id
		print "event owner"
		print event.owner
		print " "




def printCats():

	cats = session.query(ServiceType).all()
	for cat in cats:
		print cat.name
		print cat.id
		print "owner:"
		print cat.owner
		print " "


def printUsers():

	users = session.query(User).all()
	for user in users:
		print user.name
		print user.email
		print user.id


#printEvents()
#printCats()
#printUsers()
#printEvents()
deleteEvents()
deleteCats()
addCats()
addEvents()
