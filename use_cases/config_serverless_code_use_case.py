import os
from typing import Dict

from entities.artifact import Artifact
from entities.bucket import Bucket
from entities.serverless_service import ServerlessService
from use_cases.services.config_serverless_service.config_serverless_service import (
    ConfigServerlessService,
)


class ConfigServerlessCodeUseCase:
    """
    Use case to configure a serverless service
    """

    def __init__(
        self,
        config_serverless_service: ConfigServerlessService,
    ) -> None:
        self.__config_serverless_service = config_serverless_service

    def configure(self, environment: str, serverless_info: Dict) -> None:
        serverless_service = ServerlessService(
            name=serverless_info["id"],
            environment=environment,
            config=serverless_info.get("config"),
        )

        self.__config_serverless_service.configure(serverless_service)
