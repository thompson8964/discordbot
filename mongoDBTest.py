from pymongo import MongoClient
import pprint
client = MongoClient("mongodb+srv://thompson8964:S0iu47IHOzTgDiVB@cluster0.vqllooc.mongodb.net/")
db = client["chatbotDB"]
collection = db["users"]

print(collection.find_one())
