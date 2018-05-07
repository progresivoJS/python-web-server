from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# CREATE
myFirstRestaurant = Restaurant(name = "Pizza Palace")
cheesepizza = MenuItem(name = "Cheese Pizza", description = "Made with all natural ingredients and fresh mozzarella", course = "Entree", price = "$8.99", restaurant = myFirstRestaurant)
session.add(myFirstRestaurant)
session.add(cheesepizza)

session.commit()
print(session.query(Restaurant).all())
print(session.query(MenuItem).all())