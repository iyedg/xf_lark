import importlib.resources

from lark import Lark

_grammar_path_obj = importlib.resources.files(__package__) / "grammar.lark"


def get_parser() -> Lark:
    with open(_grammar_path_obj, "r", encoding="utf-8") as f:
        grammar: str = f.read()

    xlsform_parser = Lark(grammar, start="start", parser="lalr")
    return xlsform_parser


def normalize_quotes(text: str) -> str:
    replacements = {"‘": "'", "’": "'", "“": '"', "”": '"'}
    for find, replace in replacements.items():
        text = text.replace(find, replace)
    return text
