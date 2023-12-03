import array
from numpy import int64
import pandas as pd
from pathlib import Path
from prefect import flow, task
from prefect_gcp import GcsBucket, GcpCredentials
from prefect_gcp.bigquery import BigQueryWarehouse
from prefect.tasks import task_input_hash
from datetime import timedelta 
import io
from sqlalchemy import text
from google.cloud.exceptions import Conflict

@task(name='extractor', log_prints=True, retries=0, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract(path : str)->pd.DataFrame:
    """  
    Extracts data from gcs path

    :param path: gcs path containing data 
    :return df: pd.Dataframe
    """
    gcs_block = GcsBucket.load("gcs-bucket")
    data = gcs_block.read_path(path)
    data_bytes = io.BytesIO(initial_bytes=data)
    df: pd.DataFrame = pd.read_parquet(data_bytes)
    # print(f"df {type(df)} \n {df.head()}")
    print(df.info())
    return df


@task(name='transformer', log_prints=True)
def transform(df: pd.DataFrame)-> pd.DataFrame:
    """  
    Transform/remove 0 passenger counts"

    :param df: pd.Dataframe 
    :return df: pd.DataFrame
    """

    print(f"\n*** Pre: missing passenger count: {df['passenger_count'].isin([0]).sum()}")
    df['passenger_count'] = df['passenger_count'].fillna(0, inplace=True)
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])
    # print(f"\n*** Post: missing passenger count: {df['passenger_count'].isin([0]).sum()}")
    return df


@task(name='load data to google BigQuery', log_prints=True)
def load_to_gbq(df:pd.DataFrame)-> None:
    """
    Load dataset to Google Big Query
    
    :param df: pd.Dataframe 
    :return None: None
    """
    
    gcp_crdentials = GcpCredentials.load("gcp-credentials")
    df.to_gbq(destination_table='de-project-397922.trips_data_all.rides',
              project_id='de-project-397922',
              credentials=gcp_crdentials.get_credentials_from_service_account(),
              chunksize=100_000,
              if_exists='append')
    return None

@flow(name='main worker', log_prints=True)
def main_worker(color : str, year : int, month : int)-> None:
    """main etl task"""
    
    data_file = f"{color}_tripdata_{year}-{month:02}" 
    path = f"new_data/{color}/{data_file}.parquet" 
    tableName = 'trips_data_all.rides'

    df: pd.DataFrame = extract(path)
    df = transform(df)
    load_to_gbq(df)
    return len(df)

@flow(name = 'main flow', log_prints=True)
def main_flow(
    color : str, 
    year : int, 
    months : list[int]
) -> None:
    
    rows = 0

    for month in months:
        rows += main_worker( color, year, month)
    print(rows)

if __name__=="__main__":
    
    color = 'yellow'
    year = 2020
    months: list[int] = [2 , 3]

    main_flow(color, year, months)