from axiom.context.models import TestGenerationContext

class PromptGenerator:

    def generate(self,
                 context: TestGenerationContext,
    ) -> str:

        target = context.target

        prompt = f"""
You are a software testing assistant.

Your task is to analyze the provided source code and generate a test specification for the target.

TARGET
Name: {target.name}
Kind: {target.kind}
File: {target.file}
Lines: {target.start_line}-{target.end_line}

SOURCE
{context.source}

RELATED UNITS   
"""

        for unit in context.related_units:
            prompt += (
                f"- {unit.kind}: {unit.name} "
                f"({unit.file}:{unit.start_line}-{unit.end_line})\n"
            )

        prompt += "\nRELATIONSHIPS\n"

        for relationship in context.relationships:
            module = (
                f" from {relationship.module}"
                if relationship.module
                else ""
            )

            prompt += (
                f"- {relationship.kind.value}: "
                f"{relationship.name}{module}\n"
            )

        prompt += """
        TASK
        Analyze the target and identify the behavior that should be tested.
        Consider normal cases, boundary conditions, invalid inputs, and relevant dependencies.

        Return a structured test specification.
        """

        return prompt.strip()