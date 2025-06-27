import json
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["blackcoffer"]
collection = db["insights"]

with open("jsondata.json", encoding="utf-8") as f:
    data = json.load(f)

collection.delete_many({})
collection.insert_many(data)
print("Data inserted successfully")
