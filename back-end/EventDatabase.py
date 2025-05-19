from pymongo import MongoClient
from EventModel import EventModel

class EventDatabase:

    @staticmethod
    def get_eventos():
        try:
            client = MongoClient("mongodb://localhost:27017/")
            mydb = client["2_freq"]
            collection = mydb["events"]
            data = collection.find({})
            return data
        except Exception as e:
            print(e)
            raise
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

    @staticmethod
    def get_evento(id):
        try:
            client = MongoClient("mongodb://localhost:27017/")
            mydb = client["2_freq"]
            collection = mydb["events"]
            data = collection.find({"id" : id})
            return data
        except Exception as e:
            print(e)
            raise


    @staticmethod
    def get_event_last_id():
        try:
            client = MongoClient("mongodb://localhost:27017/")
            mydb = client["2_freq"]
            collection = mydb["events"]
            data = collection.find({})
            if data is None:
                return 0
            return data[-1]["id"]
        except Exception as e:
            print(e)
            raise