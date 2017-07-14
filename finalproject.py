from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    return "Lists all restaurants"

@app.route('/restaurants/new/')
def newRestaurants():
    return "Create a restaurant"

@app.route('/restaurants/<int:restaurant_id>/edit/')
def editRestaurants(restaurant_id):
    return "Edit restaurant"

@app.route('/restaurants/<int:restaurant_id>/delete/')
def deleteRestaurants(restaurant_id):
    return "Delete restaurant"

@app.route('/restaurants/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    return "Lists restaurant's menu"

@app.route('/restaurants/<int:restaurant_id>/menu/new/')
def newMenuItem(restaurant_id):
    return "Create a menu item"

@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/edit/')
def editMenuItem(restaurant_id, item_id):
    return "Edit menu item"

@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/delete/')
def deleteMenuItem(restaurant_id, item_id):
    return "Delete menu item: %s" % item_id



if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
