from datetime import datetime

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from pymongo import MongoClient

from EntrevenienteModel import EntrevenienteModel
from ParticipanteModel import ParticipanteModel
from AdminModel import AdminModel

from EventModel import EventModel
from AtividadesModel import AtividadesModel

from UtilizadorDatabase import UtilizadorDatabase
from EventDatabase import EventDatabase

from Hooks import Hooks


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


        response = UtilizadorDatabase.check_login(collUsers, data["nome"], data["password"])
        if response:
            return jsonify({"token": "83e395725af4e8ccf208f91b8d84ac2257d8c772", "tipo": response.get_tipo()}), 200
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

        # AO REGISTAR É PRECISO IDENTIFICAR O TIPO E CRIAR PELA PRIMEIRA VEZ O SEU OBJETO
        user = None
        if data["tipo"] == "Admin":
            user =  AdminModel(data["nome"], data["email"], data["data_nascimento"], data["sexo"], data["nif"], data["password"], data["tipo"])
        elif data["tipo"] == "Entreveniente":
            user = EntrevenienteModel(data["nome"], data["email"], data["data_nascimento"], data["sexo"], data["nif"], data["password"], data["tipo"] , [])
        elif data["tipo"] == "Participante":
            user =  ParticipanteModel(data["nome"], data["email"], data["data_nascimento"], data["sexo"], data["nif"], data["password"], data["tipo"], "" )

        if UtilizadorDatabase.verificar_user_exists(collUsers, user.get_nome()):
            raise Exception('Este nome de utilizador já existe!')
        success = user.criar_user(collUsers)
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
        user = UtilizadorDatabase.get_user_by_nome(data["nome"], collUsers)
        if user is None:
            return jsonify({"Erro": "Utilizador não encontrado"}), 404

        # VALIDAR NOVA PASSWORD
        if not user.verificar_password(data["password"]):
            return jsonify({"Erro": "A password deve ter mais de 6 caracteres!"})

        success = UtilizadorDatabase.alterar_password(data["nome"], data["password"], collUsers)
        if success:
            return jsonify({"Sucesso": "Password alterada com sucesso"}), 200
        else:
            return jsonify({"Erro" : "Dados inválidos"}), 404
    except Exception as e:
        return jsonify({"Erro" : str(e)}), 400


# ::::::::::::: FIM AUTH ::::::::::::::::

# ::::::::::::: USER :::::::::::::::::::

@app.route("/get-user/<string:nome>", methods=['GET'])
def get_user(nome):
    try:
        user = UtilizadorDatabase.get_user_by_nome(nome, collUsers)
        if user is None:
            return jsonify({"Erro": "Utilizador não encontrado!"}), 404
        return jsonify(user.__dict__), 200
    except Exception as e:
        print(e)
        return jsonify({"Erro" : str(e)}), 400

@app.route("/atualizar-user/<string:nome>", methods=['PUT'])
def atualizar_user(nome):
    try:
        data = request.get_json()

        user = UtilizadorDatabase.get_user_by_nome(nome, collUsers)

        if user is None:
            return jsonify({"Erro": "Utilizador não encontrado!"}), 404

        # VERIFICAR O TIPO
        updatedUserData = None
        if data["tipo"] == "Admin":
            updatedUserData =  AdminModel(data["nome"], data["email"], data["data_nascimento"], data["sexo"], data["nif"], data["password"], data["tipo"])
        elif data["tipo"] == "Entreveniente":
            updatedUserData = EntrevenienteModel(data["nome"], data["email"], data["data_nascimento"], data["sexo"], data["nif"], data["password"], data["tipo"] )
        elif data["tipo"] == "Participante":
            updatedUserData =  ParticipanteModel(data["nome"], data["email"], data["data_nascimento"], data["sexo"], data["nif"], data["password"], data["tipo"], [] )

        UtilizadorDatabase.atualizar_user(updatedUserData, collUsers, nome)
        return jsonify({"Sucesso": "User atualizado com sucesso"}), 200
    except Exception as e:
        print(e)
        return jsonify({"Erro" : str(e)}), 400

