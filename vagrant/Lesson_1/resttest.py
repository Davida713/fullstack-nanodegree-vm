from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#testing saving new thing to DB
'''
newrest = Restaurant(name = 'test1')
session.add(newrest)
session.commit()
'''

#testing spending an array from query
'''
restaurants = session.query(Restaurant).all()
rids = []
for restaurant in restaurants:
	rids.append(restaurant.id)
print rids[0]
'''

#testing what is in the db
'''
restaurants = session.query(Restaurant).all()
for restaurant in restaurants:
	print restaurant.name
'''
#testing editing the DB- this works
'''
onerest = session.query(Restaurant).filter_by(name="Urban Burger").one()
onerest.name = "Urbane Burger!"
session.add(onerest)
session.commit()
'''
