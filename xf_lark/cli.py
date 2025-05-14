from typer import Typer

from . import XFParser
from .utils import display_ast_as_tree

app = Typer()


@app.command()
def main(expression: str):
    parser = XFParser()
    ast = parser.parse(expression)
    display_ast_as_tree(ast)
