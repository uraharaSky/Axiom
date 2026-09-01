from pathlib import Path
from axiom.scanner.models import Function, Parameter
from tree_sitter import Language, Parser
import tree_sitter_javascript


JS_LANGUAGE = Language(
    tree_sitter_javascript.language()
)

parser = Parser(JS_LANGUAGE)


def parse_javascript_file(path: Path):
    """
    Parse a JavaScript source file into a Tree-sitter syntax tree.
    """

    source = path.read_bytes()

    tree = parser.parse(source)

    return tree

def discover_functions(
        tree,
        file: Path,
) -> list[Function]:

    functions: list[Function] = []

    root = tree.root_node

    for node in root.named_children:

        if node.type != "function_declaration":
            continue

        name_node = node.child_by_field_name("name")

        parameters_node = node.child_by_field_name("parameters")

        parameters: list[Parameter] = []

        if parameters_node:
            for parameter in parameters_node.named_children:

                parameters.append(
                    Parameter(
                        name=parameter.text.decode("utf-8"),
                        type=None,
                    )
                )

        functions.append(
            Function(
                name=name_node.text.decode("utf-8"),
                file=file,
                line=node.start_point[0] + 1,
                parameters=parameters,
            )
        )

    return functions