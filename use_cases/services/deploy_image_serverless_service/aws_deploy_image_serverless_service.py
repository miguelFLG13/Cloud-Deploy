import boto3

from entities.docker_image import DockerImage
from entities.serverless_service import ServerlessService
from use_cases.services.deploy_image_serverless_service.deploy_image_serverless_service import DeployImageServerlessService


class AwsDeployImageServerlessService(DeployImageServerlessService):
    """ Service to deploy a ECR image to lambda """
    STATUS_CODE_OK = 200

    def deploy(
        self,
        serverless_service: ServerlessService,
        image: DockerImage
    ) -> None:
        client = boto3.client(
            'lambda',
            aws_access_key_id=os.getenv('ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
            region_name=os.getenv('REGION_NAME')
        )

        response = client.update_function_code(
            FunctionName=serverless_service.name,
            ImageUri=image.image_uri,
            Publish=True
        )

        if response['ResponseMetadata']['HTTPStatusCode'] != self.STATUS_CODE_OK:
            raise Exception('Error updating the lambda function:\n{}'.format(str(response)))
