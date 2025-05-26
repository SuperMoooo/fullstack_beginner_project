
class EventDatabase:

    @staticmethod
    def get_eventos(collection):
        try:
            mongo_data = collection.find()
            data = []
            for row in mongo_data:
                row.pop("_id", None)
                data.append(row)
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
    def get_evento(id : int, collection):
        try:
            cursorData = collection.find({"id" : id})
            data = None
            for row in cursorData:
                row.pop("_id", None)
                data = row
            return data
        except Exception as e:
            print(e)
            raise


    @staticmethod
    def get_event_last_id(collection):
        try:
            last_event = collection.find_one(sort=[("id", -1)])
            if last_event is None:
                return 0
            return last_event["id"]
        except Exception as e:
            print(e)
            raise
