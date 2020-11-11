from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from entities.cdn import Cdn


class CdnCacheInvalidationService(ABC):

    @abstractmethod
    def invalidate(self, cdn: Cdn, files: List[Path]) -> None:
        pass
