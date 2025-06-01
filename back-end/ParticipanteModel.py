from UtilizadorModel import UtilizadorModel
from datetime import datetime
from UtilizadorInterface import UtilizadorInterface

class ParticipanteModel(UtilizadorModel, UtilizadorInterface):
    # VARS

    codigos : list[str]

    # CONSTRUTOR

    def __init__(self, nome : str, email : str, data_nascimento : datetime, sexo : str, nif : str, password : str, tipo : str, codigos : list[str]):

        super().__init__(nome, email, data_nascimento, sexo, nif, password, tipo)

        self.codigos = codigos

    # ENCAPSULAMENTO

    # GETS

    def get_codigos(self):
        return self.codigos

    # SETS


    def set_codigos(self, codigos : list[str]):
        self.codigos = codigos

    # FIM ENCAPSULAMENTO

    # FUNCS

    # CRIAR ADMIN
    def criar_user(self, collection) -> bool:
        try:
            collection.insert_one(self.__dict__)
            return True
        except Exception as e:
            print(e)
            raise


    def adicionar_codigo(self, collection, atividade_id):
        try:
            updated = collection.update_one({"nome": self.get_nome()}, {"$push": {"codigos": self.get_nif() +  atividade_id}})
            return updated.modified_count
        except Exception as e:
            print(e)
            raise