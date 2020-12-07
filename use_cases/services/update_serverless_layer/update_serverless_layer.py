from abc import ABC, abstractmethod

from entities.layer import Layer
from entities.serverless_service import ServerlessService


class UpdateServerlessLayer(ABC):

    @abstractmethod
    def update(self, serverless_service: ServerlessService, layer: Layer) -> None:
        pass
