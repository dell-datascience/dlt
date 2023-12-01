# etl download data from web to google cloud store 

## set up google cloud store and google big query with terraform

1. Start local prefect server: `prefect server start`

2. Or start prefect cloud `prefect cloud login`

3. Register **Prefect Connector** module for **Google Cloud Platform** from the command line to make it available for use in our flow `prefect block register -m prefect_gcp`

4. populate the block with conection details to our GCP Storage. Go to the GUI and      follow. Go to blocks and search for `GCS Bucket`:

    * **Block name**: data name for Block `gcs-bucket`
    * **Bucket**: Name of the cloud storage created in GCP 
    * **GCP Credentials**: 
        **Block Name**: name of credential. `google-creds`
        ***bucket**: name of the bucket
        **credentials**: create new credential by copying JSON content of service account 
    blocks created:
        1. GCS Bucket: `gcs-bucket`
        2. GCp Credentials: `google-creds`

4. Build prefect deployment via command line
    
    1. `prefect deployment build parameterized_flow.py:etl_grandparent_flow -n "Parameterized ETL" - a` 

    NB: `-a` to apply at the same time

    - it creates a metadata that workflow orchestration needs to know to deploy
    
    2. edit the parameters: {"color":"yellow", "month":[1,2,3], "year":2021}
    
    3. `prefect deployment apply etl_grandparent_flow-deployment.yaml`
    
    4. run the deployment in the prefect deployment UI
    
    5. start an agent to to run the deployment
        `prefect agent start --pool "default-agent-pool`


## elt download from google cloud store to google bigquery

1. Build prefect deployment via command line
    
    1. `prefect deployment build etl_gcs_to_gbq.py:main -n "Parameterized ETL" - a` 

    NB: `-a` to apply at the same time

    - it creates a metadata that workflow orchestration needs to know to deploy
    
    2. edit the parameters: {"color":"yellow", "month":[1,2,3], "year":2021}
    
    3. `prefect deployment apply etl_main.yaml`
    
    4. run the deployment in the prefect deployment UI
    
    5. start an agent to to run the deployment
        `prefect agent start --pool "default-agent-pool`