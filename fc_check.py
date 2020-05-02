from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
import os
import dotenv
dotenv.load_dotenv()

DBURL = os.getenv("DBURL")
client = MongoClient(DBURL)
db = client.get_database()

def paramExist(name,database):
    if database == "users":
        param = db.users.find({"name" : name},{})
    elif database == "chats":
        param = db.chats.find({"name" : name},{})
    return False if len(list(param)) == 0 else True, dumps(param)

"""
param_ID = dumps(param)
return {"status":f"An {database} with this name already exists with this ID {param_ID}. If you want to create a different {database}, please, change name","status code":"?"}
"""

def testID(ID,database):
    if database == "users":
        return db.users.find({"_id" : ObjectId(ID)},{})
    elif database == "chats":
        return db.chats.find({"_id" : ObjectId(ID)},{})


def textExist(text,date,chatID,userID):
    message = db.messages.find({"$and":[{"text" : text},{"date-time":date},{'user.$id':  ObjectId(userID)},{'chat.$id':  ObjectId(chatID)}]},{})
    return False if len(list(message)) == 0 else True, dumps(message)
"""
Para no meter dos veces el mismo texto, pero no estoy segura, una persona puede preguntar dos veces "Como estas?" en un mismo chat, solo 
podria discriminar por hora
def textExist(text,chatID,userID):
    if database == "users":
        param = db.users.find({"name" : name},{})
    elif database == "chats":
        param = db.chats.find({"name" : name},{})
    return False if len(list(param)) == 0 else True, dumps(param)
"""