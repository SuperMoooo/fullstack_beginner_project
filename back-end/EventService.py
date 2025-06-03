from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from pymongo import MongoClient
import speech_recognition as sr
import re
import threading
from datetime import datetime
from transformers import pipeline

from EntrevenienteModel import EntrevenienteModel
from ParticipanteModel import ParticipanteModel
from AdminModel import AdminModel

from EventModel import EventModel
from AtividadesModel import AtividadesModel
from Comentario import Comentario

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
    # SE O REQUEST FOR ALGO RELACIONADO Á AUTH ENTÂO IGNORA, SENÃO, VERIFICA SEM TEM TOKEN DA AUTH
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

        # VERIFICA LOGIN
        response = UtilizadorDatabase.check_login(collUsers, data["nome"], data["password"])

        if response:
            # RETORNA O TOKEN E O TIPO DO USER
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
            user = EntrevenienteModel(data["nome"], data["email"], data["data_nascimento"], data["sexo"], data["nif"], data["password"], data["tipo"] )
        elif data["tipo"] == "Participante":
            user =  ParticipanteModel(data["nome"], data["email"], data["data_nascimento"], data["sexo"], data["nif"], data["password"], data["tipo"], [] )

        # VERIFICA SE O NOME DO USER EXISTE
        if UtilizadorDatabase.verificar_user_exists(collUsers, user.get_nome()):
            raise Exception('Este nome de utilizador já existe!')

        success = user.criar_user(collUsers)

        if success:
            return jsonify({"Sucesso": "Utilizador criado"}), 200
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

        # RECEBER O USER
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

# RECEBER USER
@app.route("/get-user/<string:nome>", methods=['GET'])
def get_user(nome):
    try:
        # RECEBER USER
        user = UtilizadorDatabase.get_user_by_nome(nome, collUsers)
        if user is None:
            return jsonify({"Erro": "Utilizador não encontrado!"}), 404
        # RETORNA USER
        return jsonify(user.__dict__), 200
    except Exception as e:
        print(e)
        return jsonify({"Erro" : str(e)}), 400

# ATUALIZAR USER
@app.route("/atualizar-user/<string:nome>", methods=['PUT'])
def atualizar_user(nome):
    try:
        data = request.get_json()
        # RECEBER USER
        user = UtilizadorDatabase.get_user_by_nome(nome, collUsers)
        if user is None:
            return jsonify({"Erro": "Utilizador não encontrado!"}), 404

        codigos = []

        if user.get_tipo() == "Participante":
            # SE FOR PARTICIPANTE ENTÃO GUARDA OS CÓDIGOS PARA SE MANTEREM AO ATUALIZAR OS DADOS
            codigos = user.get_codigos()

        # VERIFICAR O TIPO
        updatedUserData = None
        if data["tipo"] == "Admin":
            updatedUserData =  AdminModel(data["nome"], data["email"], data["data_nascimento"], data["sexo"], data["nif"], data["password"], data["tipo"])
        elif data["tipo"] == "Entreveniente":
            updatedUserData = EntrevenienteModel(data["nome"], data["email"], data["data_nascimento"], data["sexo"], data["nif"], data["password"], data["tipo"] )
        elif data["tipo"] == "Participante":
            updatedUserData =  ParticipanteModel(data["nome"], data["email"], data["data_nascimento"], data["sexo"], data["nif"], data["password"], data["tipo"], codigos )

        # ATUALIZA USER
        UtilizadorDatabase.atualizar_user(updatedUserData, collUsers, nome, collEvents)

        return jsonify({"Sucesso": "Utilizador atualizado com sucesso"}), 200
    except Exception as e:
        print(e)
        return jsonify({"Erro" : str(e)}), 400

