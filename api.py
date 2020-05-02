from flask import Flask, request
from fc_mongo import *
from sentiment_analysis import *
from recomender_system import *
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
            Insert an existing user (optional): <input type="text" name="userID">
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

@app.route("/chat/adduser", methods=['GET', 'POST'])
def getChatUser():
    chat_id = request.form["chatID"]
    user_id = request.form["userID"]
    return addUser(chat_id,user_id)

#obtain data from jupyter
@app.route("/chat/<chatID>/adduser")
def askaddUserJ(chatID):
    chat_id = chatID
    user_id = request.args["userID"]
    return addUser(chat_id,user_id)


#obtain data from html
@app.route("/chat/addmessage")
def askMessageH():
    return """<form action="/chat/addmessage" method="post">
            Insert a existing chat ID: <input type="text" name="chatID">
            Insert a existing user ID: <input type="text" name="userID">
            <br> Insert a date and time (YYYY-MM-DD HH:MM): <input type="text" name="date">
            Insert a message: <input type="text" name="message">
            <input type="submit">
            </form>"""

@app.route("/chat/addmessage", methods=['GET', 'POST'])
def getMessage():
    chat_id = request.form["chatID"]
    user_id = request.form["userID"]
    date = request.form["date"]
    message = request.form["message"]
    return addMessage(chat_id,user_id,date,message)



#obtain data from jupyter
@app.route("/chat/<chatID>/addmessage")
def askMessageJ(chatID):
    chat_id = chatID
    user_id = request.args["userID"]
    date_time = request.args["date"]
    message = request.args["text"]
    return addMessage(chat_id,user_id,date_time,message)



#obtain data from html
@app.route("/chat/sentiment")
@app.route("/chat/list")
def askListH():
    return f"""<form action={request.url} method="post">
            Insert a existing chat ID: <input type="text" name="chatID">
            <input type="submit">
            </form>"""



@app.route("/chat/sentiment", methods=['GET', 'POST'])
@app.route("/chat/list", methods=['GET', 'POST'])
def getList():
    chat_id = request.form["chatID"]
    list_messages = findList(chat_id)
    if "list" in request.url:
        return list_messages
    return sentAnalysis(list_messages)
    

#obtain data from jupyter
@app.route("/chat/<chatID>/sentiment")
@app.route("/chat/<chatID>/list")
def askListJ(chatID):
    chat_id = chatID
    list_messages = findList(chat_id)
    if "list" in request.url:
        return list_messages
    return sentAnalysis(list_messages)


#prueba jupyter recommend friend
@app.route("/user/<user_id>/recommend")
def askRecommJ(user_id):
    user = user_id
    return friendRecomm(user_id)




app.run("0.0.0.0", PORT , debug=True)