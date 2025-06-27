from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson.json_util import dumps
from typing import Optional
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient("mongodb://localhost:27017")
db = client["blackcoffer"]
collection = db["insights"]

@app.get("/data")
def get_all_data():
    data = list(collection.find())
    return JSONResponse(content=data)

@app.get("/filters")
def get_unique_filters():
    filters = {
        "end_year": collection.distinct("end_year"),
        "topics": collection.distinct("topic"),
        "sector": collection.distinct("sector"),
        "region": collection.distinct("region"),
        "pestle": collection.distinct("pestle"),
        "source": collection.distinct("source"),
        "country": collection.distinct("country"),
        "city": collection.distinct("city")
    }
    return filters

@app.get("/filtered-data")
def get_filtered_data(topic: Optional[str] = None, country: Optional[str] = None, region: Optional[str] = None):
    query = {}
    if topic:
        query["topic"] = topic
    if country:
        query["country"] = country
    if region:
        query["region"] = region
    data = list(collection.find(query))
    return JSONResponse(content=data)
