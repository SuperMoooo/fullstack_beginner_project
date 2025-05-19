import re


class ParticipanteModel:
    # VARS
    nif : int
    codigo : str

    # CONSTRUTOR

    def __init__(self, nif, codigo):
        if not ParticipanteModel.validar_nif(nif):
            raise Exception("Nif num formato invalido")
        self.nif = nif
        if codigo == '':
            raise Exception("O código não pode ser vazio")
        self.codigo = codigo

    # ENCAPSULAMENTO

    # GETS

    def get_nif(self):
        return self.nif

    def get_codigo(self):
        return self.codigo

    # SETS

    def set_nif(self, nif):
        if not ParticipanteModel.validar_nif(nif):
            raise Exception("Nif num formato invalido")
        self.nif = nif

    def set_codigo(self, codigo):
        if codigo == '':
            raise Exception("O código não pode ser vazio")
        self.codigo = codigo

    # FIM ENCAPSULAMENTO

    # FUNCS

    @staticmethod
    def validar_nif(nif : int):
        # VALIDAR NIF SE 9 digitos
        return re.fullmatch(r"\d{9}$", str(nif))