from datetime import datetime
class EventModel:
    nome_evento : str
    data_evento : datetime
    lista_ativades : AtividadesModel

    # CONSTRUTOR
    def __init__(self, nome_evento, data_evento, lista_atividades, lista_participantes):
        self.nome_evento = nome_evento
