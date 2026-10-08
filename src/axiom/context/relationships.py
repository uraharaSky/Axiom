from dataclasses import dataclass
from enum import Enum

from axiom.context.models import RetrievalUnit

class RelationshipKind(Enum):
    FUNCTION_CALL = "function_call"
    CLASS_REFERENCE = "class_reference"
    IMPORT = "import"

@dataclass
class Relationship:
    kind: RelationshipKind
    name: str
    source: RetrievalUnit


