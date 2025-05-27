import os
import requests
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

def coletar_dados_clima(cidade):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={cidade}&lang=pt"
        resp = requests.get(url).json()

        if 'current' not in resp:
            print(f"Erro na resposta para {cidade}: {resp}")
            return None

        dados = resp['current']
        return {
            'cidade': cidade,
            'temperatura': dados['temp_c'],
            'sensacao_termica': dados['feelslike_c'],
            'umidade': dados['humidity'],
            'vento': dados['wind_kph'],
            'descricao': dados['condition']['text'],
            'icone_descricao': dados['condition']['icon'],
            'ponto_orvalho': dados['dewpoint_c'],
            'precipitacao': dados['precip_mm'],
            'datahora': datetime.strptime(dados['last_updated'], "%Y-%m-%d %H:%M")
        }
    except Exception as e:
        print(f"Erro com {cidade}: {e}")
        return None

def inserir_dados(dados):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS weather (
                id SERIAL PRIMARY KEY,
                cidade TEXT,
                temperatura REAL,
                sensacao_termica REAL,
                umidade INTEGER,
                vento REAL,
                descricao TEXT,
                icone_descricao TEXT,
                ponto_orvalho REAL,
                precipitacao REAL,
                datahora TIMESTAMP
            );
        """)

        cur.execute("""
            INSERT INTO weather (cidade, temperatura, sensacao_termica, umidade, vento, descricao, icone_descricao, ponto_orvalho, precipitacao, datahora)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            dados['cidade'],
            dados['temperatura'],
            dados['sensacao_termica'],
            dados['umidade'],
            dados['vento'],
            dados['descricao'],
            dados['icone_descricao'],
            dados['ponto_orvalho'],
            dados['precipitacao'],
            dados['datahora']
        ))

        conn.commit()
        cur.close()
        conn.close()
        print(f"Dados inseridos com sucesso: {dados}")
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")

if __name__ == "__main__":
    cidades = ['Sao Paulo', 'Rio de Janeiro', 'Brasilia', 'Avare']

    for cidade in cidades:
        dados = coletar_dados_clima(cidade)
        if dados:
            inserir_dados(dados)
