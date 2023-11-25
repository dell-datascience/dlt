# Ingestion jupyter notebook to ingest data from url to localhost Postgresql

In this project, an ingestion jupyter notebook loads NY taxi data from web to localhost Postgresql server via localhost PgAdinm4.

Function:

- Downloads NY taxi dataset via url
- Loads dataset into memory
- Uploads dataset into postgresql docker

## Setup

1. Start local host postgresql server

2. Run Jupyter notebook

Ensure localhost port `5432` is not being used by another program such as local postgres
    
    sof -i :5432


Connect to the postgresql docker with pgcli: 
            
    pgcli -h pg-database -p 5431 -u root -d ny_taxi
    