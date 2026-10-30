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

    def validate(self, data: Any) -> TestSpecification:
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
        self._validate_dictionary(data, "Test specification")

        self._validate_required_field(
            data,
            "target",
            str,
        )

        self._validate_required_field(
            data,
            "objective",
            str,
        )

        self._validate_required_field(
            data,
            "assumptions",
            list,
        )

        self._validate_required_field(
            data,
            "test_cases",
            list,
        )

        self._validate_non_empty_string(
            data["target"],
            "target",
        )

        self._validate_non_empty_string(
            data["objective"],
            "objective",
        )

        self._validate_string_list(
            data["assumptions"],
            "assumptions",
        )

    def _validate_test_case(
        self,
        data: Any,
        index: int,
    ) -> TestCase:

        field = f"test_cases[{index}]"

        self._validate_dictionary(data, field)

        required_fields = {
            "name": str,
            "category": str,
            "objective": str,
            "preconditions": list,
            "inputs": dict,
            "expected": dict,
            "priority": str,
        }

        for name, expected_type in required_fields.items():
            self._validate_required_field(
                data,
                name,
                expected_type,
                parent=field,
            )

        self._validate_non_empty_string(
            data["name"],
            f"{field}.name",
        )

        self._validate_non_empty_string(
            data["objective"],
            f"{field}.objective",
        )

        self._validate_string_list(
            data["preconditions"],
            f"{field}.preconditions",
        )

        category = self._validate_enum(
            data["category"],
            TestCategory,
            f"{field}.category",
        )

        priority = self._validate_enum(
            data["priority"],
            TestPriority,
            f"{field}.priority",
        )

        inputs = self._validate_inputs(
            data["inputs"],
            f"{field}.inputs",
        )

        expected = self._validate_expected(
            data["expected"],
            f"{field}.expected",
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

        self._validate_dictionary(data, field)

        self._validate_required_field(
            data,
            "args",
            list,
            parent=field,
        )

        self._validate_required_field(
            data,
            "kwargs",
            dict,
            parent=field,
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

        self._validate_dictionary(data, field)

        self._validate_required_field(
            data,
            "type",
            str,
            parent=field,
        )

        if "value" not in data:
            raise SpecificationValidationError(
                f"Missing required field: {field}.value"
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

    def _validate_required_field(
        self,
        data: dict[str, Any],
        field: str,
        expected_type: type,
        parent: str | None = None,
    ) -> None:

        location = f"{parent}.{field}" if parent else field

        if field not in data:
            raise SpecificationValidationError(
                f"Missing required field: {location}"
            )

        if not isinstance(data[field], expected_type):
            raise SpecificationValidationError(
                f"Field '{location}' must be of type "
                f"{expected_type.__name__}"
            )

    def _validate_dictionary(
        self,
        value: Any,
        field: str,
    ) -> None:

        if not isinstance(value, dict):
            raise SpecificationValidationError(
                f"{field} must be a dictionary"
            )

    def _validate_non_empty_string(
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

    def _validate_string_list(
        self,
        values: Any,
        field: str,
    ) -> None:

        if not isinstance(values, list):
            raise SpecificationValidationError(
                f"Field '{field}' must be a list"
            )

        for index, value in enumerate(values):
            item_field = f"{field}[{index}]"

            if not isinstance(value, str):
                raise SpecificationValidationError(
                    f"Field '{item_field}' must be a string"
                )

            if not value.strip():
                raise SpecificationValidationError(
                    f"Field '{item_field}' cannot be empty"
                )