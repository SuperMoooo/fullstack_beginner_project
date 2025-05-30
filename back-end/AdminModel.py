
from UtilizadorModel import UtilizadorModel
from UtilizadorInterface import UtilizadorInterface

class AdminModel(UtilizadorModel, UtilizadorInterface):
    # CONSTRUTOR
    def __init__(self, nome, email, data_nascimento, sexo, nif, password, tipo):
        super().__init__(nome, email, data_nascimento, sexo, nif, password, tipo)


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