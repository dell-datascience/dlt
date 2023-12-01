1. Prefect cloud 

    1. go tp prefect cloud and create API keys
    
        API Keys: pnu_qAPZT8DpmvaTDoTA5EPxjFFwLAycLS3fokcu
        or run 
        `prefect cloud login -k pnu_qAPZT8DpmvaTDoTA5EPxjFFwLAycLS3fokcu`

        2. create `docker block`, `bigquery block`, `gcs bucket block`, `gcp credentials`

        3. create the deployment file and run deployment file
        ```python
        from prefect.deployments import Deployment 
        from prefect.infrastructure.container import DockerContainer
        from parameterized_flow import etl_grandparent_flow

        docker_block =DockerContainer.load("zoomcontainer") ## NB: zoomcontainer is cloud bucket

        docker_deploy = Deployment.build_from_flow(
                        flow=etl_grandparent_flow,
                        name="docker-flow",
                        infrastructure=docker_block
                    )

        if __name__=="__main__":
            docker_deploy.apply()

        ```

        `python docker_deployment.py` : then you can see your flows in UI

            
2. activate the agent
    `prefect agent start --work-queue "default" --no-cloud-agent`

    5. run the deployment 
    `prefect deployment run parent_flow_runner/docker-flow -p "month=7" -p "color=yellow" -p "year=2020"`