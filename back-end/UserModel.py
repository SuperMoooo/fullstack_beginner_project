import re

class UserModel:
    # VARS
    nome : str
    email : str
    password : str

    # CONSTRUTOR
    def __init__(self, nome, email, password):
        self.nome = nome
        if not self.verificar_email(email):
            raise Exception('Email invalido!')
        self.email = email
        if not self.verificar_password(password):
            raise Exception('A password deve ter mais de 6 caracteres!')
        self.password = password

    # ENCAPSULAMENTO

    # GETS
    def get_nome(self):
        return self.nome

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password

    # SETS

    def set_nome(self, nome):
        self.nome = nome

    def set_email(self, email):
        if not self.verificar_email(email):
            raise Exception('Email invalido')
        self.email = email

    def set_password(self, password):
        if not self.verificar_password(password):
            raise Exception('A password deve ter mais de 6 caracteres!')
        self.password = password

    # FIM ENCAPSULAMENTO

    # FUNÇÕES

    @staticmethod
    def verificar_email(email):
        return re.fullmatch(r"^\S+@\S+\.\S+$", email)

    @staticmethod
    def verificar_password(password):
        return len(password) > 6