# APAGAR USER
@app.route("/apagar-user/<string:nome>", methods=['DELETE'])
def apagar_user(nome):
    try:
        data = request.get_json()
        # RECEBER USER
        user = UtilizadorDatabase.get_user_by_nome(nome, collUsers)
        if user is None:
            return jsonify({"Erro": "Utilizador não encontrado!"}), 404

        # VERIFICA SE O NOME E A PASSWORD SÃO OS DO USER E SE FOR ENTÃO ELIMINA O MESMO
        if user.get_nome() == data["nome"]:
            if user.get_password() == data["password"]:
                UtilizadorDatabase.apagar_user(collUsers, user.get_nome())

                return jsonify({"Sucesso": "A sua conta foi apagada"}), 200
            else:
                return jsonify({"Erro": "A password não está certa!"}), 400
        else:
            return jsonify({"Erro": "O seu nome não está correto!"}), 400
    except Exception as e:
        print(e)
        return jsonify({"Erro" : str(e)}), 400

# RECEBER CÓDIGOS DO USER
@app.route("/receber-codigos/<string:nome>", methods=['GET'])
def get_codigos(nome):
    try:
        if nome is None:
            return jsonify({"Erro", "Utilizador não encontrado!"}), 404

        # RECEBER USER
        user = UtilizadorDatabase.get_user_by_nome(nome, collUsers)

        # SE FOR PARTICIPANTE, RETORNA CODIGOS
        if user.get_tipo() == "Participante":
            return jsonify({"codigos": user.get_codigos()}), 200
        return jsonify({}), 404
    except Exception as e:
        print(e)
        return jsonify({"Erro" : str(e)}), 400

# ::::::::::::: FIM USER ::::::::::::::::

# ::::::::::::: EVENTO ::::::::::::::::

# RETORNA TODOS OS EVENTOS
@app.route("/eventos", methods=['GET'])
def get_eventos():
    try:
        # RECEBER EVENTOS
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
        # RECEBE EVENTO POR ID
        data = EventDatabase.get_evento(id, collEvents)
        if data is None:
            return jsonify({"Erro" : "Evento não encontrado"}), 404

        return jsonify(data)
    except Exception as e:
        print(e)
        return jsonify({"Erro" : str(e)}), 400

# CRIAR EVENTO
@app.route("/criar-evento", methods=['POST'])
def criar_evento():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"Erro" : "Dados inválidos"}), 400

        # VERIFICAR PERMISSÕES
        if data["user_tipo"] != "Admin":
            return jsonify({"Erro" : "Não tem permissão para criar eventos"}), 401

        # CRIAR OS OBJETOS COM OS DADOS DO FRONT-END
        atividades = [AtividadesModel(AtividadesModel.identificador_aleatorio(), d["data_atividade"], d["hora_atividade"], d["descricao_atividade"], d["localidade_atividade"], d["restricoes"], [],[], []) for d in data["lista_atividades"]]
        evento = EventModel(data["nome_evento"], data["data_evento"], data["capacidade_evento"], [ativi.__dict__ for ativi in atividades])
        # CRIAR EVENTO
        sucess = EventDatabase.criar_evento(evento, collEvents)
        if sucess:
            return jsonify({"Sucesso": "Evento criado"}), 200

        return jsonify({"Erro" : "Erro ao criar evento"}), 400
    except Exception as e:
        return jsonify({"Erro" : str(e)}), 400

# ATUALIZAR EVENTO
@app.route("/atualizar-evento/<int:id>", methods=['PUT'])
def atualizar_evento(id):
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"Erro" : "Dados inválidos"}), 400

        # VERIFICAR PERMISSÕES
        if data["user_tipo"] != "Admin":
            return jsonify({"Erro" : "Não tem permissão para atualizar eventos"}), 401
        # RECEBE EVENTO
        evento = EventDatabase.get_evento(id, collEvents)
        if not evento:
            return jsonify({"Erro" : "Evento não encontrado"}), 404

        atividades = [AtividadesModel(AtividadesModel.identificador_aleatorio(), d["data_atividade"], d["hora_atividade"], d["descricao_atividade"], d["localidade_atividade"], d["restricoes"], [],[], []) for d in data["lista_atividades"]]
        updatedEventoData = EventModel(data["nome_evento"], data["data_evento"], data["capacidade_evento"], [ativi.__dict__ for ativi in atividades])

        sucess = EventDatabase.atualizar_evento(evento["id"],updatedEventoData, collEvents)
        if sucess:
            return jsonify({"Sucesso": "Evento atualizado"}), 200

        return jsonify({"Erro" : "Erro ao atualizar evento"}), 400
    except Exception as e:
        return jsonify({"Erro" : str(e)}), 400

