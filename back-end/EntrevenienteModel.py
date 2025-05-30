from UtilizadorModel import UtilizadorModel
from datetime import datetime
from UtilizadorInterface import UtilizadorInterface

class EntrevenienteModel(UtilizadorModel, UtilizadorInterface):
    #VARS

    eventos_id : list[int]

    # CONSTRUTOR
    def __init__(self, nome : str, email : str, data_nascimento : datetime, sexo : str, nif : str, password : str, tipo : str, eventos_id : list[int]):
        super().__init__(nome, email, data_nascimento, sexo, nif, password, tipo)

        self.eventos_id = eventos_id

    # ENCAPSULAMENTO

    # GETS

    def get_eventos_id(self):
        return self.eventos_id

    # SETS

    def set_eventos_id(self, eventos_id : list[int]):
        self.eventos_id = eventos_id

    # FUNCS

    # CRIAR ADMIN
    def criar_user(self, collection) -> bool:
        try:
            if UtilizadorModel.verificar_user_exists(collection, self.get_nome()):
                raise Exception('Este nome de utilizador já existe!')
            collection.insert_one(self.__dict__)
            return True
        except Exception as e:
            print(e)
            raise