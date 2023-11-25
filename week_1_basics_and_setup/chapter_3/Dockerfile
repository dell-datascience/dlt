FROM python:3.9

RUN apt-get update && apt-get install -y wget
RUN pip install pandas sqlalchemy psycopg2 python-dotenv

WORKDIR /app

COPY ingest_data.py ingest_data.py
COPY .env .env

ENTRYPOINT ["python", "ingest_data.py" ]