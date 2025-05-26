import re
from TipoUserModel import TipoUserModel
from datetime import datetime

class UserModel(TipoUserModel):
    # VARS

    nif : int
    codigo : str

    # CONSTRUTOR

    def __init__(self, nome : str, email : str, data_nascimento : datetime, password : str, tipo : str, nif : int, codigo : str):

        super().__init__(nome, email, data_nascimento, password, tipo)

        if not UserModel.validar_nif(nif):
            raise Exception("Nif num formato invalido")
        self.nif = nif
        self.codigo = codigo

    # ENCAPSULAMENTO

    # GETS

    def get_nif(self):
        return self.nif

    def get_codigo(self):
        return self.codigo

    # SETS

    def set_nif(self, nif : int):
        if not UserModel.validar_nif(nif):
            raise Exception("Nif num formato invalido")
        self.nif = nif

    def set_codigo(self, codigo : str):
        self.codigo = codigo

    # FIM ENCAPSULAMENTO

    # FUNCS

    @staticmethod
    def validar_nif(nif : int):
        # VALIDAR NIF SE 9 digitos
        return re.fullmatch(r"\d{9}$", str(nif))