import os
from pathlib import Path
from typing import Optional

from entities.artifact import Artifact
from entities.bucket import Bucket
from entities.folder import Folder
from use_cases.services.upload_code_folder_service.upload_code_folder_service import UploadCodeFolderService
from use_cases.services.upload_code_service.upload_code_service import UploadCodeService


class AwsUploadCodeFolderService(UploadCodeFolderService):

    def __init__(self, upload_code_service: UploadCodeService) -> None:
        self.__upload_code_service = upload_code_service

    def upload(self, bucket: Bucket, folder: Folder, local_path: Optional[Path]) -> None:
        if local_path[-1] != '/':
            local_path = "{}/".format(local_path)

        self.__upload_folder(bucket, folder.path, local_path)

    def __upload_folder(self, bucket: Bucket, path: Path, local_path: Optional[Path]) -> None:
        for file in os.listdir(path):
            file_path = "{}/{}".format(path, file)

            if os.path.isdir(file_path):
                self.__upload_folder(bucket, file_path, local_path)
            else:
                artifact = Artifact(
                    file_name=file_path.replace(local_path, ''),
                    temp_path=file_path
                )
                self.__upload_code_service.upload(bucket, artifact)
