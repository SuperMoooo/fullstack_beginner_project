
from TipoUserModel import TipoUserModel

class AdminModel(TipoUserModel):
    # CONSTRUTOR
    def __init__(self, nome, email, data_nascimento, password, tipo):
        super().__init__(nome, email, data_nascimento, password, tipo)
