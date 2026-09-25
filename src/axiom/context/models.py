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

# @dataclass
# class ExpansionBudget:
#     max_depth: int = 1
#     max_units: int = 1
#     max_units_per_seed: int = 3
#     max_relationships_per_unit: int = 1
#     max_same_file_units: int = 3
#     max_files: int = 1
#

@dataclass
class ExpansionBudget:
    max_rounds: int = 3

    def __post_init__(self):
        if self.max_rounds < 1:
            raise ValueError("max_rounds must be at least 1")


@dataclass
class ExpansionRound:
    number: int
    input_units: list[RetrievalUnit]
    discovered_units: list[RetrievalUnit]
    visited: set[str]


