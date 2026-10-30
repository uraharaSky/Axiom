from dataclasses import dataclass
from enum import Enum
from typing import Any


class TestCategory(Enum):
    __test__ = False

    HAPPY_PATH = "happy_path"
    BOUNDARY = "boundary"
    ERROR = "error"
    EDGE_CASE = "edge_case"
    REGRESSION = "regression"


class ExpectedType(Enum):
    __test__ = False

    RETURN = "return"
    EXCEPTION = "exception"


class TestPriority(Enum):
    __test__ = False

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class TestInputs:
    __test__ = False

    args: list[Any]
    kwargs: dict[str, Any]


@dataclass
class ExpectedBehavior:
    __test__ = False

    type: ExpectedType
    value: Any


@dataclass
class TestCase:
    __test__ = False

    name: str
    category: TestCategory
    objective: str
    preconditions: list[str]
    inputs: TestInputs
    expected: ExpectedBehavior
    priority: TestPriority


@dataclass
class TestSpecification:
    __test__ = False

    target: str
    objective: str
    assumptions: list[str]
    test_cases: list[TestCase]