import pymongo
import time
from flask import Flask, request, g, render_template, redirect
import os

conn_str = os.environ['MONGOCONN']
client = pymongo.MongoClient(conn_str)
db = client.growls

app = Flask(__name__)

def db_read_growls():
    c = db.growls.find().sort("time", pymongo.DESCENDING)
    return [(g['name'], g['time'], g['text']) for g in c]

def db_add_growl(name, growl):
    t = str(time.time())
    growl = {"name": name, "time": t, "text": growl}
    db.growls.insert(growl)

@app.route("/")
def hello():
    growls = db_read_growls()
    return render_template('index.html', growls=growls)

@app.route("/api/growl", methods=["POST"])
def receive_growl():
    print(request.form)
    db_add_growl(request.form['name'], request.form['growl'])
    return redirect("/")

if __name__ == "__main__":
    app.debug = True
    app.run()