import boto3
import json
import os
import time

from entities.serverless_service import ServerlessService
from use_cases.services.config_serverless_service.config_serverless_service import (
    ConfigServerlessService,
)


class AwsConfigServerlessService(ConfigServerlessService):
    """Service to config a aws lambda"""

    STATUS_CODE_OK = 200

    def configure(self, serverless_service: ServerlessService, attempt: int=0) -> None:
        attempt += 1
        client = boto3.client(
            "lambda",
            aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"),
            region_name=os.getenv("REGION_NAME"),
        )

        if serverless_service.config:
            if serverless_service.config["environment_variables"]:
                key = f"{serverless_service.environment}_ENVVARS"
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
                if attempt < 2:
                    time.sleep(attempt + 2)
                    self.configure(serverless_service, attempt)
                
                raise Exception(
                    "Error updating the lambda configuration:\n{}".format(str(response))
                )
