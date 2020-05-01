from flask import Flask, request
from fc_mongo import *
import os
import dotenv
dotenv.load_dotenv()

PORT = os.getenv("PORT")


app = Flask(__name__)


#obtain data from html
@app.route("/user/create")
def askUserH():
    return """<form action="/user/create" method="post">
            Insert a new user: <input type="text" name="username">
            <input type="submit">
            </form>"""

@app.route("/user/create", methods=['GET', 'POST'])
def getUser():
    username = request.form["username"]
    return createUser(username)

#obtain data from jupyter
@app.route("/user/create/<username>")
def askUserJ(username):
    username = username
    return createUser(username)

"""
modificar para que no tenga nada de mongo
@app.route("/user/<username>") #con decorador para saber el ID de un usuario
def userID(username):
    usuario = db.users.find({"name":username},{})
    return dumps(usuario)
"""

#obtain data from html
@app.route("/chat/create")
def askChatH():
    return """<form action="/chat/create" method="post">
            Insert a new chat: <input type="text" name="chatname">
            Insert an existing user: <input type="text" name="userID">
            <input type="submit">
            </form>"""

@app.route("/chat/create", methods=['GET', 'POST'])
def getChat():
    chatname = request.form["chatname"]
    if request.form["userID"]:
        userID = request.form["userID"]
    else:
        userID = None
    return createChat(chatname, userID)

#obtain data from jupyter
@app.route("/chat/create/<chatname>")
def askChatJ(chatname):
    chatname = chatname
    if request.args:
        #el usuario ya debe existir en la base de datos usuarios si quiero introducirlo en un chat
        userID = request.args["users"]
    else:
        userID = None
    return createChat(chatname, userID)


"""
Cambiar para que no llame a mongo y solo obtenga el chat name
@app.route("/chat/<chatname>") #con decorador para saber el ID de un usuario
def chatID(chatname):
    chat = db.chats.find({"name":chatname},{})
    return chat
"""

#obtain data from html
@app.route("/chat/adduser")
def askaddUserH():
    return """<form action="/chat/adduser" method="post">
            Insert a existing chat ID: <input type="text" name="chatID">
            Insert a existing user ID: <input type="text" name="userID">
            <input type="submit">
            </form>"""

@app.route("/user/create", methods=['GET', 'POST'])
def getChatUser():
    chat_id = request.form["chatID"]
    user_id = request.form["userID"]
    return addUser(chatID,userID)

#obtain data from jupyter
@app.route("/chat/<chatID>/adduser")
def askaddUserJ(chatID):
    chat_id = chatID
    user_id = request.args["userID"]
    return addUser(chat_id,user_id)


"""
@app.route("/chat/<chatID>/user/<userID>/addmessage/<text>")
def addMessage(chatID,userID,text):
    #Purpose:Add a message to the conversation. Help: Before adding the chat message to the database, check that the incoming user is part of this chat id. If not, raise an exception.

    db.chats.update_one({"_id" : ObjectId(chatID)}, {"$push" : { "users": userID }})
    return {"_id" : chatID}

- (POST) `/chat/<chat_id>/addmessage`
  - **Params:**
    - `chat_id`: Chat to store message
    - `user_id`: the user that writes the message
    - `text`: Message text
  - **Returns:** `message_id`
"""

app.run("0.0.0.0", PORT , debug=True)