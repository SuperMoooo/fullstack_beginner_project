from UtilizadorModel import UtilizadorModel
from datetime import datetime
from UtilizadorInterface import UtilizadorInterface

class EntrevenienteModel(UtilizadorModel, UtilizadorInterface):

    # CONSTRUTOR
    def __init__(self, nome : str, email : str, data_nascimento : datetime, sexo : str, nif : str, password : str, tipo : str):
        super().__init__(nome, email, data_nascimento, sexo, nif, password, tipo)


    # FUNCS

    # CRIAR ADMIN
    def criar_user(self, collection) -> bool:
        try:
            collection.insert_one(self.__dict__)
            return True
        except Exception as e:
            print(e)
            raise