from pymongo import MongoClient

URI = "mongodb://root:example@localhost:27017"

mongodb_client = MongoClient(URI)
db = mongodb_client["mercado-livre"]
