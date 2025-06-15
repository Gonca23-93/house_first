# 🏠 Real Estate Data Ingestion

Este projeto permite fazer scraping de imóveis à venda em Lisboa com tipologia `T2` ou superior e área mínima de `75m²` a partir de três portais:

- Casa Sapo  
- Imovirtual  
- BPI Expresso Imobiliário  

Os dados são guardados numa base de dados PostgreSQL acessível por API via FastAPI.

---

## ⚙️ Requisitos

- Docker  
- Docker Compose  
- Python 3.11 (apenas para desenvolvimento local/testes)

---

## 🐳 1. Build da imagem Docker

Antes de levantar os containers, constrói a imagem para o serviço da aplicação:

```bash
docker build -t real-estate-ingest .
docker-compose up -d
docker-compose logs -f
```

## 🛠️ 3. Correr o Ingestor

O script de ingestão vai buscar dados dos três sites e guardá-los na base de dados. Para o executar:
```bash
docker-compose exec app python ingest.py
```
Este comando corre o ingest.py, que por sua vez importa e executa os scrapers:

- casa_sapo.py

- imovirtual.py

- bpi_expresso.py

## 📬 Endpoints da API (FastAPI)

Após subir os containers, podes aceder à documentação automática da API em:

```bash
http://localhost:8000/docs
```
## 📁 Estrutura de pastas (resumo)
```bash
/app
├── ingest/
│   ├── casa_sapo.py
│   ├── imovirtual.py
│   ├── bpi_expresso.py
├── ingest.py
├── main.py
├── models.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
```