import boto3
import os

from entities.artifact import Artifact
from entities.bucket import Bucket
from entities.serverless_service import ServerlessService
from use_cases.services.deploy_code_serverless_service.deploy_code_serverless_service import DeployCodeServerlessService


class AwsDeployCodeServerlessService(DeployCodeServerlessService):
    """ Service to deploy code in a aws lambda """
    STATUS_CODE_OK = 200

    def deploy(
        self,
        serverless_service: ServerlessService,
        bucket: Bucket,
        artifact: Artifact
    ) -> None:
        client = boto3.client(
            'lambda',
            aws_access_key_id=os.getenv('ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
            region_name=os.getenv('REGION_NAME')
        )

        response = client.update_function_code(
            FunctionName=serverless_service.name,
            S3Bucket=bucket.name,
            S3Key=artifact.file_name,
            Publish=True
        )

        if response['ResponseMetadata']['HTTPStatusCode'] != self.STATUS_CODE_OK:
            raise Exception('Error updating the lambda function:\n{}'.format(str(response)))
