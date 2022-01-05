from flask import Flask, redirect, url_for, render_template, request
from pymongo import MongoClient
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os
import datetime

app = Flask(__name__)
host = os.environ.get('DB_URL')
mongo= PyMongo(app)
client = MongoClient(host=host)

db = client.virtcloset

item = db.clothingitem
collection = db.collection


@app.route("/")
def home():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    if 'clothing_image' in request.files:
        clothing_image = request.files['clothing_image']
        mongo.save_file(clothing_image.filename)
        mongo.db.users.insert({'clothing_type' : request.form.get('clothing_type'), 'clothing_image_name' : clothing_image.filename})

        return 'Done!'


if __name__ == "__main__":
    app.run(debug=True)