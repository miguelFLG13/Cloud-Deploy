import os
from pathlib import Path

from entities.bucket import Bucket
from entities.folder import Folder
from entities.cdn import Cdn
from environments import PRODUCTION_ENVIRONMENT
from use_cases.services.cdn_cache_invalidation.cdn_cache_invalidation import CdnCacheInvalidationService
from use_cases.services.empty_bucket_service.empty_bucket_service import EmptyBucketService
from use_cases.services.list_bucket_content_service.list_bucket_content_service import ListBucketContentService
from use_cases.services.upload_code_folder_service.upload_code_folder_service import UploadCodeFolderService



class DeployStaticCodeUseCase:
    """
    Use case to, in cloud, upload a version of your static code
    (HTML, CSS and JS) and manage your CDN
    """

    def __init__(
        self,
        empty_bucket_service: EmptyBucketService,
        upload_code_folder_service: UploadCodeFolderService,
        list_bucket_content_service: ListBucketContentService,
        cdn_cache_invalidation_service: CdnCacheInvalidationService
    ) -> None:
        self.__empty_bucket_service = empty_bucket_service
        self.__upload_code_folder_service = upload_code_folder_service
        self.__list_bucket_content_service = list_bucket_content_service
        self.__cdn_cache_invalidation_service = cdn_cache_invalidation_service

    def deploy(self, environment: str, path: str) -> None:
        bucket_name = os.getenv('BUCKET_{}'.format(environment))
        bucket = Bucket(
            name=bucket_name,
            environment=environment
        )

        self.__empty_bucket_service.empty(bucket)

        folder = Folder(path=Path(path))

        self.__upload_code_folder_service.upload(bucket, folder, path)

        if environment == PRODUCTION_ENVIRONMENT:
            files = self.__list_bucket_content_service.list(bucket)

            cdn = Cdn(id=os.getenv('CDN_ID'))

            self.__cdn_cache_invalidation_service.invalidate(cdn, files)
