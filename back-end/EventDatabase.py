

class EventDatabase:

    @staticmethod
    def get_eventos(collection):
        try:
            data = collection.find({})
            return data
        except Exception as e:
            print(e)
            raise
    @staticmethod
    def criar_evento(evento, collection):
        try:
            collection.insert_one(evento.__dict__)
            return True
        except Exception as e:
            print(e)
            raise

    @staticmethod
    def get_evento(id, collection):
        try:
            data = collection.find({"id" : id})
            return data
        except Exception as e:
            print(e)
            raise


    @staticmethod
    def get_event_last_id(collection):
        try:
            data = collection.find({})
            if data is None:
                return 0
            return data[-1]["id"]
        except Exception as e:
            print(e)
            raise