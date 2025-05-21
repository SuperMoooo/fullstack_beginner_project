from TipoUserModel import TipoUserModel
from pymongo import MongoClient

class ParticipanteModel(TipoUserModel):
    #VARS

    eventos_id : list[int]

    # CONSTRUTOR
    def __init__(self, nome, email, data_nascimento, password, eventos_id, tipo):
        super().__init__(nome, email, data_nascimento, password, tipo)

        self.eventos_id = eventos_id

    # ENCAPSULAMENTO

    # GETS

    def get_eventos_id(self):
        return self.eventos_id

    # SETS

    def set_eventos_id(self, eventos_id):
        self.eventos_id = eventos_id