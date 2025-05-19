from pymongo import MongoClient
from EventModel import EventModel

class EventDatabase:

    @staticmethod
    def get_eventos():
        client = MongoClient("mongodb://localhost:27017/")
        mydb = client["2_freq"]
        collection = mydb["events"]
        data = collection.find({})
        return data

    @staticmethod
    def criar_evento(evento : EventModel):
        try:
            client = MongoClient("mongodb://localhost:27017/")
            mydb = client["2_freq"]
            collection = mydb["events"]
            collection.insert_one(evento.__dict__)
        except Exception as e:
            print(e)
            raise

