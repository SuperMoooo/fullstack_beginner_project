from datetime import datetime
from AtividadesModel import AtividadesModel
from ParticipanteModel import ParticipanteModel

class EventModel:
    nome_evento : str
    data_evento : datetime
    lista_ativades : AtividadesModel
    lista_participantes : list[ParticipanteModel]

    # CONSTRUTOR
    def __init__(self, nome_evento, data_evento, lista_atividades, lista_participantes):
        self.nome_evento = nome_evento
        self.data_evento = data_evento
        self.lista_atividades = lista_atividades
        self.lista_participantes = lista_participantes
        
