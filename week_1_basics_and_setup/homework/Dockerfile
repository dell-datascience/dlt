FROM python:3.9

RUN apt-get update && apt-get install -y wget
RUN pip install pandas sqlalchemy psycopg2 python-dotenv

WORKDIR /app

COPY ingest_homework.py ingest_homework.py
COPY .env .env

ENTRYPOINT ["python", "ingest_homework.py" ]
