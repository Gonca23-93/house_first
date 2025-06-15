import requests
from bs4 import BeautifulSoup
from sqlalchemy import insert
from models import engine, imoveis

def fetch_casa_sapo():
    url = "https://casa.sapo.pt/venda/apartamentos/lisboa/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.select(".searchResultProperty")
    with engine.begin() as conn:
        for item in items:
            try:
                tipologia = item.select_one(".propertyTypology").text.strip()
                area_text = item.select_one(".propertyArea").text.strip().replace("m²", "")
                area = float(area_text)
                preco_text = item.select_one(".propertyPrice").text.strip().replace("€", "").replace(".", "").replace(",", "")
                preco = float(preco_text)
                concelho = "Lisboa"

                if tipologia >= "T2" and area >= 75:
                    conn.execute(insert(imoveis).values(
                        tipologia=tipologia,
                        area=area,
                        concelho=concelho,
                        preco=preco,
                        fonte="Casa Sapo"
                    ))
            except Exception as e:
                print(f"[Casa Sapo] Erro: {e}")
