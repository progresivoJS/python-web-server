from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def read_all_restaurants():
    items = session.query(Restaurant).all()
    return items

def read_restaurant_by_id(target_id):
    restaurant = session.query(Restaurant).filter_by(id = target_id).one()
    return restaurant

def edit_restaurant(id, new_name):
    restaurant = read_restaurant_by_id(id)
    restaurant.name = new_name
    session.add(restaurant)
    session.commit()
    return

def delete_restaurant(id):
    restaurant = read_restaurant_by_id(id)
    session.delete(restaurant)
    session.commit()
    return

def add_new_restaurant(restaurant_name):
    new_restaurant = Restaurant(name = restaurant_name)
    session.add(new_restaurant)
    session.commit()
    return