import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine 

Base = declarative_base()


class Shelter(Base):
	__tablename__ = 'shelter'

	name = Column(String, nullable=False)
	address = Column(String)
	city = Column(String(150))
	state = Column(String(150))
	zipCode = Column(Integer)
	website = Column(String)
	id = Column(Integer, primary_key=True)


class Puppy (Base):
	__tablename__ = "puppy"

	name = Column(String(80), nullable=False)
	dateOfBirth = Column(String(10))
	gender = Column(String(6))
	weight = Column(Integer)
	shelter_id = Column(Integer,ForeignKey('shelter.id'))
	shelter = relationship(Shelter)
	id = Column(Integer, primary_key=True)


engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.create_all(engine)