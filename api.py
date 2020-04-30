from flask import Flask, request
from pymongo import MongoClient
from bson.json_util import dumps
import os
import dotenv
dotenv.load_dotenv()

PORT = os.getenv("PORT")
DBURL = os.getenv("DBURL")

app = Flask(__name__)

client = MongoClient(DBURL)
db = client.get_database()

@app.route("/saluda")
def saluda():
    return {"Hola":"saludo"}

@app.route("/user/create/<username>")
def createUser(username):
    user_profile = {'name': username, 'chats': [], 'quotes': [{'chat':None,'quotes':None}]}
    db.users.insert_one(user_profile)
    return userID(username)

@app.route("/user/create/<username>")
def userID(name):
    print("he entrado")
    usuario = db.users.find({"name":name},{})
    print("ok")
    return dumps(usuario)

@app.route("/chat/create/<chatname>")
def createChat(chatname):
    chat_profile = {'name': chatname, 'users': [], 'quotes': [{'user':None,'quotes':None,'time':None}]}
    db.chats.insert_one(chat_profile)
    return userID(username)
  - **Purpose:** Create a conversation to load messages
  - **Params:** An array of users ids `[user_id]`
  - **Returns:** `chat_id`

app.run(host = "0.0.0.0", PORT , debug=True)