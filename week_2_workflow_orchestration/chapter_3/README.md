# Dockerize ingestion script

1. Dockerfile deployment

    a. create Dockerfile

    ```docker
    FROM prefecthq/prefect:2.7.7-python3.9

    COPY docker-requirement.txt .

    RUN pip install -r docker-requirement.txt --trusted-host pypi.python.org --no-cache-dir

    COPY chapter_2 /opt/prefect/flows

    COPY chapter_2/new_data /opt/prefect/data
    ``` 
    b. build the docker image:
    `docker build -t albydel/prefect:DE .`

    c. push docker image to dockerhub
    sign in to docker hub by `docker login`
    `docker image push albydel/prefect:DE`

2. create docker block with the UI:

set parameters:
    Block Name: `zoom`
    image: `albydel/prefect:DE`
    image pull policy: `Always`
    auto remove: `true`

    ### alternative to creating DockerContainer block in the UI
    save it in a file and import it
    ```python
    docker_block = DockerContainer(
        image="albydel/prefect:DE"
        image_pull_policy="ALWAYS",
        auto_remove=True,
        network_mode="bridge"
    )
    docker_block.save("zoom", overwrite=True)
    ```

3. deploy from python file, create deploymenet file
        `docker_deployment.py`

        ```python
        from prefect.deployments import Deployment 
        from prefect.infrastructure.container import DockerContainer
        from parameterized_flow import etl_grandparent_flow

        docker_block =DockerContainer.load("zoom")

        docker_deploy = Deployment.build_from_flow(
                        flow=etl_grandparent_flow,
                        name="docker-flow"
                        infrastructure=docker_block
            )
        
        if __name__=="__main__":
            docker_deploy.apply()
        ```

        8.1. run the deployed task
            `python docker_deployment`

        8.2 check profile, shows that we are using the default profile
            `prefect profile ls`
        
        8.3 use API end point to enable docker container to interact with prefect server
            `prefect config set PREFECT_API_URL="http://127.0.0.1:4200/api"`

        8.4 start the API agent: the agent picks up any queue and execute it
            `prefect agent start --work-queue "default"`

        8.5 Run the queue with parameter month=7
            `prefect deployment run parent_flow_runner/docker-flow -p "month=7" -p "color=yellow" -p "year=2020"`