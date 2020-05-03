from src.config import DBURL
from src.fc_check import *
import re
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.dbref import DBRef
from bson.json_util import dumps


client = MongoClient(DBURL)
db = client.get_database()





def createUser(username):
    check = userID(username)
    if check!="Failed":
        return {"status":f"An user with this name already exists with the ID {check}. If you want to create a different user, please, change the user name","status code":"?"}
    user_profile = {'name': username, "chats":[]}
    db.users.insert_one(user_profile)
    user_id = userID(username)
    return {"status":f"The user '{username}' has been created with the corresponding ID {user_id}"}

# funcion para introducir chat en la base de datos y para devolver chatID a las funciones de la api
def createChat(chatname,userID):
    if userID:
        try:
            #testar si el ID es valido
            usuario = db.users.find({"_id" : ObjectId(userID)})
        except:
            return {"status":"The user ID is not valid", "status code":"?"}
        if usuario.count() == 0:
            #el usuario ya debe existir en la base de datos usuarios si quiero introducirlo en un chat
            return {"status":"The user ID doesn't exist in the database. Please, confirm the user ID using /user/<username>", "status code":"?"}
    check = chatID(chatname)
    if check!="Failed":
        #no debe existir otro chat con el mismo nombre
        return {"status":f"A chat with that name already exists with the ID {check}. To insert an user in it,please, use:/chat/<chatID>/adduser/<userID>", "status code":"?"}
    chat_profile = {'name': chatname, 'users': []}
    db.chats.insert_one(chat_profile)
    chat_id = chatID(chatname)
    if userID:
        db.chats.update_one({"_id" : ObjectId(chat_id)}, {"$push" : { "users": {"$ref": "users","$id": ObjectId(userID),"$db" : "api-project"}}})
        db.users.update_one({"_id" : ObjectId(userID)}, {"$push" : { "chats": {"$ref": "chats","$id": ObjectId(chat_id),"$db" : "api-project"}}})      
    return {"status":f"The chat '{chatname}' has been created with the corresponding ID {chat_id}"}


def addUser(chatID,userID):
    try:
        chat = db.chats.find({"_id" : ObjectId(chatID)}).count()
        user = db.users.find({"_id" : ObjectId(userID)}).count()
    except: 
        # cuando los id no son validos
        return {"status":"The user or chat ID is not valid", "status code":"?"}
    if chat == 0 or user == 0:
        return {"status":"The user or chat ID does not exist in the database. Please, confirm the user or chat ID using /user/<username> or /chat/<chatname>","status code":"?"}
    userInChat = db.chats.find({"$and" : [{"_id" : ObjectId(chatID)},{'users.$id':  ObjectId(userID)}]}).count()
    if userInChat != 0:
        return {"status":"This user is already in this chat","status code":"?"}
    db.chats.update_one({"_id" : ObjectId(chatID)}, {"$push" : { "users": {"$ref": "users","$id": ObjectId(userID),"$db" : "api-project"}}})
    db.users.update_one({"_id" : ObjectId(userID)}, {"$push" : { "chats": {"$ref": "chats","$id": ObjectId(chatID),"$db" : "api-project"}}})     
    return {"status":f"The chat with the ID '{chatID}' has a new user with the ID '{userID}'"}

def addMessage(chatID,userID,date,text):
    #Add a message to the conversation. Check that the incoming user is part of this chat id. If not, raise an exception.
    try:
        chat = db.chats.find({"_id" : ObjectId(chatID)}).count()
        user = db.users.find({"_id" : ObjectId(userID)}).count()
    except: 
        # cuando los id no son validos
        return {"status":"The user or chat ID is not valid", "status code":"?"}
    if chat == 0 or user == 0:
        return {"status":"The user or chat ID does not exist in the database. Please, confirm the user or chat ID using /user/<username> or /chat/<chatname>","status code":"?"}
    userInChat = db.chats.find({"$and" : [{"_id" : ObjectId(chatID)},{'users.$id':  ObjectId(userID)}]}).count()
    if userInChat == 0:
        return {"status":"This user is not in this chat. Please, add the user to this chat before doing this step","status code":"?"}
    message = messageID(text,date,chatID,userID)
    if message != "Failed":
        return {"status":f"This message from this user at that date-time is already in this chat with the ID {message}","status code":"?"}
    message_profile = {'text': text, "date-time":date,"chat":DBRef("chats",ObjectId(chatID),"api-project"), "user":DBRef("users",ObjectId(userID),"api-project")}
    db.messages.insert(message_profile)
    message_id = messageID(text,date,chatID,userID)
    return {"status":f"The message with the ID '{message_id}' has been added"}


def findList(chatID):
    try:
        chat = db.chats.find({"_id" : ObjectId(chatID)}).count()
    except: 
        # cuando los id no son validos
        return {"status":"The chat ID is not valid", "status code":"?"}
    if chat == 0:
        return {"status":"The chat ID does not exist in the database. Please, confirm the chat ID using /chat/<chatname>","status code":"?"}
    message = db.messages.find({'chat.$id':  ObjectId(chatID)},{"text":1,"date-time":1,'user.$id':1})
    if message.count() == 0:
        return {"status":"The chat with this ID does not contain messages yet", "status code":"?"}
    dict_messages = {}
    for mes in message:
        message_id = (re.search(r"\w+\d+\w*",dumps(mes["_id"]))).group()
        user_id = (re.search(r"\w+\d+\w*",dumps(mes["user"]["$id"]))).group()
        dict_messages["Message ID:"+message_id] = [mes["text"],"User ID:"+user_id,"Date:"+mes["date-time"]]
    return dict_messages
