from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# READ
# firstResult = session.query(Restaurant).first()
# print(firstResult.name)

items = session.query(MenuItem).all()
for item in items:
    print(item.name)