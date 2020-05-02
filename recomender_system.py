from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity as distance
import re
import pandas as pd
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
from bson.objectid import ObjectId
import os
import dotenv
dotenv.load_dotenv()
DBURL = os.getenv("DBURL")
client = MongoClient(DBURL)
db = client.get_database()


def friendRecomm(userID):
    messages = db.messages.aggregate([{ "$group" : {"_id":"$user", "messages": { "$push": "$text" } } }])
    docs = {}
    for mes in messages:
        identificador = (re.search(r"\w+\d+",dumps(mes["_id"]))).group()
        docs[identificador] = (".".join(mes['messages']))

    count_vectorizer = CountVectorizer()
    sparse_matrix = count_vectorizer.fit_transform(docs.values())

    doc_term_matrix = sparse_matrix.todense()
    df = pd.DataFrame(doc_term_matrix, columns=count_vectorizer.get_feature_names(), index=docs.keys())
    similarity_matrix = distance(df,df)

    sim_df = pd.DataFrame(similarity_matrix, columns=docs.keys(), index=docs.keys())

    chats = db.chats.find({})
    all_chats = []
    for ident in chats:
        all_chats.append(ident["_id"])

    
    chats = db.chats.find({"users": { "$elemMatch": {"$id": ObjectId(userID)}}})
    user_chats = []
    for ident in chats:
        user_chats.append(ident["_id"])

    chats_noUser = all_chats.copy()
    for e in user_chats:
        chats_noUser.remove(e)
    
    
#me he quedado aquí, buscar los usuarios de los chats en los que no está userID
    for e in chats_noUser:
        db.chats.find({},{"name":1,"_id":0})


    return {"all":all_chats,"user":user_chats, "not_user":chats_noUser}
    
