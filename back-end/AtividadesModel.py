import re
from datetime import datetime
from ParticipanteModel import ParticipanteModel
import random
import string
from EntrevenienteModel import EntrevenienteModel

class AtividadesModel:

    # VARS

    identificador : str
    data_atividade : datetime
    hora_atividade : str
    descricao_atividade : str
    localidade_atividade : str
    restricoes : str
    lista_participantes : list[ParticipanteModel]
    lista_entrevenientes : list[EntrevenienteModel]
    comentarios : list[str]


    # CONSTRUTOR

    def __init__(self, identificador : str, data_atividade : datetime, hora_atividade : str, descricao_atividade : str, localidade_atividade : str, restricoes : str, lista_participantes: list[ParticipanteModel], lista_entrevenientes : list[EntrevenienteModel],  comentarios : list[str]):
        self.identificador = identificador
        if not AtividadesModel.validar_data(data_atividade):
            raise Exception("A data da atividade está num formato inválido")
        self.data_atividade = data_atividade
        if not AtividadesModel.validar_hora(hora_atividade):
            raise Exception("A hora da atividade está num formato inválido")
        self.hora_atividade = hora_atividade
        if descricao_atividade == '':
            raise Exception("A descrição da atividade não pode ser vazia")
        self.descricao_atividade = descricao_atividade

        if localidade_atividade == '':
            raise Exception("A localidade da atividade não pode ser vazia")
        self.localidade_atividade = localidade_atividade

        self.restricoes = restricoes

        self.lista_participantes = lista_participantes

        self.lista_entrevenientes = lista_entrevenientes

        self.comentarios = comentarios

    # ENCAPSULAMENTO

    # GETS

    def get_identificador(self):
        return self.identificador

    def get_data_atividade(self):
        return self.data_atividade

    def get_hora_atividade(self):
        return self.hora_atividade

    def get_descricao_atividade(self):
        return self.descricao_atividade

    def get_localidade_atividade(self):
        return self.localidade_atividade

    def get_restricoes(self):
        return self.restricoes

    def get_lista_participantes(self):
        return self.lista_participantes

    def get_lista_entrevenientes(self):
        return self.lista_entrevenientes

    def get_comentarios(self):
        return self.comentarios
    # SETS

    def set_data_atividade(self, data_atividade : datetime):
        if not AtividadesModel.validar_data(data_atividade):
            raise Exception("A data da atividade está num formato inválido")
        self.data_atividade = data_atividade

    def set_hora_atividade(self, hora_atividade : str):
        if not AtividadesModel.validar_hora(hora_atividade):
            raise Exception("A hora da atividade está num formato inválido")
        self.hora_atividade = hora_atividade

    def set_descricao_atividade(self, descricao_atividade : str):
        if descricao_atividade == '':
            raise Exception("A descrição da atividade não pode ser vazia")
        self.descricao_atividade = descricao_atividade

    def set_localidade_atividade(self, localidade_atividade : str):
        if localidade_atividade == '':
            raise Exception("A localidade da atividade não pode ser vazia")
        self.localidade_atividade = localidade_atividade

    def set_restricoes(self, restricoes : str):
        self.restricoes = restricoes

    def set_lista_participantes(self, lista_participantes : list[ParticipanteModel]):
        self.lista_participantes = lista_participantes

    def set_lista_entrevenientes(self, lista_entrevenientes : list[EntrevenienteModel]):
        self.lista_entrevenientes = lista_entrevenientes

    def set_comentarios(self, comentarios : list[str]):
        self.comentarios = comentarios

    # FIM ENCAPSULAMENTO

    # FUNCS
    @staticmethod
    def validar_data(data: datetime):
        # VERIFICAR FORMATO DA DATA (dd/mm/yyyy)
        return re.fullmatch(r"\d{2}/\d{2}/\d{4}$", str(data))

    @staticmethod
    def validar_hora(hora : str):
        # VERIFICAR FORMATO DA HORA (hh:mm)
        return re.fullmatch(r"\d{2}:\d{2}", str(hora))

    @staticmethod
    def identificador_aleatorio():
        caracteres = string.ascii_letters + string.digits
        return ''.join(random.choices(caracteres, k=15))