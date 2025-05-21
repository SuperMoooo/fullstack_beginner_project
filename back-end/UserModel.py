import re
from TipoUserModel import TipoUserModel


class UserModel(TipoUserModel):
    # VARS

    nif : int
    codigo : str

    # CONSTRUTOR

    def __init__(self, nome, email, data_nascimento, password, tipo, nif, codigo ):

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

    def set_nif(self, nif):
        if not UserModel.validar_nif(nif):
            raise Exception("Nif num formato invalido")
        self.nif = nif

    def set_codigo(self, codigo):
        self.codigo = codigo

    # FIM ENCAPSULAMENTO

    # FUNCS

    @staticmethod
    def validar_nif(nif : int):
        # VALIDAR NIF SE 9 digitos
        return re.fullmatch(r"\d{9}$", str(nif))