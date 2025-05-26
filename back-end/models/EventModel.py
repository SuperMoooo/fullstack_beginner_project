import re
from datetime import datetime
from AtividadesModel import AtividadesModel
from ..database.EventDatabase import EventDatabase
from pymongo import MongoClient
from UserModel import UserModel

class EventModel:
    id : int
    nome_evento : str
    data_evento : datetime
    lista_atividades : list[AtividadesModel]
    lista_utilizadores : list[UserModel]
    comentarios : list[str]

    # CONSTRUTOR
    def __init__(self, nome_evento : str, data_evento :  datetime, lista_atividades : list[AtividadesModel], lista_utilizadores : list[UserModel], comentarios : list[str]):
        self.id = EventModel.get_id()
        if nome_evento == '':
            raise Exception('O nome do evento não pode ser vazio')
        self.nome_evento = nome_evento
        if not EventModel.validar_data(data_evento):
            raise Exception("A data do evento está num formato inválido")
        self.data_evento = data_evento
        if not lista_atividades :
            raise Exception("Lista de Atividades vazia")
        self.lista_atividades = lista_atividades

        self.lista_utilizadores = lista_utilizadores
        self.comentarios = comentarios

    # ENCAPSULAMENTO

    # GETS

    def get_nome_evento(self):
        return self.nome_evento

    def get_data_evento(self):
        return self.data_evento

    def get_lista_atividades(self):
        return self.lista_atividades

    def get_lista_utilizadores(self):
        return self.lista_utilizadores

    def get_comentarios(self):
        return self.comentarios

    # SETS

    def set_nome_evento(self, nome_evento : str):
        if nome_evento == '':
            raise Exception('O nome do evento não pode ser vazio')
        self.nome_evento = nome_evento

    def set_data_evento(self, data_evento : datetime):
        if not EventModel.validar_data(data_evento):
            raise Exception("A data do evento está num formato inválido")
        self.data_evento = data_evento

    def set_lista_atividades(self, lista_atividades : list[AtividadesModel]):
        if not lista_atividades :
            raise Exception("Lista de Atividades vazia")
        self.lista_atividades = lista_atividades

    def set_lista_utilizadores(self, lista_utilizadores : list[UserModel]):
        self.lista_utilizadores = lista_utilizadores

    def set_comentarios(self, comentarios : list[str]):
        self.comentarios = comentarios

    # FIM ENCAPSULAMENTO

    # FUNCS
    @staticmethod
    def validar_data(data: datetime):
        # VERIFICAR FORMATO DA DATA (dd/mm/yyyy)
        return re.fullmatch(r"\d{2}/\d{2}/\d{4}$", str(data))

    @staticmethod
    def get_id() -> int:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["2_freq"]
        collEvents = db["events"]

        last_id = EventDatabase.get_event_last_id(collEvents)
        return last_id + 1