# ELIMINAR EVENTO
@app.route("/eliminar-evento/<int:id>", methods=['DELETE'])
def eliminar_evento(id):
    try:
        if not id:
            return jsonify({"Erro" : "Evento não encontrado"}), 400
        # ELIMINA O EVENTO
        sucess = EventDatabase.eliminar_evento(id, collEvents)
        if sucess:
            return jsonify({"Sucesso": "Evento eliminado"}), 200

        return jsonify({"Erro" : "Erro ao eliminar evento"}), 400
    except Exception as e:
        return jsonify({"Erro" : str(e)}), 400


# IMPORTAR EVENTO
@app.route("/importar-evento", methods=['POST'])
def importar_evento():
    try:
        # VAI RECEBER O FICHEIRO
        file = request.files['csvFile']
        if not file:
            return jsonify({"Erro" : "Ficheiro inválio"}), 400
        # VERIFICA SE É CSV
        if file.content_type != "text/csv":
            return jsonify({"Erro" : "Ficheiro não é csv"}), 400

        # GUARDA PARA DEPOIS PODER USAR O CAMINHO
        file.save("csv_file_evento.csv")
        # VAI BUSCAR A DATA DENTRO DO CSV
        result = Hooks.get_csv_data("./csv_file_evento.csv")
        for data in result:
            atividades = [AtividadesModel(AtividadesModel.identificador_aleatorio(), d["data_atividade"], d["hora_atividade"], d["descricao_atividade"], d["localidade_atividade"], d["restricoes"], [],[], []) for d in data["lista_atividades"]]
            evento = EventModel(data["nome_evento"], data["data_evento"], int(data["capacidade_evento"]), [ativi.__dict__ for ativi in atividades])

            # CRIA O EVENTO
            sucess = EventDatabase.criar_evento(evento, collEvents)
            if not sucess:
                return jsonify({"Erro": "Não foi possivel importar o evento"}), 400

        # FECHA O FICHEIRO
        file.close()
        return jsonify({"Sucesso": "Evento importado"}), 200
    except Exception as e:
        print(e)
        return jsonify({"Erro" : str(e)}), 400


# EXPORTAR EVENTO PELO ID E PELA LINGUA
@app.route("/exportar-evento-pdf/<int:id>/<string:lingua>", methods=['GET'])
def exportar_evento_pdf(id, lingua):
    try:
        if not id:
            return jsonify({"Erro" : "Evento não encontrado"}), 400
        if not lingua:
            return jsonify({"Erro" : "Linguagem não selecionada"}), 400

        # RECEBE O EVENTO
        evento = EventDatabase.get_evento(id, collEvents)

        if not evento:
            return jsonify({"Erro" : "Evento não encontrado"}), 400

        # CRIA O EVENTO
        Hooks.criar_pdf(EventModel(evento["nome_evento"], evento["data_evento"], evento["capacidade_evento"], evento["lista_atividades"]), lingua)
        # ANONIMA O EVENTO
        Hooks.anonimar_pdf(lingua, "./evento_pdf.pdf")
        # RETORNA O EVENTO
        return send_file("./evento_pdf_anonimado.pdf", as_attachment=True), 200

    except Exception as e:
        print(e)
        return jsonify({"Erro" : str(e)}), 400


# ::::::::::::: FIM EVENTO ::::::::::::::::


