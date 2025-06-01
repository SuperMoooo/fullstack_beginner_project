
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
            res = collection.insert_one(evento.__dict__)
            return res.inserted_id
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

    @staticmethod
    def eliminar_evento(id, collection):
        try:
            res = collection.delete_one({ "id" : id })
            return res.deleted_count
        except Exception as e:
            print(e)
            raise


    # ATIVIDADES RELATED
    @staticmethod
    def delete_atividade(identificador : str, collection):
        try:
            res = collection.update_one(
                {"lista_atividades.identificador": identificador},
                {"$pull": {"lista_atividades": {"identificador": identificador}}}
            )
            return res.modified_count
        except Exception as e:
            print(e)
            raise

    @staticmethod
    def atualizar_atividade(identificador: str, updatedAtividade, collection):
        try:
            res = collection.update_one(
                {"lista_atividades.identificador": identificador},
                {"$set": {"lista_atividades.$": updatedAtividade.__dict__}}
            )
            return res.modified_count
        except Exception as e:
            print(e)
            raise


    @staticmethod
    def atualizar_atividade_listas_por_campo(identificador: str, user, collection, campo):
        try:
            res = collection.update_one(
                {"lista_atividades.identificador": identificador},
                {
                    "$push": {f"lista_atividades.$[elem].{campo}": user.__dict__}
                },
                array_filters=[{"elem.identificador": identificador}]
            )
            return res.modified_count
        except Exception as e:
            print(e)
            raise

    @staticmethod
    def remover_user_atividades(identificador: str, user, collection, campo):
        try:
            res = collection.update_one(
                {"lista_atividades.identificador": identificador},
                {
                    "$pull": {
                        f"lista_atividades.$[elem].{campo}": {"nome": user.get_nome()}
                    }
                },
                array_filters=[{"elem.identificador": identificador}]
            )
            return res.modified_count
        except Exception as e:
            print(e)
            raise



