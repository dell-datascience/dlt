#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd
from sqlalchemy import create_engine, text
from time import time
from dotenv import load_dotenv
from prefect import flow, task
from prefect.tasks import task_input_hash
load_dotenv(verbose=True)
from datetime import timedelta
from prefect_sqlalchemy import SqlAlchemyConnector, ConnectionComponents, SyncDriver

# connector is cached till 10 weeks for reuse
@task(log_prints=True, cache_key_fn=task_input_hash, cache_expiration=timedelta(weeks=10))
def connector() -> None:
    """  
    establish postgresql connection to postgresql using prefect sqlalchemy connector

    :param: None
    :param: None
    :return: None
    """

    connector = SqlAlchemyConnector(
            connection_info=ConnectionComponents(
                driver=SyncDriver.POSTGRESQL_PSYCOPG2,
                username= os.getenv(key="user"),
                password= os.getenv(key="password"),
                host= os.getenv(key="host"),
                port= os.getenv(key="port"),
                database=os.getenv(key="databaseName"),
                network=os.getenv(key="docker_network")                        
            )
            
    )
    connector.save(name=os.getenv(key="BLOCK_NAME"), overwrite=True)

# ingest may fail for whatever reason hence 3 retries
@task(log_prints=True, retries=1, cache_key_fn=task_input_hash, cache_expiration= timedelta(days=1))
def ingest_data() -> pd.DataFrame:
    """  
    downloads url dataset, loads dataset to directory

    :param: None
    :param: None
    :return: pd.dataframe
    """

    url = os.getenv("URL")

    if url.endswith('csv.gz'):
        csv_name = "output.csv.gz"
        print("\n **** URL is zipped")

    else:
        csv_name = "output.csv"
        print(" **** URL is not zipped")
    
    try:
        os.system(f"wget {url} -O {csv_name}")
        print("\n *** CSV download successful")
        print(f"\n *** Success Downloaded url ...{url} as {csv_name}")

        if not os.path.exists(csv_name) or os.path.getsize(csv_name) == 0:
            raise ValueError("Downloaded CSV file is empty or not present")

    except Exception as e:
        raise ValueError("CSV download failed",e)
    
    try:
        print("\n *** Loading data_iter")
        data_iter = next(pd.read_csv(csv_name, \
                        parse_dates=['tpep_pickup_datetime','tpep_dropoff_datetime'],\
                        iterator=True, \
                        chunksize=100000))
        print("\n *** Success data_iter Loaded")

    except Exception as e:
        raise ValueError("Error loading data_iter",e)
    
    return data_iter

@task(log_prints=True, name='transformer')
def transform_data(df : pd.DataFrame) -> pd.DataFrame:
    """  
    Transforms data: remove 0 passenger counts"

    :param df: Dataframe 
    :return: pd.DataFrame
    """

    print(f"\n*** Pre: missing passenger count: {df['passenger_count'].isin([0]).sum()}")
    df = df[df['passenger_count'] != 0]
    print(f"\n*** Post: missing passenger count: {df['passenger_count'].isin([0]).sum()}")
    return df

@task(log_prints=True, name='data loader', retries=3)
def load_data(data_iter : pd.DataFrame) -> None:
    """  
    Load data to docker postgresql using prefect sqlalchemy connector

    :param df: Dataframe 
    :return: None
    """
    tableName = os.getenv(key="tableName")
    with SqlAlchemyConnector.load(name=os.getenv("BLOCK_NAME")) as database_block: 
        with database_block.get_connection(begin=False) as engine:
            data_iter.head(n=0).to_sql(name=tableName, con=engine, if_exists='replace')
            print(f"\nSuccess !! Table: {tableName} schema")
            print('\n***ingestion in process')
            [data_iter.to_sql(name= tableName, con=engine, if_exists= 'append') for _ in data_iter]
            
@flow(name= 'ingest_data', )
def main() -> None:
    connector()
    df: pd.DataFrame = ingest_data()
    df: pd.DataFrame =transform_data(df)
    load_data(df)

if __name__ =='__main__':
    main()