import csv
import json
from datetime import datetime

import spacy
import fitz
from fpdf import FPDF
from googletrans import Translator
import pandas as pd

from EventModel import EventModel
from AtividadesModel import AtividadesModel
from Comentario import Comentario

from ParticipanteModel import ParticipanteModel
from EntrevenienteModel import EntrevenienteModel

class Hooks:

    @staticmethod
    def get_csv_data(filepath):
        result = []
        # ABRE O CSV
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            # RECEBE AS LINHAS COM AS CHAVES (HEADER)
            rows = csv.DictReader(csvfile, delimiter=',')
            # COMO O CSV TEM AS ATIVIDADES EM FORMATO "JSON" (STRING) IREMOS CONVERTER PARA VERDADEIRO JSON
            for row in rows:
                row['lista_atividades'] = json.loads(row['lista_atividades'])  # Converter para json
                result.append(row)
        return result


    @staticmethod
    def dados_especificos(dados):
        # SE NÃO HOUVER PARTICIPANTES ENTÂO RETORNA SEM DADOS
        if not dados:
            return {"moda_sexo" : "Sem dados", "media_idade" : "Sem dados"}
        df = pd.DataFrame(dados)

        # CALCULA IDADE
        df["idade"] = datetime.today().year - df["data_nascimento"].str.split("/").str[2].astype(int)
        # MODA DO SEXO
        moda_sexo = df["sexo"].mode()[0]

        # MÉDIA DAS IDADES
        media_idade = df["idade"].mean()

        return {"moda_sexo" : moda_sexo, "media_idade" : media_idade}

    @staticmethod
    def criar_pdf(evento : EventModel, lingua : str):
        pdf = FPDF()
        # CRIA PÁGINA
        pdf.add_page()
        pdf.set_font('Arial', '', 14)
        pdf.cell(0, 10, evento.get_nome_evento(), ln=True, align='C') # ln = Quebra de linha
        # IREI CHAMAR O TRADUZIR TEXTO PARA CADA STRING E PASSO A LINGUA QUE QUERO O RESULTADO
        pdf.cell(0, 10, Hooks.traduzir_texto(f"Data do Evento: {evento.get_data_evento()}", lingua), ln=True)
        pdf.cell(0, 10, Hooks.traduzir_texto(f"Capacidade: {evento.get_capacidade_evento()} pessoas", lingua), ln=True)
        pdf.cell(0, 10, "-------------------------------------------", ln=True)
        pdf.cell(0,10,  Hooks.traduzir_texto("Atividades:", lingua), ln=True, )

        for atividade in evento.get_lista_atividades():
            aux = AtividadesModel("", atividade["data_atividade"], atividade["hora_atividade"], atividade["descricao_atividade"], atividade["localidade_atividade"], atividade["restricoes"], atividade["lista_participantes"], atividade["lista_entrevenientes"], atividade["comentarios"])
            pdf.cell(0,10,  Hooks.traduzir_texto(f"Descrição: {aux.get_descricao_atividade()}", lingua), ln=True)
            pdf.cell(0,10,  Hooks.traduzir_texto(f"Data: {aux.get_data_atividade()}", lingua), ln=True)
            pdf.cell(0,10,  Hooks.traduzir_texto(f"Hora: {aux.get_hora_atividade()}", lingua), ln=True)
            pdf.cell(0,10,  Hooks.traduzir_texto(f"Local: {aux.get_localidade_atividade()}", lingua), ln=True)
            pdf.cell(0,10,  Hooks.traduzir_texto(f"Restrições: {aux.get_restricoes()}", lingua), ln=True)
            pdf.cell(0,10,  Hooks.traduzir_texto(f"Participantes:", lingua), ln=True)
            for participante in aux.get_lista_participantes():
                parti = ParticipanteModel(participante["nome"], participante["email"], participante["data_nascimento"], participante["sexo"], participante["nif"], participante["password"], participante["tipo"], participante["codigos"])
                idade_user = datetime.today().year - int(parti.get_data_nascimento().split("/")[2])
                pdf.cell(0,10,  Hooks.traduzir_texto(f"Nome: {parti.get_nome()} | Idade: {idade_user} | Sexo: {parti.get_sexo()} | Nif: {parti.get_nif()}", lingua), ln=True)
            pdf.cell(0, 10,Hooks.traduzir_texto(f"Média Idades: {Hooks.dados_especificos(aux.get_lista_participantes())['media_idade']}", lingua), ln=True)
            pdf.cell(0, 10,Hooks.traduzir_texto(f"Moda do Sexo: {Hooks.dados_especificos(aux.get_lista_participantes())['moda_sexo']}", lingua), ln=True)
            pdf.cell(0,10,  "---------------------------------", ln=True)
            pdf.cell(0,10,  Hooks.traduzir_texto(f"Entrevenientes:", lingua), ln=True)
            for entreveniente in aux.get_lista_entrevenientes():
                entre = EntrevenienteModel(entreveniente["nome"], entreveniente["email"], entreveniente["data_nascimento"], entreveniente["sexo"], entreveniente["nif"], entreveniente["password"], entreveniente["tipo"])
                idade_user = datetime.today().year - int(entre.get_data_nascimento().split("/")[2])
                pdf.cell(0,10,  Hooks.traduzir_texto(f"Nome: {entre.get_nome()} | Idade: {idade_user} | Sexo: {entre.get_sexo()} | Nif: {entre.get_nif()}", lingua), ln=True)
                pdf.cell(0,10, "---------------------------------", ln=True)
            pdf.cell(0,10,  Hooks.traduzir_texto(f"Comentários:", lingua), ln=True)
            for coment in aux.get_comentarios():
                comentario = Comentario(coment["nome"], coment["comentario"], coment["emocao"])
                pdf.cell(0,10,  Hooks.traduzir_texto(f"User: {comentario.get_nome()}", lingua), ln=True)
                pdf.cell(0,10,  Hooks.traduzir_texto(f"Comentário: {comentario.get_comentario()} | {comentario.get_emocao()}", lingua), ln=True)
            pdf.cell(0,10, "---------------------------------", ln=True)

        pdf.output('evento_pdf.pdf')


    @staticmethod
    def anonimar_pdf(lingua, pdf_path):
        # CARREGAR OS MODELOS
        if lingua == "en":
            cerebro = spacy.load("en_core_web_trf")
        elif lingua == "it":
            cerebro = spacy.load("it_core_news_lg")
        else:
            cerebro = spacy.load("pt_core_news_lg")

        pdf_document = fitz.open(pdf_path)

        for page_num in range(len(pdf_document)):
            # GUARDA A PÁG
            page = pdf_document.load_page(page_num)
            # DETETA ENTIDADES
            Hooks.detect_and_anonymize_entities(page, cerebro)
        # GUARDA E FECHA
        pdf_document.save("evento_pdf_anonimado.pdf")
        pdf_document.close()



    @staticmethod
    def detect_and_anonymize_entities(page, cerebro):
        text = page.get_text("text")
        doc = cerebro(text)

        for ent in doc.ents:
            # TENTAR ANONIMAR TUDO
            #print(ent.label_)
            if ent.label_ in ["PER", "LOC", "MISC", "ORG", "TIME", "EVENT", "DATE", "QUANTITY"]:
                areas = page.search_for(ent.text)
                for area in areas:
                    # DESENHA UM RETANGULO PRETO
                    page.draw_rect(area, color=(0,0,0), fill=(0,0,0))


    @staticmethod
    def traduzir_texto(text, lingua):
        # SE FOR PORTUGUÊS ENTÂO NÂO TRADUZ
        if lingua == "pt":
            return text
        tradutor = Translator()
        # TRADUZ PARA A LINGUA DESEJADA
        resultado = tradutor.translate(text, src='pt', dest=lingua)
        return resultado.text