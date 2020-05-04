import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
nltk.download("vader_lexicon")
from src.helpers.errorHandler import errorHandler, Error404
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
from src.config import DBURL

client = MongoClient(DBURL)
db = client.get_database()

sia = SentimentIntensityAnalyzer()

def sentAnalysis(sentence):
    for key in sentence.keys():
        if key == "status":
            return sentence
    for key,value in sentence.items():
        sentiment = sia.polarity_scores(value[0])
        sentence[key].append(sentiment)
    return sentence

@errorHandler
def ReportsentAnalysis(chatID):
    try:
        chat = db.chats.find({"_id" : ObjectId(chatID)}).count()
    except: 
        # cuando los id no son validos
        return {"message":"The chat ID is not valid", "status":"error"}
    if chat == 0:
        raise Error404("The chat ID does not exist in the database. Please, confirm the chat ID using /chat/<chatname>")
    messages = db.messages.aggregate([{ "$match": {"chat.$id": ObjectId(chatID)} },{ "$group" : {"_id":"$user", "messages": { "$push": "$text" }} }])
    docs = {}
    for mes in messages:
        identificador = (re.search(r"\w+\d+\w*",dumps(mes["_id"]))).group()
        docs[identificador] = (".".join(mes['messages']))
    if not docs:
        raise Error404("The chat with this ID does not contain messages yet")
    analysis_by_user={}
    for key,value in docs.items():
        sentiment = sia.polarity_scores(value)
        analysis_by_user[key] = sentiment
    return {f"Sentiment analysis per user in chat with ID {chatID}":analysis_by_user}
