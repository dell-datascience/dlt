# Ingestion script using prefect sqlalchemy connector

## Prefect
It is an open-source Python-based flow orchestration tool. It allows us to create flows with tasks and subtasks to, in our case, build an ETL. It has a GUI from which we can monitor and program the execution of workflows. In addition, it includes a kind of security vault to store source/destination connections, with connectors for the most widely used public cloud storage services. Basically, it consists of the following elements: Flow, Task, and Block that work as Python decorators.

## Flow
Collection of organized Tasks that we are going to schedule and execute. They are considered DAG (directed acyclic graphs), which is a type of mathematical structure that meets the following premises:

- **Graph**: A data structure made up of nodes and their connections. A Flow would be a graph and the Tasks would be the nodes.

- **Directed**: they always go in one direction

- **Acyclic** : they are not cyclical, they never go through a task that has already been executed.

        @flow("Ingest newyork taxis data")
        def my_flow():

## Task
Re represents an action within a Flow. For example, for an ETL we would have at least three tasks: extract, transformation and load. They can be set to rerun in the event of a failure (ideal for ingestion). Actually, a task is a Python method that can perform any type of action. It can be configured with the following parameters:

- **name**: A name is assigned. `name = "Ingest data"`

- **log_prints**: admits or ; Allows you to paint traces per console.`True`, `False`: `log_prints = true`

- **retries**: Configure number of retries if it fails. `retries = 3`

- **Tags**: We can add tags to catalog the tasks. `tags = ["Ingest","ETL"]`

- **cache_key**: A function is specified that we should import as a library. It caches the result in the event of an error, so it doesn't need to be re-executed. `imported from prefect.tasks cache_key_fn=task_input_hash`

- **cache_expiration**: Setting the length of time for which the cache will be saved. `cache_expiration=timedelta(days=1)`

    
        @task(retries=3, log_prints=True)
        def ingest_data(source):
            return
## Blocks
Stores connections with external resources (GCS Bucket, Azure, Docker, Databricks, etc.). They can be reused with different tasks. They can be created by command line (CLI) or from the GUI.

        gcs_block = GcsBucket.load("zoom-gcs")
        
## Prerequisites
1. Install [prefect](https://docs.prefect.io/concepts/overview/)

2. install the `requirementss.txt` 

        pip install -r requirements.txt

Sqlalchemy connector connects script to postgresql database