from flask import Flask, redirect, url_for, render_template
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import datetime

app = Flask(__name__)
host = os.environ.get('DB_URL')

@app.route("/")
def home():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)