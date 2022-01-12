from flask import Flask, redirect, url_for, render_template, request, flash, session
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_bcrypt import Bcrypt
import datetime
import os
import requests


app = Flask(__name__)

bcrypt = Bcrypt(app)

host = os.environ.get('DB_URL')
app.secret_key = os.environ.get('SKEY')

client = MongoClient(host=host)

db = client.clothesapp
clothes = db.clothes
users = db.user


''' SHOW ALL Clothing Item------------------------------------------------- '''
@app.route("/")
def home():
    return render_template('index.html')





''' CREATE NEW Clothing Item ------------------------------------------------- '''
@app.route("/clothes/new", methods=['GET'])
def clothes_new():
    _id = session['_id']
    return render_template('clothing_new.html', title='New Clothing Item', _id=_id)




''' SUBMIT A NEW Clothing Item ------------------------------------------------- '''
@app.route("/clothes", methods=['POST'])
def clothes_submit():
    _id = session['_id']
    clothe = {
        'name': request.form.get('title'),
        'type': request.form.get('type'),
        'created': datetime.datetime.utcnow(),
        'user_id': _id
    }
    clothes.insert_one(clothe)
    return redirect(url_for('user'))




''' EDIT A Clothing Item  ---------------------------------------------------------'''
@app.route("/clothes/<clothes_id>/edit")
def clothes_edit(clothes_id):
    clothe = clothes.find_one({'_id': ObjectId(clothes_id)})
    return render_template('clothes_edit.html', clothe = clothe)





''' SUBMIT THE EDITED Clothing Item ------------------------------------------------- '''
@app.route("/clothes/<clothes_id>", methods=['POST'])
def clothes_update(clothes_id):
    updated_clothe = {
        'name': request.form.get('title'),
        'content': request.form.get('description'),
        'created': datetime.datetime.utcnow(),
    }

    clothes.update_one(
        {'_id': ObjectId(clothes_id)},
        {'$set': updated_clothe})
    return redirect(url_for('user', clothess_id=clothes_id, title='Edit Clothing Item'))




''' DELETE A Clothing Item ------------------------------------------------- '''

@app.route("/clothes/<clothes_id>/delete", methods=['POST'])
def clothess_delete(clothes_id):
    """Delete one playlist."""
    clothes.delete_one({'_id': ObjectId(clothes_id)})
    return redirect(url_for('user'))






'''HELPER FUNCTIONS ---------------------------------------------------------------------- '''

def logged_in():
    return session.get('username') and session.get('password')

def current_user():
    found_user = users.find_one ({
        'username':session.get('username'),
        'password':session.get('password')
    })
    return found_user
    




@app.route("/user")
def user():
    if logged_in:
        user = current_user()
        _id = session['_id']

        return render_template("user.html", _id=_id, user=user, clothes=clothes.find({'user_id': _id}).sort([['_id', -1]]))
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))
        





'''LOGIN AND LOGOUT ROUTES -----------------------------------------'''


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        email = request.form['logname']
        password = request.form['logpass']
        user = users.find_one({'username': email})
        if user:
            if bcrypt.check_password_hash(user['password'], password):
                session['email'] = user['username']
                session['_id'] = str(user['_id'])
                return redirect(url_for('user'))
            else:
                flash("Incorrect username/password")
            pass 
        else:
            flash("Incorrect username/password 2")
            return render_template('login.html')
    else:
        if "email" in session:
            # flash("Already logged in!!")
            return redirect(url_for("user"))
        else:
            return render_template('login.html')


@app.route("/logout")
def logout():
    flash("You have been logged out", "info")
    session.pop("email", None)
    return redirect(url_for("login"))


''' REGISTER A USER ---------------------------------------- '''


@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/signup', methods=['POST'])
def signup_form():
    username = request.form.get("usern")
    password = request.form.get("passw")
    password_hash = bcrypt.generate_password_hash(password)
    name = request.form.get("sname")

    found_user = users.find_one({'username':username})
    if found_user:
        flash("User already exists")
        return redirect(url_for('signup'))
    
    user = {
        'username':username,
        'password':password_hash,
        'name':name,
        'created':datetime.datetime.utcnow()
    }

    users.insert_one(user)

    # session["username"] = user['username']
    # session["password"] = user['password']

    return redirect(url_for("user"))


if __name__ == "__main__":
    app.run(debug=True)