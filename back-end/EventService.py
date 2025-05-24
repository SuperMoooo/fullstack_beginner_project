from flask import Flask, jsonify, request
from flask_cors import CORS
from UserDatabase import UserDatabase
from AdminModel import AdminModel
from EventDatabase import EventDatabase
from pymongo import MongoClient
from UserModel import UserModel
from ParticipanteModel import ParticipanteModel
from EventModel import EventModel
from AtividadesModel import AtividadesModel


# APP
app = Flask(__name__)

# Ativar o CORS
CORS(app)

# DATABASE
client = MongoClient("mongodb://localhost:27017/")
db = client["2_freq"]
collUsers = db["users"]
collEvents = db["events"]




# VERIFICAR SE TEM TOKEN
@app.before_request
def verify_auth():
    if request.method == 'OPTIONS':
        return None
    # SE O REQUEST FOR ALGO RELACIONADO Á AUTH ENTÂO IGNORA, SENÃO, VERIFICA SEM TEM TOKEN DE AUTH
    if request.path not in ["/login", "/register", "/alterar-password"]:
        auth = request.headers.get("Authorization")
        if auth != "Bearer 83e395725af4e8ccf208f91b8d84ac2257d8c772":
            return jsonify({"Erro": "Não Autenticado"}), 401
        return None
    return None

# ::::::::::::: AUTH ::::::::::::::::

# LOGIN
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"Erro" : "Dados inválidos"}), 400
        # RECEBER USER DA DB
        userAux = UserDatabase.get_user_by_nome(data["nome"], collUsers)
        userDB = UserDatabase(userAux)

        if userDB.check_login(data["password"]):
            return jsonify({"token": "83e395725af4e8ccf208f91b8d84ac2257d8c772", "tipo": userAux.get_tipo()}), 200
        else:
            return jsonify({"Erro": "Verifique as suas credenciais"}), 401
    except Exception as e:
        return jsonify({"Erro": str(e)}), 400

# REGISTAR
@app.route("/register", methods=['POST'])
def register():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"Erro" : "Dados inválidos"}), 400

        user = None
        if data["tipo"] == "admin":
            user = AdminModel(data["nome"], data["email"], data["data_nascimento"], data["password"], data["tipo"])
        elif data["tipo"] == "user":
            user = UserModel(data["nome"], data["email"], data["data_nascimento"], data["password"], data["tipo"], data["nif"], "")
        elif data["tipo"] == "participante":
            user = ParticipanteModel(data["nome"], data["email"], data["data_nascimento"], data["password"], data["tipo"], [])

        userDB = UserDatabase(user)
        success = userDB.criar_user(collUsers)
        if success:
            return jsonify({"Sucesso": "User criado"}), 200
        else:
            return jsonify({"Erro" : "Erro Desconhecido"}), 404
    except Exception as e:
        print(e)
        return jsonify({"Erro" : str(e)}), 400

# ALTERAR PASSWORD
@app.route("/alterar-password", methods=['PUT'])
def alterar_password():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"Erro" : "Dados inválidos"}), 400
        # VERIFICAR SE USER EXISTE
        userAux = UserDatabase.get_user_by_nome(data["nome"], collUsers)
        if userAux is None:
            return jsonify({"Erro": "Utilizador não encontrado"}), 404
        # VALIDAR NOVA PASSWORD
        if not AdminModel.verificar_password(data["password"]):
            return jsonify({"Erro": "A password deve ter mais de 6 caracteres!"})
        userDB = UserDatabase(userAux)
        success = userDB.alterar_password(data["password"], collUsers)
        if success:
            return jsonify({"Sucesso": "Password alterada com sucesso"}), 200
        else:
            return jsonify({"Erro" : "Dados inválidos"}), 404
    except Exception as e:
        return jsonify({"Erro" : str(e)}), 400


# ::::::::::::: FIM AUTH ::::::::::::::::

# ::::::::::::: EVENTO ::::::::::::::::

# RETORNA TODOS OS EVENTOS
@app.route("/eventos", methods=['GET'])
def get_eventos():
    try:
        data = EventDatabase.get_eventos(collEvents)
        if data is None:
            return jsonify({"Erro", "Sem eventos!"}), 404
        return jsonify({"Data": data})
    except Exception as e:
        print(e)
        return jsonify({"Erro" : str(e)}), 400

# RETORNA EVENTO PELO ID
@app.route("/evento/<int:id>", methods=['GET'])
def get_evento(id):
    try:
        data = EventDatabase.get_evento(id, collEvents)
        if data is None:
            return jsonify({"Erro" : "Evento não encontrado"}), 404
        return jsonify({"Sucesso": data})
    except Exception as e:
        return jsonify({"Erro" : str(e)}), 400


@app.route("/criar-evento", methods=['POST'])
def criar_evento():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"Erro" : "Dados inválidos"}), 400
        # VERIFICAR PERMISSÕES
        if data["user_tipo"] != "admin":
            return jsonify({"Erro" : "Não tem permissão para criar eventos"}), 401

        evento = EventModel(data["nome_evento"], data["data_evento"], data["lista_atividades"], [], [])
        sucess = EventDatabase.criar_evento(evento, collEvents)
        if sucess:
            return jsonify({"Sucesso": "Evento criado"}), 200
        else:
            return jsonify({"Erro" : "Erro ao criar evento"}), 400
    except Exception as e:
        return jsonify({"Erro" : str(e)}), 400

# VALIDAR INSERIR ATIVIDADE
@app.route("/validar-atividade", methods=['POST'])
def validar_atividade():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"Erro" : "Dados inválidos"}), 400
        AtividadesModel(data["data_atividade"], data["hora_atividade"], data["descricao_atividade"], data["localidade_atividade"], [])
        return jsonify({"Sucesso": "Atividade validada com sucesso"}), 200
    except Exception as e:
        return jsonify({"Erro" : str(e)}), 400



if __name__ == '__main__':
    app.run(debug=True)