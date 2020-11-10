from dataclasses import dataclass


@dataclass
class Artifact:
    file_name: str
    temp_path: str
