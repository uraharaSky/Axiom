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

@dataclass
class ExpansionBudget:
    max_depth: int = 1
    max_units: int = 1
    max_units_per_seed: int = 3
    max_relationships_per_unit: int = 1
    max_same_file_units: int = 3
    max_files: int = 1
    


