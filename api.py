from flask import Flask, request
from pymongo import MongoClient
from bson.objectid import ObjectId
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

@app.route("/user/<username>") #con decorador para saber el ID de un usuario
def userID(username):
    usuario = db.users.find({"name":username},{})
    return dumps(usuario)


@app.route("/chat/create/<chatname>")
def createChat(chatname):
    if request.args:
        userID = request.args["users"]
        chat_profile = {'name': chatname, 'users': [userID], 'quotes': [{'user':None,'quotes':None,'time':None}]}
    else:
        chat_profile = {'name': chatname, 'users': [], 'quotes': [{'user':None,'quotes':None,'time':None}]}
    db.chats.insert_one(chat_profile)
    return chatID(chatname)

@app.route("/chat/<chatname>") #con decorador para saber el ID de un usuario
def chatID(chatname):
    chat = db.chats.find({"name":chatname},{})
    return dumps(chat)

@app.route("/chat/<chatID>/adduser/<userID>")
def addUser(chatID,userID):
    #chat_id = 'ObjectId("'+chatID+'")'
    db.chats.update_one({"_id" : ObjectId(chatID)}, {"$push" : { "users": userID }})
    return {"_id" : chatID}

app.run("0.0.0.0", PORT , debug=True)