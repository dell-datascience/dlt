from prefect.deployments import Deployment
from etl_to_gcs import main_flow 
from prefect.filesystems import GitHub

github_block = GitHub.load("github-block")

deployment = Deployment.build_from_flow(
            flow=main_flow,
            name='github-web-to-gcs-deployment',
            storage=github_block,
            entrypoint='/Users/air/Documents/a_zoom_data_engineer/week2/homework/etl_to_gcs.py:main_flow'
            )

if __name__=='__main__':
    deployment.apply()