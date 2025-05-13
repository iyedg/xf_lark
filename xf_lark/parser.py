import importlib.resources

from lark import Lark

from .transformer import AstTransformer

_grammar_path_obj = importlib.resources.files(__package__) / "grammar.lark"


def get_lark_parser() -> Lark:
    with _grammar_path_obj.open("r", encoding="utf-8") as f:
        grammar: str = f.read()

    if not grammar.strip():
        raise ValueError(f"Grammar file is empty: {_grammar_path_obj}")

    return Lark(grammar, start="start", parser="lalr", import_paths=[])


class XFParser:
    def __init__(self):
        self.lark_parser: Lark = get_lark_parser()
        self.ast_transformer: AstTransformer = AstTransformer()

    def parse(self, expression_string: str):
        parse_tree = self.lark_parser.parse(expression_string)
        ast = self.ast_transformer.transform(parse_tree)
        return ast
