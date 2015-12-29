from sqlalchemy import Column, ForeignKey, Integer, String, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()



#end of beginning

#table for taking student information

class User(Base):
	__tablename__ = 'user'

	name =Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True) 
	email =Column(String(80), nullable = False)
	grade=Column(Integer(2))
	teacher=Column(String(80))


class ServiceType(Base):
	__tablename__ = 'type'

	name =Column(String(80), nullable = False)
	id =Column(Integer, primary_key = True) 
	description =Column(String, nullable = False)

class Event(Base):
	__tablename__ = 'event'

	name =Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True) 
	date = Column(Date)
	time =Column(Time)
	address = Column(String(80))
	description =Column(String)
	type_id = Column(Integer, ForeignKey('type.id'))
	type = relationship(ServiceType)








#for the end



engine = create_engine('sqlite:///serviceevents.db')
 

Base.metadata.create_all(engine)