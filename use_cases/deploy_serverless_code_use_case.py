import os
from time import strftime
from typing import Dict

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

    def deploy(self, environment: str, serverless_info: Dict) -> None:
        current_directory = os.getcwd()
        os.chdir("../")
        for module in serverless_info['extra_modules']:
            os.system("cp -r {} {}".format(module, serverless_info['path']))

        os.chdir(serverless_info['path'])
        temp_file_name = "{}.zip".format(serverless_info['path'].replace('/', '_'))
        os.system("zip -r {} *".format(temp_file_name))
        os.system("mv {} {}/../".format(temp_file_name, current_directory))
        os.chdir(current_directory)

        version = strftime("%Y%m%d%H%M%S")
        file_name = "{}/{}_{}_build.zip".format(
            environment,
            version,
            serverless_info['id']
        )

        artifact = Artifact(
            file_name=file_name,
            temp_path="../{}".format(temp_file_name)
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

        serverless_service = ServerlessService(
            name=serverless_info['id'],
            environment=environment
        )

        self.__deploy_code_serverless_service.deploy(
            serverless_service,
            bucket,
            artifact
        )
