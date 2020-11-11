from abc import ABC, abstractmethod

from entities.bucket import Bucket

class EmptyBucketService(ABC):

    @abstractmethod
    def empty(self, bucket: Bucket) -> None:
        pass
