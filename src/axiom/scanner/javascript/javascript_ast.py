from pathlib import Path
from axiom.scanner.models import Function, Parameter, Import, Class
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

def discover_imports(
        tree,
        file: Path,
) -> list[Import]:

    imports: list[Import] = []

    for node in tree.root_node.named_children:

        if node.type != "import_statement":
            continue

        source = node.child_by_field_name("source")

        if source is None:
            continue

        module = source.text.decode("utf-8").strip('"\'')
        names: list[str] = []

        for child in node.named_children:

            if child.type != "import_clause":
                continue

            for imported in child.named_children:

                if imported.type == "identifier":

                    names.append(
                        imported.text.decode("utf-8")
                    )

                elif imported.type == "named_imports":

                    for specifier in imported.named_children:

                        if specifier.type != "import_specifier":
                            continue

                        name_node = specifier.child_by_field_name(
                            "name"
                        )

                        if name_node:
                            names.append(
                                name_node.text.decode("utf-8")
                            )

        imports.append(
            Import(
                module=module,
                file=file,
                names=names,
            )
        )

    return imports

def discover_classes(
        tree,
        file: Path,
) -> list[Class]:

    classes = []

    for node in tree.root_node.named_children:

        if node.type != "class_declaration":
            continue

        name_node = node.child_by_field_name("name")
        class_body = node.child_by_field_name("body")

        methods: list[Function] = []

        for child in class_body.named_children:
            if child.type != "method_definition":
                continue

            method_name_node = child.child_by_field_name("name")
            parameters_node = child.child_by_field_name("parameters")

            parameters = []

            if parameters_node:
                for parameter in parameters_node.named_children:

                    parameters.append(
                        Parameter(
                            name = parameter.text.decode("utf-8"),
                            type = None,
                        )
                    )

            methods.append(
                Function(
                    name=method_name_node.text.decode("utf-8"),
                    file=file,
                    line=child.start_point[0] + 1,
                    parameters=parameters,
                )
            )

        classes.append(
            Class(
                name=node.child_by_field_name("name").text.decode("utf-8"),
                file=file,
                line=node.start_point[0] + 1,
                methods=methods,
            )
        )


    return classes