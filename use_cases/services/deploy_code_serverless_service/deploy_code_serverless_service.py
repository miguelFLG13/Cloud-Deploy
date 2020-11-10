from abc import ABC, abstractmethod

from entities.artifact import Artifact
from entities.bucket import Bucket
from entities.serverless_service import ServerlessService


class DeployCodeServerlessService(ABC):
    """ Service to deploy code in a cloud serverless sevice """

    @abstractmethod
    def deploy(self, serverless_service: ServerlessService, bucket: Bucket, artifact: Artifact) -> None:
        pass
