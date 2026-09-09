from dataclasses import dataclass
from pathlib import Path

@dataclass
class RetrievalUnit:
    id: str
    kind: str
    name: str
    file: Path
    start_line: int
    end_line: int