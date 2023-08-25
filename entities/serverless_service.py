from dataclasses import dataclass
from typing import Dict


@dataclass
class ServerlessService:
    name: str
    environment: str
    config: Dict
