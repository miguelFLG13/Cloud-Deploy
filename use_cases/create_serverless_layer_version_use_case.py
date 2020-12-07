import os
from time import strftime
from typing import Dict

from entities.artifact import Artifact
from entities.bucket import Bucket
from entities.layer import Layer
from entities.serverless_service import ServerlessService
from use_cases.services.publish_layer_version.publish_layer_version import PublishLayerVersion
from use_cases.services.update_serverless_layer.update_serverless_layer import UpdateServerlessLayer
from use_cases.services.upload_code_service.upload_code_service import UploadCodeService


class CreateServerlessLayerVersionUseCase:

    def __init__(
        self,
        upload_code_service: UploadCodeService,
        publish_layer_version: PublishLayerVersion,
        update_serverless_layer: UpdateServerlessLayer
    ):
        self.__upload_code_service = upload_code_service
        self.__publish_layer_version = publish_layer_version
        self.__update_serverless_layer = update_serverless_layer

    def create(
        self,
        environment: str,
        serverless_info: Dict,
        layer_zip_file_name: str
    ) -> None:
        version = strftime("%Y%m%d%H%M%S")
        file_name = "{}_layers/{}_{}_build.zip".format(
            environment,
            version,
            serverless_info['id']
        )

        artifact = Artifact(
            file_name=file_name,
            temp_path=layer_zip_file_name
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

        layer_arn = self.__publish_layer_version.publish(
            bucket,
            artifact
        )

        serverless_service = ServerlessService(
            name=serverless_info['id'],
            environment=environment
        )

        layer = Layer(id=layer_arn)

        self.__update_serverless_layer.update(
            serverless_service,
            layer
        )
