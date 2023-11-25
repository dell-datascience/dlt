# Dockerize ETL ingestion script to ingest data from web to Postgresql docker

In this project `ingest_data.py` script is baked into docker image `taxi_ingestion:v001` via `Dockerfile`. When run, it loads NY taxi data from web to Postgresql docker and the data is queried via PgAdinm4 dockers. Secrets are read from `.env` file

Function:

- Downloads NY taxi dataset via url
- Loads dataset into memory
- Uploads dataset into postgresql docker

## Setup

1. Provision Postgresql, PgAdmin4 and docker network all in terminal

    - Create docker network

            docker network create pg-network

    - Create postgresql docker in network

            docker run -it \
                -e POSTGRES_USER="root" \
                -e POSTGRES_PASSWORD="root" \
                -e POSTGRES_DB="ny_taxi" \
                -v $(pwd)/cli_docker_postgres/ny_taxi_postgres_data:/var/lib/postgresql/data \
                -p 5432:5432 \
            --network=pg-network\
            --name pg-database\
            postgres:13

    - create PgAdmin4 docker in network

            docker run -it \
                -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
                -e PGADMIN_DEFAULT_PASSWORD="root" \
                -p 8080:80 \
                --network=pg-network \
                --name pgadmin \
            dpage/pgadmin4


2. create `.env` file and populate Postgresql connection parameters

        URL='https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-01.csv.gz'
        user=root
        password=root
        host=pg-database
        port=5432
        tableName=yellow_taxi_trips
        databaseName=ny_taxi


3. Bulid ETL ingestion image `taxi_ingestion:v001` via the Dockerfile 

        docker build -t taxi_ingestion:v001 .


4. Run the ETL ingestion image

        docker run -it taxi_ingestion:v001


5. Login to PgAdmin4 endpoint to query data




cli_docker_postgres directory contains postgres file system

-p 5432(computer port):5432(docker postgres port)
        
    docker is listening to requests on port 5432
    
    links docker postgres to localhost computer

Ensure localhost port `5432` is not being used by another program such as local postgres
    
    sof -i :5432


Connect to the postgresql docker with pgcli: 
            
    pgcli -h pg-database -p 5431 -u root -d ny_taxi
    