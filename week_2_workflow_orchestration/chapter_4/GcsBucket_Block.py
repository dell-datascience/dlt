from prefect_gcp.cloud_storage import GcsBucket, GcpCredentials

bucket_block = GcsBucket(gcp_credentials=GcpCredentials.load(name="gcp-credentials"),
                bucket="de_data_lake_de-project-397922",
                )

bucket_block.save(name="zoom-gcs", overwrite=True)