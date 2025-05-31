import csv
import json

import spacy
import fitz
from fpdf import FPDF
from googletrans import Translator

from EventModel import EventModel
from AtividadesModel import AtividadesModel

class Hooks:

    @staticmethod
    def get_csv_data(filepath):
        result = []
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            rows = csv.DictReader(csvfile, delimiter=',')
            for row in rows:
                row['lista_atividades'] = json.loads(row['lista_atividades'])  # Converter para json
                result.append(row)
        return result

    @staticmethod
    def criar_pdf(evento : EventModel, lingua : str):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', '', 14)
        pdf.cell(0, 10, evento.get_nome_evento(), ln=True, align='C') # ln = Quebra de linha
        pdf.cell(0, 10, Hooks.traduzir_texto(f"Data do Evento: {evento.get_data_evento()}", lingua), ln=True)
        pdf.cell(0, 10, Hooks.traduzir_texto(f"Capacidade: {evento.get_capacidade_evento()} pessoas", lingua), ln=True)
        pdf.cell(0, 10, "-------------------------------------------", ln=True)
        pdf.cell(0,10,  Hooks.traduzir_texto("Atividades:", lingua), ln=True, )

        for atividade in evento.get_lista_atividades():
            aux = AtividadesModel("", atividade["data_atividade"], atividade["hora_atividade"], atividade["descricao_atividade"], atividade["localidade_atividade"], atividade["restricoes"], atividade["lista_participantes"], atividade["lista_entrevenientes"], atividade["comentarios"])
            pdf.cell(0,10,  Hooks.traduzir_texto(f"Descrição: {aux.get_descricao_atividade()}", lingua), ln=True,)
            pdf.cell(0,10,  Hooks.traduzir_texto(f"Data: {aux.get_data_atividade()}", lingua), ln=True,)
            pdf.cell(0,10,  Hooks.traduzir_texto(f"Hora: {aux.get_hora_atividade()}", lingua), ln=True,)
            pdf.cell(0,10,  Hooks.traduzir_texto(f"Local: {aux.get_localidade_atividade()}", lingua), ln=True,)
            pdf.cell(0,10,  Hooks.traduzir_texto(f"Restrições: {aux.get_restricoes()}", lingua), ln=True,)
            pdf.cell(0,10,  Hooks.traduzir_texto(f"Participantes: {aux.get_lista_participantes()}", lingua), ln=True,)
            pdf.cell(0,10,  Hooks.traduzir_texto(f"Entrevenientes: {aux.get_lista_entrevenientes()}", lingua), ln=True,)
            pdf.cell(0,10,  Hooks.traduzir_texto(f"Comentários: {aux.get_comentarios()}", lingua), ln=True,)
            pdf.cell(0,10, "---------------------------", ln=True,)

        pdf.output('evento_pdf.pdf')


    @staticmethod
    def anonimar_pdf(lingua, pdf_path):
        if lingua == "en":
            cerebro = spacy.load("en_core_web_trf")
        elif lingua == "it":
            cerebro = spacy.load("it_core_news_lg")
        else:
            cerebro = spacy.load("pt_core_news_lg")

        pdf_document = fitz.open(pdf_path)

        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            Hooks.detect_and_anonymize_entities(page, cerebro)

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
                    page.draw_rect(area, color=(0,0,0), fill=(0,0,0))


    @staticmethod
    def traduzir_texto(text, lingua):
        tradutor = Translator()
        resultado = tradutor.translate(text, src='pt', dest=lingua)
        return resultado.text