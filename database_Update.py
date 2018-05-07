from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# UrbanVeggieBurger = session.query(MenuItem).filter_by(id = 2).one()
# UrbanVeggieBurger.price = "$2.99"
# session.add(UrbanVeggieBurger)
# session.commit()

veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for veggieBurger in veggieBurgers:
    if veggieBurger.price != '$3.99':
        veggieBurger.price = '$3.99'
        session.add(veggieBurger)
        # session.commit() 여기에 넣어도 되겠지만,
session.commit() # 한방에 하는게 더 효율적.

for veggieBurger in veggieBurgers:
    print(veggieBurger.price)