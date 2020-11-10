import os
from time import strftime

from entities.artifact import Artifact
from entities.bucket import Bucket
from entities.serverless_service import ServerlessService
from use_cases.services.deploy_code_serverless_service.deploy_code_serverless_service import DeployCodeServerlessService
from use_cases.services.upload_code_service.upload_code_service import UploadCodeService


class DeployServerlessCodeUseCase:
    """
    Use case to, in cloud, upload a version of your code to a
    bucket and deploy in a serverless service
    """

    def __init__(
        self,
        upload_code_service: UploadCodeService,
        deploy_code_serverless_service: DeployCodeServerlessService
    ) -> None:
        self.__upload_code_service = upload_code_service
        self.__deploy_code_serverless_service = deploy_code_serverless_service

    def deploy(self, environment: str, path: str) -> None:
        version = strftime("%Y%m%d%H%M%S")
        file_name = "{}/{}_build.zip".format(environment, version)

        artifact = Artifact(
            file_name=file_name,
            temp_path=path
        )

        bucket_name = os.getenv('BUCKET_{}'.format(environment))
        bucket = Bucket(
            name=bucket_name,
            environment=environment
        )

        self.__upload_code_service.upload(
            bucket,
            artifact
        )

        serverless_service_name = os.getenv(
            'SERVERLESS_SERVICE_{}'.format(environment)
        )
        serverless_service = ServerlessService(
            name=serverless_service_name,
            environment=environment
        )

        self.__deploy_code_serverless_service.deploy(
            serverless_service,
            bucket,
            artifact
        )
