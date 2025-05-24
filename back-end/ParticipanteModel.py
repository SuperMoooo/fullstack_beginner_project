from TipoUserModel import TipoUserModel
from datetime import datetime

class ParticipanteModel(TipoUserModel):
    #VARS

    eventos_id : list[int]

    # CONSTRUTOR
    def __init__(self, nome : str, email : str, data_nascimento : datetime, password : str, eventos_id : list[int], tipo : str):
        super().__init__(nome, email, data_nascimento, password, tipo)

        self.eventos_id = eventos_id

    # ENCAPSULAMENTO

    # GETS

    def get_eventos_id(self):
        return self.eventos_id

    # SETS

    def set_eventos_id(self, eventos_id : list[int]):
        self.eventos_id = eventos_id