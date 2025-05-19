from flask import Flask, jsonify, request
from flask_cors import CORS
from UserDatabase import UserDatabase
from UserModel import UserModel
from EventDatabase import EventDatabase

# APP
app = Flask(__name__)
# Ativar o CORS para Front ligar ao Back
CORS(app)


# VERIFICAR SE TEM TOKEN
@app.before_request
def verify_auth():
    # SE O REQUEST FOR ALGO RELACIONADO Á AUTH ENTÂO IGNORA, SENÃO, VERIFICA SEM TEM TOKEN DE AUTH
    if request.path != "/login" and request.path != "/register" and request.path != "/alterar-password":
        auth = request.authorization
        if auth.token != "83e395725af4e8ccf208f91b8d84ac2257d8c772":
            return jsonify({"Erro": "Não Autenticado"}), 401
    else:
        pass

# ::::::::::::: AUTH ::::::::::::::::

# LOGIN
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"Erro" : "Dados inválidos"}), 404
        # RECEBER USER DA DB
        userAux = UserDatabase.get_user_by_nome(data["nome"])
        userDB = UserDatabase(userAux)

        if userDB.check_login(data["password"]):
            return jsonify({"token": "83e395725af4e8ccf208f91b8d84ac2257d8c772"}), 200
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
            return jsonify({"Erro" : "Dados inválidos"}), 404
        user = UserModel(data["nome"], data["email"], data["password"])
        userDB = UserDatabase(user)
        success = userDB.criar_user()
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
            return jsonify({"Erro" : "Dados inválidos"}), 404
        # VERIFICAR SE USER EXISTE
        userAux = UserDatabase.get_user_by_nome(data["nome"])
        if userAux is None:
            return jsonify({"Erro": "Utilizador não encontrado"}), 404
        # VALIDAR NOVA PASSWORD
        if not UserModel.verificar_password(data["password"]):
            return jsonify({"Erro": "A password deve ter mais de 6 caracteres!"})
        userDB = UserDatabase(userAux)
        success = userDB.alterar_password(data["password"])
        if success:
            return jsonify({"Sucesso": "Password alterada com sucesso"}), 200
        else:
            return jsonify({"Erro" : "Dados inválidos"}), 404
    except Exception as e:
        return jsonify({"Erro" : str(e)}), 400


# ::::::::::::: FIM AUTH ::::::::::::::::

# ::::::::::::: EVENTO ::::::::::::::::

@app.route("/eventos", methods=['GET'])
def get_eventos():
    try:
        data = EventDatabase.get_eventos()
        return jsonify({"Data": data})
    except Exception as e:
        return jsonify({"Erro" : str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)