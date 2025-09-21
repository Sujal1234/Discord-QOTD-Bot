import pymongo
import os

pswd = os.environ["password"]

cluster = pymongo.MongoClient("mongodb://sujal1234:"+pswd+"@cluster0-shard-00-00.mew0u.mongodb.net:27017,cluster0-shard-00-01.mew0u.mongodb.net:27017,cluster0-shard-00-02.mew0u.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-y152pb-shard-0&authSource=admin&retryWrites=true&w=majority")

db = cluster["QOTD_Bot"]
collection = db["QOTD Scores"]

def post(user_id, score):
  post = {
    "UserId": user_id,
    "Score": score
  }
  collection.insert_one(post)

def search(user_id):
  result = collection.find_one({"UserId" : user_id})
  return result
  #returns None is user not found

def update(user_id, new_score=None, new_attempts=None):
  query = {}
  if(not new_score is None):
    query["Score"] = new_score
  if(not new_attempts is None):
    query["attempts"] = new_attempts
  collection.update_one({"UserId":user_id},
   {
     "$set": query
   })
  
def reset_all():
    collection.update_many(
      {},
      {
        "$set": {"Score": 0}
      }
    )