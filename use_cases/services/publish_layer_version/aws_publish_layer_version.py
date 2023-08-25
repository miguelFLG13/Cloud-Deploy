import boto3
import os
from time import strftime

from entities.artifact import Artifact
from entities.bucket import Bucket
from entities.layer import Layer
from use_cases.services.publish_layer_version.publish_layer_version import (
    PublishLayerVersion,
)


class AwsPublishLayerVersion(PublishLayerVersion):
    STATUS_CODE_OK = 201

    def publish(self, bucket: Bucket, artifact: Artifact) -> Layer:
        client = boto3.client(
            "lambda",
            aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"),
            region_name=os.getenv("REGION_NAME"),
        )

        version = strftime("%Y%m%d%H%M%S")
        response = client.publish_layer_version(
            LayerName=f"{bucket.environment}-{os.environ['LAYER_NAME']}",
            Description=version,
            Content={
                "S3Bucket": bucket.name,
                "S3Key": artifact.file_name,
            },
        )

        if response["ResponseMetadata"]["HTTPStatusCode"] != self.STATUS_CODE_OK:
            raise Exception("Error publishing layer:\n{}".format(str(response)))

        return response["LayerVersionArn"]
