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
        # ENCONTRA O USER NO MONGO
        result = collection.find_one({"nome": nome})
        # E DEPOIS ATRIBUI O OBJETO DEPENDENDO DO TIPO
        if result:
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
            # RECEBE O USER
            user = UtilizadorDatabase.get_user_by_nome(nome, collection)
            # VERIFICA SE A PASSWORD CORRESPONDE
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
            # REMOVE O USER
            collection.delete_one({"nome": nome})
            # ADICIONA O USER NOVAMENTE COM OS DADOS ATUALIZADOS
            collection.insert_one(updatedUserData.__dict__)

            # SE ELE FOR PARTICIPANTE VAI TER CÓDIGOS
            if updatedUserData.get_tipo() == "Participante":
                codigos = updatedUserData.get_codigos()
                for codigo in codigos:
                    atividadeId = re.sub(r'^\d{9}', '', codigo)
                    # COMO O USER ESTÁ EM ATIVIDADES ENTÃO VAMOS REMOVÊ-LO
                    EventDatabase.remover_user_atividades(atividadeId, nome, eventColl, "lista_participantes")
                    # E ADICIONAR OS NOVOS DADOS DO USER
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


