from pymongo import MongoClient

URI = "mongodb+srv://mercado-livre:mercado-livre123456@cluster0.oysisva.mongodb.net/"

mongodb_client = MongoClient(URI)
db = mongodb_client["mercado-livre"]
