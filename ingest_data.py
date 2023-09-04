#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd
from sqlalchemy import create_engine, text
from time import time

from dotenv import load_dotenv
load_dotenv(verbose=True)

def upload():
    
    url = os.getenv("URL")
    databaseName = os.getenv("databaseName")
    user =  os.getenv("user")
    password =  os.getenv("password")
    host = os.getenv("host")
    port= os.getenv("port")
    databaseName = os.getenv("databaseName")
    tableName = os.getenv("tableName")

    # if all(url, databaseName, user,  password, host, databaseName,tableName):
    #     print("\n **** All input detected")

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
        print("\n **** Loading data frame")
        df = pd.read_csv(csv_name, \
                parse_dates=['tpep_pickup_datetime','tpep_dropoff_datetime'],\
                nrows=10)
        print("\n *** Loaded data frame successfully")
    except Exception as e:
        raise ValueError("Error reading the df file",e)
    
    # print (df[["VendorID","passenger_count"]].head())

    # read the data in chunks
    
    try:
        print("\n *** Loading data_iter")
        data_iter = pd.read_csv(csv_name, \
                        parse_dates=['tpep_pickup_datetime','tpep_dropoff_datetime'],\
                        iterator=True, \
                        chunksize=100000)
        print("\n *** Success data_iter Loaded")

    except Exception as e:
        raise ValueError("Error loading data_iter",e)
    
    # connect to postgres db and read csv into dataframe
    # create_engine(postgresql://user:passwpord@localhost:port/databaseName)
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{databaseName}')

    # test the connection
    if engine.connect():
        print("\n **** Success Connection viable")
    else:
        print(" \n !!!! Connection not viable")
    
    # create postgresql shcema
    schema = text(pd.io.sql.get_schema(df,tableName,con=engine))
    drop_sql_table = text(f'DROP TABLE IF EXISTS {tableName}')

    with engine.connect() as conn:
    #     drop table if exists
        conn.execute(drop_sql_table)
        print(f"\n **** Existing table: {tableName} dropped")
    #     create the table with schema
        conn.execute(schema)
        print(f"\n **** Table: {tableName} schema cretaed")

    # insert the data into database in chunks
    print(f"\n **** Inserting data into table: {tableName} ....")
    try:
        for data in data_iter:
            start_time = time()
            data.to_sql(name= tableName, con=engine, if_exists= 'append')
            print(f'\n **** Inserted {len(data)} chunk data ... took %.3f'%(time() - start_time))
        print("\n **** Data ingestion finished successfully")
        return None
    
    except Exception as e:
        raise ValueError("Ingestion failed with error: ", e)

if __name__ =='__main__':
    upload()

