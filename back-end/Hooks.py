import csv
import json

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
