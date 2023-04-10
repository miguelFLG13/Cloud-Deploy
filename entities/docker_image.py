from dataclasses import dataclass


@dataclass
class DockerImage:
    repository: str
    tag: str
    image_uri: str