@app.route("/apagar-user/<string:nome>", methods=['DELETE'])
def apagar_user(nome):
    try:
        data = request.get_json()
        user = UtilizadorDatabase.get_user_by_nome(nome, collUsers)
        if user is None:
            return jsonify({"Erro": "Utilizador não encontrado!"}), 404

        if user.get_nome() == data["nome"]:
            if user.get_password() == data["password"]:
                user.apagar_user(collUsers)
                return jsonify({"Sucesso": "A sua conta foi apagada"}), 200
            else:
                return jsonify({"Erro": "A password não está certa!"}), 400
        else:
            return jsonify({"Erro": "O seu nome não está correto!"}), 400
    except Exception as e:
        print(e)
        return jsonify({"Erro" : str(e)}), 400

# ::::::::::::: EVENTO ::::::::::::::::

# RETORNA TODOS OS EVENTOS
@app.route("/eventos", methods=['GET'])
def get_eventos():
    try:
        data = EventDatabase.get_eventos(collEvents)
        if data is None:
            return jsonify({"Erro", "Sem eventos!"}), 404
        return jsonify(data)
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
        return jsonify(data)
    except Exception as e:
        print(e)
        return jsonify({"Erro" : str(e)}), 400


@app.route("/criar-evento", methods=['POST'])
def criar_evento():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"Erro" : "Dados inválidos"}), 400
        # VERIFICAR PERMISSÕES
        if data["user_tipo"] != "Admin":
            return jsonify({"Erro" : "Não tem permissão para criar eventos"}), 401
        atividades = [AtividadesModel(AtividadesModel.identificador_aleatorio(), d["data_atividade"], d["hora_atividade"], d["descricao_atividade"], d["localidade_atividade"], d["restricoes"], [],[], []) for d in data["lista_atividades"]]
        evento = EventModel(data["nome_evento"], data["data_evento"], data["capacidade_evento"], [ativi.__dict__ for ativi in atividades])
        sucess = EventDatabase.criar_evento(evento, collEvents)
        if sucess:
            return jsonify({"Sucesso": "Evento criado"}), 200

        return jsonify({"Erro" : "Erro ao criar evento"}), 400
    except Exception as e:
        return jsonify({"Erro" : str(e)}), 400

@app.route("/eliminar-evento/<int:id>", methods=['DELETE'])
def eliminar_evento(id):
    try:
        if not id:
            return jsonify({"Erro" : "Evento não encontrado"}), 400
        sucess = EventDatabase.eliminar_evento(id, collEvents)
        if sucess:
            return jsonify({"Sucesso": "Evento eliminado"}), 200
        return jsonify({"Erro" : "Erro ao eliminar evento"}), 400
    except Exception as e:
        return jsonify({"Erro" : str(e)}), 400


@app.route("/importar-evento", methods=['POST'])
def importar_evento():
    try:
        file = request.files['csvFile']
        if not file:
            return jsonify({"Erro" : "Ficheiro inválio"}), 400
        if file.content_type != "application/vnd.ms-excel":
            return jsonify({"Erro" : "Ficheiro não é csv"}), 400
        file.save("csv_file_evento.csv")
        result = Hooks.get_csv_data("./csv_file_evento.csv")
        for data in result:
            atividades = [AtividadesModel(AtividadesModel.identificador_aleatorio(), d["data_atividade"], d["hora_atividade"], d["descricao_atividade"], d["localidade_atividade"], d["restricoes"], [],[], []) for d in data["lista_atividades"]]
            evento = EventModel(data["nome_evento"], data["data_evento"], int(data["capacidade_evento"]), [ativi.__dict__ for ativi in atividades])
            sucess = EventDatabase.criar_evento(evento, collEvents)
            if not sucess:
                return jsonify({"Erro": "Não foi possivel importar o evento"}), 400
        file.close()
        return jsonify({"Sucesso": "Evento importado"}), 200
    except Exception as e:
        print(e)
        return jsonify({"Erro" : str(e)}), 400


