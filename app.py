import os
import uuid
from flask import Flask, session,render_template,request, Response, redirect, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from db import db_init, db
from models import  User, Product, Item
from datetime import datetime
from flask_session import Session
from helpers import login_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#static file path
@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

# Home route
@app.route("/")
def sign_in_page():
    return render_template('index.html')


@app.route("/logout")
def logout():
    return render_template('index.html')

# @app.route("/")
# def sign_in_page():
#     return render_template('sign_in.html')

@app.route("/home", methods=["GET", "POST"])
def sign_in_proses():
    if request.method == "POST":
        user_name = request.form.get("username")
        if user_name == 'factory':
            return render_template("factory.html")
        elif user_name == 'farmer':
            return render_template("farmer.html")
        elif user_name == 'user':
            return render_template("user_food.html")
        else:
            return render_template("404.html")

# User Menu
@app.route("/")
def index():
	bbrows = Item.query.filter_by(category='Bakery & Breakfast')
	idrows = Item.query.filter_by(category='Indonesian')
	ffrows = Item.query.filter_by(category='Fast Food')
	return render_template("user_food.html", bbrows=bbrows,idrows=idrows,ffrows=ffrows)


@app.route("/food",  methods=["GET", "POST"])
def food():
	bbrows = Item.query.filter_by(category='Bakery & Breakfast')
	idrows = Item.query.filter_by(category='Indonesian')
	ffrows = Item.query.filter_by(category='Fast Food')
	return render_template("user_food.html", bbrows=bbrows,idrows=idrows,ffrows=ffrows)

@app.route("/user_profile")
def user_profile():
    return render_template('input_user_profile.html')

@app.route("/food_vision")
def food_vision():
    return render_template('food_vision.html')
    
@app.route("/prediction")
def prediction():
    return render_template('prediction.html')

@app.route("/patient")
def patient():
    return render_template('patient.html')
    
@app.route("/hospital")
def hospital():
    return render_template('hospital.html')

@app.route("/factory")
def factory():
    return render_template('factory.html')

@app.route("/farmer")
def farmer():
    return render_template('farmer.html')
    
@app.route("/user_predict")
def user_predict():
    return render_template('input_user_predict.html')


@app.route("/resto")
def resto():
	idrows = Item.query.filter_by(category='Indonesian')
	return render_template('resto.html',idrows=idrows)


#login as merchant
@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method=="POST":
		session.clear()
		username = request.form.get("username")
		password = request.form.get("password")
		result = User.query.filter_by(username=username).first()
		print(result)
		# Ensure username exists and password is correct
		if result == None or not check_password_hash(result.password, password):
			return render_template("error.html", message="Invalid username and/or password")
		# Remember which user has logged in
		session["username"] = result.username
		return redirect("/home")
	return render_template("login.html")

# #logout
# @app.route("/logout")
# def logout():
# 	session.clear()
# 	return redirect("/login")

#signup as merchant
@app.route("/signup", methods=["GET","POST"])
def signup():
	if request.method=="POST":
		session.clear()
		password = request.form.get("password")
		repassword = request.form.get("repassword")
		if(password!=repassword):
			return render_template("error.html", message="Passwords do not match!")

		#hash password
		pw_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
		
		fullname = request.form.get("fullname")
		username = request.form.get("username")
		#store in database
		new_user =User(fullname=fullname,username=username,password=pw_hash)
		try:
			db.session.add(new_user)
			db.session.commit()
		except:
			return render_template("error.html", message="Username already exists!")
		return render_template("login.html", msg="Account created!")
	return render_template("signup.html")

#merchant home page to add new products and edit existing products
@app.route("/home", methods=["GET", "POST"], endpoint='home')
@login_required
def home():
	if request.method == "POST":
		image = request.files['image']
		filename = str(uuid.uuid1())+os.path.splitext(image.filename)[1]
		image.save(os.path.join("static/images", filename))
		category= request.form.get("category")
		name = request.form.get("pro_name")
		description = request.form.get("description")
		price_range = request.form.get("price_range")
		comments = request.form.get("comments")
		new_pro = Product(category=category,name=name,description=description,price_range=price_range,comments=comments, filename=filename, username=session['username'])
		db.session.add(new_pro)
		db.session.commit()
		rows = Product.query.filter_by(username=session['username'])
		return render_template("home.html", rows=rows, message="Product added")
	
	rows = Product.query.filter_by(username=session['username'])
	return render_template("home.html", rows=rows)

#when edit product option is selected this function is loaded
@app.route("/edit/<int:pro_id>", methods=["GET", "POST"], endpoint='edit')
@login_required
def edit(pro_id):
	#select only the editing product from db
	result = Product.query.filter_by(pro_id = pro_id).first()
	if request.method == "POST":
		#throw error when some merchant tries to edit product of other merchant
		if result.username != session['username']:
			return render_template("error.html", message="You are not authorized to edit this product")
		category= request.form.get("category")
		name = request.form.get("pro_name")
		description = request.form.get("description")
		price_range = request.form.get("price_range")
		comments = request.form.get("comments")
		result.category = category
		result.name = name
		result.description = description
		result.comments = comments
		result.price_range = price_range
		db.session.commit()
		rows = Product.query.filter_by(username=session['username'])
		return render_template("home.html", rows=rows, message="Product edited")
	return render_template("edit.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)