# ::::::::::::: ATIVIDADE ::::::::::::::::


# ADICIONAR PARTICIPANTE
@app.route("/evento/<int:eventoId>/atividade/<string:atividadeId>/adicionar-participante", methods=['PUT'])
def adicionar_participante(eventoId, atividadeId):
    try:
        data = request.get_json()
        if not eventoId or not atividadeId:
            return jsonify({"Erro" : "Evento ou atividade não encontrado"}), 400
        # RECEBER USER
        user = UtilizadorDatabase.get_user_by_nome(data["nome_participante"], collUsers)
        if not user :
            return jsonify({"Erro" : "Utilizador não encontrado"}), 400
        if user.get_tipo() != "Participante":
            return jsonify({"Erro" : "Utilizador não é participante"}), 400

        # VERIFICAR RESTRIÇÕES DA ATIVIDADE E EVENTO
        evento = EventDatabase.get_evento(eventoId, collEvents)
        atividade = EventDatabase.get_atividade(atividadeId, collEvents)

        if int(evento["capacidade_evento"]) == len(atividade["lista_participantes"]):
            return jsonify({"Erro" : "Este evento já está na capacidade máxima"}), 400

        restricao_idade = re.findall(r"\d+", atividade["restricoes"])
        idade_user = datetime.today().year - int(user.get_data_nascimento().split("/")[2])

        if restricao_idade and int(restricao_idade[0]) > idade_user:
            return jsonify({"Erro" : "Utilizador não tem idade suficiente para entrar na atividade"}), 400


        codigo = user.get_nif() +  atividadeId
        updated = user.adicionar_codigo(collUsers, codigo)
        user.set_codigos([codigo])
        EventDatabase.atualizar_atividade_listas_por_campo(atividadeId, user, collEvents, "lista_participantes")

        if updated:
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
        # RECEBER USER
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
        # RECEBER USER
        user = UtilizadorDatabase.get_user_by_nome(data["nome_participante"],collUsers)
        if not user :
            return jsonify({"Erro" : "Utilizador não encontrado"}), 400
        if user.get_tipo() != "Participante":
            return jsonify({"Erro" : "Utilizador não é participante"}), 400

        sucess = EventDatabase.remover_user_atividades(atividadeId, user.get_nome() , collEvents, "lista_participantes")
        user.remover_codigo(collUsers, atividadeId)
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
        # RECEBER USER
        user = UtilizadorDatabase.get_user_by_nome(data["nome_entreveniente"],collUsers)
        if not user :
            return jsonify({"Erro" : "Utilizador não encontrado"}), 400
        if user.get_tipo() != "Entreveniente":
            return jsonify({"Erro" : "Utilizador não é entreveniente"}), 400

        sucess = EventDatabase.remover_user_atividades(atividadeId, user.get_nome() , collEvents, "lista_entrevenientes")
        # ADICIONAR EVENTOS IDS AO USER
        if sucess:
            return jsonify({"Sucesso" : "Entreveniente removido"}), 200
        return jsonify({"Erro" : "Não foi possível remover o entreveniente"}), 400
    except Exception as e:
        print(e)
        return jsonify({"Erro" : str(e)}), 400


# VALIDAR ATIVIDADE
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

# ATUALIZAR ATIVIDADE
@app.route("/atualizar-atividade/<string:atividadeId>", methods=['PUT'])
def atualizar_atividade(atividadeId):
    try:
        data = request.get_json()
        if atividadeId is None or data is None:
            return jsonify({"Erro" : "Atividade não encontrada"}), 400

        atividade = EventDatabase.get_atividade(atividadeId, collEvents)
        print(len(atividade["lista_participantes"]) > 0 or len(atividade["lista_entrevenientes"]) > 0)
        if len(atividade["lista_participantes"]) > 0 or len(atividade["lista_entrevenientes"]) > 0:
            return jsonify({"Erro": "Não pode atualizar a atividade quando existem pessoas já inscritas na mesma"}), 400

        updatedAtividade = AtividadesModel(atividadeId, data["data_atividade"], data["hora_atividade"], data["descricao_atividade"], data["localidade_atividade"], data["restricoes"], [], [], [])
        sucess = EventDatabase.atualizar_atividade(atividadeId, updatedAtividade,  collEvents)

        if sucess:
            return jsonify({"Sucesso": "Atividade atualizada"}), 200
        return jsonify({"Erro": "Não foi possível atualizar a atividade"}), 400
    except Exception as e:
        print(e)
        return jsonify({"Erro" : str(e)}), 400


