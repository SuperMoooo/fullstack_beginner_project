from pymongo import MongoClient
from TipoUserModel import TipoUserModel
class UserDatabase:
    # VARS
    user : TipoUserModel

    # CONSTRUTOR
    def __init__(self, user: TipoUserModel):
        self.user = user

    # ENCAPSULAMENTO

    # GETS

    def get_user(self):
        return self.user

    def set_user(self, user: TipoUserModel):
        self.user = user

    # FUNÇÕES

    # VERIFICAR LOGIN
    def check_login(self, password : str) -> bool:
        try:
            if self.get_user().get_password() == password:
                return True
            return False
        except Exception as e:
            print(e)
            return False


    # ADICIONAR USER (SE NÃO EXISTIR) Á DB

    def criar_user(self, collection) -> bool:
        try:
            if self.verificar_user_exists(collection):
                raise Exception('Este nome de utilizador já existe!')
            collection.insert_one(self.get_user().__dict__)
            return True
        except Exception as e:
            print(e)
            raise

    # VERIFICAR SE NOME DE UTILIZADOR JÁ EXISTE
    def verificar_user_exists(self, collection) -> bool:
        data = self.get_users(collection)
        for user in data:
            if self.get_user().get_nome() in user["nome"]:
                return True
        return False


    # RECEBER TODOS OS USERS DA DB
    def get_users(self, collection) :
        result = collection.find({})
        return result

    # RETORNAR USER BY NOME
    @staticmethod
    def get_user_by_nome(nome : str, collection) -> TipoUserModel | None:
        result = collection.find({})
        for user in result:
            if nome == user["nome"]:
                return TipoUserModel(user["nome"], user["email"], user["data_nascimento"], user["password"], user["tipo"])
        return None

    # ALTERAR PASSWORD
    def alterar_password(self, password : str, collection) -> bool:
        try:
            collection.update_one({"nome": self.get_user().get_nome()}, {"$set": {"password": password}})
            return True
        except Exception as e:
            print(e)
            return False



