class Comentario:
    # VARS
    nome : str
    codigo : str
    emocao : str

    # CONSTRUTOR
    def __init__(self, nome, comentario, emocao):
        self.nome = nome
        self.comentario = comentario
        self.emocao = emocao

    # ENCAPSULAMENTO

    # GETS

    def get_nome(self):
        return self.nome

    def get_comentario(self):
        return self.comentario

    def get_emocao(self):
        return self.emocao

    # SETS

    def set_nome(self, nome):
        self.nome = nome

    def set_comentario(self, comentario):
        self.comentario = comentario

    def set_emocao(self, emocao):
        self.emocao = emocao

    # FIM ENCAPSULAMENTO