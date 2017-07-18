from flask import Flask, render_template, redirect, url_for, request
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
    restaurants = session.query(Restaurant).all()

    return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurants/new/', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name = request.form['name'])
        session.add(newRestaurant)
        session.commit()

        return redirect(url_for('showRestaurants'))

    else:
        return render_template("new_restaurant.html")

@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = resquest.form['name']

        session.add(editedRestaurant)
        session.commit()

        return redirect(url_for('showRestaurants'))

    else:
        return render_template("edit_restaurant.html", restaurant_id = restaurant_id, restaurant = editedRestaurant)

@app.route('/restaurants/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    deletedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(deletedRestaurant)
        session.commit()

        return redirect(url_for('showRestaurants'))

    else:
        return render_template("delete_restaurant.html", restaurant_id = restaurant_id, restaurant = deletedRestaurant)

@app.route('/restaurants/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)

    return render_template("menu.html", restaurant_id = restaurant_id, restaurant = restaurant, items = items)

@app.route('/restaurants/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'],
                        description = request.form['description'],
                        price = request.form['price'],
                        restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()

        return redirect(url_for('showMenu', restaurant_id = restaurant_id))

    else:
        return render_template("new_menu_item.html", restaurant_id = restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, item_id):
    editedItem = session.query(MenuItem).filter_by(id = item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']

        if request.form['description']:
            editedItem.description = request.form['description']

        if request.form['price']:
            editedItem.price = request.form['price']

        session.add(editedItem)
        session.commit()

        return redirect(url_for("showMenu", restaurant_id = restaurant_id))

    else:
        return render_template("edit_menu_item.html", restaurant_id = restaurant_id, item_id = item_id, item = editedItem)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, item_id):
    deletedItem = session.query(MenuItem).filter_by(id = item_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()

        return redirect(url_for('showMenu', restaurant_id = restaurant_id))

    else:
        return render_template("delete_menu_item.html", restaurant_id = restaurant_id, item_id = item_id, item = deletedItem)


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
