import requests
from bs4 import BeautifulSoup
from sqlalchemy import insert
from models import engine, imoveis

def fetch_imovirtual():
    url = "https://www.imovirtual.com/comprar/apartamento/lisboa/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.select("article.offer-item")
    with engine.begin() as conn:
        for item in items:
            try:
                tipologia = item.select_one(".offer-item-rooms").text.strip()
                area_text = item.select_one(".offer-item-area").text.strip().replace("m²", "")
                area = float(area_text)
                preco_text = item.select_one(".offer-item-price").text.strip().replace("€", "").replace(".", "").replace(",", "")
                preco = float(preco_text)
                concelho = "Lisboa"

                if tipologia >= "T2" and area >= 75:
                    conn.execute(insert(imoveis).values(
                        tipologia=tipologia,
                        area=area,
                        concelho=concelho,
                        preco=preco,
                        fonte="Imovirtual"
                    ))
            except Exception as e:
                print(f"[Imovirtual] Erro: {e}")
