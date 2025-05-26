from datetime import datetime
import re

class TipoUserModel:
    # VARS
    nome : str
    email : str
    data_nascimento : datetime
    password : str
    tipo : str

    def __init__(self, nome : str, email : str, data_nascimento : datetime, password : str, tipo : str):
        if nome == '':
            raise Exception('O nome não pode ser vazio')
        self.nome = nome

        if not self.verificar_email(email):
            raise Exception('Email invalido!')
        self.email = email

        if not self.verificar_data(data_nascimento):
            raise Exception('Data nascimento invalida!')
        self.data_nascimento = data_nascimento

        if not self.verificar_password(password):
            raise Exception('A password deve ter mais de 6 caracteres!')
        self.password = password

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
        if not self.verificar_email(email):
            raise Exception('Email invalido')
        self.email = email

    def set_data_nascimento(self, data_nascimento : datetime):
        if not self.verificar_data(data_nascimento):
            raise Exception('Data nascimento invalida!')
        self.data_nascimento = data_nascimento

    def set_password(self, password : str):
        if not self.verificar_password(password):
            raise Exception('A password deve ter mais de 6 caracteres!')
        self.password = password

    def set_tipo(self, tipo : str):
        if not self.verificar_tipo(tipo):
            raise Exception('Tipo invalido!')
        self.tipo = tipo

    # FIM ENCAPSULAMENTO

    # FUNÇÕES

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
        # VERIFICAR FORMATO DA DATA (dd/mm/yyyy)
        return re.fullmatch(r"admin|user|participante", tipo.lower())