@app.route("/exportar-evento-pdf/<int:id>/<string:lingua>", methods=['GET'])
def exportar_evento_pdf(id, lingua):
    try:
        if not id:
            return jsonify({"Erro" : "Evento não encontrado"}), 400
        if not lingua:
            return jsonify({"Erro" : "Linguagem não selecionada"}), 400

        evento = EventDatabase.get_evento(id, collEvents)

        if not evento:
            return jsonify({"Erro" : "Evento não encontrado"}), 400

        Hooks.criar_pdf(EventModel(evento["nome_evento"], evento["data_evento"], evento["capacidade_evento"], evento["lista_atividades"]), lingua)
        Hooks.anonimar_pdf(lingua, "./evento_pdf.pdf")
        return send_file("./evento_pdf_anonimado.pdf", as_attachment=True), 200

    except Exception as e:
        print(e)
        return jsonify({"Erro" : str(e)}), 400

# ADICIONAR PARTICIPANTE
@app.route("/evento/<int:eventoId>/atividade/<string:atividadeId>/adicionar-participante", methods=['PUT'])
def adicionar_participante(eventoId, atividadeId):
    try:
        data = request.get_json()
        if not eventoId or not atividadeId:
            return jsonify({"Erro" : "Evento ou atividade não encontrado"}), 400

        user = UtilizadorDatabase.get_user_by_nome(data["nome_participante"],collUsers)
        if not user :
            return jsonify({"Erro" : "Utilizador não encontrado"}), 400
        if user.get_tipo() != "Participante":
            return jsonify({"Erro" : "Utilizador não é participante"}), 400
        # VERIFICAR RESTRIÇÕES DA ATIVIDADE

        restricao = EventDatabase.get_atividade(atividadeId, collEvents)

        idade_user = datetime.today().year - int(user.get_data_nascimento().split("/")[2])

        if int(restricao[0]) > idade_user:
            return jsonify({"Erro" : "Utilizador não tem idade suficiente para entrar na atividade"}), 400
        sucess = EventDatabase.atualizar_atividade_listas_por_campo(atividadeId, user , collEvents, "lista_participantes")

        updated = user.adicionar_codigo(collUsers, atividadeId)

        if sucess and updated:
            return jsonify({"Sucesso" : "Participante adicionado"}), 200
        return jsonify({"Erro" : "Não foi possível adicionar o participante"}), 400
    except Exception as e:
        print(e)
        return jsonify({"Erro" : str(e)}), 400

# ADICIONAR ENTREVENIENTE
@app.route("/evento/<int:eventoId>/atividade/<string:atividadeId>/adicionar-entreveniente", methods=['PUT'])
def adicionar_entreveniente(eventoId, atividadeId):
    try:
        data = request.get_json()
        if not eventoId or not atividadeId:
            return jsonify({"Erro" : "Evento ou atividade não encontrado"}), 400

        user = UtilizadorDatabase.get_user_by_nome(data["nome_entreveniente"],collUsers)
        if not user :
            return jsonify({"Erro" : "Utilizador não encontrado"}), 400
        if user.get_tipo() != "Entreveniente":
            return jsonify({"Erro" : "Utilizador não é entreveniente"}), 400

        sucess = EventDatabase.atualizar_atividade_listas_por_campo(atividadeId, user , collEvents, "lista_entrevenientes")

        if sucess:
            return jsonify({"Sucesso" : "Entreveniente adicionado"}), 200
        return jsonify({"Erro" : "Não foi possível adicionar o entreveniente"}), 400
    except Exception as e:
        print(e)
        return jsonify({"Erro" : str(e)}), 400


