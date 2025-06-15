import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Float
import os

DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL)
metadata = MetaData()

imoveis = Table(
    'imoveis', metadata,
    Column('id', Integer, primary_key=True),
    Column('tipologia', String),
    Column('area', Float),
    Column('concelho', String),
    Column('preco', Float),
)

metadata.create_all(engine)

def fetch_data():
    # Exemplo hipotético (precisa adaptação ao site real)
    url = 'https://www.exemplo-imobiliaria.pt/casas/lisboa'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    with engine.connect() as conn:
        for casa in soup.select('.casa-item'):
            tipologia = casa.select_one('.tipologia').text.strip()
            area = float(casa.select_one('.area').text.replace("m²", "").strip())
            concelho = casa.select_one('.concelho').text.strip()
            preco = float(casa.select_one('.preco').text.replace("€", "").replace(",", "").strip())

            if tipologia >= 'T2' and area >= 75 and 'Lisboa' in concelho:
                conn.execute(imoveis.insert().values(
                    tipologia=tipologia, area=area, concelho=concelho, preco=preco
                ))

if __name__ == "__main__":
    fetch_data()
