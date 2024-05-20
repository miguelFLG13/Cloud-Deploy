import boto3
import json
import os

from entities.serverless_service import ServerlessService
from use_cases.services.config_serverless_service.config_serverless_service import (
    ConfigServerlessService,
)


class AwsConfigServerlessService(ConfigServerlessService):
    """Service to config a aws lambda"""

    STATUS_CODE_OK = 200

    def deploy(self, serverless_service: ServerlessService) -> None:
        client = boto3.client(
            "lambda",
            aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"),
            region_name=os.getenv("REGION_NAME"),
        )

        if serverless_service.config:
            if serverless_service.config["environment_variables"]:
                key = f"{bucket.environment}_ENVVARS"
                environment_variables = json.loads(os.environ[key])
            else:
                environment_variables = {}

            response = client.update_function_configuration(
                FunctionName=serverless_service.name,
                Environment={"Variables": environment_variables},
                Layers=serverless_service.config["layers"],
                Timeout=serverless_service.config["time_out"],
                MemorySize=serverless_service.config["memory_size"],
            )

            if response["ResponseMetadata"]["HTTPStatusCode"] != self.STATUS_CODE_OK:
                raise Exception(
                    "Error updating the lambda configuration:\n{}".format(str(response))
                )