# REMOVER PARTICIPANTE
@app.route("/evento/<int:eventoId>/atividade/<string:atividadeId>/remover-participante", methods=['PUT'])
def remover_participante(eventoId, atividadeId):
    try:
        data = request.get_json()
        if not eventoId or not atividadeId:
            return jsonify({"Erro" : "Evento ou atividade não encontrado"}), 400

        user = UtilizadorDatabase.get_user_by_nome(data["nome_participante"],collUsers)
        if not user :
            return jsonify({"Erro" : "Utilizador não encontrado"}), 400
        if user.get_tipo() != "Participante":
            return jsonify({"Erro" : "Utilizador não é participante"}), 400

        sucess = EventDatabase.remover_user_atividades(atividadeId, user , collEvents, "lista_participantes")
        # ADICIONAR CODIGOS DOS EVENTOS PARA VALIDAR AO USER
        if sucess:
            return jsonify({"Sucesso" : "Participante removido"}), 200
        return jsonify({"Erro" : "Não foi possível remover o participante"}), 400
    except Exception as e:
        print(e)
        return jsonify({"Erro" : str(e)}), 400

# REMOVER Entreveniente
@app.route("/evento/<int:eventoId>/atividade/<string:atividadeId>/remover-entreveniente", methods=['PUT'])
def remover_entreveniente(eventoId, atividadeId):
    try:
        data = request.get_json()
        if not eventoId or not atividadeId:
            return jsonify({"Erro" : "Evento ou atividade não encontrado"}), 400

        user = UtilizadorDatabase.get_user_by_nome(data["nome_entreveniente"],collUsers)
        if not user :
            return jsonify({"Erro" : "Utilizador não encontrado"}), 400
        if user.get_tipo() != "Entreveniente":
            return jsonify({"Erro" : "Utilizador não é entreveniente"}), 400

        sucess = EventDatabase.remover_user_atividades(atividadeId, user , collEvents, "lista_entrevenientes")
        # ADICIONAR EVENTOS IDS AO USER
        if sucess:
            return jsonify({"Sucesso" : "Entreveniente removido"}), 200
        return jsonify({"Erro" : "Não foi possível remover o entreveniente"}), 400
    except Exception as e:
        print(e)
        return jsonify({"Erro" : str(e)}), 400


# ::::::::::::: FIM EVENTO ::::::::::::::::


# ::::::::::::: ATIVIDADE ::::::::::::::::


# VALIDAR INSERIR ATIVIDADE
@app.route("/validar-atividade", methods=['POST'])
def validar_atividade():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"Erro" : "Dados inválidos"}), 400
        AtividadesModel("" ,data["data_atividade"], data["hora_atividade"], data["descricao_atividade"], data["localidade_atividade"], data["restricoes"], [], [], [])
        return jsonify({"Sucesso": "Atividade validada com sucesso"}), 200
    except Exception as e:
        print(e)
        return jsonify({"Erro" : str(e)}), 400

@app.route("/atualizar-atividade/<string:identificador>", methods=['PUT'])
def atualizar_atividade(identificador):
    try:
        data = request.get_json()
        if identificador is None or data is None:
            return jsonify({"Erro" : "Atividade não encontrada"}), 400
        updatedAtividade = AtividadesModel(identificador, data["data_atividade"], data["hora_atividade"], data["descricao_atividade"], data["localidade_atividade"], data["restricoes"], [], [], [])
        sucess = EventDatabase.atualizar_atividade(identificador, updatedAtividade,  collEvents)
        if sucess:
            return jsonify({"Sucesso": "Atividade atualizada"}), 200
        return jsonify({"Erro": "Não foi possível atualizar a atividade"}), 400
    except Exception as e:
        print(e)
        return jsonify({"Erro" : str(e)}), 400


@app.route("/eliminar-atividade/<string:identificador>", methods=['PUT'])
def eliminar_atividade(identificador):
    try:
        if not identificador:
            return jsonify({"Erro" : "Atividade não encontrada"}), 404
        sucess = EventDatabase.delete_atividade(identificador, collEvents)
        if sucess:
            return jsonify({"Sucesso": "Atividade removida com sucesso"}), 200

        return jsonify({"Erro": "Erro ao remover atividade"}), 400

    except Exception as e:
        return jsonify({"Erro" : str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)