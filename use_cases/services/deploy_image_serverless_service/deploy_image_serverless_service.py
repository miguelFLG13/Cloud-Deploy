from abc import ABC, abstractmethod

from entities.docker_image import DockerImage
from entities.serverless_service import ServerlessService


class DeployImageServerlessService(ABC):
    """ Service to deploy docker image in a cloud serverless sevice """

    @abstractmethod
    def deploy(self, serverless_service: ServerlessService, image: DockerImage) -> None:
        pass
