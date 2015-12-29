from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
app = Flask(__name__)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants')
def showRestaurants():
	restaurants =  session.query(Restaurant).all()
	return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET','POST'])
def editRestaurant(restaurant_id):
	rest = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		if request.form['name']:
			rest.name = request.form['name']
			session.add(rest)
			session.commit()
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('editrestaurant.html', rest=rest, restaurant_id =restaurant_id)
@app.route('/restaurants/<int:restaurant_id>/delete', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
	rest = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		session.delete(rest)
		session.commit()
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('deleterestaurant.html', rest=rest, restaurant_id =restaurant_id) 


@app.route('/restaurants/new', methods=['GET','POST'])
def newRestaurant():
	if request.method == 'POST':
		newrest = Restaurant(name=request.form['name'])
		session.add(newrest)
		session.commit()
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('newrestaurant.html')

@app.route('/restaurants/<int:restaurant_id>')
@app.route('/restaurants/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id= restaurant_id).all()
	return render_template('menu.html', items=items, restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/menu/new', methods=['GET','POST'])
def newMenu(restaurant_id):
	if request.method =='POST':
		newitem = MenuItem(name=request.form['name'], restaurant_id=restaurant_id, 
			description=request.form['description'], price=request.form['price'], course=request.form['course'])
		session.add(newitem)
		session.commit()
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('newmenuitem.html', restaurant_id=restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET','POST'])
def editMenu(restaurant_id, menu_id):
	edititem= session.query(MenuItem).filter_by(id=menu_id).one()

	if request.method == 'POST':
		if request.form['name']:
			edititem.name=request.form['name']
		if request.form['description']:
			edititem.description=request.form['description']
		if request.form['price']:
			edititem.price=request.form['price']
		if request.form['course']:
			edititem.course=request.form['course']
		session.add(edititem)
		session.commit()
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, i=edititem)




@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET','POST'])
def deleteMenu(restaurant_id, menu_id):
	deletedItem = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		session.delete(deletedItem)
		session.commit()
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template(
			'deletemenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=deletedItem)

@app.route('/restaurants/JSON')
def restaurantsJSON():
	restaurants= session.query(Restaurant).all()
	return jsonify(MenuItems=[i.serialize for i in restaurants])

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def menusJSON(restaurant_id):
	items= session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
	return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menusitemJSON(restaurant_id, menu_id):
	item= session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).one()
	return jsonify(MenuItems=[item.serialize])









if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)