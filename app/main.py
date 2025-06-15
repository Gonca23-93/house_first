from fastapi import FastAPI
from sqlalchemy import create_engine, Table, MetaData, select
import os

app = FastAPI()
DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL)
metadata = MetaData(bind=engine)
imoveis = Table('imoveis', metadata, autoload_with=engine)

@app.get("/casas")
def get_casas():
    with engine.connect() as conn:
        query = select(imoveis).where(
            imoveis.c.tipologia >= 'T2',
            imoveis.c.area >= 75,
            imoveis.c.concelho == 'Lisboa'
        )
        result = conn.execute(query)
        return [dict(r) for r in result]
