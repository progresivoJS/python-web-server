# Configuration
import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# class
class Restaurant(Base):
    # table
    __tablename__ = 'restaurant'
    
    # mapping
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
class MenuItem(Base):
    # table
    __tablename__ = 'menu_item'

    # mapping
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

# Configuration
## insert at the end of file ##
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)