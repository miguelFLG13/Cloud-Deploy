import boto3
import os
from time import strftime

from entities.layer import Layer
from entities.serverless_service import ServerlessService
from use_cases.services.update_serverless_layer.update_serverless_layer import UpdateServerlessLayer


class AwsUpdateServerlessLayer(UpdateServerlessLayer):
    STATUS_CODE_OK = 200

    def update(self, serverless_service: ServerlessService, layer: Layer) -> None:
        client = boto3.client(
            'lambda',
            aws_access_key_id=os.getenv('ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
            region_name=os.getenv('REGION_NAME')
        )

        response = client.update_function_configuration(
            FunctionName=serverless_service.name,
            Layers=[layer.id]
        )

        if response['ResponseMetadata']['HTTPStatusCode'] != self.STATUS_CODE_OK:
            raise Exception('Error updating layer:\n{}'.format(str(response)))
