import re
from datetime import datetime


class AtividadesModel:

    # VARS

    data_atividade : datetime
    hora_atividade : str
    descricao_atividade : str
    localidade_atividade : str

    # CONSTRUTOR

    def __init__(self, data_atividade, hora_atividade, descricao_atividade, localidade_atividade):
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

    # ENCAPSULAMENTO

    # GETS

    def get_data_atividade(self):
        return self.data_atividade

    def get_hora_atividade(self):
        return self.hora_atividade

    def get_descricao_atividade(self):
        return self.descricao_atividade

    def get_localidade_atividade(self):
        return self.localidade_atividade

    # SETS

    def set_data_atividade(self, data_atividade):
        if not AtividadesModel.validar_data(data_atividade):
            raise Exception("A data da atividade está num formato inválido")
        self.data_atividade = data_atividade

    def set_hora_atividade(self, hora_atividade):
        if not AtividadesModel.validar_hora(hora_atividade):
            raise Exception("A hora da atividade está num formato inválido")
        self.hora_atividade = hora_atividade

    def set_descricao_atividade(self, descricao_atividade):
        if descricao_atividade == '':
            raise Exception("A descrição da atividade não pode ser vazia")
        self.descricao_atividade = descricao_atividade

    def set_localidade_atividade(self, localidade_atividade):
        if localidade_atividade == '':
            raise Exception("A localidade da atividade não pode ser vazia")
        self.localidade_atividade = localidade_atividade

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