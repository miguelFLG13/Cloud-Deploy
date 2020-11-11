from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from entities.bucket import Bucket


class ListBucketContentService(ABC):

    @abstractmethod
    def list(self, bucket: Bucket) -> List[Path]:
        pass
