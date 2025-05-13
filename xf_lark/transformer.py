from lark import Token, Transformer, v_args


class AstTransformer(Transformer):
    def number_literal(self, items):
        return {"type": "number_literal", "value": float(items[0].value)}

    def string_literal(self, items):
        return {"type": "string_literal", "value": items[0].value[1:-1]}

    def variable_ref(self, items):
        return {"type": "variable_ref", "name": items[0].value[2:-1]}

    def bare_variable_ref(self, items):
        return {"type": "bare_variable_ref", "name": items[0].value}

    def current_ref(self, items):
        return {"type": "current_ref"}

    def parent_ref(self, items):
        return {"type": "parent_ref"}

    @v_args(inline=True)
    def unary_minus(self, minus_token: Token, operand_expression):
        return {
            "type": "unary_op",
            "operator": "unary_minus",
            "operand": operand_expression,
        }

    def add(self, items):
        return {
            "type": "binary_op",
            "operator": "add",
            "left": items[0],
            "right": items[2],
        }

    def subtract(self, items):
        return {
            "type": "binary_op",
            "operator": "subtract",
            "left": items[0],
            "right": items[2],
        }

    def multiply(self, items):
        return {
            "type": "binary_op",
            "operator": "multiply",
            "left": items[0],
            "right": items[2],
        }

    def divide(self, items):
        return {
            "type": "binary_op",
            "operator": "divide",
            "left": items[0],
            "right": items[2],
        }

    def eq(self, items):
        return {
            "type": "binary_op",
            "operator": "eq",
            "left": items[0],
            "right": items[2],
        }

    def ne(self, items):
        return {
            "type": "binary_op",
            "operator": "ne",
            "left": items[0],
            "right": items[2],
        }

    def lt(self, items):
        return {
            "type": "binary_op",
            "operator": "lt",
            "left": items[0],
            "right": items[2],
        }

    def gt(self, items):
        return {
            "type": "binary_op",
            "operator": "gt",
            "left": items[0],
            "right": items[2],
        }

    def lte(self, items):
        return {
            "type": "binary_op",
            "operator": "lte",
            "left": items[0],
            "right": items[2],
        }

    def gte(self, items):
        return {
            "type": "binary_op",
            "operator": "gte",
            "left": items[0],
            "right": items[2],
        }

    def logical_or(self, items):
        return {
            "type": "binary_op",
            "operator": "or",
            "left": items[0],
            "right": items[2],
        }

    def logical_and(self, items):
        return {
            "type": "binary_op",
            "operator": "and",
            "left": items[0],
            "right": items[2],
        }

    def function_call(self, items):
        function_name_token = items[0]
        # Arguments are items[1], items[2], ..., excluding COMMA tokens
        # Lark passes the children of the rule. For `NAME LPAR (logical_or_expr (COMMA logical_or_expr)*)? RPAR`,
        # `items` will contain [NAME_TOKEN, LPAR_TOKEN, arg1, COMMA_TOKEN, arg2, ..., RPAR_TOKEN]
        # We need to filter these. A more robust way is to check type.

        # Start scanning for arguments after the function name (items[0]) and LPAR.
        # RPAR will be the last token.
        # A simpler v_args approach for arguments might be better if grammar is adjusted.
        # For now, let's assume items after name are arguments or tokens like COMMA, LPAR, RPAR.
        # The `function_call` rule in grammar.lark is:
        # function_call: NAME LPAR (logical_or_expr (COMMA logical_or_expr)*)? RPAR
        # The children passed to the transformer method are the results of transforming/visiting these components.
        # Terminals (like LPAR, RPAR, COMMA, NAME) are passed as Tokens.
        # Non-terminals (like logical_or_expr) are passed as their transformed results.

        # items would be [Token(NAME), Token(LPAR), transformed_arg1, Token(COMMA), transformed_arg2, ..., Token(RPAR)]
        # or [Token(NAME), Token(LPAR), Token(RPAR)] if no args.

        function_name = function_name_token.value

        # Extract arguments: these are the transformed logical_or_expr items
        # They are not Tokens (unless a transformed item happens to be a Token, which it shouldn't be with our dict structure)
        # And they are not the NAME, LPAR, RPAR, or COMMA tokens.
        arguments = [
            item
            for item in items[1:]
            if not isinstance(item, Token) and item is not None
        ]

        return {"type": "function_call", "name": function_name, "arguments": arguments}

    @v_args(inline=True)
    def parentheses(self, lpar_token, expression, rpar_token):
        return expression

    @v_args(inline=True)
    def atom(self, child):
        return child

    @v_args(inline=True)
    def unary_expr(self, child):
        return child

    @v_args(inline=True)
    def multiplicative_expr(self, child):
        return child

    @v_args(inline=True)
    def additive_expr(self, child):
        return child

    @v_args(inline=True)
    def comparison_expr(self, child):
        return child

    @v_args(inline=True)
    def logical_and_expr(self, child):
        return child

    @v_args(inline=True)
    def logical_or_expr(self, child):
        return child

    @v_args(inline=True)
    def start(self, child):
        return child
