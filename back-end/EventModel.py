import re
from datetime import datetime
from AtividadesModel import AtividadesModel
from EventDatabase import EventDatabase
from pymongo import MongoClient
from EntrevenienteModel import EntrevenienteModel

class EventModel:
    id : int
    nome_evento : str
    data_evento : datetime
    capacidade_evento: int
    lista_atividades : list[AtividadesModel]
    lista_entrevenientes : list[EntrevenienteModel]

    # CONSTRUTOR
    def __init__(self, nome_evento : str, data_evento :  datetime, capacidade_evento : int, lista_atividades : list[AtividadesModel], lista_entrevenientes : list[EntrevenienteModel]):
        self.id = EventModel.get_id()
        if nome_evento == '':
            raise Exception('O nome do evento não pode ser vazio')
        self.nome_evento = nome_evento
        if not EventModel.validar_data(data_evento):
            raise Exception("A data do evento está num formato inválido")
        self.data_evento = data_evento

        if int(capacidade_evento) < 0:
            raise Exception("A capacidade do evento têm de ser maior que 0")
        self.capacidade_evento = capacidade_evento


        if not lista_atividades:
            raise Exception("Lista de Atividades vazia, adicione pelo menos 1 atividade")

        self.lista_atividades = lista_atividades

        self.lista_entrevenientes = lista_entrevenientes


    # ENCAPSULAMENTO

    # GETS

    def get_nome_evento(self):
        return self.nome_evento

    def get_data_evento(self):
        return self.data_evento

    def get_capacidade_evento(self):
        return self.capacidade_evento

    def get_lista_atividades(self):
        return self.lista_atividades

    def get_lista_entrevenientes(self):
        return self.lista_entrevenientes


    # SETS

    def set_nome_evento(self, nome_evento : str):
        if nome_evento == '':
            raise Exception('O nome do evento não pode ser vazio')
        self.nome_evento = nome_evento

    def set_data_evento(self, data_evento : datetime):
        if not EventModel.validar_data(data_evento):
            raise Exception("A data do evento está num formato inválido")
        self.data_evento = data_evento

    def set_capacidade_evento(self, capacidade_evento : int):
        if int(capacidade_evento) < 0:
            raise Exception("A capacidade do evento têm de ser maior que 0")
        self.capacidade_evento = capacidade_evento


    def set_lista_atividades(self, lista_atividades : list[AtividadesModel]):
        if not lista_atividades :
            raise Exception("Lista de Atividades vazia")
        self.lista_atividades = lista_atividades

    def set_lista_entrevenientes(self, lista_entrevenientes : list[EntrevenienteModel]):
        self.lista_entrevenientes = lista_entrevenientes



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
