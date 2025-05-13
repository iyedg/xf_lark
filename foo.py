from xf_lark import XFParser
from xf_lark.utils import display_ast_as_tree

p = XFParser()

expression = "selected(${foo}, '1')"
expression = "1 and 2 or 3"
expression = "(${var1} + 5 * (count(${group}) - 1)) > 0"

expression = "--5"
ast = p.parse(expression)

display_ast_as_tree(ast, title=f"AST for: [code]{expression}[/code]")
