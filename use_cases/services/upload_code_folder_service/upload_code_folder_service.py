from abc import ABC, abstractmethod

from entities.bucket import Bucket
from entities.folder import Folder
from use_cases.services.upload_code_service.upload_code_service import UploadCodeService


class UploadCodeFolderService(ABC):

    @abstractmethod
    def upload(self, bucket: Bucket, folder: Folder) -> None:
        pass
