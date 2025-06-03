import re

from AdminModel import AdminModel
from ParticipanteModel import ParticipanteModel
from EntrevenienteModel import EntrevenienteModel
from EventDatabase import EventDatabase

class UtilizadorDatabase:
    def __init__(self):
        pass

    # RETORNAR USER BY NOME
    @staticmethod
    def get_user_by_nome(nome : str, collection):
        user = collection.find({"nome": nome})
        if user:
            result = user[0]
            if result["tipo"] == "Admin":
                return AdminModel(result["nome"], result["email"], result["data_nascimento"], result["sexo"], result["nif"], result["password"], result["tipo"])
            elif result["tipo"] == "Entreveniente":
                return EntrevenienteModel(result["nome"], result["email"], result["data_nascimento"], result["sexo"], result["nif"], result["password"], result["tipo"])
            elif result["tipo"] == "Participante":
                return ParticipanteModel(result["nome"], result["email"], result["data_nascimento"], result["sexo"], result["nif"], result["password"], result["tipo"], result["codigos"] )
        return None

    # VERIFICAR LOGIN
    @staticmethod
    def check_login(collection, nome, password : str):
        try:
            user = UtilizadorDatabase.get_user_by_nome(nome, collection)
            if user.get_password() == password:
                return user
            return None
        except Exception as e:
            print(e)
            return False

    # ALTERAR PASSWORD
    @staticmethod
    def alterar_password(nome, password : str, collection) -> bool:
        try:
            collection.update_one({"nome": nome}, {"$set": {"password": password}})
            return True
        except Exception as e:
            print(e)
            raise


    # ATUALIZAR USER
    @staticmethod
    def atualizar_user(updatedUserData, collection, nome, eventColl):
        try:
            collection.delete_one({"nome": nome})
            collection.insert_one(updatedUserData.__dict__)

            if updatedUserData.get_tipo() == "Participante":
                codigos = updatedUserData.get_codigos()
                for codigo in codigos:
                    atividadeId = re.sub(r'^\d{9}', '', codigo)
                    EventDatabase.remover_user_atividades(atividadeId, nome, eventColl, "lista_participantes")
                    EventDatabase.atualizar_atividade_listas_por_campo(atividadeId, updatedUserData, eventColl, "lista_participantes")
            return True
        except Exception as e:
            print(e)
            raise


    # APAGAR USER
    @staticmethod
    def apagar_user(collection, nome):
        try:
            collection.delete_one({"nome": nome})
            return True
        except Exception as e:
            print(e)
            raise


    # VERIFICAR SE NOME DE UTILIZADOR JÁ EXISTE
    @staticmethod
    def verificar_user_exists(collection, nome) -> bool:
        data = UtilizadorDatabase.get_users(collection)
        for user in data:
            if nome == user["nome"]:
                return True
        return False

    # RECEBER TODOS OS USERS DA DB
    @staticmethod
    def get_users(collection) :
        result = collection.find({})
        return result


