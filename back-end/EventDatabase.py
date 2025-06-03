import re
from ParticipanteModel import ParticipanteModel

class EventDatabase:

    @staticmethod
    def get_eventos(collection):
        try:
            mongo_data = collection.find()
            data = []
            for row in mongo_data:
                # REMOVER OS _IDS DO MONGO
                row.pop("_id", None)
                data.append(row)

            for evento in data:
                for atividade in evento["lista_atividades"]:
                    for d in atividade["lista_participantes"]:
                        d.pop("_id", None)

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
    def atualizar_evento(eventoId, updatedEvento, collection):
        try:
            res = collection.update_one(
                {"id": eventoId},
                {"$set": updatedEvento.__dict__}
            )
            return res.modified_count
        except Exception as e:
            print(e)
            raise

    @staticmethod
    def get_evento(id : int, collection):
        try:
            cursorData = collection.find({"id" : id})
            data = None
            # REMOVER OS IDS DO MONGO
            for row in cursorData:
                row.pop("_id", None)
                data = row

            for d in data["lista_atividades"]:
                for participante in d["lista_participantes"]:
                    participante.pop("_id", None)

            return data
        except Exception as e:
            print(e)
            raise


    @staticmethod
    def get_event_last_id(collection):
        try:
            # ENCONTRAR O ULTIMO EVENTO PARA RETORNAR O ID
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
    def get_atividade(atividadeId : str, collection):
        try:
            # RETORNA EVENTO COM AQUELA ATIVIDADE
            evento = collection.find_one({"lista_atividades.identificador": atividadeId})
            if evento is None:
                raise Exception("Atividade não encontrada")

            for atividade in evento["lista_atividades"]:
                # PROCURA ATIVIDADE CORRETA
                if atividade["identificador"] == atividadeId:
                    return atividade

            return 0
        except Exception as e:
            print(e)
            raise


    @staticmethod
    def delete_atividade(atividadeId : str, collection):
        try:
            # RETIRA DA LISTA DE ATIVIDADES A ATIVIDADE COM IDENTIFICADOR IGUAL Á PROCURA
            res = collection.update_one(
                {"lista_atividades.identificador": atividadeId},
                {"$pull": {"lista_atividades": {"identificador": atividadeId}}}
            )
            return res.modified_count
        except Exception as e:
            print(e)
            raise

    @staticmethod
    def atualizar_atividade(atividadeId: str, updatedAtividade, collection):
        try:
            # ATUALIZA A ATIVIDADE COM IDENTIFICADOR IGUAL Á PROCURA
            res = collection.update_one(
                {"lista_atividades.identificador": atividadeId},
                {"$set": {"lista_atividades.$": updatedAtividade.__dict__}}
            )
            return res.modified_count
        except Exception as e:
            print(e)
            raise


    @staticmethod
    def atualizar_atividade_listas_por_campo(atividadeId: str, user, collection, campo : str):
        try:
            # IRÁ PROCURAR A ATIVIDADE COM O IDENTIFICADOR IGUAL Á PROCURA E DEPOIS NESSA ATIVIDADE *
            # * IRÁ ATUALIZAR NO CAMPO QUE EU DIZER COM O USER QUE EU DIZER
            res = collection.update_one(
                {"lista_atividades.identificador": atividadeId},
                {
                    "$push": {f"lista_atividades.$[elem].{campo}": user.__dict__}
                },
                # SÓ VAI ATUALIZAR A ATIVIDADE COM AQUELE IDENTIFICADOR
                array_filters=[{"elem.identificador": atividadeId}]
            )
            return res.modified_count
        except Exception as e:
            print(e)
            raise

    @staticmethod
    def remover_user_atividades(atividadeId: str, nome : str, collection, campo : str):
        try:
            # IRÁ PROCURAR A ATIVIDADE COM O IDENTIFICADOR IGUAL Á PROCURA E DEPOIS NESSA ATIVIDADE *
            # * IRÁ REMOVER DO CAMPO QUE EU DIZER O USER QUE EU DIZER
            res = collection.update_one(
                {"lista_atividades.identificador": atividadeId},
                {
                    "$pull": {
                        f"lista_atividades.$[elem].{campo}": {"nome": nome}
                    }
                },
                array_filters=[{"elem.identificador": atividadeId}]
            )
            return res.modified_count
        except Exception as e:
            print(e)
            raise

    @staticmethod
    def validar_codigo(user : ParticipanteModel, nif, codigo, atividadeId, collection, res):
        try:
            # VERIFICA SE O NIF CORRESPONDE
            if user.get_nif() == nif:
                codigos = user.get_codigos()
                # VAI VER TODOS OS CODIGOS DO PARTICIPANTE
                for c in codigos:
                    # REMOVE OS PRIMEIROS 9 CHARS (NIF) E DEIXA SÓ O IDENTIFICADOR DA ATIVIDADE
                    if c == codigo and re.sub(r'^\d{9}', '', c) == atividadeId:

                        sucesso = user.codigo_validado(collection, codigo)
                        codigos = user.get_codigos()
                        # A FORMA DE VALIDAR O CÓDIGO É DIZER "VALIDADO" DEPOIS DO CODIGO
                        novo_codigos = [c + "VALIDADO" if c == codigo else c for c in codigos]
                        user.set_codigos(novo_codigos)

                        if not sucesso:
                            res['sucesso'] = False
                            return False
                        res['sucesso'] = True
                        return True
            res['sucesso'] = False
            return False
        except Exception as e:
            raise


    @staticmethod
    def adicionar_comentario(atividadeId, comentario, collection):
        try:
            res = collection.update_one(
                {"lista_atividades.identificador": atividadeId},
                {
                    "$push": {f"lista_atividades.$[elem].comentarios": comentario.__dict__}
                },
                array_filters=[{"elem.identificador": atividadeId}]
            )
            return res.modified_count
        except Exception as e:
            print(e)
            raise

