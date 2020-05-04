from src.config import DBURL
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity as distance
import re
import pandas as pd
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps


client = MongoClient(DBURL)
db = client.get_database()


def friendRecomm(userID):
    messages = db.messages.aggregate([{ "$group" : {"_id":"$user", "messages": { "$push": "$text" } } }])
    docs = {}
    for mes in messages:
        identificador = (re.search(r"\w+\d+\w*",dumps(mes["_id"]))).group()
        docs[identificador] = (".".join(mes['messages']))

    #generate matrix of similarity by conversation topics
    count_vectorizer = CountVectorizer()
    sparse_matrix = count_vectorizer.fit_transform(docs.values())
    doc_term_matrix = sparse_matrix.todense()
    #dataframe with word counts per user 
    df = pd.DataFrame(doc_term_matrix, columns=count_vectorizer.get_feature_names(), index=docs.keys())
    #similarity matrix between users based on word counts
    similarity_matrix = distance(df,df)
    #dataframe from similarity matrix
    sim_df = pd.DataFrame(similarity_matrix, columns=docs.keys(), index=docs.keys())

    #find users in chats where analysed user is not in. 
    users_chats_noUser = db.chats.find({"users": {"$not": { "$elemMatch": {"$id": ObjectId(userID)}}}},{"users":1,"_id":0})
    #find users in chats where analysed user is in. 
    users_chats_User = db.chats.find({"users": { "$elemMatch": {"$id": ObjectId(userID)}}},{"users":1,"_id":0})
    
    #list of user IDs from chats where analysed user is not in
    list_users_chats_noUser = []
    for users in users_chats_noUser:
        for value in users.values():
            for e in value:
                list_users_chats_noUser.append(dumps(e))
    list_users_chats_noUser = list(set(list_users_chats_noUser))

    #list of user IDs from chats where analysed user is in
    list_users_chats_User = []
    for users in users_chats_User:
        for value in users.values():
            for e in value:
                list_users_chats_User.append(dumps(e))
    list_users_chats_User = list(set(list_users_chats_User))
    
    #list of users who analysed user have never spoken with
    for e in list_users_chats_User:
        if e in list_users_chats_noUser:
            list_users_chats_noUser.remove(e)

    #list containing only the ID of users who analysed user have never spoken with
    id_friends_recomm=[]
    for e in list_users_chats_noUser:
        id_friends_recomm.append((re.search(r"\w+\d+\w*",dumps(e))).group())

    #from similarity matrix, choose the top 3 friends to recommend the analysed user
    df_friend_recommed = pd.DataFrame(sim_df[userID])

    labels = id_friends_recomm
    
    df_friend_recommed = list(df_friend_recommed.loc[df_friend_recommed.index.intersection(labels)].sort_values(userID, ascending=False)[:3].index.values)

    return {"top_friends":df_friend_recommed}

    
    
