import requests
from bs4 import BeautifulSoup
from sqlalchemy import insert
from models import engine, imoveis

def fetch_bpi_expresso():
    url = "https://expresso.sapo.pt/imobiliario"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.select(".property")
    with engine.begin() as conn:
        for item in items:
            try:
                tipologia = item.select_one(".tipologia").text.strip()
                area_text = item.select_one(".area").text.strip().replace("m²", "")
                area = float(area_text)
                preco_text = item.select_one(".preco").text.strip().replace("€", "").replace(".", "").replace(",", "")
                preco = float(preco_text)
                concelho = "Lisboa"

                if tipologia >= "T2" and area >= 75:
                    conn.execute(insert(imoveis).values(
                        tipologia=tipologia,
                        area=area,
                        concelho=concelho,
                        preco=preco,
                        fonte="BPI Expresso"
                    ))
            except Exception as e:
                print(f"[BPI Expresso] Erro: {e}")
