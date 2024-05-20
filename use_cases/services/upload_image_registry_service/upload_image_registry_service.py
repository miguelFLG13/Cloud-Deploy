from abc import ABC, abstractmethod


class UploadImageRegistryService(ABC):
    """Service to upload a docker image in a registry"""

    @abstractmethod
    def upload(self, image) -> None:
        pass
