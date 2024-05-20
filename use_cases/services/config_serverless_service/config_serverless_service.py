from abc import ABC, abstractmethod

from entities.serverless_service import ServerlessService


class ConfigServerlessService(ABC):
    """Service to config a cloud serverless sevice"""

    @abstractmethod
    def configure(self, serverless_service: ServerlessService) -> None:
        pass
