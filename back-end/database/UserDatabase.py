from ..models.TipoUserModel import TipoUserModel
from ..models.UserModel import UserModel
from ..models.AdminModel import AdminModel
from ..models.ParticipanteModel import ParticipanteModel

class UserDatabase:
    # VARS
    user : TipoUserModel

    # CONSTRUTOR
    def __init__(self, user):
        self.user = user

    # ENCAPSULAMENTO

    # GETS

    def get_user(self):
        return self.user

    # SETS

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
    def get_user_by_nome(nome : str, collection):
        user = collection.find({"nome": nome})
        if user:
            result = user[0]
            if result["tipo"] == "admin":
                return AdminModel(result["nome"], result["email"], result["data_nascimento"], result["password"], result["tipo"])
            elif result["tipo"] == "user":
                return UserModel(result["nome"], result["email"], result["data_nascimento"], result["password"], result["tipo"], result["nif"], "")
            elif result["tipo"] == "participante":
                return ParticipanteModel(result["nome"], result["email"], result["data_nascimento"], result["password"],[], result["tipo"] )
        return None

    # ALTERAR PASSWORD
    def alterar_password(self, password : str, collection) -> bool:
        try:
            collection.update_one({"nome": self.get_user().get_nome()}, {"$set": {"password": password}})
            return True
        except Exception as e:
            print(e)
            raise

    # ATUALIZAR USER
    def atualizar_user(self, updatedUserData, collection):
        try:
            collection.delete_one({"nome": self.get_user().get_nome()})
            collection.insert_one(updatedUserData.__dict__)
            return True
        except Exception as e:
            print(e)
            raise



    def apagar_user(self, collection):
        try:
            collection.delete_one({"nome": self.get_user().get_nome()})
            return True
        except Exception as e:
            print(e)
            raise