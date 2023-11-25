from prefect.deployments import Deployment 
from prefect.infrastructure.container import DockerContainer
from parameterized_flow import etl_grandparent_flow

docker_block =DockerContainer.load("zoomcontainer")

docker_deploy = Deployment.build_from_flow(
                flow=etl_grandparent_flow,
                name="docker-flow",
                infrastructure=docker_block
            )

if __name__=="__main__":
    docker_deploy.apply()