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
    content = request.json
    print(content)
    _id = session['_id']
    
    if len(content['title']) > 0:
        clothe = {
            'name': content['title'],
            'type': content['category'],
            'image_url': content['cdnURL'], 
            'created': datetime.datetime.utcnow(),
            'user_id': _id,
        }
        clothes.insert_one(clothe)
        return {"success": True}
    else:
        return {'success': False, 'error': "Title can't be blank"}




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
    return redirect(url_for('user', clothes_id=clothes_id, title='Edit Clothing Item'))




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
    filter = request.args.get('filter')
    if logged_in:
        user = current_user()
        _id = session['_id']
        if filter:
            find_clothes = clothes.find({'user_id': _id, 'type': filter}).sort([['_id', -1]])
        else:
            find_clothes = clothes.find({'user_id': _id}).sort([['_id', -1]])

        return render_template("user.html", _id=_id, user=user, clothes=find_clothes)
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



"""ROUTES FOR CLOTHING FILTERS -----------------------------"""


""" FILTERS """
# @app.route('/user')
# def fitler(filter):
#     user = current_user()
#     _id = session['_id']
#     filtered_items = clothes.find({type: filter})
#     return render_template(f"clothingfilter/f{filter}.html")

""" HAT ------------------------------------------------------------------------------ """
@app.route("/user/hats")
def hat():

        user = current_user()

        _id = session['_id']

        hat = clothes.find({type: 'Hat'})

        return render_template("clothingfilter/hats.html", _id=_id, user=user, clothes=clothes.find({'user_id': _id}).sort([['_id', -1]]), hat=hat)

""" SHIRT ----------------------------------------------------------------------------- """

@app.route("/user/shirts")
def shirt():
    if logged_in:

        user = current_user()

        _id = session['_id']

        shirt = clothes.find({type: 'Shirt'})

        return render_template("clothingfilter/shirts.html", _id=_id, user=user, clothes=clothes.find({'user_id': _id}).sort([['_id', -1]]), shirt=shirt)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

""" JACKET ----------------------------------------------------------------------------- """

@app.route("/user/jackets")
def jacket():
    if logged_in:

        user = current_user()

        _id = session['_id']

        jacket = clothes.find({type: 'Jacket'})

        return render_template("clothingfilter/jackets.html", _id=_id, user=user, clothes=clothes.find({'user_id': _id}).sort([['_id', -1]]), jacket=jacket)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

""" PANTS ----------------------------------------------------------------------------- """

@app.route("/user/pants")
def pants():
    if logged_in:

        user = current_user()

        _id = session['_id']

        pants = clothes.find({type: 'Pants'})

        return render_template("clothingfilter/pants.html", _id=_id, user=user, clothes=clothes.find({'user_id': _id}).sort([['_id', -1]]), pants=pants)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

""" SOCKS ----------------------------------------------------------------------------- """

@app.route("/user/socks")
def socks():
    if logged_in:

        user = current_user()

        _id = session['_id']

        sock = clothes.find({type: 'Socks'})

        return render_template("clothingfilter/socks.html", _id=_id, user=user, clothes=clothes.find({'user_id': _id}).sort([['_id', -1]]), sock=sock)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

""" SHOES ----------------------------------------------------------------------------- """

@app.route("/user/shoes")
def shoe():
    if logged_in:

        user = current_user()

        _id = session['_id']

        shoe = clothes.find({'type' : 'Shoes'})

        return render_template("clothingfilter/shoes.html", _id=_id, user=user, clothes=clothes.find({'user_id': _id}), shoe=shoe)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))


    


if __name__ == "__main__":
    app.run(debug=True)