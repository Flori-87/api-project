#from api import username,chatname,userID
from fc_check import *
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.dbref import DBRef
from bson.json_util import dumps
import os
import dotenv
dotenv.load_dotenv()

DBURL = os.getenv("DBURL")
client = MongoClient(DBURL)
db = client.get_database()

"""
def createUser(username):
    user = db.users.find({"name" : username},{"name":1})
    if len(list(user)) != 0:
        user_id = dumps(user)
        return {"status":f"An user with this name already exists with this ID {user_id}. If you want to create a different user, please, change the user name","status code":"?"}
    user_profile = {'name': username, "chats":[]}
    db.users.insert_one(user_profile)
    return userID(username)
"""

def createUser(username):
    check = paramExist(username,"users")
    if check[0]:
        return {"status":f"An user with this name already exists with this ID {check[1]}. If you want to create a different user, please, change the user name","status code":"?"}
    user_profile = {'name': username, "chats":[]}
    db.users.insert_one(user_profile)
    return userID(username)

"""
def createChat(chatname,userID):
    if userID:
        try:
            #testar si el ID es valido
            usuario = db.users.find({"_id" : ObjectId(userID)})
        except:
            return {"status":"The user ID is not valid", "status code":"?"}
        if len(list(usuario)) == 0:
            #el usuario ya debe existir en la base de datos usuarios si quiero introducirlo en un chat
            return {"status":"The user ID doesn't exist in the database. Please, confirm the user ID using /user/<username>", "status code":"?"}
    chat = db.chats.find({"name" : chatname},{"name":1})
    if len(list(chat)) != 0:
        chat_id = dumps(chat)
        #no debe existir otro chat con el mismo nombre
        return {"status":f"A chat with that name already exists with the ID {chat_id}. To insert an user in it,please, use:/chat/<chatID>/adduser/<userID>", "status code":"?"}
    chat_profile = {'name': chatname, 'users': []}
    db.chats.insert_one(chat_profile)
    cur = chatID(chatname)
    chat_id = cur[0]['_id']
    db.chats.update_one({"_id" : ObjectId(chat_id)}, {"$push" : { "users": {"$ref": "users","$id": ObjectId(userID),"$db" : "api-project"}}})
    db.users.update_one({"_id" : ObjectId(userID)}, {"$push" : { "chats": {"$ref": "chats","$id": ObjectId(chat_id),"$db" : "api-project"}}})      
    return dumps(cur)
"""

# funcion para introducir chat en la base de datos y para devolver chatID a las funciones de la api
def createChat(chatname,userID):
    if userID:
        try:
            #testar si el ID es valido
            usuario = db.users.find({"_id" : ObjectId(userID)})
        except:
            return {"status":"The user ID is not valid", "status code":"?"}
        check = paramExist(username,"users")
        if not check[0]:
            #el usuario ya debe existir en la base de datos usuarios si quiero introducirlo en un chat
            return {"status":"The user ID doesn't exist in the database. Please, confirm the user ID using /user/<username>", "status code":"?"}
    check = paramExist(chatname,"chats")
    if check[0]:
        #no debe existir otro chat con el mismo nombre
        return {"status":f"A chat with that name already exists with the ID {check[1]}. To insert an user in it,please, use:/chat/<chatID>/adduser/<userID>", "status code":"?"}
    chat_profile = {'name': chatname, 'users': []}
    db.chats.insert_one(chat_profile)
    cur = chatID(chatname)
    chat_id = cur[0]['_id']
    db.chats.update_one({"_id" : ObjectId(chat_id)}, {"$push" : { "users": {"$ref": "users","$id": ObjectId(userID),"$db" : "api-project"}}})
    db.users.update_one({"_id" : ObjectId(userID)}, {"$push" : { "chats": {"$ref": "chats","$id": ObjectId(chat_id),"$db" : "api-project"}}})      
    return dumps(cur)

def userID(username):
    usuario = db.users.find({"name":username},{})
    return dumps(usuario)

def chatID(chatname):
    chat = db.chats.find({"name":chatname},{})
    return chat

def addUser(chatID,userID):
    try:
        chat = db.chats.find({"_id" : ObjectId(chatID)})
        user = db.users.find({"_id" : ObjectId(userID)})
    except: 
        # cuando los id no son validos
        return {"status":"The user ID or chat ID is not valid", "status code":"?"}
    if len(list(chat)) == 0 or len(list(user)) == 0:
        return {"status":"Chat ID or User ID does not exist in the database. Please, create it before doing this step","status code":"?"}
    userInChat = db.chats.find({"$and" : [{"_id" : ObjectId(chatID)},{'users.$id':  ObjectId(userID)}]})
    if len(list(userInChat)) != 0:
        return {"status":"This user is already in this chat","status code":"?"}
    db.chats.update_one({"_id" : ObjectId(chatID)}, {"$push" : { "users": {"$ref": "users","$id": ObjectId(userID),"$db" : "api-project"}}})
    db.users.update_one({"_id" : ObjectId(userID)}, {"$push" : { "chats": {"$ref": "chats","$id": ObjectId(chatID),"$db" : "api-project"}}})     
    return {"_id" : chatID}

def addMessage(chatID,userID,date,text):
    #Purpose:Add a message to the conversation. Help: Before adding the chat message to the database, check that the incoming user is part of this chat id. If not, raise an exception.
    try:
        chat = db.chats.find({"_id" : ObjectId(chatID)})
        user = db.users.find({"_id" : ObjectId(userID)})
    except: 
        # cuando los id no son validos
        return {"status":"The user ID or chat ID is not valid", "status code":"?"}
    if len(list(chat)) == 0 or len(list(user)) == 0:
        return {"status":"Chat ID or User ID does not exist in the database. Please, create it before doing this step","status code":"?"}
    message = textExist(text,date,chatID,userID)
    if message[0]:
        return {"status":"This message by this user at that date-time is already in this chat","status code":"?"}
    message_profile = {"chat":DBRef("chats",ObjectId(chatID),"api-project"), "user":DBRef("users",ObjectId(userID),"api-project"),'text': text, "date-time":date}
    db.messages.insert(message_profile)
    message = messageID(text,date,chatID,userID)
    return dumps(message)

#me acabo de dar cuenta que las funciones de buscar el ID y de buscar la existencia son iguales, debo reducir a uno
def messageID(text,date,chatID,userID):
    message = db.messages.find({"$and":[{"text" : text},{"date-time":date},{'user.$id':  ObjectId(userID)},{'chat.$id':  ObjectId(chatID)}]},{})
    return message
    
"""
    `/chat/<chat_id>/addmessage`
  - **Purpose:** Add a message to the conversation. Help: Before adding the chat message to the database, check that the incoming user is part of this chat id. If not, raise an exception.
  - **Params:**
    - `chat_id`: Chat to store message
    - `user_id`: the user that writes the message
    - `text`: Message text
  - **Returns:** `message_id`
"""