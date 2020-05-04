from src.config import DBURL
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
import re
from src.helpers.errorHandler import errorHandler, Error404


client = MongoClient(DBURL)
db = client.get_database()



def userID(username):
    usuario = db.users.find({"name":username},{"name":1})
    if usuario.count()>0:
        usuarioID = (re.search(r"\w+\d+\w*",dumps(usuario))).group()

        return usuarioID
    else:
        return "Failed"

def chatID(chatname):
    chat = db.chats.find({"name":chatname},{})
    if chat.count()>0:
        chatID = (re.search(r"\w+\d+\w*",dumps(chat))).group()
        return chatID
    else:
        return "Failed"

def messageID(text,date,chatID,userID):
    message = db.messages.find({"$and":[{"text" : text},{"date-time":date},{'user.$id':  ObjectId(userID)},{'chat.$id':  ObjectId(chatID)}]},{})
    if message.count()>0:
        messageID = (re.search(r"\w+\d+\w*",dumps(message))).group()
        return messageID
    else:
        return "Failed"

@errorHandler
def returnID(ID,topic,name):
    # return the response for an ID asked
    if ID == "Failed":
        raise Error404(f"No {topic} exists with that name in the database")
    return {f"The corresponding ID for the {topic} '{name}' is":ID}