import os
from time import strftime
from typing import Dict

from entities.docker_image import DockerImage
from entities.serverless_service import ServerlessService
from use_cases.services.deploy_image_serverless_service.deploy_image_serverless_service import (
    DeployImageServerlessService,
)
from use_cases.services.upload_image_registry_service.upload_image_registry_service import (
    UploadImageRegistryService,
)


class DeployServerlessImageUseCase:
    """
    Use case to, in cloud, create a version of your docker image, upload it and deploy in a serverless service
    """

    def __init__(
        self,
        upload_image_registry_service: UploadImageRegistryService,
        deploy_image_serverless_service: DeployImageServerlessService,
    ) -> None:
        self.__upload_image_registry_service = upload_image_registry_service
        self.__deploy_image_serverless_service = deploy_image_serverless_service

    def deploy(self, environment: str, serverless_info: Dict) -> None:
        os.chdir("../")
        directory = os.getcwd()
        for module in serverless_info["extra_modules"]:
            os.system("cp -r {} {}".format(module, serverless_info["path"]))

        os.chdir(serverless_info["path"])

        image = DockerImage(
            repository=serverless_info["image_repository"],
            tag=f"{serverless_info['image_repository']}",
            image_uri=f"{account}.dkr.ecr.{region}.amazonaws.com/{serverless_info['image_repository']}:latest",
        )

        self.__upload_image_registry_service.upload(image)

        serverless_service = ServerlessService(
            name=serverless_info["id"], environment=environment
        )

        self.__deploy_code_serverless_service.deploy(serverless_service, image)
