from abc import ABC, abstractmethod

from entities.artifact import Artifact
from entities.bucket import Bucket


class UploadCodeService(ABC):
    """ Service to upload to cloud a artifact """

    @abstractmethod
    def upload(self, bucket: Bucket, artifact: Artifact) -> None:
        pass
