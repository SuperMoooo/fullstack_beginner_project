from pymongo import MongoClient


class EventDatabase:
    @staticmethod
    def criar_evento():
        client = MongoClient("mongodb://localhost:27017/")
        mydb = client["2_freq"]
        collection = mydb["events"]