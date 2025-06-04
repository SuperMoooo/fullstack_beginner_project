from datetime import datetime
import re

class UtilizadorModel:
    # VARS
    nome : str
    email : str
    data_nascimento : datetime
    sexo : str
    nif : str
    password : str
    tipo : str

    def __init__(self, nome : str, email : str, data_nascimento : datetime, sexo: str, nif : str, password : str, tipo : str):
        if nome == '':
            raise Exception('O nome não pode ser vazio')
        self.nome = nome

        # VALIDAR FORMATO EMAIL
        if not self.verificar_email(email):
            raise Exception('Email invalido!')
        self.email = email

        # VALIDAR FORMATO DATA
        if not self.verificar_data(data_nascimento):
            raise Exception('Data nascimento invalida!')
        self.data_nascimento = data_nascimento

        # VALIDAR SEXO
        if not self.verificar_sexo(sexo):
            raise Exception('Sexo invalido!')
        self.sexo = sexo

        # VALIDAR FORMATO DO NIF
        if not self.verificar_nif(nif):
            raise Exception('Nif invalido!')
        self.nif = nif

        # VALIDAR PASSWORD
        if not self.verificar_password(password):
            raise Exception('A password deve ter mais de 6 caracteres!')
        self.password = password

        # VALIDAR TIPO
        if not self.verificar_tipo(tipo):
            raise Exception('Tipo invalido!')
        self.tipo = tipo


    # ENCAPSULAMENTO

    # GETS
    def get_nome(self):
        return self.nome

    def get_email(self):
        return self.email

    def get_data_nascimento(self):
        return self.data_nascimento

    def get_sexo(self):
        return self.sexo

    def get_nif(self):
        return self.nif

    def get_password(self):
        return self.password

    def get_tipo(self):
        return self.tipo



    # SETS

    def set_nome(self, nome : str):
        if nome == '':
            raise Exception('O nome não pode ser vazio')
        self.nome = nome

    def set_email(self, email : str):
        # VALIDAR FORMATO EMAIL
        if not self.verificar_email(email):
            raise Exception('Email invalido')
        self.email = email

    def set_data_nascimento(self, data_nascimento : datetime):
        # VALIDAR FORMATO DATA
        if not self.verificar_data(data_nascimento):
            raise Exception('Data nascimento invalida!')
        self.data_nascimento = data_nascimento

    def set_sexo(self, sexo : str):
        # VALIDAR SEXO
        if not self.verificar_sexo(sexo):
            raise Exception('Sexo invalido!')
        self.sexo = sexo

    def set_nif(self, nif : str):
        # VALIDAR FORMATO DO NIF
        if not self.verificar_nif(nif):
            raise Exception('Nif invalido!')
        self.nif = nif

    def set_password(self, password : str):
        # VALIDAR PASSWORD
        if not self.verificar_password(password):
            raise Exception('A password deve ter mais de 6 caracteres!')
        self.password = password

    def set_tipo(self, tipo : str):
        # VALIDAR TIPO
        if not self.verificar_tipo(tipo):
            raise Exception('Tipo invalido!')
        self.tipo = tipo

    # FIM ENCAPSULAMENTO

    # FUNÇÕES

    # VERIFICAÇÕES

    @staticmethod
    def verificar_email(email : str):
        return re.fullmatch(r"^\S+@\S+\.\S+$", email)

    @staticmethod
    def verificar_password(password : str):
        # PASSWORD TEM DE SER MAIS DE 6 CHARS
        return len(password) > 6

    @staticmethod
    def verificar_data(data : datetime):
        # VERIFICAR FORMATO DA DATA (dd/mm/yyyy)
        return re.fullmatch(r"\d{2}/\d{2}/\d{4}$", str(data))

    @staticmethod
    def verificar_tipo(tipo : str):
        # VERIFICAR SE É UM DOS 3 TIPOS
        return re.fullmatch(r"admin|entreveniente|participante", tipo.lower())

    @staticmethod
    def verificar_sexo(sexo : str):
        # VALIDAR SEXO
        return re.fullmatch(r"homem|mulher|outro|prefiro não dizer", sexo.lower())

    @staticmethod
    def verificar_nif(nif : str):
        # VALIDAR SE O NIF TEM SÓ 9 digitos
        return re.fullmatch(r"\d{9}$", nif)
