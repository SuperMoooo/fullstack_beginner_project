from pymongo import MongoClient
from UserModel import UserModel
class UserDatabase:
    # VARS
    user : UserModel

    # CONSTRUTOR
    def __init__(self, user: UserModel):
        self.user = user

    # ENCAPSULAMENTO

    # GETS

    def get_user(self):
        return self.user

    def set_user(self, user: UserModel):
        self.user = user

    # FUNÇÕES

    # VERIFICAR LOGIN
    def check_login(self, password) -> bool:
        try:
            if self.get_user().get_password() == password:
                return True
            return False
        except Exception as e:
            print(e)
            return False


    # ADICIONAR USER (SE JÁ NÃO EXISTIR) Á DB

    def criar_user(self) -> bool:
        try:
            client = MongoClient("mongodb://localhost:27017/")
            mydb = client["2_freq"]
            collection = mydb["users"]
            if self.verificar_user_exists():
                raise Exception('Este nome de utilizador já existe!')
            collection.insert_one(self.user.__dict__)
            return True
        except Exception as e:
            print(e)
            return False

    # VERIFICAR SE NOME DE UTILIZADOR JÁ EXISTE
    def verificar_user_exists(self) -> bool:
        data = self.get_users()
        for user in data:
            if self.user.get_nome().nome in user.values():
                return True
        return False


    # RECEBER TODOS OS USERS DA DB
    def get_users(self) :
        client = MongoClient("mongodb://localhost:27017/")
        mydb = client["2_freq"]
        collection = mydb["users"]
        result = collection.find({})
        return result

    # RETORNAR USER BY NOME
    @staticmethod
    def get_user_by_nome(nome) -> UserModel | None:
        client = MongoClient("mongodb://localhost:27017/")
        mydb = client["2_freq"]
        collection = mydb["users"]
        result = collection.find({})
        for user in result:
            if nome == user["nome"]:
                return UserModel(user["nome"], user["email"], user["password"])
        return None

    # ALTERAR PASSWORD
    def alterar_password(self, password) -> bool:
        try:
            # VERIFICAR SE USER EXISTE
            user = self.get_user_by_nome(self.get_user().nome)
            if user is None:
                raise Exception('User not found!')
            client = MongoClient("mongodb://localhost:27017/")
            mydb = client["2_freq"]
            collection = mydb["users"]
            collection.update_one({"nome": user.nome}, {"$set": {"password": password}})
            return True
        except Exception as e:
            print(e)
            return False



