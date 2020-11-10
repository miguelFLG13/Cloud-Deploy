from dataclasses import dataclass


@dataclass
class ServerlessService:
    name: str
    environment: str
