import boto3
import os
from datetime import datetime
from pathlib import Path
from typing import List

from entities.cdn import Cdn
from use_cases.services.cdn_cache_invalidation.cdn_cache_invalidation import CdnCacheInvalidationService


class AwsCdnCacheInvalidationService(CdnCacheInvalidationService):

    def invalidate(self, cdn: Cdn, files: List[Path]) -> None:
        client = boto3.client(
            'cloudfront',
            aws_access_key_id=os.getenv('ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
            region_name=os.getenv('REGION_NAME')
        )

        client.create_invalidation(
            DistributionId=cdn.id,
            InvalidationBatch={
                'Paths': {
                    'Quantity': len(files),
                    'Items': ['/{}'.format(f) for f in files]
                },
                'CallerReference': '{}'.format(datetime.now())
            }
        )
