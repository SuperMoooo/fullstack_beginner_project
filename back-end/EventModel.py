import re
from datetime import datetime
from AtividadesModel import AtividadesModel
from ParticipanteModel import ParticipanteModel
from EventDatabase import EventDatabase

class EventModel:
    id : int
    nome_evento : str
    data_evento : datetime
    lista_ativades : list[AtividadesModel]
    lista_participantes : list[ParticipanteModel]

    # CONSTRUTOR
    def __init__(self, nome_evento, data_evento, lista_atividades, lista_participantes):
        id = EventModel.get_id()
        self.id = id
        if nome_evento == '':
            raise Exception('O nome do evento não pode ser vazio')
        self.nome_evento = nome_evento
        if not EventModel.validar_data(data_evento):
            raise Exception("A data do evento está num formato inválido")
        self.data_evento = data_evento
        if not lista_atividades :
            raise Exception("Lista de Atividades vazia")
        self.lista_atividades = lista_atividades
        if not lista_participantes :
            raise Exception("Lista de Participantes vazia")
        self.lista_participantes = lista_participantes

    # ENCAPSULAMENTO

    # GETS

    def get_nome_evento(self):
        return self.nome_evento

    def get_data_evento(self):
        return self.data_evento

    def get_lista_atividades(self):
        return self.lista_atividades

    def get_lista_participantes(self):
        return self.lista_participantes

    # SETS

    def set_nome_evento(self, nome_evento):
        if nome_evento == '':
            raise Exception('O nome do evento não pode ser vazio')
        self.nome_evento = nome_evento

    def set_data_evento(self, data_evento):
        if not EventModel.validar_data(data_evento):
            raise Exception("A data do evento está num formato inválido")
        self.data_evento = data_evento

    def set_lista_atividades(self, lista_atividades):
        if not lista_atividades :
            raise Exception("Lista de Atividades vazia")
        self.lista_atividades = lista_atividades

    def set_lista_participantes(self, lista_participantes):
        if not lista_participantes :
            raise Exception("Lista de Participantes vazia")
        self.lista_participantes = lista_participantes

    # FIM ENCAPSULAMENTO

    # FUNCS
    @staticmethod
    def validar_data(data: datetime):
        # VERIFICAR FORMATO DA DATA (dd/mm/yyyy)
        return re.fullmatch(r"\d{2}/\d{2}/\d{4}$", str(data))

    @staticmethod
    def get_id() -> int:
        last_id = EventDatabase.get_event_last_id()
        return last_id + 1
