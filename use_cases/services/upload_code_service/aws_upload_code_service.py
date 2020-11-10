import boto3
import os

from entities.artifact import Artifact
from entities.bucket import Bucket
from use_cases.services.upload_code_service.upload_code_service import UploadCodeService


class AwsUploadCodeService(UploadCodeService):
    """ Service to upload to S3 a artifact  """

    def upload(self, bucket: Bucket, artifact: Artifact) -> None:
        client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
            region_name=os.getenv('REGION_NAME')
        )

        client.put_object(
            Body=open(artifact.temp_path, 'rb'),
            Bucket=bucket.name,
            Key=artifact.file_name
        )
