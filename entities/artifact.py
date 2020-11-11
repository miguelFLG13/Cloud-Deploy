from dataclasses import dataclass
from pathlib import Path


@dataclass
class Artifact:
    file_name: Path
    temp_path: Path