# ELIMINAR ATIVIDADE
@app.route("/eliminar-atividade/<string:atividadeId>", methods=['PUT'])
def eliminar_atividade(atividadeId):
    try:
        if not atividadeId:
            return jsonify({"Erro" : "Atividade não encontrada"}), 404
        sucess = EventDatabase.delete_atividade(atividadeId, collEvents)
        if sucess:
            return jsonify({"Sucesso": "Atividade removida com sucesso"}), 200

        return jsonify({"Erro": "Erro ao remover atividade"}), 400

    except Exception as e:
        return jsonify({"Erro" : str(e)}), 400


# OUVIR O MICROFONE
@app.route("/ouvir", methods=["GET"])
def ouvir():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            texto = recognizer.recognize_google(audio, language='pt-PT')
            return jsonify({'texto': texto}) , 200
        except sr.UnknownValueError:
            return jsonify({'texto': 'Audio não reconhecido.'}), 404
        except sr.RequestError:
            return jsonify({'texto': 'Erro desconhecido.'}) , 404


# VALIDAR CÓDIGO
@app.route("/validar-codigo/<string:atividadeId>", methods=['POST'])
def validar_codigo(atividadeId):
    try:
        if not atividadeId:
            return jsonify({"Erro" : "Atividade não encontrada"}), 404
        data = request.get_json()
        if not data:
            return jsonify({"Erro" : "Dados inválidos"}), 404

        nome = data["nome"]
        codigo = data["codigo"]
        nif = data["nif"]
        # RECEBER USER
        user = UtilizadorDatabase.get_user_by_nome(nome, collUsers)
        if not user:
            return jsonify({"Erro" : "Utilizador não encontrado"}), 404

        res = {}
        threadAux = threading.Thread(target=EventDatabase.validar_codigo, args=(user, nif, codigo, atividadeId, collUsers, res))
        threadAux.start()
        threadAux.join()
        if res.get("sucesso"):
            return jsonify({"Sucesso": "O código é válido"}), 200

        return jsonify({"Erro" : "Código inválido"}), 404
    except Exception as e:
        print(e)
        return jsonify({"Erro" : str(e)}), 400


# ADICIONAR COMENTÁRIO Á ATIVIDADE
@app.route("/atividade/<string:atividadeId>/comentar", methods=['POST'])
def comentar(atividadeId):
    try:
        sentimento_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
        if not atividadeId:
            return jsonify({"Erro" : "Atividade não encontrada"}), 404
        data = request.get_json()
        if not data:
            return jsonify({"Erro" : "Dados inválidos"}), 404
        # RECEBER USER
        user = UtilizadorDatabase.get_user_by_nome(data["nome"], collUsers)
        coment = data["comentario"]
        emocao = sentimento_pipeline(coment)[0]
        if len(coment) > 100:
            return jsonify({"Erro" : "O seu comentário não pode exceder mais de 100 caracteres"}), 404
        comentario = Comentario(user.get_nome(), coment, emocao["label"])

        sucess = EventDatabase.adicionar_comentario(atividadeId, comentario, collEvents)
        if sucess:
            return jsonify({"Sucesso" : "Comentário adicionado"}), 200
        return jsonify({"Erro" : "Erro ao adicionar comentário"}), 404

    except Exception as e:
        print(e)
        return jsonify({"Erro" : str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)