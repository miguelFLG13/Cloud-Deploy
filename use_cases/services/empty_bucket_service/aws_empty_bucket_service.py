import boto3
import os

from entities.bucket import Bucket
from use_cases.services.empty_bucket_service.empty_bucket_service import EmptyBucketService


class AwsEmptyBucketService(EmptyBucketService):

    def empty(self, bucket: Bucket) -> None:
        client = boto3.resource(
            's3',
            aws_access_key_id=os.getenv('ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
            region_name=os.getenv('REGION_NAME')
        )
        s3_bucket = client.Bucket(bucket.name)
        s3_bucket.objects.all().delete()
