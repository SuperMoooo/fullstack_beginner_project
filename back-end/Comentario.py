class Comentario:
    # VARS
    nome : str
    codigo : str
    emocao : str

    # CONSTRUTOR
    def __init__(self, nome : str, comentario : str, emocao : str):
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

    def set_nome(self, nome : str):
        self.nome = nome

    def set_comentario(self, comentario: str):
        self.comentario = comentario

    def set_emocao(self, emocao: str):
        self.emocao = emocao

    # FIM ENCAPSULAMENTO