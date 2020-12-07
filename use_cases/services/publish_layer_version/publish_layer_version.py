from abc import ABC, abstractmethod

from entities.artifact import Artifact
from entities.bucket import Bucket
from entities.layer import Layer


class PublishLayerVersion(ABC):

    @abstractmethod
    def publish(
        self,
        bucket: Bucket,
        artifact: Artifact
    ) -> Layer:
        pass
