import boto3
import os
from pathlib import Path
from typing import List

from entities.bucket import Bucket
from use_cases.services.list_bucket_content_service.list_bucket_content_service import ListBucketContentService


class AwsListBucketContentService(ListBucketContentService):

    def list(self, bucket: Bucket) -> List[Path]:
        client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
            region_name=os.getenv('REGION_NAME')
        )

        return [
            Path(obj['Key'])
            for obj in client.list_objects(Bucket=bucket.name)['Contents']
        ]
