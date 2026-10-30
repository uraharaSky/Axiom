from typing import Any

from axiom.llm.specification import (
    ExpectedBehavior,
    ExpectedType,
    TestCase,
    TestCategory,
    TestInputs,
    TestPriority,
    TestSpecification,
)


class SpecificationValidationError(Exception):
    """Raised when an LLM test specification fails validation."""


class SpecificationValidator:

    def validate(self, data: dict[str, Any]) -> TestSpecification:
        self._validate_top_level(data)

        test_cases = [
            self._validate_test_case(test_case, index)
            for index, test_case in enumerate(data["test_cases"])
        ]

        return TestSpecification(
            target=data["target"],
            objective=data["objective"],
            assumptions=data["assumptions"],
            test_cases=test_cases,
        )

    def _validate_top_level(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise SpecificationValidationError(
                "Test specification must be a dictionary"
            )

        required_fields = {
            "target": str,
            "objective": str,
            "assumptions": list,
            "test_cases": list,
        }

        for field, expected_type in required_fields.items():
            if field not in data:
                raise SpecificationValidationError(
                    f"Missing required field: {field}"
                )

            if not isinstance(data[field], expected_type):
                raise SpecificationValidationError(
                    f"Field '{field}' must be of type "
                    f"{expected_type.__name__}"
                )

        if not data["target"].strip():
            raise SpecificationValidationError(
                "Field 'target' cannot be empty"
            )

        if not data["objective"].strip():
            raise SpecificationValidationError(
                "Field 'objective' cannot be empty"
            )

    def _validate_test_case(
        self,
        data: Any,
        index: int,
    ) -> TestCase:

        prefix = f"test_cases[{index}]"

        if not isinstance(data, dict):
            raise SpecificationValidationError(
                f"{prefix} must be a dictionary"
            )

        required_fields = [
            "name",
            "category",
            "objective",
            "preconditions",
            "inputs",
            "expected",
            "priority",
        ]

        for field in required_fields:
            if field not in data:
                raise SpecificationValidationError(
                    f"Missing required field: {prefix}.{field}"
                )

        self._validate_string(
            data["name"],
            f"{prefix}.name",
        )

        self._validate_string(
            data["objective"],
            f"{prefix}.objective",
        )

        self._validate_list(
            data["preconditions"],
            f"{prefix}.preconditions",
        )

        self._validate_string_list(
            data["preconditions"],
            f"{prefix}.preconditions",
        )

        category = self._validate_enum(
            data["category"],
            TestCategory,
            f"{prefix}.category",
        )

        priority = self._validate_enum(
            data["priority"],
            TestPriority,
            f"{prefix}.priority",
        )

        inputs = self._validate_inputs(
            data["inputs"],
            f"{prefix}.inputs",
        )

        expected = self._validate_expected(
            data["expected"],
            f"{prefix}.expected",
        )

        return TestCase(
            name=data["name"],
            category=category,
            objective=data["objective"],
            preconditions=data["preconditions"],
            inputs=inputs,
            expected=expected,
            priority=priority,
        )

    def _validate_inputs(
        self,
        data: Any,
        field: str,
    ) -> TestInputs:

        if not isinstance(data, dict):
            raise SpecificationValidationError(
                f"Field '{field}' must be a dictionary"
            )

        required_fields = ["args", "kwargs"]

        for required_field in required_fields:
            if required_field not in data:
                raise SpecificationValidationError(
                    f"Missing required field: "
                    f"{field}.{required_field}"
                )

        self._validate_list(
            data["args"],
            f"{field}.args",
        )

        if not isinstance(data["kwargs"], dict):
            raise SpecificationValidationError(
                f"Field '{field}.kwargs' must be a dictionary"
            )

        return TestInputs(
            args=data["args"],
            kwargs=data["kwargs"],
        )

    def _validate_expected(
        self,
        data: Any,
        field: str,
    ) -> ExpectedBehavior:

        if not isinstance(data, dict):
            raise SpecificationValidationError(
                f"Field '{field}' must be a dictionary"
            )

        required_fields = ["type", "value"]

        for required_field in required_fields:
            if required_field not in data:
                raise SpecificationValidationError(
                    f"Missing required field: "
                    f"{field}.{required_field}"
                )

        expected_type = self._validate_enum(
            data["type"],
            ExpectedType,
            f"{field}.type",
        )

        return ExpectedBehavior(
            type=expected_type,
            value=data["value"],
        )

    def _validate_enum(
        self,
        value: Any,
        enum_type: type,
        field: str,
    ):
        if not isinstance(value, str):
            raise SpecificationValidationError(
                f"Field '{field}' must be a string"
            )

        try:
            return enum_type(value)
        except ValueError:
            valid_values = [
                member.value
                for member in enum_type
            ]

            raise SpecificationValidationError(
                f"Invalid value for '{field}': "
                f"'{value}'. Expected one of: "
                f"{valid_values}"
            )

    def _validate_string(
        self,
        value: Any,
        field: str,
    ) -> None:

        if not isinstance(value, str):
            raise SpecificationValidationError(
                f"Field '{field}' must be a string"
            )

        if not value.strip():
            raise SpecificationValidationError(
                f"Field '{field}' cannot be empty"
            )

    def _validate_list(
        self,
        value: Any,
        field: str,
    ) -> None:

        if not isinstance(value, list):
            raise SpecificationValidationError(
                f"Field '{field}' must be a list"
            )

    def _validate_string_list(
        self,
        values: list[Any],
        field: str,
    ) -> None:

        for index, value in enumerate(values):
            if not isinstance(value, str):
                raise SpecificationValidationError(
                    f"Field '{field}[{index}]' "
                    f"must be a string"
                )

            if not value.strip():
                raise SpecificationValidationError(
                    f"Field '{field}[{index}]' "
                    f"cannot be empty"
                )