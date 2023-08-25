from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class ServerlessService:
    name: str
    environment: str
    config: Optional[Dict] = None
