from pathlib import Path
from tree_sitter import Language, Parser
import tree_sitter_javascript

JS_LANGUAGE = Language(
    tree_sitter_javascript.language()
)

parser = Parser(JS_LANGUAGE)

def parse_javascript_file(path: Path):
    source = path.read_bytes()
    tree = parser.parse(source)

    return tree
